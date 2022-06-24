from rest_framework.test import APITestCase
from rest_framework import status
import json
from datetime import datetime

from marketAPI.models import ShopUnit


class MarketAPIPostTestCase(APITestCase):
    def test_postStandart(self):
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товары",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Продукт",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "price": 79000
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }
        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShopUnit.objects.count(), 2)

    def test_postEqualIds(self):
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товары",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                },
                {
                    "type": "OFFER",
                    "name": "Продукт",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "price": 79000
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_postNullName(self):
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": None,
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_postNullCategoryPrice(self):
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товар",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                    "price": 30000
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_postNullOfferPrice(self):
        data = {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Товар",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                    "price": None
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_postUncorrectOfferPrice(self):
        data = {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Товар",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                    "price": -1000
                }
            ],
            "updateDate": "2022-02-01T12:00:00.000Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_postUncorrectDate(self):
        data = {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Товар",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                    "price": -1000
                }
            ],
            "updateDate": "2022-02-01T12:00:00.0Z"
        }

        response = self.client.post('/imports', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ShopUnit.objects.count(), 0)
