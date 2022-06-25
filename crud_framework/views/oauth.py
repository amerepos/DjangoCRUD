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


class _SetUserCrudView(BaseCrudView):
    def get(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).get(
            request=request, initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).post(
            request=request, initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).put(
            request=request, initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).delete(
            request=request, initkwargs=dict(user=request.resource_owner), *args, **kwargs)


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthChoiceView(ProtectedResourceMixin, OAuthLibMixin, ChoicesView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthCrudView(ProtectedResourceMixin, OAuthLibMixin, _SetUserCrudView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthFunctionalView(ProtectedResourceMixin, OAuthLibMixin, BaseView):
    pass
