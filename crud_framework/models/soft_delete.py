from django.db import models


class _SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self):
        print('delete')
        self.update(is_deleted=True)


class _SoftDeleteManager(models.Manager):
    def get_query_set(self):
        return _SoftDeleteQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return super(_SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


class SoftDeleteMixin:
    is_deleted = models.BooleanField(default=False, null=False, blank=True, db_index=True)
    objects = _SoftDeleteManager()#TODO doesnt work
