from oauth2_provider.views.mixins import ProtectedResourceMixin, OAuthLibMixin
from .base import method_decorator, csrf_exempt, view_catch_error, BaseCrudView, BaseView
from .lookups import ChoicesView


# def set_user(f): TODO
#     def wrap(self, request, *args, **kwargs):
#         self.user = request.resource_owner
#         return f(self=self,  *args, **kwargs)
#
#     wrap.__doc__ = f.__doc__
#     wrap.__name__ = f.__name__
#     return wrap


class _SetUserCrudView(BaseCrudView):
    def get(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).get(
            initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).post(files=request._files.dict(), body=request._post.dict(),
                                                  initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).put(files=request._files.dict(), body=request._post.dict(),
                                                 initkwargs=dict(user=request.resource_owner), *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(_SetUserCrudView, self).delete(
            initkwargs=dict(user=request.resource_owner), *args, **kwargs)


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthChoiceView(ProtectedResourceMixin, ChoicesView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthCrudView(ProtectedResourceMixin, _SetUserCrudView):
    pass


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthFunctionalView(ProtectedResourceMixin, BaseView):
    pass
