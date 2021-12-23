import json
from pprint import pprint
from urllib.parse import parse_qsl

from django.db.models import Model
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse

from player.views.views import GuardedView


class ListView(GuardedView):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get(self, request, model: Model):
        model_list = model.objects.all().values()
        # pprint(list(model_list))
        return JsonResponse(list(model_list), safe=False)

    def post(self, request: HttpRequest, model: Model):
        print(f'Hit POST endpoint for {model}')
        if request.content_type == 'application/json':
            body_data = json.loads(request.body)
        elif request.content_type == 'application/x-www-form-urlencoded':
            body_data = dict(parse_qsl(request.body.decode('utf-8')))
        else:
            return HttpResponseBadRequest()
        print('BODY:', body_data)

        created_object = model.objects.create(**body_data)
        # pprint(created_object)
        created_object.save()
        return HttpResponse()

    def delete(self, request, model: Model):
        model.objects.all().delete()
        return HttpResponse()


class SingleView(GuardedView):
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']

    def get(self, request, model: Model, model_id):
        pprint(model.objects.get(id=model_id))
        return HttpResponse()

    def put(self, request, model: Model, model_id):
        model.objects.update_or_create(id=model_id, defaults=request.POST["item_data"]).save()
        return HttpResponse()

    def patch(self, request: HttpRequest, model: Model, model_id):
        print(f'Hit PATCH endpoint for {model}')
        if request.content_type == 'application/json':
            body_data = json.loads(request.body)
        elif request.content_type == 'application/x-www-form-urlencoded':
            body_data = dict(parse_qsl(request.body.decode('utf-8')))
        else:
            return HttpResponseBadRequest()
        print('BODY:', body_data)
        model_instance = model.objects.get(id=model_id)

        for attribute in body_data:
            print(attribute)
            setattr(model_instance, attribute, body_data[attribute])

        model_instance.save()

        return HttpResponse()

    def delete(self, request, model: Model, model_id):
        model.objects.get(id=model_id).delete()
        return HttpResponse()
