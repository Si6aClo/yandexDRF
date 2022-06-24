from rest_framework.test import APITestCase
from rest_framework import status
import json

from marketAPI.models import ShopUnit

class MarketAPIGetByDateTestCase(APITestCase):
    def test_getSingleOffer(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=5500
        )

        now_date = "2022-02-01T12:00:00.000Z"
        response = self.client.get(f'/sales?date={now_date}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)

    def test_getBadFormatDate(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=5500
        )

        now_date = "2022-02-01T12:00:00.0Z"
        response = self.client.get(f'/sales?date={now_date}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_getUpdatedDate(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=5500
        )
        data = {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Товары",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                    "price": 6500
                }
            ],
            "updateDate": "2022-02-03T12:00:00.000Z"
        }
        response = self.client.post('/imports', json.dumps(data), content_type='application/json')

        now_date = "2022-02-03T15:00:00.000Z"
        response = self.client.get(f'/sales?date={now_date}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)

    def test_getMoreData(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары1",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=5500
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            name="Товары2",
            date="2022-02-02T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=6500
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            name="Товары3",
            date="2022-02-03T12:00:00.000Z",
            parentId=None,
            type="OFFER",
            price=7500
        )

        now_date = "2022-02-03T12:00:00.000Z"
        response = self.client.get(f'/sales?date={now_date}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)

        now_date = "2022-02-03T15:00:00.000Z"
        response = self.client.get(f'/sales?date={now_date}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)