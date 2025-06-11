import os
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理
        
        Args:
            config_file: 配置文件路径
        """
        self.config = {}
        self._load_defaults()
        
        if config_file:
            self._load_from_file(config_file)
        
        self._load_from_env()
    
    def _load_defaults(self):
        """加载默认配置"""
        self.config = {
            "base_url": "https://performance.ozon.ru/api/v1",
            "timeout": 30,
            "max_retries": 3,
            "backoff_factor": 1.0,
            "debug": False,
            "date_from": "2023-01-01",
            "date_to": "2023-12-31"
        }
    
    def _load_from_file(self, config_file: str):
        """从配置文件加载配置"""
        if not os.path.exists(config_file):
            return
        
        ext = os.path.splitext(config_file)[1].lower()
        if ext == '.json':
            with open(config_file, 'r') as f:
                self.config.update(json.load(f))
        elif ext == '.yaml' or ext == '.yml':
            try:
                import yaml
                with open(config_file, 'r') as f:
                    self.config.update(yaml.safe_load(f))
            except ImportError:
                pass
        elif ext == '.ini':
            import configparser
            config = configparser.ConfigParser()
            config.read(config_file)
            if 'ozon_api' in config:
                ozon_api_config = config['ozon_api']
                self.config["client_id"] = ozon_api_config.get("client_id", self.config.get("client_id", ""))
                self.config["api_key"] = ozon_api_config.get("api_key", self.config.get("api_key", ""))
                self.config["date_from"] = ozon_api_config.get("date_from", self.config.get("date_from", ""))
                self.config["date_to"] = ozon_api_config.get("date_to", self.config.get("date_to", ""))
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        self.config["client_id"] = os.getenv("OZON_CLIENT_ID", self.config.get("client_id", ""))
        self.config["api_key"] = os.getenv("OZON_API_KEY", self.config.get("api_key", ""))
        self.config["base_url"] = os.getenv("OZON_BASE_URL", self.config.get("base_url", ""))
        self.config["debug"] = os.getenv("OZON_DEBUG", self.config.get("debug", False))
        self.config["date_from"] = os.getenv("OZON_DATE_FROM", self.config.get("date_from", ""))
        self.config["date_to"] = os.getenv("OZON_DATE_TO", self.config.get("date_to", ""))
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        self.config[key] = value
    
    def __getitem__(self, key: str) -> Any:
        """通过索引获取配置项"""
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any):
        """通过索引设置配置项"""
        self.config[key] = value
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self.config.copy()