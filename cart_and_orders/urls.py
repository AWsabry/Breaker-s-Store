from django.urls import path

from Register_Login.views import email_sent

from . import views

app_name = 'cart_and_orders'


urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('yourorders', views.yourorders, name='yourorders'),
    path('thankyou', views.ThankYou, name='thankyou'),
    path('order_sent', views.order_sent, name='order_sent'),
    path('email_template', views.email_template, name='email_template'),
    path('order_confirmation', view = views.order_confirmation, name='order_confirmation'),

    
]
