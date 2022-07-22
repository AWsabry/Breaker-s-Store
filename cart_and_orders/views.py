from pydoc import render_doc
from django.http import HttpResponse
from django.shortcuts import redirect, render
from sqlalchemy import false
from Register_Login.forms import RegisterForm
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from Breakers_Store import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from cart_and_orders.models import Cart, CartItems, Codes, Order

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

    # subject = _('Breaker\'s store codes')
    # body = render_to_string('order_sent.html', {
    #         'user': request.user,
    #     })
    # email = EmailMessage(
    #         subject, body, settings.EMAIL_HOST_USER, [request.user.email])
    # print(email)
    # email.send()


def yourorders(request):

    user_codes = Codes.objects.filter(
        user=request.user, addToCart=True, ordered=True)

    context = {
        'codes': user_codes,
    }

    return render(request, 'yourorders.html', context)


def order_confirmation(request):
    return render(request, "order_confirmation.html")


def ThankYou(request):
    return render(request, 'thankyou.html')


def email_template(request):
    return render(request, 'email_template.html')


def order_sent(request):
    order_codes = Codes.objects.filter(
        user=request.user, addToCart=True, ordered=False)
    print(order_codes)
    return render(request, 'order_sent.html', {'order_codes': order_codes})


def cart(request):
    if request.user.is_authenticated:
        cartItems = CartItems.objects.filter(user=request.user, ordered=False)
        cart = Cart.objects.filter(user=request.user)

        context = {
            'cartItems': cartItems,
            'cart': cart,
        }

        if request.method == 'POST':
            if cartItems.exists():
                order = Order.objects.filter(
                    user=request.user, delivered=False, paid=False).values()
                cart = Cart.objects.get(user=request.user)
                order_codes = Codes.objects.filter(
                    user=request.user, addToCart=True, ordered=False,active = True)

                for getting_Id in order:
                    order_id = getting_Id['id']
                order_id
                print(order_id)

                order_sent = Order.objects.create(
                    user=request.user,
                    totalPrice=30,
                    cart=cart,
                )
                if order_sent:
                    send_code_email(request, order_codes)
                print('Email Sent')

            # Updates
                if order_id == None:
                    Codes.objects.filter(user=request.user, addToCart=True, ordered=False,active = True).update(
                        order_id=1, ordered=True,active = False)
                else:
                    Codes.objects.filter(user=request.user, addToCart=True, ordered=False,active = True).update(
                        order_id=order_id, ordered=True,active = False)

            # Updating the cartItem with the order id that's ordered
                CartItems.objects.filter(user=request.user, ordered=False).update(
                    ordered=True,
                    orderId=order_id,
                )
             # Updating the total price in the cart
                Cart.objects.filter(user=request.user).update(total_price=0)
                return redirect('cart_and_orders:order_confirmation')
            else:
                messages.error(request, _('* Your Cart is Empty, Please add to cart first'),
                           extra_tags='danger')

    else:
        messages.error(request, _('* Login First Please'),
                       extra_tags='danger')
        return redirect('Register_Login:login')

    return render(request, 'cart.html', context)
