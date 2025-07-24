import subprocess
import sys
import os

def run_pytest():
    """运行 pytest 测试"""
    print("开始执行 pytest 测试...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "--alluredir", "allure-results"
    ])
    return result.returncode == 0

def main():
    """主函数"""
    print("自动化测试启动器")
    print("=" * 30)

    # 执行 pytest
    success = run_pytest()

    if success:
        print("测试执行成功！")
        print("测试报告数据已生成至 allure-results 目录")
    else:
        print("测试执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
