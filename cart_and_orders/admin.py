from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Codes, Order
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


class CodesAdmin(admin.TabularInline):
    model = Codes
    list_display = ('id')
    # raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'totalPrice',
                    'paid',
                    'ordered_date',
                    'id',
                    'OrderName',
                    'PhoneNumber',

                    ]
    inlines = [
        CodesAdmin,
    ]
    list_filter = ['user',
                   'ordered_date',
                   ]
    search_fields = ['user']


    def OrderName(self, obj):
        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber





class CodeAdmin(admin.ModelAdmin):
    list_display = ('code','codeCategory','user','price','order','addToCart','ordered','id','active','created','total_profit_calculated_from_sales')
    list_filter = ('codeCategory','user','addToCart','ordered','active',)
    readonly_fields = ['total_profit_calculated_from_sales','price','profit'] 

    search_fields = ['code']
 


class CartItemssAdmin(admin.ModelAdmin):
    list_display = ('id',)



admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Codes,CodeAdmin)


admin.site.register(CartItems,CartItemssAdmin)
# admin.site.register(BromoCode, BromoCodeAdmin)
