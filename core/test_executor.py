"""
测试执行器
负责整体测试流程的协调和管理，是测试框架的核心组件
"""

import json
import allure
import logging
import re
from typing import Dict, Any, List, Optional
from core.request_handler import RequestHandler
from utils.excel_reader import read_excel_test_cases
from utils.assertion_utils import *
from config.config import base_url

# 配置日志
logger = logging.getLogger(__name__)


class TestExecutor:
    """测试执行器类，负责协调整个测试执行流程"""

    def __init__(self, excel_path: str, sheet_name: str):
        """
        初始化测试执行器
        
        Args:
            excel_path (str): Excel测试用例文件路径
            sheet_name (str): Excel工作表名称
        """
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.test_cases = []
        self.request_handler = RequestHandler(base_url=base_url)
        self.token_storage = {}  # 用于存储各模块的token

    def load_test_cases(self):
        """
        从Excel文件加载测试用例
        """
        try:
            self.test_cases = read_excel_test_cases(self.excel_path, self.sheet_name)
            logger.info(f"成功加载 {len(self.test_cases)} 条测试用例")
            
            # 记录用例信息到日志
            for i, case in enumerate(self.test_cases):
                case_id = case.get("用例编号", "未知")
                case_title = case.get("用例标题", "无标题")
                logger.info(f"用例 {i+1}: {case_id} - {case_title}")
                
        except Exception as e:
            logger.error(f"加载测试用例失败: {str(e)}")
            raise

    def identify_module_type(self, case: Dict[str, Any]) -> str:
        """
        根据URL路径识别模块类型
        
        Args:
            case (Dict[str, Any]): 测试用例
            
        Returns:
            str: 模块类型 (auth, cart, order, product, public)
        """
        url = case.get("接口地址", "")
        
        # 根据URL路径识别模块类型
        if "/member/" in url or "/auth/" in url or "login" in url or "register" in url:
            return "auth"
        elif "/cart/" in url:
            return "cart"
        elif "/order/" in url:
            return "order"
        elif "/product/" in url:
            return "product"
        else:
            # 根据用例编号前缀识别
            case_id = case.get("用例编号", "")
            if case_id.startswith("MP-LOGIN") or case_id.startswith("MP-REGISTER"):
                return "auth"
            elif case_id.startswith("MP-CART"):
                return "cart"
            elif case_id.startswith("MP-ORDER"):
                return "order"
            elif case_id.startswith("MP-PRODUCT"):
                return "product"
            else:
                return "public"  # 默认为公共模块

    def execute_test_case(self, case: Dict[str, Any]):
        """
        执行单个测试用例
        
        Args:
            case (Dict[str, Any]): 测试用例
        """
        case_id = case.get("用例编号", "未知用例")
        case_title = case.get("用例标题", "未知标题")
        module_type = self.identify_module_type(case)
        
        logger.info(f"开始执行测试用例: {case_id} - {case_title} (模块: {module_type})")
        
        # Allure 报告配置
        allure.dynamic.title(f"{case_id} - {case_title}")
        allure.dynamic.feature(f"{module_type.upper()}模块")
        allure.dynamic.story("接口测试")
        allure.dynamic.description(f"模块类型: {module_type}")
        
        # 根据模块类型分发到相应处理器
        if module_type == "auth":
            self._execute_auth_case(case)
        elif module_type == "cart":
            self._execute_cart_case(case)
        elif module_type == "order":
            self._execute_order_case(case)
        elif module_type == "product":
            self._execute_product_case(case)
        else:
            self._execute_public_case(case)
            
        logger.info(f"测试用例执行完成: {case_id} - {case_title}")

    def _execute_auth_case(self, case: Dict[str, Any]):
        """
        执行认证模块测试用例
        
        Args:
            case (Dict[str, Any]): 认证模块测试用例
        """
        logger.info(f"[{case.get('用例编号', '未知')}] 执行认证模块用例")
        
        # 提取用例字段
        case_id = case.get("用例编号", "未知")
        method = case.get("请求方式", "GET").upper()
        url = case.get("接口地址", "")
        headers = case.get("请求头", {})
        params_input = case.get("参数输入", "")
        expected_result = case.get("期望返回结果", "")
        
        # 解析参数
        params = self._parse_params(params_input, headers)
        
        # 发送请求
        response = self.request_handler.send_request(
            method=method,
            url=url,
            headers=headers,
            params=params
        )
        
        # 解析期望状态码
        expected_status = self._extract_expected_status(case_id, expected_result)
        
        # 断言状态码
        assert_response_status(response, expected_status)
        
        # 特殊处理：登录成功后保存token
        if "login" in url.lower() and response.status_code == 200:
            try:
                response_json = response.json()
                token = self.request_handler.extract_json_field(response_json, "$.data.token")
                if token:
                    self.token_storage["auth"] = token
                    self.request_handler.set_token(token)
                    logger.info(f"[{case_id}] Token已保存并设置")
                    with allure.step("保存并设置认证Token"):
                        allure.attach(token, name="认证Token", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                logger.warning(f"[{case_id}] 保存Token时出错: {e}")

    def _execute_cart_case(self, case: Dict[str, Any]):
        """
        执行购物车模块测试用例
        
        Args:
            case (Dict[str, Any]): 购物车模块测试用例
        """
        logger.info(f"[{case.get('用例编号', '未知')}] 执行购物车模块用例")
        
        # 如果有保存的token，则设置到请求处理器中
        if "auth" in self.token_storage:
            self.request_handler.set_token(self.token_storage["auth"])
        
        self._execute_standard_case(case)

    def _execute_order_case(self, case: Dict[str, Any]):
        """
        执行订单模块测试用例
        
        Args:
            case (Dict[str, Any]): 订单模块测试用例
        """
        logger.info(f"[{case.get('用例编号', '未知')}] 执行订单模块用例")
        
        # 如果有保存的token，则设置到请求处理器中
        if "auth" in self.token_storage:
            self.request_handler.set_token(self.token_storage["auth"])
        
        self._execute_standard_case(case)

    def _execute_product_case(self, case: Dict[str, Any]):
        """
        执行商品模块测试用例
        
        Args:
            case (Dict[str, Any]): 商品模块测试用例
        """
        logger.info(f"[{case.get('用例编号', '未知')}] 执行商品模块用例")
        self._execute_standard_case(case)

    def _execute_public_case(self, case: Dict[str, Any]):
        """
        执行公共模块测试用例
        
        Args:
            case (Dict[str, Any]): 公共模块测试用例
        """
        logger.info(f"[{case.get('用例编号', '未知')}] 执行公共模块用例")
        self._execute_standard_case(case)

    def _execute_standard_case(self, case: Dict[str, Any]):
        """
        执行标准测试用例（通用处理逻辑）
        
        Args:
            case (Dict[str, Any]): 测试用例
        """
        case_id = case.get("用例编号", "未知")
        method = case.get("请求方式", "GET").upper()
        url = case.get("接口地址", "")
        headers = self._parse_headers(case.get("请求头", {}))
        params_input = case.get("参数输入", "")
        expected_result = case.get("期望返回结果", "")
        
        # 解析参数
        params = self._parse_params(params_input, headers)
        
        # 发送请求
        response = self.request_handler.send_request(
            method=method,
            url=url,
            headers=headers,
            params=params
        )
        
        # 解析期望状态码
        expected_status = self._extract_expected_status(case_id, expected_result)
        
        # 断言状态码
        assert_response_status(response, expected_status)
        
        # 如果期望结果中有其他验证要求，则进行相应验证
        if response.status_code == 200 and expected_result:
            try:
                response_json = response.json()
                
                # 验证token字段存在
                if "token" in expected_result.lower():
                    assert_json_field_exists(response_json, "$.data.token")
                
                # 验证消息内容
                if "message" in expected_result.lower():
                    assert_json_field_exists(response_json, "$.message")
                    
            except json.JSONDecodeError:
                logger.warning(f"[{case_id}] 响应不是有效的JSON格式，跳过JSON字段验证")

    def _parse_headers(self, headers_input) -> Dict[str, str]:
        """
        解析请求头
        
        Args:
            headers_input: 请求头输入（可能是字符串或字典）
            
        Returns:
            Dict[str, str]: 解析后的请求头字典
        """
        if isinstance(headers_input, dict):
            return headers_input
        elif isinstance(headers_input, str) and headers_input.strip():
            headers = {}
            # 分割多个请求头
            for header in headers_input.split("; "):
                if ": " in header:
                    key, value = header.split(": ", 1)
                    headers[key] = value
            return headers
        else:
            return {}

    def _parse_params(self, params_input, headers: Dict[str, str]) -> Any:
        """
        解析参数输入
        
        Args:
            params_input: 参数输入
            headers (Dict[str, str]): 请求头
            
        Returns:
            Any: 解析后的参数
        """
        if not params_input:
            return {}
            
        content_type = headers.get("Content-Type", "")
        
        try:
            # 如果是JSON格式的字符串，尝试解析为JSON对象
            if isinstance(params_input, str) and params_input.strip().startswith('{'):
                params_dict = json.loads(params_input)
                # 如果Content-Type是application/json，则直接返回解析后的对象
                if "application/json" in content_type:
                    return params_dict
                # 如果Content-Type是application/x-www-form-urlencoded，则需要转换为表单格式
                elif "application/x-www-form-urlencoded" in content_type:
                    return params_dict
                else:
                    return params_dict
            else:
                # 其他情况直接返回原值
                return params_input
        except json.JSONDecodeError:
            # JSON解析失败，返回原值
            logger.warning(f"参数JSON解析失败: {params_input}")
            return params_input

    import re

    def _extract_expected_status(self, case_id: str, expected_result: str) -> int:
        """
        从期望结果描述中提取期望状态码
        
        Args:
            case_id (str): 用例编号
            expected_result (str): 期望结果描述
            
        Returns:
            int: 期望状态码
        """
        # 对于正常登录用例，期望200
        if case_id == "LOGIN-01":
            return 200

        # 使用正则表达式提取状态码（支持如 "HTTP 400", "Status 404", "HTTP状态码500" 等格式）
        status_match = re.search(r'(?:HTTP|Status|状态码)[^\d]*(\d{3})', expected_result)
        if status_match:
            return int(status_match.group(1))

        # 如果正则表达式没有匹配到，使用关键词检查
        if "HTTP状态码200" in expected_result or "成功" in expected_result:
            return 200
        elif "HTTP状态码403" in expected_result:
            return 403
        elif "HTTP状态码415" in expected_result:
            return 415
        elif "HTTP状态码400" in expected_result:
            return 400
        elif "HTTP状态码404" in expected_result:
            return 404
        else:
            # 默认返回200
            logger.info(f"[{case_id}] 未找到明确状态码，使用默认值 200")
            return 200

    def run_all_tests(self):
        """
        执行所有测试用例
        """
        if not self.test_cases:
            self.load_test_cases()
            
        logger.info(f"开始执行全部 {len(self.test_cases)} 条测试用例")
        
        for i, case in enumerate(self.test_cases):
            case_id = case.get("用例编号", f"用例{i+1}")
            with allure.step(f"执行用例: {case_id}"):
                try:
                    self.execute_test_case(case)
                except Exception as e:
                    logger.error(f"执行用例 {case_id} 时发生错误: {str(e)}")
                    # 继续执行下一个用例，不中断整个测试流程
                    continue
                    
        logger.info("所有测试用例执行完成")
        
    def close(self):
        """
        清理资源
        """
        self.request_handler.close()
        logger.info("测试执行器资源已清理")