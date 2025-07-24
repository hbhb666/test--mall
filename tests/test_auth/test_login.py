import pytest
import allure
import logging
import sys
import os
from core.test_executor import TestExecutor
from utils.excel_reader import read_excel_test_cases

# 配置日志输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 常量定义
# 修复Excel文件路径，使用相对于项目根目录的路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_PATH = os.path.join(PROJECT_ROOT, "data", "mall测试用例.xlsx")
SHEET_NAME = "Sheet1"

# 创建全局测试执行器实例
test_executor = TestExecutor(EXCEL_PATH, SHEET_NAME)

# 读取测试用例
try:
    test_executor.load_test_cases()
    test_cases = test_executor.test_cases
    logger.info(f"成功读取到 {len(test_cases)} 条测试用例")
    for i, case in enumerate(test_cases):
        logger.info(f"用例 {i+1}: {case.get('用例编号', '未知')} - {case.get('用例标题', '无标题')}")
except Exception as e:
    pytest.fail(f"读取测试用例失败：{str(e)}")


@allure.feature("认证模块")
@allure.story("登录功能")
class TestLogin:
    """登录功能测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        logger.info("开始执行登录测试")
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("登录测试执行完成")
    
    @allure.title("执行所有登录相关测试用例")
    def test_all_login_cases(self):
        """执行所有登录相关的测试用例"""
        login_cases = [case for case in test_cases if self._is_login_case(case)]
        
        if not login_cases:
            pytest.skip("未找到登录相关的测试用例")
            
        logger.info(f"开始执行 {len(login_cases)} 条登录测试用例")
        
        for i, case in enumerate(login_cases):
            case_id = case.get("用例编号", f"用例{i+1}")
            with allure.step(f"执行用例: {case_id}"):
                try:
                    test_executor.execute_test_case(case)
                except Exception as e:
                    logger.error(f"执行用例 {case_id} 时发生错误: {str(e)}")
                    raise
    
    def _is_login_case(self, case: dict) -> bool:
        """
        判断是否为登录相关测试用例
        
        Args:
            case (dict): 测试用例
            
        Returns:
            bool: 是否为登录用例
        """
        # 根据URL判断
        url = case.get("接口地址", "")
        if "login" in url:
            return True
            
        # 根据用例编号判断
        case_id = case.get("用例编号", "")
        if case_id.startswith("MP-LOGIN"):
            return True
            
        # 根据模块类型判断
        module = case.get("接口模块", "")
        if "登录" in module or "认证" in module:
            return True
            
        return False


def test_cleanup():
    """测试结束后的清理工作"""
    logger.info("执行测试清理工作")
    test_executor.close()