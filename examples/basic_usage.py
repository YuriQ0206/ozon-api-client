from ozon_api.client import OzonAPIClient
from ozon_api.config import Config
import os

# 加载配置
config = Config()
config["client_id"] = os.getenv("OZON_CLIENT_ID", "your_client_id")
config["api_key"] = os.getenv("OZON_API_KEY", "your_api_key")

# 初始化客户端
client = OzonAPIClient(
    client_id=config["client_id"],
    api_key=config["api_key"],
    base_url=config["base_url"]
)

def main():
    try:
        # 获取广告活动列表
        campaigns = client.get_campaigns()
        print(f"获取到 {len(campaigns)} 个广告活动")
        
        if campaigns:
            campaign = campaigns[0]
            campaign_id = campaign["id"]
            print(f"第一个广告活动: {campaign['name']} (ID: {campaign_id})")
            
            # 获取广告活动统计数据
            stats = client.get_campaign_stats(
                campaign_id=campaign_id,
                date_from="2023-01-01",
                date_to="2023-12-31",
                metrics=["clicks", "impressions", "spent", "orders"]
            )
            
            print(f"广告活动统计: {stats}")
            
            # 获取广告组列表
            ad_groups = client.get_ad_groups(campaign_id=campaign_id)
            print(f"获取到 {len(ad_groups)} 个广告组")
            
            if ad_groups:
                ad_group_id = ad_groups[0]["id"]
                print(f"第一个广告组: {ad_groups[0]['name']} (ID: {ad_group_id})")
                
                # 获取广告列表
                ads = client.get_ads(campaign_id=campaign_id, ad_group_id=ad_group_id)
                print(f"获取到 {len(ads)} 个广告")
                
                if ads:
                    ad_id = ads[0]["id"]
                    print(f"第一个广告: (ID: {ad_id})")
                    
                    # 获取广告统计数据
                    ad_stats = client.get_ad_stats(
                        campaign_id=campaign_id,
                        ad_group_id=ad_group_id,
                        ad_id=ad_id,
                        date_from="2023-01-01",
                        date_to="2023-12-31",
                        metrics=["clicks", "impressions", "spent", "orders"]
                    )
                    print(f"广告统计: {ad_stats}")
    
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
