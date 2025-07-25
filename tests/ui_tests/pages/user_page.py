from selenium.webdriver.common.by import By
from .base_page import BasePage


class UserPage(BasePage):
    """
    用户页面类
    实现"我的"页面的具体操作和元素定位
    """

    def __init__(self, driver_manager):
        """
        初始化"我的"页面实例

        Args:
            driver_manager: WebDriver管理器实例
        """
        super().__init__(driver_manager)
        
        # 页面头部用户信息区域元素定位器
        self.user_background = (By.CSS_SELECTOR, ".user-section .bg")  # 用户背景图
        self.user_portrait = (By.CSS_SELECTOR, ".user-info-box .portrait")  # 用户头像
        self.username = (By.CSS_SELECTOR, ".user-info-box .username")  # 用户名
        self.vip_card = (By.CSS_SELECTOR, ".vip-card-box")  # VIP卡区域
        self.vip_title = (By.CSS_SELECTOR, ".vip-card-box .tit")  # VIP标题
        self.vip_benefits = (By.CSS_SELECTOR, ".vip-card-box .e-b")  # VIP权益说明
        
        # 积分、成长值、优惠券统计区域元素定位器
        self.points = (By.CSS_SELECTOR, ".tj-sction .tj-item:nth-child(1) .num")  # 积分
        self.growth_value = (By.CSS_SELECTOR, ".tj-sction .tj-item:nth-child(2) .num")  # 成长值
        self.coupons = (By.CSS_SELECTOR, ".tj-sction .tj-item:nth-child(3) .num")  # 优惠券数量
        
        # 订单管理区域元素定位器
        self.all_orders = (By.CSS_SELECTOR, ".order-section .order-item:nth-child(1)")  # 全部订单
        self.pending_payment = (By.CSS_SELECTOR, ".order-section .order-item:nth-child(2)")  # 待付款
        self.pending_delivery = (By.CSS_SELECTOR, ".order-section .order-item:nth-child(3)")  # 待收货
        self.refund_after_sale = (By.CSS_SELECTOR, ".order-section .order-item:nth-child(4)")  # 退款/售后
        
        # 功能列表区域元素定位器
        self.address_management = (By.CSS_SELECTOR, ".history-section .mix-list-cell:nth-child(1)")  # 地址管理
        self.browsing_history = (By.CSS_SELECTOR, ".history-section .mix-list-cell:nth-child(2)")  # 我的足迹
        # 我的关注 - 使用更通用的定位方式，通过包含特定文本的span元素定位
        self.my_following = (By.XPATH, "//span[contains(text(), '我的关注')]/..")  # 我的关注
        self.my_favorites = (By.CSS_SELECTOR, ".history-section .mix-list-cell:nth-child(4)")  # 我的收藏
        self.my_reviews = (By.CSS_SELECTOR, ".history-section .mix-list-cell:nth-child(5)")  # 我的评价
        self.settings = (By.CSS_SELECTOR, ".history-section .mix-list-cell:nth-child(6)")  # 设置
        
        # 底部导航栏图标定位器
        self.home_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-home']")  # 首页图标
        self.category_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-cate']")  # 分类图标
        self.cart_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-cart']")  # 购物车图标
        self.profile_icon = (By.CSS_SELECTOR, ".uni-tabbar__icon > img[src*='tab-my']")  # 我的图标

    def navigate_to_user_page(self):
        """
        导航到"我的"页面
        """
        self.open("/pages/user/user")

    def get_username(self):
        """
        获取用户名
        
        Returns:
            str: 用户名文本
        """
        return self.get_text(*self.username)

    def get_points(self):
        """
        获取用户积分
        
        Returns:
            str: 积分文本
        """
        return self.get_text(*self.points)

    def get_growth_value(self):
        """
        获取用户成长值
        
        Returns:
            str: 成长值文本
        """
        return self.get_text(*self.growth_value)

    def get_coupons_count(self):
        """
        获取优惠券数量
        
        Returns:
            str: 优惠券数量文本
        """
        return self.get_text(*self.coupons)

    def click_all_orders(self):
        """
        点击"全部订单"
        """
        self.click(*self.all_orders)

    def click_pending_payment(self):
        """
        点击"待付款"
        """
        self.click(*self.pending_payment)

    def click_pending_delivery(self):
        """
        点击"待收货"
        """
        self.click(*self.pending_delivery)

    def click_refund_after_sale(self):
        """
        点击"退款/售后"
        """
        self.click(*self.refund_after_sale)

    def click_address_management(self):
        """
        点击"地址管理"
        """
        self.click(*self.address_management)

    def click_browsing_history(self):
        """
        点击"我的足迹"
        """
        self.click(*self.browsing_history)

    def click_my_following(self):
        """
        点击"我的关注"
        使用XPath定位器来查找并点击"我的关注"元素。
        """
        print("正在点击'我的关注'")
        self.click(*self.my_following)
        # 点击后等待1秒
        import time
        time.sleep(1)

    def click_my_favorites(self):
        """
        点击"我的收藏"
        """
        self.click(*self.my_favorites)

    def click_my_reviews(self):
        """
        点击"我的评价"
        """
        self.click(*self.my_reviews)

    def click_settings(self):
        """
        点击"设置"
        """
        self.click(*self.settings)

    def click_home_icon(self):
        """
        点击首页图标，跳转到首页
        """
        self.click(*self.home_icon)

    def click_category_icon(self):
        """
        点击分类图标，跳转到分类页面
        """
        self.click(*self.category_icon)

    def click_cart_icon(self):
        """
        点击购物车图标，跳转到购物车页面
        """
        self.click(*self.cart_icon)

    def is_vip(self):
        """
        检查用户是否为VIP
        
        Returns:
            bool: 如果是VIP返回True，否则返回False
        """
        try:
            self.get_text(*self.vip_title)
            return True
        except:
            return False