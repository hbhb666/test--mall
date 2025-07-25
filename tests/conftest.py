"""
测试配置文件
包含测试会话和函数级别的fixtures
"""
import pytest
import requests
from utils.token_manager import TokenManager
from utils.excel_reader import read_excel_test_cases


# 全局token管理器实例
token_manager = TokenManager()


@pytest.fixture(scope="session")
def global_token_manager():
    """
    全局token管理器fixture
    
    Returns:
        TokenManager: 全局token管理器实例
    """
    return token_manager


@pytest.fixture(scope="function")
def http_session():
    """
    HTTP会话fixture
    为每个测试函数提供独立的requests Session实例
    
    Yields:
        requests.Session: HTTP会话实例
    """
    with requests.Session() as session:
        yield session


@pytest.fixture(scope="session")
def test_cases():
    """
    测试用例数据fixture
    从Excel文件中读取所有测试用例
    
    Returns:
        list: 测试用例列表
    """
    # 从Excel文件中读取测试用例
    # 这里可以按模块分类读取不同的Excel sheet或文件
    cases = read_excel_test_cases("test_cases/mall测试用例.xlsx", "Sheet1")
    return cases