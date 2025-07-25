import subprocess
import sys
import os

def run_all_tests():
    """运行所有测试并生成Allure报告数据"""
    print("开始执行所有测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行测试时出错: {e}")
        return False

def run_cart_tests():
    """运行购物车测试用例并生成Allure报告数据"""
    print("开始执行购物车测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/test_cart",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行购物车测试时出错: {e}")
        return False

def run_with_mark(mark):
    """根据标记运行测试"""
    print(f"开始执行标记为 {mark} 的测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            f"-m {mark}",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行标记测试时出错: {e}")
        return False

def show_menu():
    """显示菜单选项"""
    print("\n请选择要执行的操作:")
    print("1. 运行所有测试")
    print("2. 运行购物车测试")
    print("3. 运行带cart标记的测试")
    print("0. 退出")
    choice = input("\n请输入选项 (0-3): ").strip()
    return choice

def main():
    """主函数 - 运行测试并生成报告"""
    print("自动化测试启动器")
    print("=" * 30)
    
    # 默认自动运行所有测试
    print("自动运行所有测试...")
    success = run_all_tests()
    
    if success:
        print("\n测试执行完成！")
        print("测试报告数据已生成至 allure-results 目录")
        print("\n要查看报告，可以执行以下操作之一:")
        print("1. 在项目根目录执行: allure serve allure-results")
        print("2. 或执行: allure generate allure-results -o allure-report && allure open allure-report")
    else:
        print("\n测试执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()