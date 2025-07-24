import pytest
import requests
import allure
import logging
import json
from jsonpath_ng import parse
from typing import Dict, Any, Union, Optional
from utils.excel_reader import read_excel_test_cases
from config import base_url
import sys

# 配置日志输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 常量定义
EXCEL_PATH = "mall测试用例.xlsx"
SHEET_NAME = "Sheet1"
TIMEOUT = 10

# 读取测试用例
try:
    test_cases = read_excel_test_cases(EXCEL_PATH, SHEET_NAME)
    logger.info(f"成功读取到 {len(test_cases)} 条测试用例")
    for i, case in enumerate(test_cases):
        logger.info(f"用例 {i+1}: {case.get('用例编号', '未知')} - {case.get('用例标题', '无标题')}")
except Exception as e:
    pytest.fail(f"读取测试用例失败：{str(e)}")

# 参数化测试函数
@pytest.mark.parametrize("case", test_cases)
@allure.feature("会员模块")
@allure.story("登录功能")
def test_case_executor(case: Dict[str, Any]):
    """
    核心测试逻辑：支持单步请求，根据请求头类型构建参数
    :param case: 单个测试用例字典
    """
    # 提取测试用例字段
    case_id = case.get("用例编号", "未知用例")
    case_title = case.get("用例标题", "未知标题")
    pre_condition = case.get("前置条件", "无")
    headers = case.get("请求头", {})
    request_method = case.get("请求方式", "GET").upper()
    url = case.get("接口地址", "").replace("{{portal.mall}}", base_url)
    params_input = case.get("参数输入", "")
    expected_result = case.get("期望返回结果", "")
    use_token = case.get("use_token", False)  # 控制是否使用 Token

    logger.info(f"开始执行测试用例: {case_id} - {case_title}")
    logger.info(f"前置条件: {pre_condition}")
    logger.info(f"请求方法: {request_method}")
    logger.info(f"请求URL: {url}")
    logger.info(f"请求头: {headers}")
    logger.info(f"参数输入: {params_input}")
    logger.info(f"期望结果: {expected_result}")
    logger.info(f"是否使用Token: {use_token}")

    # Allure 报告配置
    allure.dynamic.title(f"{case_id} - {case_title}")
    allure.dynamic.description(f"前置条件：{pre_condition}\n期望结果：{expected_result}")
    allure.attach(str(params_input), name="原始参数输入", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(headers), name="请求头", attachment_type=allure.attachment_type.TEXT)

    # 解析参数输入
    try:
        if isinstance(params_input, str) and params_input.strip():
            # 如果是字符串且非空，则尝试解析为JSON
            params = json.loads(params_input)
            logger.info(f"解析后的参数: {params}")
        else:
            # 如果是字典或其他类型，直接使用
            params = params_input if params_input else {}
            logger.info(f"直接使用的参数: {params}")
    except json.JSONDecodeError as e:
        pytest.fail(f"参数输入JSON解析失败：{str(e)}，内容：{params_input}")

    # 处理单步请求
    handle_single_step_request(
        case_id=case_id,
        method=request_method,
        url=url,
        headers=headers,
        params=params,
        expected_result=expected_result,
        use_token=use_token
    )

    logger.info(f"测试用例执行完成: {case_id} - {case_title}")


def handle_single_step_request(
    case_id: str,
    method: str,
    url: str,
    headers: dict,
    params: Union[dict, str],
    expected_result: str,
    use_token: bool
):
    """
    处理单步请求，根据请求头类型构建参数，并控制是否使用Token
    :param case_id: 用例编号
    :param method: 请求方法
    :param url: 请求URL
    :param headers: 请求头
    :param params: 请求参数
    :param expected_result: 期望结果描述
    :param use_token: 是否使用 Token
    """
    logger.info(f"[{case_id}] 开始执行单步请求")

    # 创建独立 session
    with requests.Session() as session:
        # 可选注入 Token
        token = get_token_from_case(case_id)
        if use_token and token:
            session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info(f"[{case_id}] 当前请求头: {dict(session.headers)}")

        # 构建请求参数
        request_params = build_request_params(method, url, headers, params)

        # 发送请求
        with allure.step(f"发送 {method} 请求到 {url}"):
            response = session.request(
                method=method,
                url=url,
                headers=headers,
                **request_params,
                timeout=TIMEOUT
            )

    # 记录响应内容
    logger.info(f"[{case_id}] 收到响应: 状态码={response.status_code}")
    logger.info(f"[{case_id}] 响应内容: {response.text}")
    allure.attach(response.text, name="原始响应内容", attachment_type=allure.attachment_type.TEXT)

    # 尝试解析 JSON 并验证业务状态码
    try:
        response_json = response.json()
        logger.info(f"[{case_id}] 解析响应JSON: {response_json}")

        # 提取期望业务码
        expected_status = extract_expected_status(expected_result)

        # 验证业务状态码（code字段）
        actual_code = response_json.get("code")
        if actual_code is not None:
            logger.info(f"[{case_id}] 验证业务状态码: 期望={expected_status}, 实际={actual_code}")
            with allure.step(f"验证业务状态码：期望 {expected_status}，实际 {actual_code}"):
                assert actual_code == expected_status, (
                    f"[{case_id}] 业务状态码断言失败：期望{expected_status}，实际{actual_code}")
        else:
            logger.warning(f"[{case_id}] 响应中未找到 'code' 字段，跳过业务码验证")

    except ValueError:
        # 如果响应不是有效的 JSON，退而求其次验证 HTTP 状态码
        logger.warning(f"[{case_id}] 响应不是有效的 JSON 格式：{response.text}")
        expected_status = extract_expected_status(expected_result)
        with allure.step(f"响应非JSON，验证HTTP状态码：期望 {expected_status}，实际 {response.status_code}"):
            assert response.status_code == expected_status, (
                f"[{case_id}] HTTP状态码错误：期望{expected_status}，实际{response.status_code}")
        logger.info(f"[{case_id}] 非JSON响应，HTTP状态码验证通过")

    # 无论是否为 JSON，都记录响应结果
    with allure.step("记录响应结果"):
        allure.attach(
            response.text,
            name=f"响应结果（状态码：{response.status_code}）",
            attachment_type=allure.attachment_type.JSON
        )

    # 特殊用例处理 - 保存Token
    if case_id == "MP-LOGIN-001" and response.status_code == 200:
        logger.info(f"[{case_id}] 检测到登录成功，尝试保存Token")
        save_token(response_json)

    # 通用断言 - 消息内容（从期望结果描述中提取关键词）
    if "token或用户信息" in expected_result and response.status_code == 200:
        logger.info(f"[{case_id}] 验证Token字段存在")
        assert_json_field_exists(response_json, "$.data.token")

    if "账户已锁定" in expected_result and response.status_code == 403:
        logger.info(f"[{case_id}] 验证账户锁定消息")
        assert_json_field_contains(response_json, "$.message", "账户已锁定")


