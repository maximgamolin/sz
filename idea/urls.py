from django.urls import path, re_path

from idea.views import IndexView, AllMyIdeas, IdeaView, IdeaCreate

urlpatterns = [
    path('my-ideas/', AllMyIdeas.as_view(), name='my_ideas'),
    path('create/', IdeaCreate.as_view(), name='create'),
    re_path(r'(?P<idea_uid>[0-9a-f-]{36})/$', IdeaView.as_view(), name='idea'),
    path('', IndexView.as_view())
]
