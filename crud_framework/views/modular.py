from .base import method_decorator, csrf_exempt, view_catch_error, BaseCrudView


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class CrudView(BaseCrudView):
    pass
