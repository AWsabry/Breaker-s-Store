from django.contrib import admin
from cart_and_orders.models import Cart, CartItems, Codes, Order


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
                    'total_price_after_taxes',
                    'paid',
                    'ordered_date',
                    'id',
                    'OrderName',
                    'PhoneNumber',
                    'order_response',
                    'paid_by',
                    ]
    inlines = [
        CodesAdmin,
    ]
    list_filter = ['paid',
                   'ordered_date',
                   'user'
                   ]
    search_fields = ['user__email']


    def OrderName(self, obj):
        return   str(obj.user.first_name) + " " + str(obj.user.last_name)
      

    def PhoneNumber(self, obj):
        return obj.user.PhoneNumber





class CodeAdmin(admin.ModelAdmin):
    list_display = ('code','codeCategory','user','price','order','addToCart','ordered','paid','id','active','created')
    list_filter = ('codeCategory','addToCart','ordered','active','paid','created')
    readonly_fields = ['total_profit_calculated_from_sales','price','profit'] 

    search_fields = ['code']
 


class CartItemssAdmin(admin.ModelAdmin):
    list_display = ('id','created')



admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Codes,CodeAdmin)


# admin.site.register(CartItems,CartItemssAdmin)
# admin.site.register(BromoCode, BromoCodeAdmin)
