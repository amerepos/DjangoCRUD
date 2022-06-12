from oauth2_provider.views.mixins import ProtectedResourceMixin, OAuthLibMixin
from crud_framework.views.base_views import CrudView


class OauthCrudView(ProtectedResourceMixin, OAuthLibMixin, CrudView):
    pass
