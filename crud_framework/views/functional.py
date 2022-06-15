from .base import method_decorator, csrf_exempt, view_catch_error, BaseView


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class FunctionalView(BaseView):
    pass
