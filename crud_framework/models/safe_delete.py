from django.db.models import Q, BooleanField
from safedelete import models as safedelete_models
from crud_framework.errors import Error


class SoftDeleteCascadeMixin(safedelete_models.SafeDeleteModel):
    class Meta:
        abstract = True

    UNIQUE_FIELDS = []
    _safedelete_policy = safedelete_models.SOFT_DELETE_CASCADE
    is_deleted = BooleanField(default=False, null=False, blank=True)

    def clean_unique(self):
        if not self.UNIQUE_FIELDS:
            return True
        filters = {f: getattr(self, f) for f in self.UNIQUE_FIELDS}
        if self.__class__.objects.filter(~Q(pk=self.pk), is_deleted=False, **filters).exists():
            data = ', '.join([f'{field_name} {getattr(self, field_name)}' for field_name in self.UNIQUE_FIELDS])
            raise Error(message=f'{data} already exist!', field_name=self.UNIQUE_FIELDS[-1])

    def clean(self):
        self.clean_unique()
        super(SoftDeleteCascadeMixin, self).clean()

    def save(self, *args, **kwargs):
        if self.deleted:
            self.is_deleted = True
        super(SoftDeleteCascadeMixin, self).save(*args, **kwargs)
