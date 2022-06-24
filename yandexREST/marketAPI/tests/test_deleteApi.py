from rest_framework.test import APITestCase
from rest_framework import status

from marketAPI.models import ShopUnit


class MarketAPIDeleteTestCase(APITestCase):
    def test_deleteCategory(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            price=None,
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
            name="Товары2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            price=5500,
            type="OFFER"
        )

        response = self.client.delete('/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_deleteOffer(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            price=None,
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
            name="Товары2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            price=5500,
            type="OFFER"
        )

        response = self.client.delete('/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShopUnit.objects.count(), 1)

    def test_deleteNotFound(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            price=None,
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
            name="Товары2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            price=5500,
            type="OFFER"
        )

        response = self.client.delete('/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deleteFullTree(self):
        self.get_big_db()

        response = self.client.delete('/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShopUnit.objects.count(), 0)

    def test_deleteSomeTree(self):
        self.get_big_db()

        response = self.client.delete('/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShopUnit.objects.count(), 4)

    def get_big_db(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            name="Телефоны",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            name="Компьютеры",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            type="CATEGORY"
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
            name="Телефоны1",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            type="OFFER",
            price=5500
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
            name="Телефоны2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            type="OFFER",
            price=5500
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df6",
            name="Компьютеры1",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            type="OFFER",
            price=5500
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df7",
            name="Компьютеры2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            type="OFFER",
            price=5500
        )
