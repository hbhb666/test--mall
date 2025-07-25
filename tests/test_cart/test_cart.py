import pytest
import allure
import logging
import sys
import os
import json
import re
from core.test_executor import TestExecutor
from utils.token_manager import TokenManager

# 配置日志输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 常量定义
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_PATH = os.path.join(PROJECT_ROOT, "data", "mall测试用例.xlsx")
SHEET_NAME_LOGIN = "Sheet1"  # 登录用例所在的Sheet
SHEET_NAME_CART = "Sheet2"   # 购物车用例所在的Sheet

def parse_headers(header_str):
    """解析请求头字符串为字典格式"""
    if not header_str:
        return {}
    
    headers = {}
    # 处理请求头字符串，格式如 "Content-Type: application/json; Authorization: Bearer xxx"
    if isinstance(header_str, str):
        pairs = header_str.split(';')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                headers[key.strip()] = value.strip()
    elif isinstance(header_str, dict):
        headers = header_str
    return headers

def format_headers(headers_dict):
    """将字典格式的请求头转换为字符串格式"""
    if not headers_dict:
        return ""
    
    header_items = []
    for key, value in headers_dict.items():
        header_items.append(f"{key}: {value}")
    return "; ".join(header_items)

def clear_cart_data(auth_token):
    """清理购物车数据"""
    try:
        # 创建临时执行器用于清理购物车
        executor = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
        
        # 构建清理购物车的请求
        clear_cart_case = {
            "用例编号": "CLEAR_CART",
            "接口模块": "购物车模块",
            "用例标题": "清理购物车数据",
            "请求头": {
                "Authorization": auth_token,
                "Content-Type": "application/json"
            },
            "请求方式": "POST",
            "接口地址": "http://localhost:8085/cart/clear",
            "参数输入": "",
            "期望返回结果": "HTTP状态码200"
        }
        
        # 执行清理购物车操作
        logger.info("开始清理购物车数据...")
        executor.execute_test_case(clear_cart_case)
        logger.info("购物车数据清理完成")
        
        executor.close()
    except Exception as e:
        logger.warning(f"清理购物车数据时发生错误: {str(e)}")

def get_cart_list(auth_token):
    """获取购物车列表数据"""
    try:
        # 创建临时执行器用于获取购物车列表
        executor = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
        
        # 构建获取购物车列表的请求
        get_cart_case = {
            "用例编号": "GET_CART_LIST",
            "接口模块": "购物车模块",
            "用例标题": "获取购物车列表",
            "请求头": {
                "Authorization": auth_token,
                "Content-Type": "application/json"
            },
            "请求方式": "GET",
            "接口地址": "http://localhost:8085/cart/list",
            "参数输入": "",
            "期望返回结果": "HTTP状态码200"
        }
        
        # 执行获取购物车列表操作
        logger.info("开始获取购物车列表...")
        response = executor.request_handler.send_request(
            method=get_cart_case['请求方式'],
            url=get_cart_case['接口地址'],
            headers=get_cart_case['请求头']
        )
        
        # 解析响应数据
        if response.status_code == 200:
            response_json = response.json()
            cart_data = response_json.get('data', [])
            if cart_data and isinstance(cart_data, list) and len(cart_data) > 0:
                cart_id = cart_data[0].get('id')
                logger.info(f"获取到购物车项目ID: {cart_id}")
                executor.close()
                return cart_id
        
        executor.close()
        return None
    except Exception as e:
        logger.warning(f"获取购物车列表时发生错误: {str(e)}")
        return None

def replace_cart_id_in_params(params_input, cart_id):
    """在参数中替换购物车ID"""
    if not params_input or not cart_id:
        return params_input
    
    try:
        # 如果参数是JSON字符串
        if isinstance(params_input, str) and params_input.strip().startswith('{'):
            params_dict = json.loads(params_input)
            # 替换参数中的id字段
            if 'id' in params_dict:
                params_dict['id'] = cart_id
                return json.dumps(params_dict, ensure_ascii=False)
            return params_input
        # 如果参数是字典
        elif isinstance(params_input, dict) and 'id' in params_input:
            params_input['id'] = cart_id
            return params_input
        else:
            # 尝试在字符串参数中替换id值（如"id=15&quantity=2"格式）
            if isinstance(params_input, str):
                # 使用正则表达式替换id的值
                updated_params = re.sub(r'id=(\d+)', f'id={cart_id}', params_input)
                return updated_params
            return params_input
    except Exception as e:
        logger.warning(f"替换购物车ID时发生错误: {str(e)}")
        return params_input

# Fixtures定义
@pytest.fixture(scope="session")
def test_executors():
    """创建测试执行器实例的fixture，作用域为整个测试会话"""
    executor_login = TestExecutor(EXCEL_PATH, SHEET_NAME_LOGIN)
    executor_cart = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
    
    # 读取测试用例
    try:
        executor_login.load_test_cases()
        executor_cart.load_test_cases()
        logger.info(f"成功读取登录测试用例 {len(executor_login.test_cases)} 条")
        logger.info(f"成功读取购物车测试用例 {len(executor_cart.test_cases)} 条")
        yield executor_login, executor_cart
    except Exception as e:
        pytest.fail(f"读取测试用例失败：{str(e)}")
    finally:
        executor_login.close()
        executor_cart.close()

@pytest.fixture(scope="session")
def token_manager():
    """创建TokenManager实例的fixture"""
    return TokenManager()

