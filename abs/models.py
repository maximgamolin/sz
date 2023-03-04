from django.db import models


class BaseModel(models.Model):
    version = models.SmallIntegerField(verbose_name='Версия', default=0)
    is_deleted = models.BooleanField(verbose_name='Удален?', default=False)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.version += 1
        return super(BaseModel, self).save(force_insert, force_update, using, update_fields)