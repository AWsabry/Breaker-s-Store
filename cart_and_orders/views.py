from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from cart_and_orders.emptying_cart import deleting_from_cart, reset_all_users_cartItems_and_release_codes
from cart_and_orders.models import Cart, CartItems, Codes, Order
from django.db.models import Sum
import requests
import hashlib

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Rest API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from categories_and_products.models import Code_Categories
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
    reset_all_users_cartItems_and_release_codes(request)
    if request.user.is_authenticated:
        user_codes = Codes.objects.filter(
            user=request.user, addToCart=True, ordered=True).order_by('-created')
        order = Order.objects.filter(
            user=request.user, paid=True).order_by('-ordered_date')

        context = {
            'codes': user_codes,
            'order': order,
        }
    else:
        messages.error(request, _('* Login First Please'))
        return redirect('Register_Login:login')

    return render(request, 'yourorders.html', context)


def order_confirm(request,):
    cart = Cart.objects.get(user=request.user)
    response = request.session.get('refrence')
    if CartItems.objects.filter(user=request.user, ordered=False, paid=False,status=None).exists():
        return redirect('cart_and_orders:cart')
    else:
        pass

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
        order_id=order_sent.id, ordered=True, active=False,  status='Success',)

# Updating the cartItem with the order id that's ordered
    CartItems.objects.filter(user=request.user, ordered=True, paid=False,).update(
        orderId=order_sent.id,
        paid=True,
        status='Success'
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


def email_template(request):
    return render(request, 'email_template.html')


def order_sent(request):
    reset_all_users_cartItems_and_release_codes(request)
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
        now = timezone.now()
        cartItemschecking = CartItems.objects.filter(
            user=request.user, ordered=False,).last()

        cartItems = CartItems.objects.filter(user=request.user, paid=False)
        cart = Cart.objects.filter(user=request.user)

        gettingcart = Cart.objects.get(user=request.user,)

        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.02 * gettingcart.total_price)

        if cartItemschecking != None:

            periodic_time = cartItemschecking.created + \
                timedelta(days=0, hours=0, minutes=0, seconds=30)

            pendingTime = cartItemschecking.created + \
                timedelta(days=0, hours=3, minutes=0, seconds=0)

            if cartItemschecking.status == "Pending":
                if now > pendingTime:
                    messages.error(request, _(
                        '* Your Pending limit has been expiered'), extra_tags='danger')
                    deleting_from_cart(request)

            elif cartItemschecking.status == "Success":
                pass

            else:
                if now > periodic_time:
                    messages.error(request, _(
                        '* Your Cart has been expired'), extra_tags='danger')
                    deleting_from_cart(request)

        else:
            pass
            print("Your Cart is Empty")

        if request.method == 'POST':
            if cartItems.exists():
                print("exist")
                pass
            else:
                messages.error(request, _('* Your Cart is Empty, Please add to cart first'),
                               extra_tags='danger')

        context = {
            'cartItems': cartItems,
            'cart': cart,
            'total_price_after_taxes': total_price_after_taxes
        }

    else:
        reset_all_users_cartItems_and_release_codes(request)
        messages.error(request, _('* Login First Please'),
                       extra_tags='danger')
        return redirect('Register_Login:login')

    return render(request, 'cart.html', context)


def PaymentChoice(request):
    reset_all_users_cartItems_and_release_codes(request)
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

        Codes.objects.filter(user=request.user, addToCart=True,
                             ordered=False, active=True).update(status='Pending',)

        # Updating the cartItem with the order id that's ordered
        CartItems.objects.filter(user=request.user, ordered=False).update(
            status='Pending',
        )

        # Getting Refrence ID to link between payment & dashboard & store it in the session
        refrence = str(datetime.now()) + str(request.user.username)
        request.session['refrence'] = refrence

# Calculating the Taxes and adding it
        gettingcart = Cart.objects.get(user=request.user,)
        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.021 * gettingcart.total_price)


