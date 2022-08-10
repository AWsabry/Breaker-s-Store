from operator import mod
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from categories_and_products.models import Code_Categories
from django.db.models import Sum

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,unique=True)
    total_price = models.FloatField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    comment = models.TextField(max_length=2000, blank=True, null=True)
    totalPrice = models.PositiveIntegerField(default=0)
    total_price_after_taxes =  models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

@receiver(pre_save, sender=Order)
def calculatedFromSales(sender, **kwargs):
    orders = kwargs['instance']
    total_price_after_taxes = orders.totalPrice + 2 + (0.02 * orders.totalPrice)
    orders.total_price_after_taxes = total_price_after_taxes



class Codes(models.Model):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,blank=True,null= True)
    code = models.CharField(max_length=1000, blank=True,unique=True)
    codeCategory = models.ForeignKey(Code_Categories, on_delete=models.CASCADE,)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order,on_delete= models.SET_NULL, blank= True, null=True)
    paid = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    addToCart = models.BooleanField(default=False)
    profit = models.FloatField(default=0, verbose_name= 'Profit From This Code' )
    total_profit_calculated_from_sales = models.FloatField(default=0, verbose_name= 'Profit From Orders' )
    price = models.FloatField(default=0, verbose_name= 'Price Of This Code' )

    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural = "Codes"

@receiver(pre_save, sender=Codes)
def calculatedFromSales(sender, **kwargs):
    codes = kwargs['instance']
    codes.price = float(codes.codeCategory.price)
    codes.profit = float(codes.codeCategory.price) - float(codes.codeCategory.price_bought_by)

    

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    orderId = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    codeCategory = models.ForeignKey(Code_Categories, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1, name='quantity')
    created = models.DateTimeField(auto_now_add=True)
    totalOrderItemPrice = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user.email) + " " + str(self.codeCategory.codeCategory)

    class Meta:
        verbose_name_plural = "CartItems"


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_codeCategory = Code_Categories.objects.get(id=cart_items.codeCategory.id)
    cart_items.totalOrderItemPrice = cart_items.quantity * float(price_of_codeCategory.price)
    total_cart_items = CartItems.objects.filter(user=cart_items.user)

