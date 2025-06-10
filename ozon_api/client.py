import requests
import json
import hmac
import hashlib
import time
from typing import Dict, List, Optional, Any, Union

from .exceptions import OzonAPIError
from .utils import retry_on_failure


class OzonAPIClient:
    """Ozon广告API客户端"""
    
    def __init__(self, client_id: str, api_key: str, base_url: str = "https://performance.ozon.ru/api/v1"):
        """
        初始化Ozon API客户端
        
        Args:
            client_id: Ozon API的client_id
            api_key: Ozon API的api_key
            base_url: API基础URL
        """
        self.client_id = client_id
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self._configure_session()
    
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
    
    # 其他方法保持不变...
