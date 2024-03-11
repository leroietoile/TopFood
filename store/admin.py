from django.contrib import admin

# Register your models here.
from .models import Plat, Category, Order, Cart, DeliveryPrice


class PlatAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'price')


# Register your models here.
admin.site.register(Plat, PlatAdmin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(DeliveryPrice)
