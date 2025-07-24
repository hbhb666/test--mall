# import json
# import logging
# import pytest
# from utils import excel_reader
#
# #配置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# #配置常量
# SHEET_NAME="Sheet1"
# WORKBOOK_PATH= "data/mall测试用例.xlsx"
# TIMEOUT=10
#
# #读取用例
# test_cases = excel_reader.read_excel_test_cases(WORKBOOK_PATH, SHEET_NAME)
# logger.info(f"读取到{len(test_cases)}条测试用例")
#
# #使用pytest编写代码执行用例
# @pytest.mark.parametrize("case", test_cases)
# def test_case(case):
#     #使用获取的参数构建请求头
#     headers =case["请求头"]
#     #使用获取的参数构建请求方式
#     method = case["请求方式"]
#     #使用获取的参数构建请求路径
#     url = case["接口地址"]
#     #使用获取的参数构建请求参数
#     params = case["参数输入"]
#     #根据请求头里面的规定的参数类型构建请求参数
#     if "Content-Type" in headers and headers["Content-Type"] == "application/json":
#         params = json.loads(params)
#         logger.info(f"请求参数：{params}")
#     if "Content-Type" in headers and headers["Content-Type"] == "application/x-www-form-urlencoded":
#         # 处理表单参数,从json转
#         params = {k: v for k, v in params.items()}
#         logger.info(f"请求参数：{params}")
#         #拼接参数
#         params = "&".join([f"{k}={v}" for k, v in params.items()])
#
#
import sys

print(sys.executable)  # 输出PyCharm实际使用的解释器路径