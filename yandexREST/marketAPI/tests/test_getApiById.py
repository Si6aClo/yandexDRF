from rest_framework.test import APITestCase
from rest_framework import status

from marketAPI.models import ShopUnit


class MarketAPIGetByIdTestCase(APITestCase):
    def test_getOffer(self):
        self.get_big_db()
        response = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df7')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['children'], None)

    def test_getSimpleCategory(self):
        self.get_big_db()
        response = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2')
        response_child1 = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df4')
        response_child2 = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df5')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['children'], [response_child1.data, response_child2.data])

    def test_getHardCategory(self):
        self.get_big_db()
        response = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
        response_child1 = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2')
        response_child2 = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['children'], [response_child1.data, response_child2.data])

    def test_getEmptyCategory(self):
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            name="Товары",
            date="2022-02-01T12:00:00.000Z",
            parentId=None,
            type="CATEGORY"
        )

        response = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['children'], [])

    def test_getNotFound(self):
        self.get_big_db()

        response = self.client.get('/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df9')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
            price=3000
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
            name="Телефоны2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
            type="OFFER",
            price=4000
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df6",
            name="Компьютеры1",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            type="OFFER",
            price=5000
        )
        ShopUnit.objects.create(
            id="069cb8d7-bbdd-47d3-ad8f-82ef4c269df7",
            name="Компьютеры2",
            date="2022-02-01T12:00:00.000Z",
            parentId="069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
            type="OFFER",
            price=6000
        )