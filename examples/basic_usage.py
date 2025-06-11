import pandas as pd
from ozon_api.client import OzonAPIClient

# 配置文件路径
config_file = '../config.ini'

# 初始化客户端
client = OzonAPIClient(config_file)

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

            # 将数据保存到Excel文件
            data_frames = {
                'Campaigns': pd.DataFrame(campaigns),
                'Campaign Stats': pd.DataFrame(stats),
                'Ad Groups': pd.DataFrame(ad_groups),
                'Ads': pd.DataFrame(ads),
                'Ad Stats': pd.DataFrame(ad_stats)
            }

            with pd.ExcelWriter('ozon_api_data.xlsx') as writer:
                for sheet_name, df in data_frames.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()