from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
import datetime
import re

from .models import ShopUnit


# Класс для создания новых моделей или обновления старых в базе данных
# Путь imports/
class MarketAPICreate(APIView):
    def post(self, request):
        # Проверка на повторяющиеся id
        # Если id нет в массиве, значит его добавляем
        # В ином случае, если такой id уже был добавлен ранее, отправляем ответ со статусом 400
        ids = []
        for data in request.data['items']:
            if data['id'] not in ids:
                ids.append(data['id'])
            else:
                return Response({'code': 400, "message": "Validation Failed"}, status=400)

        # Флаг, означающий, соответствует ли пришедшие данные всем условиям
        fi = True
        # Извлекаем время добавления данных
        now_date = request.data['updateDate']

        for data in request.data['items']:
            # Если какое-то из условий не выполнено, выходим из цикла и ставим флаг в False
            if data['name'] == None \
                or (data['type'] != "CATEGORY" and (not data['price'] or data['price'] < 0)) \
                or (data['type'] == "CATEGORY" and ('price' in data and not(data['price'] is None))) \
                or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', now_date):
                fi = False
                break

        if fi:
            for data in request.data['items']:
                # Этот флаг отображает, есть ли такая запись в базе данных или нет
                fl = True
                # Создаём переменную для id родителя для дальнейших операций
                parent_id = None
                # Элемент, с которым производятся действия
                curr_item = None
                # Пытаемся получить элемент по id, в ином случае ставим флаг в False
                try:
                    curr_item = ShopUnit.objects.get(id=data['id'])
                except:
                    fl = False

                # Если такого элемента нет в базе данных, сохраняем его туда
                # Если возникает какая-то ошибка при создании записи, ставим флаг в False и выходим из цикла
                # Если такой элемент есть, просто обновляем в нём данные, при ошибка ставим флаг в False и выходим из цикла
                # Сохраняем id родителя
                if not fl:
                    try:
                        post_new = ShopUnit.objects.create(
                            id=data['id'],
                            name=data['name'],
                            date=now_date,
                            parentId=data['parentId'] if 'parentId' in data else None,
                            price=data['price'] if data['type'] != "CATEGORY" else None,
                            type=data['type']
                        )
                        parent_id = data['parentId'] if 'parentId' in data else None

                    except:
                        fi = False
                        break
                else:
                    if curr_item.type == data['type']:
                        curr_item.name = data['name']
                        curr_item.parentId = data['parentId'] if 'parentId' in data else None
                        curr_item.price = data['price']
                        curr_item.date = now_date
                        curr_item.save(update_fields=["name", 'type', 'parentId', 'price', 'date'])
                        parent_id = data['parentId'] if 'parentId' in data else None
                    else:
                        fi = False
                        break
                # Получаем первый родительский элемент для добавленной строки
                parent_category = ShopUnit.objects.filter(id=parent_id)
                # Пока мы находим следующий родительский элемент, мы обновляем у него дату обновления и переходим выше
                while len(parent_category) > 0:
                    parent_category[0].date = now_date
                    new_id = parent_category[0].parentId
                    parent_category[0].save()
                    parent_category = ShopUnit.objects.filter(id=new_id)

        # Если флаг стоит в положении False возвращаем сообщение с кодом 400
        if fi:
            return Response({'code': 200, "message": "Validation Successfully"})
        else:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)


# Класс для удаления элемента по id и всех его дочерних элементов
# Путь delete/{id}
class MarketAPIDelete(APIView):
    def delete(self, request, *args, **kwargs):
        # получаем id элемента и возвращаем код ошибки 400 при неправильном url
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        # Пытаемся достать элемент из БД, если такого нет - возвращаем код ошибки 404
        curr_item = None
        try:
            curr_item = ShopUnit.objects.get(id=pk)
        except:
            return Response({'code': 404, "message": "Item not found"}, status=404)

        # Пытаемся удалить все дочерние ошибки, при возникновении ошибки возвращаем код ошибки 400
        try:
            self.deleteTree(curr_item)
        except:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)
        # Если в процессе не возникло ошибок, возвращаем код 200
        return Response({'code': 200, "message": "Validation Successfully"})

    # Реккурсивный алгоритм для удаления всех дочерних элементов
    def deleteTree(self, curr_item):
        # Получаем всех детей текущего элемента
        allChildren = ShopUnit.objects.filter(parentId=curr_item.id)
        # Проходим по каждому из детей
        # Если это дочерний элемент с типом категория, то и для него запускаем функцию deleteTree
        # В ином случае просто удаляем элемент
        for item in allChildren:
            if item.type == 'CATEGORY':
                self.deleteTree(item)
            else:
                item.delete()
        # В конце удаляем и текущий элемент
        curr_item.delete()


