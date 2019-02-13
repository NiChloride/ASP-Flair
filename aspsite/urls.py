"""



The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login),
    path('forget_password', views.forgetPassword),
    path('reset_password_request', views.processResetPassword),
    path('reset_password', views.resetPassword),
    path('register', views.register.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('login_handling', views.login_handling.as_view()),

    path('clinic_manager_item', views.ClinicManagerView.as_view()),
    path('clinic_manager_item_description/<int:itemid>', views.ItemDescriptionView.as_view()),
    path('clinic_manager_order', views.OrderView.as_view(), name = 'clinic_manager_order'),
    path('receive_confirmation', views.receive_confirmation),

    path('warehouse_personnel_order', views.WarehousePersonnelView.as_view(), name = 'warehouse_personnel_order'),
    path('warehouse_personnel_checklist/<int:orderid>', views.OrderItemsView.as_view()),

    path('dispatcher_order', views.DispatcherView.as_view(), name = 'dispatcher_order'),

    
    

    path('apply_changes', views.edit_profile),
    path('place_order', views.place_order),
    path('cancel_order/<int:orderid>', views.cancel_order),
    path('process_order', views.process_order),
    path('packing', views.packing),
    path('dispatch_selected', views.dispatch_selected),
    path('sendShippingLabel', views.sendShippingLabel),
    path('download_itinerary', views.download_itinerary),
    path('send_token', views.send_token),
    path('dispatch_drone', views.dispatch_drone),
    path("new_account", views.new_account),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
