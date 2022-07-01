from .base import method_decorator, csrf_exempt, view_catch_error, BaseCrudView


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class CrudView(BaseCrudView):
    def get(self, request, *args, **kwargs):
        return super(CrudView, self).get(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(CrudView, self).post(files=request.FILES.dict(), body=request.POST.dict(),
                                          request=request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super(CrudView, self).put(files=request.FILES.dict(), body=request.POST.dict(),
                                         request=request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(CrudView, self).delete(request=request, *args, **kwargs)
