from operator import mod
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    BromoCode = models.CharField(max_length=10, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    comment = models.TextField(max_length=2000, blank=True, null=True)
    totalPrice = models.PositiveIntegerField(default=0)
    offerPercentage = models.PositiveIntegerField(default=0, null= True, blank=True)
    deliveryFees = models.PositiveIntegerField(default=0)
    total_after_offer = models.PositiveIntegerField(default=0)



    # delivery_fees = models.ForeignKey(Delivery, on_delete=models.CASCADE)

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


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    orderId = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1, name='quantity')
    created = models.DateTimeField(auto_now_add=True)
    totalOrderItemPrice = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user.email) + " " + str(self.product.name)

    class Meta:
        verbose_name_plural = "CartItems"


@receiver(pre_save, sender=CartItems)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    # price_of_product = Product.objects.get(id=cart_items.product.id)
    # cart_items.price = cart_items.quantity * float(price_of_product.price)
    total_cart_items = CartItems.objects.filter(user=cart_items.user)

