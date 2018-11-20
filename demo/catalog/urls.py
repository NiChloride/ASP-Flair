from django.urls import path
from . import views

urlpatterns = [
    path('', views.supply, name='index'),
]