def build_request_params(
    method: str,
    url: str,
    headers: dict,
    params: Union[dict, str]
) -> dict:
    """
    根据请求头类型构建请求参数
    :param method: 请求方法
    :param url: 请求URL
    :param headers: 请求头
    :param params: 请求参数
    :return: 构建后的请求参数字典
    """
    logger.info(f"构建请求参数，请求方法: {method}, 请求头: {headers}, 参数: {params}")

    content_type = headers.get("Content-Type", "")

    if method == "GET":
        return {"params": params}

    elif method == "POST":
        if "application/json" in content_type:
            return {"json": params}
        elif "application/x-www-form-urlencoded" in content_type:
            from urllib.parse import urlencode
            return {"data": urlencode(params)}
        else:
            return {"data": params}

    elif method in ["PUT", "PATCH"]:
        if "application/json" in content_type:
            return {"json": params}
        elif "application/x-www-form-urlencoded" in content_type:
            from urllib.parse import urlencode
            return {"data": urlencode(params)}
        else:
            return {"data": params}

    elif method == "DELETE":
        return {"params": params}

    else:
        raise ValueError(f"不支持的请求方式：{method}")


def extract_expected_status(expected_result: str) -> int:
    """
    从期望结果描述中提取期望业务码
    """
    logger.info(f"提取期望状态码，描述: {expected_result}")

    if "HTTP状态码200" in expected_result:
        status = 200
    elif "HTTP状态码403" in expected_result:
        status = 403
    elif "HTTP状态码415" in expected_result:
        status = 415
    elif "HTTP状态码400" in expected_result:
        status = 400
    elif "HTTP状态码404" in expected_result:
        status = 404
    else:
        status = 200  # 默认返回200

    logger.info(f"提取到的期望状态码: {status}")
    return status


def get_token_from_case(case_id: str) -> Optional[str]:
    """
    根据用例编号模拟获取 Token
    :param case_id: 用例编号
    :return: Token 字符串 或 None
    """
    # 模拟 Token 获取
    if case_id == "MP-LOGIN-001":
        return "mocked_token_from_case_MP_LOGIN_001"
    elif case_id == "MP-LOGIN-002":
        return "mocked_token_from_case_MP_LOGIN_002"
    else:
        return None


def save_token(response_json: dict):
    """
    保存 Token（模拟）
    :param response_json: 登录成功后的响应 JSON
    """
    expr = parse("$.data.token")
    match = expr.find(response_json)

    if match:
        token = match[0].value
        logger.info(f"Token 已保存: {token}")
        allure.attach(token, name="Token", attachment_type=allure.attachment_type.TEXT)
    else:
        logger.warning("未找到Token字段：$.data.token")


def assert_json_field(json_data: dict, path: str, expected: Any):
    """
    验证指定JSON路径的值是否符合预期
    :param json_data: 响应JSON数据
    :param path: JSON字段路径
    :param expected: 期望值
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 值为 {expected}"):
        if not match:
            logger.error(f"未找到字段: {path}")
            assert False, f"未找到字段：{path}"

        actual_value = match[0].value
        logger.info(f"字段值匹配: 实际值={actual_value}, 期望值={expected}")
        assert actual_value == expected, (
            f"{path} 验证失败：期望 {expected}，实际 {actual_value}"
        )


def assert_json_field_contains(json_data: dict, path: str, substring: str):
    """
    验证指定JSON字段是否包含子串
    :param json_data: 响应JSON数据
    :param path: JSON字段路径
    :param substring: 期望包含的子串
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 包含 '{substring}'"):
        if not match:
            logger.error(f"未找到字段: {path}")
            assert False, f"未找到字段：{path}"

        actual_value = match[0].value
        logger.info(f"字段值包含检查: 实际值={actual_value}, 期望包含={substring}")
        assert substring in actual_value, (
            f"{path} 验证失败：期望包含 '{substring}'，实际 '{actual_value}'"
        )


def assert_json_field_exists(json_data: dict, path: str):
    """
    验证指定JSON字段是否存在
    :param json_data: 响应JSON数据
    :param path: JSON字段路径
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 存在"):
        if not match:
            logger.error(f"未找到字段: {path}")
            assert False, f"未找到字段：{path}"

        logger.info(f"字段存在验证通过: {path}")
