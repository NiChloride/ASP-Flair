from django.contrib import admin

from aspsite.models import *


admin.site.register(Item)
admin.site.register(ItemCategory)
admin.site.register(Distance)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(User)
admin.site.register(Dispatch_Record)
admin.site.register(Deliver_Record)
admin.site.register(Dispatch_Queue)
admin.site.register(Pack)
admin.site.register(Packing_Queue)
admin.site.register(Token)
