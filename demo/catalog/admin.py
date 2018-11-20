from django.contrib import admin
from import_export.admin import *
# Register your models here.
from .models import Supply, Order, OrderSupplyMatching, Clinic,Drone,DistanceBetween2Clinics,Category

# Define the admin class
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name','weight','image')
    #fields = ['image_tag']
    #readonly_fields = ['image_tag']

# Register the admin class with the associated model
admin.site.register(Supply, SupplyAdmin)

@admin.register(OrderSupplyMatching)
class OrderSupplyMatchingAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Drone)
class DroneAdmin(ImportExportModelAdmin):
    pass

@admin.register(DistanceBetween2Clinics)
class DistanceBetween2ClinicsAdmin(admin.ModelAdmin):
    list_display = ('clinicA','clinicB','distance')

class OrderSupplyMatchingInline(admin.TabularInline):
    model = OrderSupplyMatching

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','priority','status','weight','destination')
    list_filter = ('status','priority', 'orderedtime','dispatchedtime','arrivedtime')
    inlines = [OrderSupplyMatchingInline]

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name','latitude','longitude','altitude')
