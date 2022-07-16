from .base import method_decorator, csrf_exempt, view_catch_error, BaseCrudView, unjsonize


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class CrudView(BaseCrudView):
    def get(self, request, *args, **kwargs):
        return super(CrudView, self).get(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CrudView, self).post(body=unjsonize(request.body.decode()), request=request, *args, **kwargs)

    def post_file(self, request, *args, **kwargs):
        return super(CrudView, self).post_file(
            request=request, files=request._files.dict(), body=request._post.dict(), *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super(CrudView, self).put(body=unjsonize(request.body.decode()), request=request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(CrudView, self).delete(request=request, *args, **kwargs)
