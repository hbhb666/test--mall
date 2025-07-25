"""
WebDriver管理器模块
用于初始化和管理Selenium WebDriver实例
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WebDriverManager:
    """
    WebDriver管理器类
    负责初始化WebDriver实例并提供通用操作方法
    """
    def __init__(self, headless=False):
        """
        初始化WebDriver管理器
        
        Args:
            headless (bool): 是否以无头模式运行浏览器，默认为False
        """
        self.headless = headless
        self.driver = None
        self.wait = None

    def init_driver(self):
        """
        初始化WebDriver实例
        
        Returns:
            WebDriver: 初始化的WebDriver实例
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 自动下载并设置ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver

    def quit_driver(self):
        """关闭WebDriver实例"""
        if self.driver:
            self.driver.quit()

    def navigate_to(self, url):
        """
        导航到指定URL
        
        Args:
            url (str): 要导航到的URL
        """
        self.driver.get(url)

    def find_element(self, by, value):
        """
        查找单个元素
        
        Args:
            by: 定位方式
            value: 定位值
            
        Returns:
            WebElement: 找到的元素
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by, value):
        """
        查找多个元素
        
        Args:
            by: 定位方式
            value: 定位值
            
        Returns:
            list: 找到的元素列表
        """
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def click_element(self, by, value):
        """
        点击元素
        
        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        
    def clear_element(self, by, value):
        """
        清空元素内容
        
        Args:
            by: 定位方式
            value: 定位值
        """
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.clear()
        
    def input_text(self, by, value, text):
        """
        在元素中输入文本
        
        Args:
            by: 定位方式
            value: 定位值
            text (str): 要输入的文本
        """
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.clear()
        element.send_keys(text)
        
    def clear_all_cookies(self):
        """
        清除所有cookies
        """
        self.driver.delete_all_cookies()
        
    def refresh_page(self):
        """
        刷新当前页面
        """
        self.driver.refresh()
        # 等待页面加载
        import time
        time.sleep(1)
        
    def close_all_popups(self):
        """
        关闭所有可能的弹窗
        """
        try:
            # 查找并点击可能的关闭按钮
            close_buttons = self.driver.find_elements(By.XPATH, "//uni-toast//button | //*[contains(@class, 'close') or contains(@class, 'cancel')]")
            for button in close_buttons:
                try:
                    if button.is_displayed():
                        button.click()
                        time.sleep(0.5)
                except:
                    continue
        except:
            pass

    def get_element_text(self, by, value):
        """
        获取元素文本
        
        Args:
            by: 定位方式
            value: 定位值
            
        Returns:
            str: 元素文本内容
        """
        element = self.find_element(by, value)
        return element.text

    def wait_for_element_visible(self, by, value, timeout=5):
        """
        等待元素可见
        
        Args:
            by: 定位方式
            value: 定位值
            timeout (int): 超时时间，默认为5秒
        """
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
