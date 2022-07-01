from django.conf import settings
from django.db import models

from crud_framework.errors import Error


class BaseChoices:
    @classmethod
    def get_choices(cls):
        res = []
        for k, v in cls.__dict__.items():
            if k not in ['__module__', '__dict__', '__weakref__', '__doc__']:
                res.append((v, v))
        return res

    @classmethod
    def is_choice_or_err(cls, value):
        for _, v in cls.get_choices():
            if value == v:
                return True
        raise Error(field_name=cls.__name__, message=f'({value}) is not a choice')


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.getter_model = kwargs.pop('getter_model', ValueError('model is required'))
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.getter_model.objects.get_queryset()


# TODO handle errors
# TODO Soft delete model
class BaseModel(models.Model):
    class Meta:
        abstract = True


class BaseTrackedModel(BaseModel):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='%(class)s_editor_user')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='%(class)s_creator_user')

    def __init__(self, *args, **kwargs):
        super(BaseTrackedModel, self).__init__(*args, **kwargs)
        if self.editor and not self.creator:
            self.creator = self.editor

    @classmethod
    def get_user_field(cls):
        raise NotImplemented('Refer user_field to filter')
