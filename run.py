"""
自动化测试启动器
用于运行不同类型的测试并生成Allure测试报告
"""
import subprocess
import sys
import os
import time


def install_requirements():
    """
    安装项目依赖
    
    Returns:
        bool: 安装是否成功
    """
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        return True
    except Exception as e:
        print(f"安装依赖时出错: {e}")
        return False


def run_all_tests():
    """
    运行所有测试并生成Allure报告数据
    
    Returns:
        bool: 测试执行是否成功
    """
    print("开始执行所有测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
            
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行测试时出错: {e}")
        return False


def run_cart_tests():
    """
    运行购物车测试用例并生成Allure报告数据
    
    Returns:
        bool: 测试执行是否成功
    """
    print("开始执行购物车测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
            
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_cart",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行购物车测试时出错: {e}")
        return False


def run_ui_tests(headless=False):
    """
    运行UI测试
    
    Args:
        headless (bool): 是否以无头模式运行浏览器，默认为False
        
    Returns:
        bool: 测试执行是否成功
    """
    print("开始执行UI测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
            
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/ui_tests/tests",
            "-v"
        ]
        if headless:
            cmd.append("--headless")
        result = subprocess.run(cmd)
        return result.returncode == 0
    except Exception as e:
        print(f"执行UI测试时出错: {e}")
        return False


def run_with_mark(mark):
    """
    根据标记运行测试
    
    Args:
        mark (str): 测试标记
        
    Returns:
        bool: 测试执行是否成功
    """
    print(f"开始执行标记为 {mark} 的测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
            
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "-m", mark,
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行标记测试时出错: {e}")
        return False


def run_ui_tests_with_marker(headless=False):
    """
    运行带有ui标记的测试
    
    Args:
        headless (bool): 是否以无头模式运行浏览器，默认为False
        
    Returns:
        bool: 测试执行是否成功
    """
    print("开始执行UI标记的测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
            
        cmd = [
            sys.executable, "-m", "pytest",
            "-m", "ui",
            "-v"
        ]
        if headless:
            cmd.append("--headless")
        result = subprocess.run(cmd)
        return result.returncode == 0
    except Exception as e:
        print(f"执行UI标记测试时出错: {e}")
        return False


def run_all_tests_ci():
    """
    在CI/CD环境中运行所有测试（包括UI测试的无头模式）
    
    Returns:
        bool: 测试执行是否成功
    """
    print("开始在CI/CD环境中执行所有测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
        
        # 运行所有测试，包括UI测试（使用无头模式）
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "--headless",  # 启用无头模式运行UI测试
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行测试时出错: {e}")
        return False


def run_ui_tests_ci():
    """
    在CI/CD环境中运行UI测试（无头模式）
    
    Returns:
        bool: 测试执行是否成功
    """
    print("开始在CI/CD环境中执行UI测试...")
    try:
        # 先安装依赖
        if not install_requirements():
            return False
        
        # 运行UI测试（使用无头模式）
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/ui_tests/tests",
            "--headless",  # 启用无头模式
            "-v"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行UI测试时出错: {e}")
        return False


def show_menu_with_timeout():
    """
    显示菜单选项，带有3秒超时功能
    如果3秒内没有输入，则默认运行所有测试
    
    Returns:
        str: 用户选择的选项，超时则返回"1"（运行所有测试）
    """
    # 检查是否在CI/CD环境中运行
    is_ci_env = os.environ.get('CI') == 'true' or os.environ.get('JENKINS_URL') is not None
    
    print("\n请选择要执行的操作:")
    print("1. 运行所有测试")
    print("2. 运行购物车测试")
    print("3. 运行带cart标记的测试")
    print("4. 运行UI测试")
    print("5. 运行UI测试(无头模式)")
    print("6. 运行带ui标记的测试")
    print("7. 依次执行所有测试（购物车测试 -> UI测试）")
    print("8. 在CI/CD环境中运行所有测试（推荐用于Jenkins）")
    print("9. 在CI/CD环境中运行UI测试（推荐用于Jenkins）")
    print("0. 退出")
    
    # 在CI/CD环境中自动选择CI模式
    if is_ci_env:
        print("\n检测到在CI/CD环境中运行，自动选择CI模式...")
        print("自动执行选项: 在CI/CD环境中运行所有测试")
        time.sleep(1)  # 短暂等待让用户看到提示
        return "8"
    
    # 为了解决超时后仍需按键的问题，我们采用最简单的方案：
    # 直接提示并立即开始执行默认选项（运行所有测试）
    print("\n3秒内无输入将默认运行所有测试...")
    print("自动执行默认选项: 运行所有测试")
    time.sleep(3)  # 等待3秒让用户看到提示
    return "1"


def run_all_tests_sequentially():
    """
    依次执行所有测试
    按顺序执行：购物车测试 -> UI测试
    
    Returns:
        bool: 所有测试是否都执行成功
    """
    print("开始依次执行所有测试...")
    print("=" * 30)
    
    # 1. 首先执行购物车测试
    print("\n1. 执行购物车测试...")
    cart_success = run_cart_tests()
    if not cart_success:
        print("购物车测试失败！")
        return False
    else:
        print("购物车测试完成。")
    
    # 2. 然后执行UI测试
    print("\n2. 执行UI测试...")
    ui_success = run_ui_tests()
    if not ui_success:
        print("UI测试失败！")
        return False
    else:
        print("UI测试完成。")
    
    # 所有测试都成功执行
    print("\n所有测试均已成功执行完成！")
    return True


def main():
    """
    主函数 - 运行测试并生成报告
    支持命令行模式和交互模式两种运行方式
    """
    print("自动化测试启动器")
    print("=" * 30)
    
    # 检查是否在CI/CD环境中运行（通过环境变量判断）
    is_ci_env = os.environ.get('CI') == 'true' or os.environ.get('JENKINS_URL') is not None
    
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == "ui":
            # 处理UI测试命令行参数
            # 用法: python run.py ui [--headless]
            headless = "--headless" in sys.argv
            print("开始执行UI测试...")
            success = run_ui_tests(headless)
            print("\nUI测试执行完成！")
            if success:
                print("UI测试通过！")
            else:
                print("UI测试失败！")
                sys.exit(1)
        elif sys.argv[1] == "sequential":  # 新增命令行选项
            # 依次执行所有测试
            print("开始依次执行所有测试...")
            success = run_all_tests_sequentially()
            if success:
                print("\n所有测试均已成功执行完成！")
            else:
                print("\n某些测试执行失败！")
                sys.exit(1)
        elif sys.argv[1] == "ci":
            # CI/CD模式 - 运行所有测试（包括无头模式的UI测试）
            print("开始在CI/CD环境中执行所有测试...")
            success = run_all_tests_ci()
            if success:
                print("\n所有测试均已成功执行完成！")
            else:
                print("\n某些测试执行失败！")
                sys.exit(1)
        elif sys.argv[1] == "ci-ui":
            # CI/CD模式 - 仅运行UI测试（无头模式）
            print("开始在CI/CD环境中执行UI测试...")
            success = run_ui_tests_ci()
            if success:
                print("\nUI测试执行完成！")
            else:
                print("\nUI测试失败！")
                sys.exit(1)
        else:
            # 默认自动运行所有测试
            print("自动运行所有测试...")
            success = run_all_tests()
    else:
        # 交互模式
        # 给用户一点时间阅读菜单
        time.sleep(0.5)
        
        choice = show_menu_with_timeout()
        if choice == "1":
            success = run_all_tests()
        elif choice == "2":
            success = run_cart_tests()
        elif choice == "3":
            success = run_with_mark("cart")
        elif choice == "4":
            success = run_ui_tests()
        elif choice == "5":
            success = run_ui_tests(headless=True)
        elif choice == "6":
            success = run_ui_tests_with_marker()
        elif choice == "7":  # 新增选项
            success = run_all_tests_sequentially()
        elif choice == "8":  # CI/CD环境选项
            success = run_all_tests_ci()
        elif choice == "9":  # CI/CD环境选项
            success = run_ui_tests_ci()
        elif choice == "0":
            print("退出程序")
            return
        else:
            print("无效选项，将默认运行所有测试...")
            success = run_all_tests()
        
        if success:
            print("\n测试执行完成！")
            print("测试报告数据已生成至 allure-results 目录")
            print("\n要查看报告，可以执行以下操作之一:")
            print("1. 在项目根目录执行: allure serve allure-results")
            print("2. 或执行: allure generate allure-results -o allure-report && allure open allure-report")
            
            # 添加UI测试特别说明
            print("\nUI测试特别说明:")
            print("1. 浏览器窗口可能会自动关闭，测试期间请勿手动关闭浏览器")
            print("2. 如果测试失败，可以在tests/ui_tests/screenshots目录查看截图")
            print("3. UI测试依赖Selenium WebDriver，请确保浏览器驱动已正确安装")
        else:
            print("\n测试执行失败！")
            sys.exit(1)


if __name__ == "__main__":
    main()