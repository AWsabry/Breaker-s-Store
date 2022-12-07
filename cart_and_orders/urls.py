from django.urls import path
from . import views

app_name = 'cart_and_orders'


urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('yourorders', views.yourorders, name='yourorders'),

    path('order_sent', views.order_sent, name='order_sent'),
    path('email_template', views.email_template, name='email_template'),
    path('order_confirm', view = views.order_confirm, name='order_confirm'),

    # Payments
    path('PaymentChoice', views.PaymentChoice, name='PaymentChoice'),
    path('CardsPayment', views.CardsPayment, name='CardsPayment'),
    path('WalletPayment', views.WalletPayment, name='WalletPayment'),
    path('RefrenceCode', views.RefrenceCode, name='RefrenceCode'),
    path('callbackurl', views.callbackurl,name = 'callbackurl'),
    path('fawrypay', views.fawrypay, name='fawrypay'),
    path('datajson', views.datajson, name='datajson'),

    path('webhook/fawary/', views.WebhookFawary.as_view(), name='webhook'),
    path('PaymentFailed', views.PaymentFailed, name='PaymentFailed'),
    
    path('<int:id>', views.deleting, name='deleting'),
    
]
