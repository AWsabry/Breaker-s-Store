from django.shortcuts import redirect
from datetime import timedelta
from django.utils import timezone
from pyclbr import Class
from cart_and_orders.models import Cart, CartItems, Codes
from django.contrib import messages
import datetime
from django.utils.translation import gettext as _

from django.db.models import Exists, OuterRef


def deleting_from_cart(request):
    deleteing = CartItems.objects.filter(
        user=request.user, ordered=False,).delete()

    if deleteing:
        Codes.objects.filter(
            user=request.user, addToCart=True, ordered=False).update(user=None, addToCart=False, status='', active=True)
        Cart.objects.filter(
            user=request.user).update(total_price=0)
        print("DELETED FROM CART")
    return deleteing


def reset_all_users_cartItems_and_release_codes(request):
    now = timezone.now()
    cartItemschecking = CartItems.objects.filter(ordered=False).values()
    if cartItemschecking.exists():
        for pointer in cartItemschecking:
            time = pointer['created']
            status = pointer['status']
        time
        print(time)

        periodic_time = time + \
            timedelta(days=0, hours=0, minutes=0, seconds=30)

        pendingTime = time + \
                timedelta(days=0, hours=3, minutes=0, seconds=0)

        if status == "Pending":
            if now > pendingTime:
                deleting = CartItems.objects.filter(ordered=False,).all().delete()
                if deleting:
                    Codes.objects.filter(addToCart=True, ordered=False).update(
                        user=None, addToCart=False, status='', active=True)
                print("DELETED FROM CART DUE TO Pending Time")
            if request.user.is_authenticated:
                Cart.objects.filter(
                    user=request.user).update(total_price=0)
   
        elif status == "Success":
                pass
        else:
            if now > periodic_time:
                deleting = CartItems.objects.filter(ordered=False,).all().delete()
                if deleting:
                    Codes.objects.filter(addToCart=True, ordered=False).update(
                        user=None, addToCart=False, status='', active=True)
                print("DELETED FROM CART DUE TO Periodic Time")
            if request.user.is_authenticated:
                print('ehes')
                Cart.objects.filter(
                    user=request.user).update(total_price=0)

    elif request.user.is_authenticated and cartItemschecking.exists() == False:
        Cart.objects.filter(
            user=request.user).update(total_price=0)
        print("Cart is Zero")
    else:
        pass