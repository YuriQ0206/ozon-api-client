from typing import Dict, List, Optional, Any, Union
from datetime import datetime

class BaseModel:
    """基础模型类"""
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BaseModel':
        """从字典创建模型实例"""
        return cls(**data)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self.__dict__


class Campaign(BaseModel):
    """广告活动模型"""
    
    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        status: str,
        budget: float,
        daily_budget: float,
        created_at: str,
        updated_at: str,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.type = type
        self.status = status
        self.budget = budget
        self.daily_budget = daily_budget
        self.created_at = self._parse_datetime(created_at)
        self.updated_at = self._parse_datetime(updated_at)
        
        # 添加其他字段
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def _parse_datetime(self, datetime_str: str) -> Optional[datetime]:
        """解析日期时间字符串"""
        if not datetime_str:
            return None
        try:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except ValueError:
            return datetime_str


class AdGroup(BaseModel):
    """广告组模型"""
    
    def __init__(
        self,
        id: int,
        campaign_id: int,
        name: str,
        status: str,
        bid: float,
        **kwargs
    ):
        self.id = id
        self.campaign_id = campaign_id
        self.name = name
        self.status = status
        self.bid = bid
        
        # 添加其他字段
        for key, value in kwargs.items():
            setattr(self, key, value)


class Ad(BaseModel):
    """广告模型"""
    
    def __init__(
        self,
        id: int,
        ad_group_id: int,
        product_id: int,
        status: str,
        **kwargs
    ):
        self.id = id
        self.ad_group_id = ad_group_id
        self.product_id = product_id
        self.status = status
        
        # 添加其他字段
        for key, value in kwargs.items():
            setattr(self, key, value)


class Statistic(BaseModel):
    """统计数据模型"""
    
    def __init__(
        self,
        date: str,
        clicks: int = 0,
        impressions: int = 0,
        spent: float = 0.0,
        orders: int = 0,
        revenue: float = 0.0,
        **kwargs
    ):
        self.date = date
        self.clicks = clicks
        self.impressions = impressions
        self.spent = spent
        self.orders = orders
        self.revenue = revenue
        
        # 添加其他字段
        for key, value in kwargs.items():
            setattr(self, key, value)
