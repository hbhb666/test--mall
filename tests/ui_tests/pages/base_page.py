"""
基础页面类
提供页面对象模型的基础功能
"""
from selenium.webdriver.common.by import By
from ..utils.web_driver import WebDriverManager


class BasePage:
    """
    基础页面类
    所有页面对象都应该继承此类
    """
    def __init__(self, driver_manager: WebDriverManager):
        """
        初始化基础页面
        
        Args:
            driver_manager (WebDriverManager): WebDriver管理器实例
        """
        self.driver_manager = driver_manager
        self.driver = driver_manager.driver

    def open(self, url):
        """
        打开页面
        
        Args:
            url (str): 页面URL
        """
        self.driver_manager.navigate_to(url)

    def click(self, by, value):
        """
        点击元素
        
        Args:
            by: 定位方式
            value: 定位值
        """
        self.driver_manager.click_element(by, value)
        
    def clear(self, by, value):
        """
        清空元素内容
        
        Args:
            by: 定位方式
            value: 定位值
        """
        self.driver_manager.clear_element(by, value)

    def input(self, by, value, text):
        """
        输入文本
        
        Args:
            by: 定位方式
            value: 定位值
            text (str): 要输入的文本
        """
        self.driver_manager.input_text(by, value, text)

    def get_text(self, by, value):
        """
        获取元素文本
        
        Args:
            by: 定位方式
            value: 定位值
            
        Returns:
            str: 元素文本
        """
        return self.driver_manager.get_element_text(by, value)

    def wait_for_element(self, by, value):
        """
        等待元素出现
        
        Args:
            by: 定位方式
            value: 定位值
        """
        self.driver_manager.wait_for_element_visible(by, value)