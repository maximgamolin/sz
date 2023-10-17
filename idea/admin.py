from django.contrib import admin

from abs.admin import BaseModelAdmin
from .models import Actor, ChainLink, Chain, Idea


class ActorAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['name']
    search_fields = ['name']
    filter_horizontal = ('managers', 'groups')


class ChainLinkAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['actor', 'name', 'is_technical', 'order', 'chain']
    list_filter = ['is_technical', 'chain']
    search_fields = ['name']


class ChainAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['author', 'reject_chain_link', 'accept_chain_link']
    search_fields = ['author__username']


class IdeaAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['name', 'author', 'body', 'chain', 'current_chain_link', 'idea_uid']
    search_fields = ['name', 'author__username', 'idea_uid']


admin.site.register(Actor, ActorAdmin)
admin.site.register(ChainLink, ChainLinkAdmin)
admin.site.register(Chain, ChainAdmin)
admin.site.register(Idea, IdeaAdmin)