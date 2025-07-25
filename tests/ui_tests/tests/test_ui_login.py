"""
登录功能UI测试
测试登录页面的相关功能
"""
import pytest
import allure
from tests.ui_tests.pages.login_page import LoginPage
from tests.ui_tests.pages.home_page import HomePage
from tests.ui_tests.pages.user_page import UserPage


class TestLogin:
    """登录功能测试类"""

    @allure.title("测试使用无效凭据登录")
    @allure.description("验证使用无效用户名和密码登录时，系统能正确显示错误信息")
    @allure.feature("登录功能")
    @allure.story("登录验证")
    @pytest.mark.ui
    def test_login_with_invalid_credentials(self, driver_manager):
        """
        测试使用无效凭据登录

        Args:
            driver_manager: WebDriver管理器实例
        """
        print("开始执行test_login_with_invalid_credentials测试")
        # 初始化页面对象
        home_page = HomePage(driver_manager)
        user_page = UserPage(driver_manager)
        login_page = LoginPage(driver_manager)
        
        # 1. 打开首页
        print("1. 打开首页")
        home_page.open("http://localhost:8060/#/")
        import time
        time.sleep(1)
        
        # 2. 点击"我的"图标跳转到用户页面
        print("2. 点击'我的'图标跳转到用户页面")
        home_page.click_profile_icon()
        time.sleep(1)
        
        # 3. 点击"我的关注"跳转到登录页面
        print("3. 点击'我的关注'跳转到登录页面")
        user_page.click_my_following()
        
        # 4. 执行登录操作（使用无效凭据）
        print("4. 执行登录操作（使用无效凭据: invalid_user / invalid_password）")
        login_page.login("invalid_user", "invalid_password")

        # 验证错误信息显示
        print("5. 验证错误信息显示")
        # 使用更快速的检查方法
        assert login_page.is_error_message_displayed(), "登录失败时应该显示错误信息"
        
        # 获取错误信息并进一步验证
        error_message = login_page.get_error_message()
        print(f"获取到的错误信息: {error_message}")
        # 检查错误信息是否包含预期的关键字之一
        expected_keywords = ["错误", "不正确", "error", "invalid", "失败", "wrong", "用户名", "密码"]
        assert any(keyword in error_message.lower() for keyword in expected_keywords), \
            f"错误信息应该包含预期关键字，但实际显示为: '{error_message}'"
        
        # 不再执行清理操作，因为错误弹窗会在1.5秒后自动消失
        # 这样第二个测试可以更快开始
        print("测试执行完成，错误弹窗会自动消失")

    @allure.title("从用户页面登录测试")
    @allure.description("测试从首页->我的页面->登录页面的完整登录流程")
    @allure.feature("登录功能")
    @allure.story("登录流程")
    @pytest.mark.ui
    def test_login_from_user_page(self, driver_manager):
        """
        从首页->我的页面->登录页面的完整登录流程测试
        1. 打开首页
        2. 点击"我的"图标跳转到用户页面
        3. 点击"我的关注"跳转到登录页面
        4. 执行登录（支持重试机制，应对需要点击两次才能成功登录的情况）
        5. 验证登录成功后返回用户页面并检查用户名

        Args:
            driver_manager: WebDriver管理器实例
        """
        print("开始执行test_login_from_user_page测试")
        # 初始化页面对象
        home_page = HomePage(driver_manager)
        user_page = UserPage(driver_manager)
        login_page = LoginPage(driver_manager)
        
        # 快速清理可能存在的错误提示或弹窗
        login_page.reset_page_state()
        
        # 1. 打开首页
        print("1. 打开首页")
        home_page.open("http://localhost:8060/#/")
        import time
        time.sleep(1)
        
        # 2. 点击"我的"图标跳转到用户页面
        print("2. 点击'我的'图标跳转到用户页面")
        home_page.click_profile_icon()
        time.sleep(1)
        
        # 3. 点击"我的关注"跳转到登录页面
        print("3. 点击'我的关注'跳转到登录页面")
        user_page.click_my_following()
        
        # 4. 执行登录（支持最多2次重试）
        print("4. 执行登录（使用用户名: member, 密码: member123）")
        login_page.login("member", "member123")
        
        # 验证登录是否成功
        print("5. 验证登录是否成功")
        assert login_page.is_login_successful(), "登录应该成功并跳转到其他页面"
        
        # 5. 验证登录成功后返回用户页面并检查用户名
        # 等待页面加载完成并获取用户名
        print("6. 等待页面加载完成并获取用户名")
        driver_manager.wait_for_element_visible(*user_page.username)
        username_text = user_page.get_username()
        print(f"获取到的用户名: {username_text}")
        assert username_text is not None and username_text != "", f"登录后用户名应不为空，实际值为: '{username_text}'"
        
        # 额外验证：用户名应该不是默认的"游客"
        assert username_text != "游客", f"登录后用户名应不是'游客'，实际值为: '{username_text}'"
        print("测试执行完成")

    @pytest.mark.skip(reason="需要根据实际环境调整测试数据")
    def test_login_functionality(self, driver_manager):
        """
        登录功能完整测试（需要根据实际环境调整）

        Args:
            driver_manager: WebDriver管理器实例
        """
        # 此测试需要根据实际的测试环境URL和测试账号进行调整
        login_page = LoginPage(driver_manager)
        login_page.open("http://localhost:8060/#/pages/public/login")
        login_page.login("member", "member123")
        # 添加适当的断言来验证登录结果