# Sending Payment via API

        sending_payment_request = requests.post('https://api.opaycheckout.com/api/v1/international/cashier/create', headers={
            'MerchantId': '281822021682889',
            'Authorization': 'Bearer OPAYPUB16450080851810.3897884686987133',

        },
            json={
            "country": "EG",
            "reference": refrence,
            "amount": {
                "total": (total_price_after_taxes * 100),
                "currency": "EGP"
            },
            # Payment success page after payment
            "returnUrl": "https://breakers-store.com/order_confirm",
            "cancelUrl": "https://breakers-store.com/PaymentFailed",  # Payment Failed
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
            amount = sending_payment_request.json().get('data').get('amount').get('total')
            request.session['amount'] = amount
            payment_url = sending_payment_request.json().get('data').get('cashierUrl')
            CartItems.objects.filter(user=request.user, ordered=False).update(
                ordered=True,
            )
            return redirect(str(payment_url),)
    else:
        messages.error(request, _('* Login First Please'), extra_tags='danger')
    return render(request, 'CardsPayment.html')

def WalletPayment(request):
    if request.user.is_authenticated:

        Codes.objects.filter(user=request.user, addToCart=True,
                             ordered=False, active=True).update(status='Pending',)

        # Updating the cartItem with the order id that's ordered
        CartItems.objects.filter(user=request.user, ordered=False).update(
            status='Pending',
        )

        # Getting Refrence ID to link between payment & dashboard & store it in the session
        refrence = str(datetime.now()) + str(request.user.username)
        request.session['refrence'] = refrence

# Calculating the Taxes and adding it
        gettingcart = Cart.objects.get(user=request.user,)
        total_price_after_taxes = gettingcart.total_price + \
            2 + (0.021 * gettingcart.total_price)


# Sending Payment via API

        sending_payment_request = requests.post('https://api.opaycheckout.com/api/v1/international/cashier/create', headers={
            'MerchantId': '281822021682889',
            'Authorization': 'Bearer OPAYPUB16450080851810.3897884686987133',

        },
            json={
            "country": "EG",
            "reference": refrence,
            "amount": {
                "total": (total_price_after_taxes * 100),
                "currency": "EGP"
            },
            # Payment success page after payment
            "returnUrl": "https://breakers-store.com/order_confirm",
            "cancelUrl": "https://breakers-store.com/PaymentFailed",  # Payment Failed
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
            CartItems.objects.filter(user=request.user, ordered=False).update(
                ordered=True,
            )
            return redirect(str(payment_url),)
    else:
        messages.error(request, _('* Login First Please'), extra_tags='danger')
    return render(request, 'WalletPayment.html')



def PaymentFailed(request):
    reset_all_users_cartItems_and_release_codes(request)
    return render(request, 'PaymentFailed.html')


def deleting(request, id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cartItem = CartItems.objects.get(
            user=request.user, ordered=False, id=id)
        deleteing = CartItems.objects.filter(
            user=request.user, ordered=False, id=id).delete()
        if deleteing:
            new_total_after_deleting = cart.total_price - \
                (cartItem.price * cartItem.quantity)
            Codes.objects.filter(
                user=request.user, addToCart=True, ordered=False).update(user=None, addToCart=False)
            Cart.objects.filter(user=request.user).update(
                total_price=new_total_after_deleting)
        print(new_total_after_deleting)
        return redirect('cart_and_orders:cart')
    return render(request, 'deleting.html')



def fawrypay(request):
    cart = Cart.objects.get(user=request.user)
    
    order_sent = Order.objects.create(
        user=request.user,
        totalPrice=cart.total_price,
        cart=cart,
        paid=False,
        paid_by='Fawry'
    )
        
    # FawryPay Pay at Fawry API Endpoint
    URL = "https://www.atfawry.com/ECommerceWeb/Fawry/payments/charge" 

    # Payment Data
    merchantCode = "siYxylRjSPwEzB9tRVPb0A=="
    merchantRefNum = f"{order_sent.id}"
    merchant_cust_prof_id = f"{request.user.id}"
    payment_method = 'PAYATFAWRY'
    amount = f"{cart.total_price + 2 + (0.02 * cart.total_price):.2f}"
    merchant_sec_key = '0ed20552-0a87-4293-b6ce-80b6d4c44556'
    signature = hashlib.sha256((merchantCode + merchantRefNum + merchant_cust_prof_id + payment_method + amount + merchant_sec_key).encode()).hexdigest()

    # defining a params dict for the parameters to be sent to the API
    PaymentData = {
            "merchantCode": merchantCode,
            "merchantRefNum": merchantRefNum,
            "customerName": f"{request.user.first_name + request.user.last_name}",
            "customerMobile": f"{request.user.PhoneNumber}",
            "customerEmail": f"{request.user.email}",
            "customerProfileId": merchant_cust_prof_id,
            "amount": amount,
            "currencyCode": "EGP",
            "language": "en-gb",
            "chargeItems": [
                {
                    "itemId": "897fa8e81be26df25db592e81c31c",
                    "description": "Item Descriptoin",
                    "price": amount,
                    "quantity": "1"
                }
            ],
            "signature": signature,
            "paymentMethod": payment_method,
            "description": "Example Description"
        }

    headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
            }

    # sending post request and saving the response as response object
    status_request = requests.post(headers=headers, url=URL, json=PaymentData)

    # extracting data in json format
    status_response = status_request.json()
    
    print(status_response)
    
    CartItems.objects.filter(user=request.user, ordered=False).update(
                ordered=True,
            )
    order_sent.order_response = status_response["referenceNumber"]
    order_sent.save()
    
# Updating Code Data
    Codes.objects.filter(user=request.user, addToCart=True, ordered=False, active=True).update(
        order_id=order_sent.id, ordered=True, active=False,  status='Pending',)

# # Updating the cartItem with the order id that's ordered
    CartItems.objects.filter(user=request.user, ordered=True, paid=False,).update(
        orderId=order_sent.id,
        status='Pending'
    )

#     # Updating the profit sum
#     total_Profit_from_sales = Codes.objects.filter(
#         ordered=True).aggregate(Sum('profit')).get('profit__sum')

#     Codes.objects.filter(ordered=True, active=False,).update(
#         total_profit_calculated_from_sales=total_Profit_from_sales,)

#     print(total_Profit_from_sales)

#     # Updating the total price in the cart
#     Cart.objects.filter(user=request.user).update(total_price=0)

    order_codes = Codes.objects.filter(
        user=request.user, order_id=order_sent.id, ordered=True,)

#     # Sending Email
#     if order_sent:
#         send_code_email(request, order_codes)
#         Codes.objects.filter(
#             user=request.user, order_id=order_sent.id, ordered=True,).update(paid=True)
#         print('Email Sent')


    messages.success(request, _('Your order has been placed successfully. Pay with fawary to have your code.'))

    return redirect("cart_and_orders:cart")




@method_decorator(decorator=csrf_exempt, name="dispatch")
class WebhookFawary(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print(request)
        print(request.data)
        return Response({}, status=status.HTTP_200_OK,)