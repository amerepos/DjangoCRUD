from .base import method_decorator, csrf_exempt, view_catch_error, BaseView


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class ChoicesView(BaseView):
    def get(self, request, filters):
        self.data = self.schema_class.get()
        return self._respond()
