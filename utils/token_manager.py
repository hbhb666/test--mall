# Token管理器
import logging

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self.tokens = {}

    def save_token(self, case_id, token_data):
        """保存token，支持保存完整的token信息（包括tokenHead和token）
        Args:
            case_id: 用例ID
            token_data: token数据，可以是字符串或包含tokenHead和token的字典
        """
        if isinstance(token_data, dict) and 'tokenHead' in token_data and 'token' in token_data:
            # 如果是字典格式，包含tokenHead和token，则组合存储
            full_token = token_data['tokenHead'] + token_data['token']
            self.tokens[case_id] = full_token
            logger.info(f"完整Token已保存: {case_id}")
        else:
            # 如果是字符串格式，直接存储
            self.tokens[case_id] = token_data
            logger.info(f"Token已保存: {case_id}")

    def get_token(self, case_id):
        """获取token"""
        token = self.tokens.get(case_id)
        if token:
            logger.info(f"获取到Token: {case_id}")
        else:
            logger.warning(f"未找到Token: {case_id}")
        return token

    def clear_tokens(self):
        """清空所有token"""
        self.tokens.clear()
        logger.info("所有Token已清空")