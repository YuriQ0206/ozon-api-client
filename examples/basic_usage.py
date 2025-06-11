from ozon_api.client import OzonAPIClient
from ozon_api.config import Config
import pandas as pd

# 配置文件路径
config_file = '../config.ini'
config = Config(config_file)

# 初始化客户端
client = OzonAPIClient(config_file)

date_from = config.get('date_from')
date_to = config.get('date_to')

def main():
    try:
        # 获取广告活动列表
        campaigns = client.get_campaigns()
        print(f"获取到 {len(campaigns)} 个广告活动")

        campaign_data = []
        ad_group_data = []
        ad_data = []
        campaign_stats_data = []
        ad_stats_data = []

        if campaigns:
            for campaign in campaigns:
                campaign_id = campaign["id"]
                print(f"广告活动: {campaign['name']} (ID: {campaign_id})")
                campaign_data.append(campaign)

                # 获取广告活动统计数据
                stats = client.get_campaign_stats(
                    campaign_id=campaign_id,
                    date_from=date_from,
                    date_to=date_to,
                    metrics=["clicks", "impressions", "spent", "orders"]
                )
                campaign_stats = {
                    "campaign_id": campaign_id,
                    **stats
                }
                campaign_stats_data.append(campaign_stats)
                print(f"广告活动统计: {stats}")

                # 获取广告组列表
                ad_groups = client.get_ad_groups(campaign_id=campaign_id)
                print(f"获取到 {len(ad_groups)} 个广告组")

                for ad_group in ad_groups:
                    ad_group_id = ad_group["id"]
                    ad_group_data.append({
                        "campaign_id": campaign_id,
                        **ad_group
                    })
                    print(f"广告组: {ad_group['name']} (ID: {ad_group_id})")

                    # 获取广告列表
                    ads = client.get_ads(campaign_id=campaign_id, ad_group_id=ad_group_id)
                    print(f"获取到 {len(ads)} 个广告")

                    for ad in ads:
                        ad_id = ad["id"]
                        ad_data.append({
                            "campaign_id": campaign_id,
                            "ad_group_id": ad_group_id,
                            **ad
                        })
                        print(f"广告: (ID: {ad_id})")

                        # 获取广告统计数据
                        ad_stats = client.get_ad_stats(
                            campaign_id=campaign_id,
                            ad_group_id=ad_group_id,
                            ad_id=ad_id,
                            date_from=date_from,
                            date_to=date_to,
                            metrics=["clicks", "impressions", "spent", "orders"]
                        )
                        ad_stats_data.append({
                            "campaign_id": campaign_id,
                            "ad_group_id": ad_group_id,
                            "ad_id": ad_id,
                            **ad_stats
                        })
                        print(f"广告统计: {ad_stats}")

        # 将数据保存为 Excel 文件
        campaign_df = pd.DataFrame(campaign_data)
        ad_group_df = pd.DataFrame(ad_group_data)
        ad_df = pd.DataFrame(ad_data)
        campaign_stats_df = pd.DataFrame(campaign_stats_data)
        ad_stats_df = pd.DataFrame(ad_stats_data)

        with pd.ExcelWriter('ozon_ads_data.xlsx') as writer:
            campaign_df.to_excel(writer, sheet_name='Campaigns', index=False)
            ad_group_df.to_excel(writer, sheet_name='AdGroups', index=False)
            ad_df.to_excel(writer, sheet_name='Ads', index=False)
            campaign_stats_df.to_excel(writer, sheet_name='CampaignStats', index=False)
            ad_stats_df.to_excel(writer, sheet_name='AdStats', index=False)

        print("数据已保存到 ozon_ads_data.xlsx 文件中。")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()