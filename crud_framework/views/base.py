from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from furl import furl
from django.views.generic import View
from crud_framework.errors import Error


def my_furl(url):
    args = furl(url=url).args
    res = {}
    for k in args.keys():
        vs = args.allvalues(k)
        res[k] = vs if len(vs) > 1 else vs[0]
    return res


def view_catch_error(f):
    def wrap(request, *args, **kwargs):
        try:
            try:
                filters = my_furl(request.build_absolute_uri())
            except:
                filters = {}

            return f(filters=filters, *args, **kwargs)
        except Error as e:
            return JsonResponse(status=e.status, data=dict(e))
        except Exception as e:
            data = dict(e)
            data['error_message'] = str(e)
            return JsonResponse(status=301, data=data)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class BaseView(View):
    SCHEMA_CLASS = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.schema_class = self.SCHEMA_CLASS

    @classmethod
    def get_path(cls):
        return cls.SCHEMA_CLASS.PATH

    @classmethod
    def get_route_kwargs(cls):
        return dict(route=cls.get_path(), view=cls.as_view(), name=cls.SCHEMA_CLASS.__name__)

    # TODO filters for class not per function
    # TODO handle foreign key
    def _respond(self):
        if self.data:
            return JsonResponse(status=201, data=self.data, safe=False)
        else:
            return HttpResponse(status=204)

    def get(self, filters):
        raise NotImplemented('GET not Allowed!')

    def post(self, body, filters, **kwargs):
        raise NotImplemented('POST not Allowed!')

    def put(self, body, filters, **kwargs):
        raise NotImplemented('PUT not Allowed!')

    def delete(self, filters, **kwargs):
        raise NotImplemented('DELETE not Allowed!')


class BaseCrudView(BaseView):

    def get(self, filters, **kwargs):
        crud = self.schema_class(filters=filters, initkwargs=kwargs.pop('initkwargs', {}))
        self.data = crud.get()
        return self._respond()

    def post(self, body, filters, **kwargs):
        print('in post')
        crud = self.schema_class(filters=filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in kwargs.pop('files', {}).items():
            # print(v.__dict__) todo change content from b''
            # with open('tmp') as t:
            #     t.write(v['file'].read())
            #     print(t.__dict__)
            body[k] = v

        self.data = crud.post(**body, **kwargs)
        return self._respond()

    def bulk_post(self, body, filters, **kwargs):
        crud = self.schema_class(filters=filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in kwargs.pop('files', {}).items():
            body[k] = v

        self.data = crud.bulk_post(data=body, **filters, **kwargs)
        return self._respond()

    def put(self, body, filters, **kwargs):
        crud = self.schema_class(filters=filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in kwargs.pop('files', {}).items():
            body[k] = v

        self.data = crud.put(**body, **kwargs)
        return self._respond()

    def delete(self, filters, **kwargs):
        crud = self.schema_class(filters=filters, initkwargs=kwargs.pop('initkwargs', {}))
        if not crud.delete():
            return HttpResponse(status=404)
        return self._respond()

    @classmethod
    def get_doc(cls, request):
        crud = cls.SCHEMA_CLASS({})
        return render(crud.template_path)
