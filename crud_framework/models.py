from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class BaseTypes:
    @classmethod
    def get_choices(cls):
        res = []
        for k, v in cls.__dict__.items():
            if k not in ['__module__', '__dict__', '__weakref__', '__doc__']:
                res.append((v, v))
        return res


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.getter_model = kwargs.pop('getter_model', ValueError('model is required'))
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.getter_model.objects.get_queryset()


class BaseModel(models.Model):
    pass


class BaseTrackedModel(BaseModel):
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    is_deleted = models.BooleanField(default=False, null=False, blank=False)
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='%(class)s_editor_user')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='%(class)s_creator_user')

    def __init__(self):
        super(BaseTrackedModel, self).__init__()
        # todo update editor


class BaseHistoryModel(BaseTrackedModel):
    history = HistoricalRecords(inherit=True, related_name='log')
