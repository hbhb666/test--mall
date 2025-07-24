import pytest
import requests
from utils.token_manager import TokenManager
from utils.excel_reader import read_excel_test_cases

# 全局token管理器
token_manager = TokenManager()

@pytest.fixture(scope="session")
def global_token_manager():
    """全局token管理器fixture"""
    return token_manager

@pytest.fixture(scope="function")
def http_session():
    """HTTP会话fixture"""
    with requests.Session() as session:
        yield session

@pytest.fixture(scope="session")
def test_cases():
    """读取所有测试用例"""
    # 这里可以按模块分类读取不同的Excel sheet或文件
    cases = read_excel_test_cases("test_cases/mall测试用例.xlsx", "Sheet1")
    return cases
