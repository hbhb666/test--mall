"""
Mall系统登录页面类
实现针对http://localhost:8060/#/pages/public/login页面的具体操作
"""
from selenium.webdriver.common.by import By
from tests.ui_tests.pages.base_page import BasePage


class MallLoginPage(BasePage):
    """
    Mall系统登录页面类
    包含登录页面的元素定位和操作方法
    """
    # 页面元素定位器
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='请输入用户名']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='请输入密码']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), '登录')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "el-message__content")
    PAGE_TITLE = (By.XPATH, "//div[contains(@class, 'title') and contains(text(), 'mall')]")

    def __init__(self, driver_manager):
        """
        初始化Mall登录页面
        
        Args:
            driver_manager: WebDriver管理器实例
        """
        super().__init__(driver_manager)

    def wait_for_page_load(self):
        """等待页面加载完成"""
        self.wait_for_element(*self.PAGE_TITLE)

    def enter_username(self, username):
        """
        输入用户名
        
        Args:
            username (str): 用户名
        """
        self.input(*self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """
        输入密码
        
        Args:
            password (str): 密码
        """
        self.input(*self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """点击登录按钮"""
        self.click(*self.LOGIN_BUTTON)

    def login(self, username, password):
        """
        执行登录操作
        
        Args:
            username (str): 用户名
            password (str): 密码
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self):
        """
        获取错误信息
        
        Returns:
            str: 错误信息文本
        """
        # 等待错误消息出现
        self.driver_manager.wait.until(
            lambda driver: driver.find_element(*self.ERROR_MESSAGE).text.strip() != ""
        )
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_button_enabled(self):
        """
        检查登录按钮是否可用
        
        Returns:
            bool: 登录按钮是否可用
        """
        button = self.driver_manager.find_element(*self.LOGIN_BUTTON)
        return button.is_enabled()