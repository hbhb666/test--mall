"""
UI测试配置文件
包含UI测试的fixture和配置
"""
import pytest
import allure
from tests.ui_tests.utils.web_driver import WebDriverManager


@pytest.fixture(scope="session")
def driver_manager(request):
    """
    WebDriver管理器fixture
    提供WebDriver实例用于UI测试
    
    Args:
        request: pytest request对象
        
    Returns:
        WebDriverManager: WebDriver管理器实例
    """
    # 检查是否需要无头模式
    headless = request.config.getoption("--headless", False)
    
    # 初始化WebDriver管理器
    manager = WebDriverManager(headless=headless)
    manager.init_driver()
    
    yield manager
    
    # 测试结束后关闭浏览器
    manager.quit_driver()


@pytest.fixture(scope="function")
def browser(driver_manager):
    """
    浏览器fixture
    为每个测试函数提供WebDriver实例
    
    Args:
        driver_manager: WebDriver管理器实例
        
    Returns:
        WebDriver: WebDriver实例
    """
    driver = driver_manager.driver
    
    # 每个测试前清理浏览器状态
    driver.delete_all_cookies()
    
    yield driver
    
    # 可以在这里添加测试后的清理操作


def pytest_addoption(parser):
    """
    添加pytest命令行选项
    
    Args:
        parser: pytest参数解析器
    """
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以无头模式运行浏览器"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告钩子函数，用于捕获测试结果并添加截图到Allure报告
    
    Args:
        item: 测试项目
        call: 测试调用信息
    """
    # 执行测试并获取结果
    outcome = yield
    rep = outcome.get_result()
    
    # 只在测试失败时截图
    if rep.when == "call" and rep.failed:
        try:
            # 获取driver_manager fixture
            driver_manager = item.funcargs.get('driver_manager')
            if driver_manager and driver_manager.driver:
                # 截图并添加到Allure报告
                screenshot = driver_manager.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="失败时的截图", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"截图失败: {e}")