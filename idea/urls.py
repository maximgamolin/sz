from django.urls import path
from idea.views import IndexView

urlpatterns = [
    path('', IndexView.as_view())
]
