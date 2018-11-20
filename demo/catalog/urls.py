from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('c/', views.clinicManager, name='c'),
    path('reg/', views.registration, name='reg'),
    path('',views.signin,name='signin'),
    url(r'^reg/validate_username/$', views.validate_username, name='validate_username'),
]

