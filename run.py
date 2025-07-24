import subprocess
import sys
import os

def run_tests():
    """运行测试并生成Allure报告数据"""
    print("开始执行测试...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "--alluredir", "allure-results"
        ])
        return result.returncode == 0
    except Exception as e:
        print(f"执行测试时出错: {e}")
        return False

def main():
    """主函数 - 运行测试并生成报告"""
    print("自动化测试启动器")
    print("=" * 30)
    
    # 运行测试
    success = run_tests()
    
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