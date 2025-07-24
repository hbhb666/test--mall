# Token管理器
import logging

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self.tokens = {}

    def save_token(self, case_id, token):
        """保存token"""
        self.tokens[case_id] = token
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
