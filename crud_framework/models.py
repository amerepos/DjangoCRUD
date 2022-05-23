from django.db import models


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.getter_model = kwargs.pop('getter_model', ValueError('model is required'))
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.getter_model.objects.get_queryset()


class BaseModel(models.Model):
    pass
