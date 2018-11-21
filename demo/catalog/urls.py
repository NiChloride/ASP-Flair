from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('c/', views.clinicManager, name='c'),
    path('reg/', views.registration, name='reg'),
    path('',views.signin,name='signin'),
    url('validate_username/', views.validate_username, name='validate_username'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)