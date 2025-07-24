"""
请求处理器
用于处理测试过程中的HTTP请求，包括会话管理、请求参数构建、响应处理等功能
"""

import requests
import json
import allure
import logging
from typing import Dict, Any, Union, Optional
from urllib.parse import urlencode
from jsonpath_ng import parse

# 配置日志
logger = logging.getLogger(__name__)


class RequestHandler:
    """HTTP请求处理器类"""

    def __init__(self, base_url: str = ""):
        """
        初始化请求处理器
        
        Args:
            base_url (str): 基础URL，用于替换请求中的占位符
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def set_token(self, token: str):
        """
        设置认证token
        
        Args:
            token (str): 认证token
        """
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info(f"Token已设置: {token[:10]}...")  # 只记录前10位用于调试

    def clear_token(self):
        """清除认证token"""
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        logger.info("Token已清除")

    def build_request_params(self, method: str, headers: Dict[str, str], 
                           params: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        """
        根据请求方法和内容类型构建请求参数
        
        Args:
            method (str): HTTP请求方法
            headers (Dict[str, str]): 请求头
            params (Union[Dict[str, Any], str]): 请求参数
            
        Returns:
            Dict[str, Any]: 构建好的请求参数
        """
        content_type = headers.get("Content-Type", "")
        request_params = {}

        if method == "GET":
            request_params["params"] = params
        elif method == "POST":
            if "application/json" in content_type:
                request_params["json"] = params
            elif "application/x-www-form-urlencoded" in content_type:
                # 如果参数是字典，转换为表单编码格式
                if isinstance(params, dict):
                    request_params["data"] = urlencode(params)
                else:
                    # 如果参数是字符串，直接使用
                    request_params["data"] = params
            else:
                request_params["data"] = params
        elif method in ["PUT", "PATCH"]:
            if "application/json" in content_type:
                request_params["json"] = params
            elif "application/x-www-form-urlencoded" in content_type:
                # 如果参数是字典，转换为表单编码格式
                if isinstance(params, dict):
                    request_params["data"] = urlencode(params)
                else:
                    # 如果参数是字符串，直接使用
                    request_params["data"] = params
            else:
                request_params["data"] = params
        elif method == "DELETE":
            request_params["params"] = params
        else:
            raise ValueError(f"不支持的请求方法: {method}")

        return request_params

    def send_request(self, method: str, url: str, headers: Optional[Dict[str, str]] = None,
                    params: Optional[Union[Dict[str, Any], str]] = None, 
                    timeout: int = 30) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method (str): HTTP请求方法 (GET, POST, PUT, DELETE等)
            url (str): 请求URL
            headers (Optional[Dict[str, str]]): 请求头
            params (Optional[Union[Dict[str, Any], str]]): 请求参数
            timeout (int): 超时时间（秒）
            
        Returns:
            requests.Response: HTTP响应对象
        """
        # 替换基础URL占位符
        if self.base_url:
            url = url.replace("{{portal.mall}}", self.base_url)
        
        # 合并请求头
        request_headers = dict(self.session.headers)
        if headers:
            request_headers.update(headers)
            
        # 构建请求参数
        request_params = self.build_request_params(method, request_headers, params or {})
        
        logger.info(f"发送请求: {method} {url}")
        logger.info(f"请求头: {request_headers}")
        logger.info(f"请求参数: {request_params}")
        
        # 添加Allure步骤
        with allure.step(f"发送 {method} 请求到 {url}"):
            allure.attach(json.dumps(request_headers, ensure_ascii=False, indent=2), 
                         name="请求头", attachment_type=allure.attachment_type.JSON)
            if params:
                if isinstance(params, dict):
                    allure.attach(json.dumps(params, ensure_ascii=False, indent=2), 
                                 name="请求参数", attachment_type=allure.attachment_type.JSON)
                else:
                    allure.attach(str(params), name="请求参数", 
                                 attachment_type=allure.attachment_type.TEXT)
        
        # 发送请求
        response = self.session.request(
            method=method,
            url=url,
            headers=request_headers,
            timeout=timeout,
            **request_params
        )
        
        # 记录响应
        logger.info(f"收到响应: 状态码={response.status_code}")
        logger.info(f"响应内容: {response.text}")
        
        # 添加响应到Allure报告
        with allure.step(f"收到响应，状态码: {response.status_code}"):
            allure.attach(response.text, name=f"响应内容", 
                         attachment_type=allure.attachment_type.TEXT)
            
        return response

    def extract_json_field(self, json_data: Dict[str, Any], path: str) -> Any:
        """
        从JSON数据中提取指定路径的值
        
        Args:
            json_data (Dict[str, Any]): JSON数据
            path (str): JSON路径表达式
            
        Returns:
            Any: 提取到的值，未找到返回None
        """
        try:
            expr = parse(path)
            match = expr.find(json_data)
            return match[0].value if match else None
        except Exception as e:
            logger.warning(f"提取JSON字段失败 {path}: {e}")
            return None

    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("请求会话已关闭")