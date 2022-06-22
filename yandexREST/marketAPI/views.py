from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
import datetime

from .models import ShopUnit

class MarketAPICreate(APIView):
    def post(self, request):
        ids = []
        for data in request.data['items']:
            if data['id'] not in ids:
                ids.append(data['id'])
            else:
                return Response({'code': 400, "message": "Validation Failed"}, status=400)

        fi = True
        now_date = request.data['updateDate']
        for data in request.data['items']:
            fl = True
            curr_item = None

            if data['name'] == None or \
                (data['type'] != "CATEGORY" and (not data['price'] or data['price'] < 0)):
                fi = False
                break

            parent_id = None

            try:
                curr_item = ShopUnit.objects.get(id = data['id'])
            except:
                fl = False

            if not fl:
                try:
                    post_new = ShopUnit.objects.create(
                        id = data['id'],
                        name = data['name'],
                        date = now_date,
                        parentId = data['parentId'] if 'parentId' in data else None,
                        price = data['price'] if data['type'] != "CATEGORY" else None,
                        type = data['type']
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
            parent_category = ShopUnit.objects.filter(id=parent_id)
            while len(parent_category) > 0:
                parent_category[0].date = now_date
                new_id = parent_category[0].parentId
                parent_category[0].save()
                parent_category = ShopUnit.objects.filter(id=new_id)


        if fi:

            return Response({'code': 200, "message": "Validation Successfully"})
        else:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

class MarketAPIDelete(APIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        curr_item = None
        try:
            curr_item = ShopUnit.objects.get(id = pk)
        except:
            return Response({'code': 404, "message": "Item not found"}, status=404)

        try:
            ShopUnit.objects.filter(parentId = curr_item.id).delete()
            curr_item.delete()
        except:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        return Response({'code': 200, "message": "Validation Successfully"})

class MarketAPIGetById(APIView):
    def getSumAndCount(self, curr_item):
        count = 0
        totalSum = 0
        for item in curr_item['children']:
            if item['type'] == 'CATEGORY':
                countFunc, totalSumFunc = self.getSumAndCount(item)
                count += countFunc
                totalSum += totalSumFunc
            else:
                count += 1
                totalSum += item['price']
        return count, totalSum

    def getNextTree(self, curr_item):
        curr_object = model_to_dict(curr_item)
        if curr_object['type'] != "CATEGORY":
            curr_object['children'] = None
        else:
            curr_children = ShopUnit.objects.filter(parentId=curr_object['id'])
            curr_object['children'] = []
            arrOfPrices = []

            for item in curr_children:
                new_item = model_to_dict(item)
                newTree = None
                if new_item['type'] != 'CATEGORY':
                    new_item['children'] = None
                    new_date = new_item['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    new_item['date'] = new_date[:-4] + new_date[-1]
                    curr_object['children'].append(new_item)
                else:
                    newTree = self.getNextTree(item)
                    curr_object['children'].append(newTree)

                if not newTree:
                    arrOfPrices.append(new_item['price'])
                else:
                    arrOfPrices.append(newTree['price'])
            if len(arrOfPrices) != 0:
                curr_object['price'] = int(sum(arrOfPrices) / len(arrOfPrices))

        new_date = curr_object['date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        curr_object['date'] = new_date[:-4] + new_date[-1]

        if curr_object['children']:
            count = 0
            totalSum = 0
            for item in curr_object['children']:
                if item['type'] == 'CATEGORY':
                    countFunc, totalSumFunc = self.getSumAndCount(item)
                    count += countFunc
                    totalSum += totalSumFunc
                else:
                    count += 1
                    totalSum += item['price']
            curr_object['price'] = int(totalSum / count)

        return curr_object

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'code': 400, "message": "Validation Failed"}, status=400)

        curr_item = None
        try:
            curr_item = ShopUnit.objects.get(id=pk)
        except:
            return Response({'code': 404, "message": "Item not found"}, status=404)

        curr_object = self.getNextTree(curr_item)

        return Response(curr_object)

class MarketAPIGetByDate(APIView):
    def get(self, request):
        curr_items = None
        try:
            curr_items = ShopUnit.objects.filter(type = "OFFER")
        except:
            return Response({'code': 404, "message": "Item not found"}, status=404)

        for item in curr_items:
            print(model_to_dict(item))
        now_time = datetime.datetime.fromisoformat(str(datetime.datetime.utcnow()) + '+00:00')
        past_time = now_time - datetime.timedelta(days=1)

        new_items = [dict(model_to_dict(item), **{'date': datetime.datetime.fromisoformat(str(item.date))})
                     for item in curr_items
                     if past_time <= datetime.datetime.fromisoformat(str(item.date)) <= now_time]

        return Response(new_items)
