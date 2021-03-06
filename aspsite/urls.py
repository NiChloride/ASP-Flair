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
    path('', views.mainpage),
    path('forget_password', views.forgetPassword),
    path('reset_password_request', views.processResetPassword),
    path('reset_password', views.resetPassword),
    path('register', views.register.as_view()),
    path('profile', views.Profile.as_view()),
    path('login_handling', views.login_handling.as_view()),

    path('clinic_manager_item', views.clinicManagerItem.as_view()),
    path('clinic_manager_item_description/<int:itemid>', views.clinicManagerDescription.as_view()),
    path('clinic_manager_order', views.clinicManagerOrder.as_view(), name = 'clinic_manager_order'),
    path('receive_confirmation', views.receive_confirmation),

    path('warehouse_personnel_order', views.warehousePersonnelOrder.as_view(), name = 'warehouse_personnel_order'),
    path('warehouse_personnel_checklist/<int:orderid>', views.warehousePersonnelChecklist.as_view()),

    path('dispatcher_order', views.dispatcherOrder.as_view(), name = 'dispatcher_order'),

    path('token', views.TokenView.as_view()),
    #path('sendToken', views.sendToken),
    path('send_token', views.send_token),
    

    path('changeInfo', views.changeProfile),
    path('makeOrder', views.makeOrder),
    path('cancel_order/<int:orderid>', views.cancel_order),
    path('processOrder', views.processOrder),
    path('pack', views.pack),
    path('dispatch_selected', views.dispatch_selected),
    path('sendShippingLabel', views.sendShippingLabel),
    path('download_itinerary', views.download_itinerary),
    #path('dispatch/<int:orderid>', views.dispatch),
    path('dispatch_drone', views.dispatch_drone),
    path("new_account", views.new_account),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
