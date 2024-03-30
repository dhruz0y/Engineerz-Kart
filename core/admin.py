from django.contrib import admin
from core.models import *
# Register your models here.

class OrderItemTubleinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTubleinline]

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Shop)
admin.site.register(Filter_Price)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)

