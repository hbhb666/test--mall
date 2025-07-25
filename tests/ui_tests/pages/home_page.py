from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """
    首页页面类
    实现首页的具体操作和元素定位
    """

    def __init__(self, driver_manager):
        """
        初始化首页页面实例

        Args:
            driver_manager: WebDriver管理器实例
        """
        super().__init__(driver_manager)
        # 页面主要元素定位器
        self.search_input = (By.CSS_SELECTOR, ".mp-search-box .ser-input")  # 搜索框
        self.carousel_images = (By.CSS_SELECTOR, ".carousel-item")  # 轮播图
        self.category_items = (By.CSS_SELECTOR, ".cate-item")  # 分类项
        self.brand_items = (By.CSS_SELECTOR, ".guess-item")  # 品牌制造商直供
        self.flash_sale_items = (By.CSS_SELECTOR, ".floor-item")  # 秒杀专区商品
        self.new_product_items = (By.CSS_SELECTOR, ".scoll-wrapper .floor-item")  # 新鲜好物
        self.hot_product_items = (By.CSS_SELECTOR, ".hot-section .guess-item")  # 人气推荐
        self.recommend_product_items = (By.CSS_SELECTOR, ".guess-section .guess-item")  # 猜你喜欢
        self.home_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-home']")  # 首页图标
        self.category_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-cate']")  # 分类图标
        self.cart_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-cart']")  # 购物车图标
        self.profile_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-my']")  # 我的图标

    def navigate_to_home(self):
        """
        导航到首页
        """
        self.open("/pages/index/index")

    def search_product(self, product_name):
        """
        在首页搜索指定的商品

        Args:
            product_name (str): 要搜索的商品名称
        """
        self.input(self.search_input[0], self.search_input[1], product_name)

    def click_carousel_item(self, index=0):
        """
        点击轮播图中的某一项

        Args:
            index (int): 轮播图索引，默认为0
        """
        carousel_elements = self.driver.find_elements(*self.carousel_images)
        if 0 <= index < len(carousel_elements):
            carousel_elements[index].click()
        else:
            raise IndexError("Invalid carousel index")

    def click_category_item(self, index=0):
        """
        点击分类项中的某一项

        Args:
            index (int): 分类项索引，默认为0
        """
        category_elements = self.driver.find_elements(*self.category_items)
        if 0 <= index < len(category_elements):
            category_elements[index].click()
        else:
            raise IndexError("Invalid category index")

    def click_brand_item(self, index=0):
        """
        点击品牌制造商直供中的某一项

        Args:
            index (int): 品牌项索引，默认为0
        """
        brand_elements = self.driver.find_elements(*self.brand_items)
        if 0 <= index < len(brand_elements):
            brand_elements[index].click()
        else:
            raise IndexError("Invalid brand index")

    def click_flash_sale_item(self, index=0):
        """
        点击秒杀专区中的某一项

        Args:
            index (int): 秒杀商品索引，默认为0
        """
        flash_sale_elements = self.driver.find_elements(*self.flash_sale_items)
        if 0 <= index < len(flash_sale_elements):
            flash_sale_elements[index].click()
        else:
            raise IndexError("Invalid flash sale index")

    def click_new_product_item(self, index=0):
        """
        点击新鲜好物中的某一项

        Args:
            index (int): 新鲜好物索引，默认为0
        """
        new_product_elements = self.driver.find_elements(*self.new_product_items)
        if 0 <= index < len(new_product_elements):
            new_product_elements[index].click()
        else:
            raise IndexError("Invalid new product index")

    def click_hot_product_item(self, index=0):
        """
        点击人气推荐中的某一项

        Args:
            index (int): 人气推荐索引，默认为0
        """
        hot_product_elements = self.driver.find_elements(*self.hot_product_items)
        if 0 <= index < len(hot_product_elements):
            hot_product_elements[index].click()
        else:
            raise IndexError("Invalid hot product index")

    def click_recommend_product_item(self, index=0):
        """
        点击猜你喜欢中的某一项

        Args:
            index (int): 推荐商品索引，默认为0
        """
        recommend_product_elements = self.driver.find_elements(*self.recommend_product_items)
        if 0 <= index < len(recommend_product_elements):
            recommend_product_elements[index].click()
        else:
            raise IndexError("Invalid recommend product index")

    def click_home_icon(self):
        """
        点击首页图标
        """
        self.click_element(*self.home_icon)

    def click_category_icon(self):
        """
        点击分类图标
        """
        self.click_element(*self.category_icon)

    def click_cart_icon(self):
        """
        点击购物车图标
        """
        self.click_element(*self.cart_icon)

    def click_profile_icon(self):
        """
        点击我的图标
        """
        print("正在点击'我的'图标")
        self.click(*self.profile_icon)
        # 点击后等待1秒
        import time
        time.sleep(1)