# Класс для получения элемента и всех его дочерних элементов по id
# Путь nodes/{id}
class MarketAPIGetById(APIView):
    def get(self, request, *args, **kwargs):
        # получаем id элемента и возвращаем код ошибки 400 при неправильном url
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        # Пытаемся достать элемент из БД, если такого нет - возвращаем код ошибки 404
        curr_item = None
        try:
            curr_item = ShopUnit.objects.get(id=pk)
        except:
            return Response({'code': 404, "message": "Item not found"}, status=404)

        # Получаем всё дерево
        curr_object = self.getNextTree(curr_item)

        # Возвращаем значение
        return Response(curr_object)

    # Рекурсивная функция для получения количества и суммы всех дочерних элементов типа оффер
    def getSumAndCount(self, curr_item):
        count = 0
        totalSum = 0
        # Проходимся по всем дочерним элементам
        # Если тип элемента категория, то для него тоже вызываем функцию
        # В ином случае прибавляем к count - 1, а в сумму - цену элемента
        for item in curr_item['children']:
            if item['type'] == 'CATEGORY':
                countFunc, totalSumFunc = self.getSumAndCount(item)
                count += countFunc
                totalSum += totalSumFunc
            else:
                count += 1
                totalSum += item['price']
        # Возвращаем количество и сумму товаров
        return count, totalSum

    # Рекурсивная функция для получения всех дочерних элементов для текущего элемента
    def getNextTree(self, curr_item):
        # Преобразуем текущий элемент в dict
        curr_object = model_to_dict(curr_item)
        # Если тип элемента не категория, то детей быть не должно, присваиваем None
        if curr_object['type'] != "CATEGORY":
            curr_object['children'] = None
        else:
            # Получаем всех текущих детей элемента по id
            curr_children = ShopUnit.objects.filter(parentId=curr_object['id'])
            curr_object['children'] = []

            # Проходим по всем текущим дочерним элементам
            for item in curr_children:
                # Преобразовываем в словарь
                new_item = model_to_dict(item)

                # Если тип элемента не категория, назначаем у него children в None,
                # Преобразовываем в нужный формат дату
                # Добавляем у текущего элемента в chilren дочерний элемент
                if new_item['type'] != 'CATEGORY':
                    new_item['children'] = None
                    new_date = new_item['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    new_item['date'] = new_date[:-4] + new_date[-1]
                    curr_object['children'].append(new_item)
                # Если тип данных категория, то запускаем функцию getNextTree
                # Добавляем полученный дочерний элемент в текущий
                else:
                    newTree = self.getNextTree(item)
                    curr_object['children'].append(newTree)

        # Преобразовываем в нужный формат дату
        new_date = curr_object['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        curr_object['date'] = new_date[:-4] + new_date[-1]

        # Если массив children не пустой или не None считаем сумму и кол-во элементов дочерних элементов
        if curr_object['children']:
            count = 0
            totalSum = 0
            # Повторяем всё то же самое, что и в рекурсивном алгоритме
            for item in curr_object['children']:
                if item['type'] == 'CATEGORY':
                    countFunc, totalSumFunc = self.getSumAndCount(item)
                    count += countFunc
                    totalSum += totalSumFunc
                else:
                    count += 1
                    totalSum += item['price']
            # Расчитываем price и записываем
            curr_object['price'] = int(totalSum / count)
        # Возвращаем готовый текущий элемент
        return curr_object


# Класс для получение
# Путь sales/
class MarketAPIGetByDate(APIView):

    def get(self, request):
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', request.query_params.get('date')):
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        # Сравниваем даты и сохраняем только те, которые принадлежат отрезку
        now_time = datetime.datetime.fromisoformat(request.query_params.get('date')[:-1])\
                            .astimezone(datetime.timezone(datetime.timedelta(hours=0),name="UTC"))
        past_time = now_time - datetime.timedelta(days=1)

        # Получаем все элементы с классом OFFER
        curr_items = ShopUnit.objects.filter(type="OFFER")

        # Сравниваем даты и сохраняем только те, которые принадлежат отрезку
        try:
            new_items = [dict(model_to_dict(item), **{'date': str(item.date)})
                         for item in curr_items
                         if past_time <= item.date - datetime.timedelta(hours=3) <= now_time]
        except :
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        # Возвращаем значения
        return Response({"items" : new_items})
