from django.shortcuts import redirect, render
from sqlalchemy import false
from Register_Login.forms import RegisterForm
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm

from cart_and_orders.models import Cart, CartItems, Order

# Create your views here.


def checkout(request):
    discountform = BromoCodeForm(request.POST)
    userProfile = Profile.objects.filter(id=request.user.id).first()
    # products = Product.objects.filter(active=True,).values()
    # bromocode = BromoCode.objects.filter(active=True)
    # categories = Category.objects.filter(active=True)
    userLoggedIN = Profile.objects.filter(id=request.user.id).first()

    cartItem = CartItems.objects.filter(user=request.user, ordered=False).values()

    cartItems = CartItems.objects.filter(user=request.user, ordered=False)

    cart = Cart.objects.filter(user=request.user).values()

    # OrderItem_id
    for getting_Id in cartItem:
        cartItem_id = getting_Id['id']

    # Sum of order
    totalOrderPricelist = []
    for totalPriceCheck in cartItem:
        totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    total = sum(totalOrderPricelist)



    # for totalPriceCheck in cartItem:
    #     totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    # total = sum(totalOrderPricelist)

    context = {
        # "products": products,
        # "categories": categories,
        'userLoggedIN': userLoggedIN,
        'cartItem': cartItem,
        'form': discountform,
        'cart': cart,
        'total': total,
        'userProfile': userProfile,
        'cartItems': cartItems
    }
    print(total)
    cart = Cart.objects.get(user=request.user)

    if request.method == 'POST':
        if discountform.is_valid():
            # print(float(BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage')))

            Order.objects.create(
                user=request.user,
                totalPrice= total,
                BromoCode=discountform.cleaned_data['code'],
                cart=cart,
                # offerPercentage = BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage'),
                # total_after_offer = BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage') * Cart.objects.filter(user=request.user).values('total_price')
            )
            # print(float(BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage').first())*2)

        order = Order.objects.filter(
            user=request.user, delivered=False, paid=False).values()

        for getting_Id in order:
            order_id = getting_Id['id']
        order_id
        print(order_id)
        

        CartItems.objects.filter(user=request.user, id=cartItem_id).update(
            ordered=True,
            orderId=order_id,
        )
        Cart.objects.filter(user=request.user).update(total_price=0)


        return redirect('/thankyou')
    return render(request, 'checkout.html', context)


def ThankYou(request):
    return render(request, 'thankyou.html')
