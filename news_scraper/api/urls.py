from django.urls import path
from .views import news

urlpatterns = [
    path('api/news', news)
]
