import requests
import json
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any, Union
import configparser

from .exceptions import OzonAPIError
from .utils import retry_on_failure


class OzonAPIClient:
    """Ozon广告API客户端"""

    def __init__(self, config_file: str, base_url: str = "https://performance.ozon.ru/api/v1"):
        """
        初始化Ozon API客户端

        Args:
            config_file: 配置文件的路径
            base_url: API基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self._configure_session()

        # 读取配置文件
        config = configparser.ConfigParser()
        config.read(config_file)

        # 获取 client_id 和 api_key
        try:
            self.client_id = config.get('ozon_api', 'client_id')
            self.api_key = config.get('ozon_api', 'api_key')
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise ValueError("配置文件中缺少必要的配置项，请检查 'ozon_api' 部分的 'client_id' 和 'api_key'。")

    def _configure_session(self):
        """配置请求会话"""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Host": "performance.ozon.ru"
        })

    def _generate_signature(self, method: str, url: str, body: Optional[Dict] = None) -> str:
        """生成API请求签名"""
        timestamp = str(int(time.time()))
        request_path = url.replace(self.base_url, "")

        body_str = json.dumps(body, separators=(',', ':')) if body else ""
        message = f"{timestamp}{method}{request_path}{body_str}"

        return hmac.new(
            self.api_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

    @retry_on_failure(max_retries=3, backoff_factor=1)
    def _make_request(self, method: str, endpoint: str, body: Optional[Dict] = None) -> Dict:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        timestamp = str(int(time.time()))
        signature = self._generate_signature(method, url, body)

        headers = {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp
        }

        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=headers, json=body)
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=headers, json=body)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers, json=body)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise OzonAPIError(f"API请求错误: {str(e)}", response=getattr(e, 'response', None))
        except json.JSONDecodeError:
            raise OzonAPIError(f"API响应解析错误: {response.text}", response=response)

    # 广告活动相关方法
    def get_campaigns(self, filter_params: Optional[Dict] = None) -> List[Dict]:
        """获取广告活动列表"""
        endpoint = "/campaigns"
        return self._make_request("GET", endpoint).get('campaigns', [])

    def create_campaign(self, campaign_data: Dict) -> Dict:
        """创建广告活动"""
        endpoint = "/campaigns"
        return self._make_request("POST", endpoint, campaign_data)

    def get_campaign_stats(self, campaign_id: int, date_from: str, date_to: str, metrics: List[str]) -> Dict:
        """获取广告活动统计数据"""
        endpoint = f"/campaigns/{campaign_id}/stats"
        body = {
            "date_from": date_from,
            "date_to": date_to,
            "metrics": metrics
        }
        return self._make_request("POST", endpoint, body)

    def get_ad_groups(self, campaign_id: int) -> List[Dict]:
        """获取广告组列表"""
        endpoint = f"/campaigns/{campaign_id}/ad_groups"
        return self._make_request("GET", endpoint).get('ad_groups', [])

    def get_ads(self, campaign_id: int, ad_group_id: int) -> List[Dict]:
        """获取广告列表"""
        endpoint = f"/campaigns/{campaign_id}/ad_groups/{ad_group_id}/ads"
        return self._make_request("GET", endpoint).get('ads', [])

    def get_ad_stats(self, campaign_id: int, ad_group_id: int, ad_id: int, date_from: str, date_to: str, metrics: List[str]) -> Dict:
        """获取广告统计数据"""
        endpoint = f"/campaigns/{campaign_id}/ad_groups/{ad_group_id}/ads/{ad_id}/stats"
        body = {
            "date_from": date_from,
            "date_to": date_to,
            "metrics": metrics
        }
        return self._make_request("POST", endpoint, body)