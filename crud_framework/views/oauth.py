from oauth2_provider.views.mixins import ProtectedResourceMixin, OAuthLibMixin
from .base import method_decorator, csrf_exempt, view_catch_error, BaseCrudView, BaseView
from .lookups import ChoicesView


# def set_user(f): TODO
#     def wrap(self, request, *args, **kwargs):
#         self.user = request.resource_owner
#         return f(self=self, request=request, *args, **kwargs)
#
#     wrap.__doc__ = f.__doc__
#     wrap.__name__ = f.__name__
#     return wrap


class SetUserMixin:
    def __init__(self, *args, **kwargs):
        super(SetUserMixin, self).__init__(*args, **kwargs)
        self.user = None

    def get(self, request, *args, **kwargs):
        self.user = request.resource_owner
        print(f'USER: {self.user}')
        return super(SetUserMixin, self).get(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = request.resource_owner
        print(f'USER: {self.user}')
        return super(SetUserMixin, self).get(request=request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.user = request.resource_owner
        print(f'USER: {self.user}')
        return super(SetUserMixin, self).get(request=request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.user = request.resource_owner
        print(f'USER: {self.user}')
        return super(SetUserMixin, self).get(request=request, *args, **kwargs)


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthChoiceView(ProtectedResourceMixin, OAuthLibMixin, SetUserMixin, ChoicesView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthCrudView(ProtectedResourceMixin, OAuthLibMixin, SetUserMixin, BaseCrudView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthFunctionalView(ProtectedResourceMixin, OAuthLibMixin, SetUserMixin, BaseView):
    pass