@pytest.fixture(scope="session")
def auth_token(test_executors, token_manager):
    """获取认证token的fixture，作用域为整个测试会话，只执行一次"""
    executor_login, _ = test_executors
    
    # 执行登录操作，获取token
    login_case = next((case for case in executor_login.test_cases if case.get('用例标题') == '正常登录'), None)
    if not login_case:
        pytest.fail("未找到正常登录的测试用例")
    
    with allure.step("执行登录用例，获取token"):
        try:
            # 手动执行登录逻辑，确保返回响应
            case_id = login_case.get("用例编号", "未知")
            method = login_case.get("请求方式", "GET").upper()
            url = login_case.get("接口地址", "")
            headers = login_case.get("请求头", {})
            params_input = login_case.get("参数输入", "")
            expected_result = login_case.get("期望返回结果", "")
            
            # 解析参数
            params = executor_login._parse_params(params_input, headers)
            
            # 发送请求
            response = executor_login.request_handler.send_request(
                method=method,
                url=url,
                headers=headers,
                params=params
            )
            
            if response:
                token_data = response.json().get('data', {})
                token_manager.save_token('login', token_data)
                token = token_manager.get_token('login')
                return token
            else:
                pytest.fail("登录请求失败，未收到响应")
        except Exception as e:
            logger.error(f"执行登录用例时发生错误: {str(e)}")
            raise

# 参数化测试数据准备
def get_cart_test_cases():
    """获取购物车测试用例数据用于参数化"""
    executor_cart = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
    try:
        executor_cart.load_test_cases()
        return [(case.get("用例编号", f"用例{i+1}"), case) for i, case in enumerate(executor_cart.test_cases)]
    except Exception as e:
        pytest.fail(f"读取购物车测试用例失败：{str(e)}")
        return []
    finally:
        executor_cart.close()

def get_update_cart_quantity_test_cases():
    """获取与"修改购物车中商品数量"相关的测试用例数据用于参数化"""
    executor_cart = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
    try:
        executor_cart.load_test_cases()
        relevant_cases = [
            (case.get("用例编号", f"用例{i+1}"), case) 
            for i, case in enumerate(executor_cart.test_cases) 
            if '修改购物车中商品数量' in case.get('用例标题', '')
        ]
        return relevant_cases
    except Exception as e:
        pytest.fail(f"读取购物车测试用例失败：{str(e)}")
        return []
    finally:
        executor_cart.close()

def _execute_cart_test_case(test_case, auth_token):
    """执行购物车测试用例的公共方法"""
    # 检查用例标题是否包含特定关键字
    case_title = test_case.get('用例标题', '')
    need_token = '未登录状态' not in case_title
    use_invalid_token = '无效Token' in case_title
    skip_id_replacement = 'id不存在' in case_title
    
    # 解析原有请求头
    original_headers_str = test_case.get('请求头', '')
    headers = parse_headers(original_headers_str)
    
    # 如果标题包含"无效Token"，直接使用请求头中已有的Authorization值
    # 不做任何修改，保持原样
    if use_invalid_token:
        # 设置无效的Token值
        headers['Authorization'] = 'Bearer invalid_token'
    elif need_token:
        # 如果需要token且不是无效Token测试，则使用正常获取的token
        headers['Authorization'] = auth_token
    
    # 更新测试用例的请求头
    test_case_copy = test_case.copy()
    test_case_copy['请求头'] = format_headers(headers)
    
    # 处理参数输入为None的情况
    if test_case_copy.get('参数输入') is None:
        test_case_copy['参数输入'] = ''
    
    # 如果需要替换购物车ID且不是跳过替换的情况
    if not skip_id_replacement and need_token and not use_invalid_token:
        # 检查是否需要替换ID（通过检查URL或参数中是否包含更新、删除等操作）
        url = test_case_copy.get('接口地址', '')
        method = test_case_copy.get('请求方式', '').upper()
        
        # 对于更新、删除等操作，获取购物车列表并替换ID
        if any(op in url.lower() for op in ['update', 'delete']) or method in ['PUT', 'DELETE']:
            cart_id = get_cart_list(auth_token)
            if cart_id:
                # 替换参数中的ID
                test_case_copy['参数输入'] = replace_cart_id_in_params(test_case_copy['参数输入'], cart_id)
                logger.info(f"已替换参数中的购物车ID为: {cart_id}")
            else:
                logger.warning("未获取到购物车ID，使用原始参数")
    
    # 创建临时执行器执行测试用例
    executor_cart = TestExecutor(EXCEL_PATH, SHEET_NAME_CART)
    executor_cart.load_test_cases()
    executor_cart.execute_test_case(test_case_copy)
    executor_cart.close()

@allure.feature("购物车模块")
class TestCart:
    """购物车功能测试类"""
    
    @pytest.fixture(scope="class", autouse=True)
    def clear_cart_before_test(self, auth_token):
        """在测试类执行前自动清理购物车数据"""
        clear_cart_data(auth_token)
        yield
    
    @allure.title("执行购物车相关测试用例: {case_id}")
    @pytest.mark.cart
    @pytest.mark.parametrize("case_id, test_case", get_cart_test_cases())
    def test_cart_functionality(self, case_id, test_case, auth_token):
        """参数化的购物车功能测试方法"""
        with allure.step(f"执行用例: {case_id}"):
            try:
                _execute_cart_test_case(test_case, auth_token)
            except Exception as e:
                logger.error(f"执行用例 {case_id} 时发生错误: {str(e)}")
                raise

    @allure.title("执行修改购物车中商品数量测试用例: {case_id}")
    @pytest.mark.cart
    @pytest.mark.parametrize("case_id, test_case", get_update_cart_quantity_test_cases())
    def test_update_cart_quantity(self, case_id, test_case, auth_token):
        """参数化的修改购物车中商品数量测试方法"""
        with allure.step(f"执行用例: {case_id}"):
            try:
                _execute_cart_test_case(test_case, auth_token)
            except Exception as e:
                logger.error(f"执行用例 {case_id} 时发生错误: {str(e)}")
                raise