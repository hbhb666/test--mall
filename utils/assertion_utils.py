# 断言工具
import allure
import pytest
from jsonpath_ng import parse
from typing import Any, Dict, Union


def assert_response_status(response, expected_status):
    """
    断言响应状态码，优先检查响应体中的code字段，如果没有则使用HTTP状态码
    
    Args:
        response: HTTP响应对象
        expected_status: 期望的状态码
    """
    actual_status = response.status_code  # 默认使用HTTP状态码
    
    # 尝试从响应体中的code字段获取状态码
    try:
        response_json = response.json()
        if "code" in response_json:
            actual_status = response_json["code"]
    except:
        # 如果解析JSON失败，使用HTTP状态码
        pass
    
    with allure.step(f"验证响应状态码: 期望 {expected_status}，实际 {actual_status}"):
        assert actual_status == expected_status, \
            f"状态码断言失败：期望{expected_status}，实际{actual_status}"


def assert_json_field_exists(json_data: Dict[str, Any], path: str):
    """
    断言JSON字段存在
    
    Args:
        json_data: JSON数据
        path: JSON路径表达式
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 存在"):
        assert match, f"未找到字段：{path}"


def assert_json_field_value(json_data: Dict[str, Any], path: str, expected_value: Any):
    """
    断言JSON字段值
    
    Args:
        json_data: JSON数据
        path: JSON路径表达式
        expected_value: 期望的值
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 值为 {expected_value}"):
        assert match, f"未找到字段：{path}"
        assert match[0].value == expected_value, \
            f"字段值断言失败：期望{expected_value}，实际{match[0].value}"


def assert_json_field_contains(json_data: Dict[str, Any], path: str, expected_substring: str):
    """
    断言JSON字段包含指定子串
    
    Args:
        json_data: JSON数据
        path: JSON路径表达式
        expected_substring: 期望包含的子串
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 包含 '{expected_substring}'"):
        assert match, f"未找到字段：{path}"
        actual_value = match[0].value
        assert isinstance(actual_value, str), f"字段值不是字符串类型: {type(actual_value)}"
        assert expected_substring in actual_value, \
            f"字段值不包含期望子串：期望'{expected_substring}'，实际'{actual_value}'"


def assert_json_field_type(json_data: Dict[str, Any], path: str, expected_type: type):
    """
    断言JSON字段类型
    
    Args:
        json_data: JSON数据
        path: JSON路径表达式
        expected_type: 期望的类型
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证字段 {path} 类型为 {expected_type.__name__}"):
        assert match, f"未找到字段：{path}"
        actual_value = match[0].value
        assert isinstance(actual_value, expected_type), \
            f"字段类型断言失败：期望{expected_type.__name__}，实际{type(actual_value).__name__}"


def assert_greater_than(value: Union[int, float], expected_minimum: Union[int, float]):
    """
    断言值大于期望的最小值
    
    Args:
        value: 实际值
        expected_minimum: 期望的最小值
    """
    with allure.step(f"验证值 {value} 大于 {expected_minimum}"):
        assert value > expected_minimum, \
            f"值断言失败：期望大于{expected_minimum}，实际{value}"


def assert_less_than(value: Union[int, float], expected_maximum: Union[int, float]):
    """
    断言值小于期望的最大值
    
    Args:
        value: 实际值
        expected_maximum: 期望的最大值
    """
    with allure.step(f"验证值 {value} 小于 {expected_maximum}"):
        assert value < expected_maximum, \
            f"值断言失败：期望小于{expected_maximum}，实际{value}"


def assert_list_length(json_data: Dict[str, Any], path: str, expected_length: int):
    """
    断言列表长度
    
    Args:
        json_data: JSON数据
        path: JSON路径表达式（应指向一个列表）
        expected_length: 期望的列表长度
    """
    expr = parse(path)
    match = expr.find(json_data)
    with allure.step(f"验证列表 {path} 长度为 {expected_length}"):
        assert match, f"未找到字段：{path}"
        actual_value = match[0].value
        assert isinstance(actual_value, list), f"字段值不是列表类型: {type(actual_value)}"
        actual_length = len(actual_value)
        assert actual_length == expected_length, \
            f"列表长度断言失败：期望{expected_length}，实际{actual_length}"