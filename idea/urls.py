from django.urls import path

from idea.views import IndexView, AllMyIdeas

urlpatterns = [
    path('my-ideas', AllMyIdeas.as_view(), name='my_ideas'),
    path('', IndexView.as_view())
]
