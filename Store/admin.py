from django.contrib import admin

# Register your models here.
from . models import *


class Productadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cat', 'price')


class Categoryadmin(admin.ModelAdmin):
    list_display = ('id', 'main_cat', 'category', 'cat_gender')


class MainCategoryadmin(admin.ModelAdmin):
    list_display = ('id', 'mcat', 'mcat_date')


class OrderItemadmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'date_added')


class ShippingAddressadmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'date_added')


class Orderadmin(admin.ModelAdmin):
    list_display = ('customer', 'transaction_id',
                    'complete', 'date_orderd')


admin.site.register(Customer)
admin.site.register(Product, Productadmin)
admin.site.register(Order, Orderadmin)
admin.site.register(Category, Categoryadmin)
admin.site.register(MainCategory, MainCategoryadmin)
admin.site.register(OrderItem, OrderItemadmin)
admin.site.register(ShippingAddress, ShippingAddressadmin)
admin.site.register(UserAdderess)
