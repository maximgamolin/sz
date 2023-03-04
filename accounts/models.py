from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    groups = models.ManyToManyField('accounts.SiteGroup')

    def __str__(self):
        return self.username


class SiteGroup(Group):
    pass
