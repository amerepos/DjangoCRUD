from django.db.models import UniqueConstraint, Q, BooleanField
from safedelete import models as safedelete_models


class SoftDeleteCascadeMixin(safedelete_models.SafeDeleteModel):
    class Meta:
        abstract = True

    _safedelete_policy = safedelete_models.SOFT_DELETE_CASCADE
    is_deleted = BooleanField(default=False, null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.deleted:
            self.is_deleted = True
        super(SoftDeleteCascadeMixin, self).save(*args, **kwargs)
