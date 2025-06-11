import unittest
from unittest.mock import patch, MagicMock
import json
import configparser
import os

from ozon_api.client import OzonAPIClient
from ozon_api.exceptions import OzonAPIError


class TestOzonAPIClient(unittest.TestCase):

    def setUp(self):
        # 创建一个临时的配置文件
        config = configparser.ConfigParser()
        config['ozon_api'] = {
            'client_id': 'test_client_id',
            'api_key': 'test_api_key'
        }
        with open('test_config.ini', 'w') as configfile:
            config.write(configfile)

        self.client = OzonAPIClient('test_config.ini')

    def tearDown(self):
        # 删除临时配置文件
        if os.path.exists('test_config.ini'):
            os.remove('test_config.ini')

    @patch('requests.Session.get')
    def test_get_campaigns(self, mock_get):
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"campaigns": [{"id": 1, "name": "Test Campaign"}]}
        mock_get.return_value = mock_response

        # 调用方法
        campaigns = self.client.get_campaigns()

        # 验证结果
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]["name"], "Test Campaign")

        # 验证请求参数
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://performance.ozon.ru/api/v1/campaigns")
        self.assertIn("headers", kwargs)
        headers = kwargs["headers"]
        self.assertEqual(headers["Client-Id"], 'test_client_id')
        self.assertEqual(headers["Api-Key"], 'test_api_key')

    @patch('requests.Session.post')
    def test_create_campaign(self, mock_post):
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "Test Campaign"}
        mock_post.return_value = mock_response

        # 测试数据
        campaign_data = {"name": "Test Campaign", "type": "search"}

        # 调用方法
        result = self.client.create_campaign(campaign_data)

        # 验证结果
        self.assertEqual(result["name"], "Test Campaign")

        # 验证请求参数
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://performance.ozon.ru/api/v1/campaigns")
        self.assertIn("headers", kwargs)
        self.assertIn("json", kwargs)
        self.assertEqual(kwargs["json"], campaign_data)

    @patch('requests.Session.get')
    def test_api_error(self, mock_get):
        # 模拟API错误响应
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = Exception("HTTP Error 400")
        mock_get.return_value = mock_response

        # 验证异常
        with self.assertRaises(OzonAPIError):
            self.client.get_campaigns()


if __name__ == '__main__':
    unittest.main()