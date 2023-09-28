from django.db import models

from abs.models import BaseModel


class Actor(BaseModel):
    managers = models.ManyToManyField('accounts.CustomUser', verbose_name='менеджеры', blank=True)
    groups = models.ManyToManyField('accounts.SiteGroup', verbose_name='Группы менеджеров', blank=True)
    name = models.CharField(verbose_name='Название', max_length=120)


class ChainLink(BaseModel):
    actor = models.ForeignKey('idea.Actor', verbose_name='Актор', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Название', max_length=120)
    is_technical = models.BooleanField(verbose_name='Является ли техническим звеном')
    order = models.PositiveSmallIntegerField(verbose_name='Номер в цепочке', null=True, blank=True)
    chain = models.ForeignKey('idea.Chain', verbose_name='Цепочка', on_delete=models.CASCADE, null=True, blank=True)


class Chain(BaseModel):

    author = models.ForeignKey('accounts.CustomUser', verbose_name='Автор', on_delete=models.CASCADE)
    reject_chain_link = models.ForeignKey(
        'idea.ChainLink',
        verbose_name='Звено для отклоненных',
        on_delete=models.CASCADE,
        related_name='reject_chain_links'
    )
    accept_chain_link = models.ForeignKey(
        'idea.ChainLink',
        verbose_name='Звено для принятых',
        on_delete=models.CASCADE,
        related_name='accept_chain_links'
    )


class Idea(BaseModel):
    name = models.CharField(verbose_name='Имя', max_length=255)
    author = models.ForeignKey('accounts.CustomUser', verbose_name='Автор', on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Текст')
    chain = models.ForeignKey('idea.Chain', verbose_name='Цепочка', on_delete=models.CASCADE)
    current_chain_link = models.ForeignKey('idea.ChainLink', verbose_name='Текущий этап', on_delete=models.CASCADE)
    idea_uid = models.CharField(verbose_name='Уникальный идентификатор', max_length=255, unique=True)
