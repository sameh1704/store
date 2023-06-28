from django.contrib import admin
from .models import Product_Category, Brand, Building, Room, Incoming , ResponsiblePerson, Order , Outgoing, MonitoringScreen, InventoryReport




class IncomingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Incoming, IncomingAdmin)
readonly_fields = ('barcode_number',)
 
admin.site.register(Product_Category)
admin.site.register(Brand)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(ResponsiblePerson)
admin.site.register(Order)
admin.site.register(Outgoing)
admin.site.register(MonitoringScreen)
admin.site.register(InventoryReport)