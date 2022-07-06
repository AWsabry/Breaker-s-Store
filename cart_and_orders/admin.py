from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Order
from django.conf import settings



class CartItemsAdmin(admin.TabularInline):
    model = CartItems
    # raw_id_fields = ['product']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'total_price',
                    'ordered_date',
                    'Cart_Name',
                    'PhoneNumber',

                    ]
    inlines = [
        CartItemsAdmin,
    ]
    search_fields = ['user']


    
    def Cart_Name(self, obj):
        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'totalPrice',
                    'delivered',
                    'paid',
                    'ordered_date',
                    'id',
                    'OrderName',
                    'PhoneNumber',

                    ]
    list_display_links = [
        'user',
    ]
    list_filter = ['user',
                   'delivered',
                   'ordered_date',
                   ]
    search_fields = ['user']


    def OrderName(self, obj):
        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber


class BromoCodeAdmin(admin.ModelAdmin):
    list_filter = ("active", "code",)
    list_display = ('code', "percentage", 'created', "active")

    search_fields = ['code']


class DeliveryfeesAdmin(admin.ModelAdmin):
    list_filter = ("city", "delivery_fees",)
    list_display = ('city', "delivery_fees", 'ordered_date','active')
    search_fields = ['city']



admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)

# admin.site.register(CartItems)
# admin.site.register(BromoCode, BromoCodeAdmin)
