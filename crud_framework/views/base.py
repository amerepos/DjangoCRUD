from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from furl import furl
from django.views.generic import View
from json import loads as unjsonize
from crud_framework.errors import Error
from django.conf import settings
from django.core.exceptions import ValidationError

from django.db.models import Q


def my_furl(url):  # TODO test injection
    args = furl(url=url).args
    filters = {}
    q_filters = []
    for k in args.keys():
        vs = args.allvalues(k)
        if len(vs) > 1:  # List filter
            filters[k] = vs
        else:
            vs = vs[0]  # Normal filter
            if '|' not in vs:  # Doesnt contain OR
                filters[k] = vs
            else:  # OR filter
                f = {k: vs.split('|')[0]}  # First argument
                d = []
                ff = Q(**f)
                for i in vs.split('|')[1:]:  # Rest of OR arguments
                    j = i.split('=')
                    f = {j[0]: j[1]}
                    d.append(Q(**f))

                for f in d:
                    ff = ff | f
                q_filters.append((ff))

    return filters, q_filters


def view_catch_error(f):
    def wrap(request, *args, **kwargs):
        if hasattr(settings, 'logger'):
            settings.logger.info(f'REQUEST: {request.method} || URL: {request.build_absolute_uri()}')
        try:
            filters, q_filters = my_furl(request.build_absolute_uri())

            return f(request=request, filters=filters, q_filters=q_filters, *args, **kwargs)

        except Error as e:
            return JsonResponse(status=e.status, safe=False, data=[dict(e)])

        except ValidationError as errors:
            data = []
            for att, err in dict(errors).items():
                if isinstance(err, list):
                    err = '.\n'.join(err)
                err = err.replace('Is deleted, ', '')
                err = err.replace('Is deleted and ', '')
                data.append(dict(Error(field_name=att, message=str(err))))

            return JsonResponse(status=406, safe=False, data=data)

        except Exception as e:
            return JsonResponse(status=406, safe=False, data=[dict(Error(field_name=None, message=str(e),
                                                                         description='Something unexpectedly went wrong!'))])

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

    # TODO handle foreign key
    def _respond(self):
        if self.data:
            return JsonResponse(status=201, data=self.data, safe=False)
        else:
            return HttpResponse(status=204)

    def get(self, request, filters, q_filters):
        if hasattr(settings, 'logger'):
            settings.logger.debug(f'GET || Filters: {str(filters)}')
        raise NotImplemented('GET not Allowed!')

    def post(self, request, body, filters, q_filters, **kwargs):
        if hasattr(settings, 'logger'):
            settings.logger.debug(f'GET || Filters: {str(filters)} || Data {body}')
        raise NotImplemented('POST not Allowed!')

    def post_file(self, request, body, files, filters, q_filters, **kwargs):
        if hasattr(settings, 'logger'):
            settings.logger.debug(f'GET || Filters: {str(filters)} || Data {body} || Files {files}')
        raise NotImplemented('POST not Allowed!')

    def put(self, request, body, filters, q_filters, **kwargs):
        if hasattr(settings, 'logger'):
            settings.logger.debug(f'GET || Filters: {str(filters)} || Data {body}')
        raise NotImplemented('PUT not Allowed!')

    def delete(self, request, filters, q_filters, **kwargs):
        if hasattr(settings, 'logger'):
            settings.logger.debug(f'GET || Filters: {str(filters)}')
        raise NotImplemented('DELETE not Allowed!')


class BaseCrudView(BaseView):

    def get(self, request, filters, q_filters, **kwargs):
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))
        self.data = crud.get()
        return self._respond()

    def post(self, request, body, filters, q_filters, **kwargs):
        print('in post')
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))
        self.data = crud.post(**body, **kwargs)
        return self._respond()

    def post_file(self, request, body, files, filters, q_filters, **kwargs):
        print('in post')
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in files.items():
            # print(v.__dict__) todo change content from b''
            # with open('tmp') as t:
            #     t.write(v['file'].read())
            #     print(t.__dict__)
            body[k] = v

        self.data = crud.post(**body, **kwargs)
        return self._respond()

    def bulk_post(self, request, body, filters, q_filters, **kwargs):
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in kwargs.pop('files', {}).items():
            body[k] = v

        self.data = crud.bulk_post(data=body, **filters, **kwargs)  # TODO ,q_filters=q_filters
        return self._respond()

    def put(self, request, body, filters, q_filters, **kwargs):
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))

        for k, v in kwargs.pop('files', {}).items():
            body[k] = v

        self.data = crud.put(**body, **kwargs)
        return self._respond()

    def delete(self, request, filters, q_filters, **kwargs):
        crud = self.schema_class(filters=filters, q_filters=q_filters, initkwargs=kwargs.pop('initkwargs', {}))
        if not crud.delete():
            return HttpResponse(status=404)
        return self._respond()

    @classmethod
    def get_doc(cls, request):
        crud = cls.SCHEMA_CLASS({})
        return render(request, crud.template_path)
