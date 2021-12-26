import json
from pprint import pprint
from urllib.parse import parse_qsl

from django.db import models
from django.db.models import Model
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse

from player.views.views import GuardedView


class ListView(GuardedView):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get(self, request, model: Model):
        model_list = model.objects.all().values()
        return JsonResponse(list(model_list), safe=False)

    def post(self, request: HttpRequest, model: Model):
        print(f'Hit POST endpoint for {model}')

        try:
            body_data = get_body_data(request)
        except NotImplementedError as error:
            return HttpResponseBadRequest(error)

        print('BODY:', body_data)

        created_object = model.objects.create(**body_data)
        created_object.save()
        return JsonResponse(created_object)

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

        try:
            body_data = get_body_data(request)
        except NotImplementedError as error:
            return HttpResponseBadRequest(error)

        print('BODY:', body_data)

        model_instance = model.objects.get(id=model_id)

        for attribute in body_data:
            if isinstance(model_instance._meta.get_field(attribute), models.ForeignKey):
                setattr(model_instance, f'{attribute}_id', body_data[attribute])
            else:
                setattr(model_instance, attribute, body_data[attribute])

        pprint(model_instance)

        model_instance.save()

        return HttpResponse()

    def delete(self, request, model: Model, model_id):
        model.objects.get(id=model_id).delete()
        return HttpResponse()


def get_body_data(request):
    if request.content_type == 'application/json':
        body_data = json.loads(request.body)
    elif request.content_type == 'application/x-www-form-urlencoded':
        body_data = dict(parse_qsl(request.body.decode('utf-8')))
    else:
        raise NotImplementedError(f'Content_Type {request.content_type} cannot be parsed.')

    return body_data
