from django.urls import path

from idea.views import IndexView, AllMyIdeas, IdeaView

urlpatterns = [
    path('my-ideas/', AllMyIdeas.as_view(), name='my_ideas'),
    path('idea-create/', AllMyIdeas.as_view(), name='idea_create'),
    path('idea/<str:idea_uid>/', IdeaView.as_view(), name='idea'),
    path('', IndexView.as_view())
]
