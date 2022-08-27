from datetime import datetime, timedelta
from django.utils import timezone
from http.client import HTTPResponse
from http.server import HTTPServer
from xmlrpc.client import DateTime
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from cart_and_orders.models import Cart, CartItems, Codes, Order
from django.db.models import Sum
import requests
# Create your views here.


def send_code_email(request, order_codes):
    subject, from_email, to = 'Sending Code Orders', 'noreply1@quranfordeaf.com',  request.user.email
    text_content = 'This is an important message.'
    print(order_codes)
    context = {
        'order_codes': order_codes,
        'user': request.user
    }
    html_content = render_to_string('order_sent.html', context)
    print("CODESS", order_codes)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.success(request, _('Check YOUR ORDERS section or you Email'))


def yourorders(request):
    if request.user.is_authenticated:
        user_codes = Codes.objects.filter(
            user=request.user, addToCart=True, ordered=True).order_by('-created')

        context = {
            'codes': user_codes,
        }
    else:
        messages.error(request, _('* Login First Please'))
        return redirect('Register_Login:login')

    return render(request, 'yourorders.html', context)


def order_confirmation(request):
    cart = Cart.objects.get(user=request.user)
    response = request.session.get('refrence')

    # Creating Order ID
    order_sent = Order.objects.create(
        user=request.user,
        totalPrice=cart.total_price,
        cart=cart,
        paid=True,
        order_response=response,
        paid_by='Opay'

    )
    print(response)
# Updating Code Data
    Codes.objects.filter(user=request.user, addToCart=True, ordered=False, active=True).update(
        order_id=order_sent.id, ordered=True, active=False,)

# Updating the cartItem with the order id that's ordered
    CartItems.objects.filter(user=request.user, ordered=False).update(
        ordered=True,
        orderId=order_sent.id,
        paid=True,
    )

    # Updating the profit sum
    total_Profit_from_sales = Codes.objects.filter(
        ordered=True).aggregate(Sum('profit')).get('profit__sum')

    Codes.objects.filter(ordered=True, active=False,).update(
        total_profit_calculated_from_sales=total_Profit_from_sales,)

    print(total_Profit_from_sales)

    # Updating the total price in the cart
    Cart.objects.filter(user=request.user).update(total_price=0)

    order_codes = Codes.objects.filter(
        user=request.user, order_id=order_sent.id, ordered=True,)

    # Sending Email
    if order_sent:
        send_code_email(request, order_codes)
        Codes.objects.filter(
            user=request.user, order_id=order_sent.id, ordered=True,).update(paid=True)
        print('Email Sent')

    return render(request, "order_confirmation.html")


def ThankYou(request):
    return render(request, 'thankyou.html')


def email_template(request):
    return render(request, 'email_template.html')


def payment(request):
    return render(request, 'payment.html')


def order_sent(request):
    if request.user.is_authenticated:
        order_codes = Codes.objects.filter(
            user=request.user, addToCart=True, ordered=False)
        print(order_codes)
    else:
        messages.error(request, _('* Login First Please'))
        return redirect('Register_Login:login')
    return render(request, 'order_sent.html', {'order_codes': order_codes})


def cart(request):
    if request.user.is_authenticated:
        cartItems = CartItems.objects.filter(user=request.user, ordered=False)

        cart = Cart.objects.filter(user=request.user)
        gettingcart = Cart.objects.get(user=request.user,)
        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.02 * gettingcart.total_price)

        print(total_price_after_taxes)

        print(gettingcart.total_price)

        if request.method == 'POST':
            if cartItems.exists():
                print("exist")
            else:
                messages.error(request, _('* Your Cart is Empty, Please add to cart first'),
                               extra_tags='danger')

        context = {
            'cartItems': cartItems,
            'cart': cart,
            'total_price_after_taxes': total_price_after_taxes
        }
    else:
        messages.error(request, _('* Login First Please'),
                       extra_tags='danger')
        return redirect('Register_Login:login')

    return render(request, 'cart.html', context)


def PaymentChoice(request):
    cartItems = CartItems.objects.filter(user=request.user, ordered=False)
    if cartItems.exists():
        pass
    else:
        messages.error(request, _('* Your Cart is Empty, Please add to cart first'),
                       extra_tags='danger')
        return redirect('cart_and_orders:cart')

    return render(request, 'PaymentChoice.html')


def CardsPayment(request):
    if request.user.is_authenticated:

        # Getting Refrence ID to link between payment & dashboard & store it in the session
        refrence = str(datetime.now()) + str(request.user.username)
        request.session['refrence'] = refrence

# Calculating the Taxes and adding it
        gettingcart = Cart.objects.get(user=request.user,)
        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.02 * gettingcart.total_price)


# Sending Payment via API

        sending_payment_request = requests.post('https://sandboxapi.opaycheckout.com/api/v1/international/cashier/create', headers={
            'MerchantId': '281822021543671',
            'Authorization': 'Bearer OPAYPUB16449210671400.9789067134362516',
        },
            json={
            "country": "EG",
            "reference": refrence,
            "amount": {
                "total": (total_price_after_taxes * 100),
                "currency": "EGP"
            },
            # Payment success page after payment
            "returnUrl": "http://127.0.0.1:8000/order_confirmation",
            "cancelUrl": "http://127.0.0.1:8000/PaymentFailed",  # Payment Failed
            "callbackUrl": "https://your-call-back-url",
            "expireAt": 300,
            "userInfo": {
                "userEmail": str(request.user),
                "userId": str(request.user.id),
                "userMobile": str(request.user.PhoneNumber),
                "userName": str(request.user.username),
            },
            "productList": [
                {
                    "productId": "productId",
                    "name": "name",
                    "description": "description",
                    "price": 100,
                    "quantity": 2,
                }
            ],
            "payMethod": "BankCard"
        })

        print("URL", sending_payment_request.json())

# Checking the success code to continue the operation
        if sending_payment_request.json().get('code') != '00000':
            return redirect('cart_and_orders:PaymentFailed')
        else:
            payment_url = sending_payment_request.json().get('data').get('cashierUrl')
            return redirect(str(payment_url),)
    else:
        messages.error(request, _('* Login First Please'), extra_tags='danger')
    return render(request, 'CardsPayment.html')




def WalletPayment(request):
    if request.user.is_authenticated:

        # Getting Refrence ID to link between payment & dashboard & store it in the session
        refrence = str(datetime.now()) + str(request.user.username)
        request.session['refrence'] = refrence

# Calculating the Taxes and adding it
        gettingcart = Cart.objects.get(user=request.user,)
        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.021 * gettingcart.total_price)


# Sending Payment via API

        sending_payment_request = requests.post('https://sandboxapi.opaycheckout.com/api/v1/international/cashier/create', headers={
            'MerchantId': '281822021543671',
            'Authorization': 'Bearer OPAYPUB16449210671400.9789067134362516',
        },
            json={
            "country": "EG",
            "reference": refrence,
            "amount": {
                "total": (total_price_after_taxes * 100),
                "currency": "EGP"
            },
            # Payment success page after payment
            "returnUrl": "http://127.0.0.1:8000/order_confirmation",
            "cancelUrl": "http://127.0.0.1:8000/PaymentFailed",  # Payment Failed
            "callbackUrl": "https://your-call-back-url",
            "expireAt": 300,
            "userInfo": {
                "userEmail": str(request.user),
                "userId": str(request.user.id),
                "userMobile": str(request.user.PhoneNumber),
                "userName": str(request.user.username),
            },
            "productList": [
                {
                    "productId": "productId",
                    "name": "name",
                    "description": "description",
                    "price": 100,
                    "quantity": 2,
                }
            ],
            "payMethod": "MWALLET"
        })

        print("URL", sending_payment_request.json())

# Checking the success code to continue the operation
        if sending_payment_request.json().get('code') != '00000':
            return redirect('cart_and_orders:PaymentFailed')
        else:
            payment_url = sending_payment_request.json().get('data').get('cashierUrl')
            return redirect(str(payment_url),)
    else:
        messages.error(request, _('* Login First Please'), extra_tags='danger')
    return render(request, 'WalletPayment.html')


def PaymentFailed(request):
    return render(request, 'PaymentFailed.html')


def testing(request):
    cartItems = CartItems.objects.get(user=request.user, ordered=False, id=id)
    now = timezone.now()

    periodic_time = cartItems.created + timedelta(days=0, hours=1)
    print(type(now))
    print(type(periodic_time))

    if now > periodic_time:
        print("An hour has been Passed")
    else:
        print("hour is not Passed yet")
    return render(request, 'testing.html')


def EasyKashPayment(request):
    return render(request, 'EasyKashPayment.html')


def deleting(request, id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cartItem = CartItems.objects.get(user=request.user, ordered=False,id=id)
        deleteing = CartItems.objects.filter(user=request.user, ordered=False,id=id).delete()
        if deleteing:
            new_total_after_deleting = cart.total_price - (cartItem.price * cartItem.quantity)
            Codes.objects.filter(
                user=request.user, addToCart=True, ordered=False).update(user = None, addToCart = False)
            Cart.objects.filter(user=request.user).update(total_price = new_total_after_deleting)
        print(new_total_after_deleting)
        return redirect('cart_and_orders:cart')
    return render(request, 'deleting.html')
