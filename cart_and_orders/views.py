from django.shortcuts import redirect, render
from sqlalchemy import false
from Register_Login.forms import RegisterForm
from Register_Login.models import Profile
from cart_and_orders.forms import BromoCodeForm

from cart_and_orders.models import Cart, CartItems, Codes, Order

# Create your views here.


def checkout(request):
    # discountform = BromoCodeForm(request.POST)
    # userProfile = Profile.objects.filter(id=request.user.id).first()
    # userLoggedIN = Profile.objects.filter(id=request.user.id).first()

    # cartItemm = CartItems.objects.get(
    #     user=request.user, ordered=False)

    # cartItems = CartItems.objects.filter(user=request.user, ordered=False)

    # cart = Cart.objects.filter(user=request.user).values()

    # # OrderItem_id

    # # Sum of order
    # # totalOrderPricelist = []
    # # for totalPriceCheck in cartItem:
    # #     totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    # # total = sum(totalOrderPricelist)



    # context = {
    #     # "products": products,
    #     # "categories": categories,
    #     'userLoggedIN': userLoggedIN,
    #     'form': discountform,
    #     'cart': cart,
    #     'total': total,
    #     'userProfile': userProfile,
    #     'cartItems': cartItems
    # }
    # # print(total)
    # cart = Cart.objects.get(user=request.user)

    # if request.method == 'POST':

    #     Order.objects.create(
    #         user=request.user,
    #         totalPrice=total,
    #         BromoCode=discountform.cleaned_data['code'],
    #         cart=cart,
    #         # offerPercentage = BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage'),
    #         # total_after_offer = BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage') * Cart.objects.filter(user=request.user).values('total_price')
    #     )
    #     # print(float(BromoCode.objects.filter(active=True,code = discountform.cleaned_data['code']).values('percentage').first())*2)

    #     # order = Order.objects.filter(
    #         # user=request.user, delivered=False, paid=False).values()
        
    #     order = Order.objects.get( ser=request.user, delivered=False, paid=False)

    #     CartItems.objects.filter(user=request.user, id=cartItemm.id).update(
    #         ordered=True,
    #         orderId=order.id,
    #     )
    #     Cart.objects.filter(user=request.user).update(total_price=0)

    #     return redirect('/thankyou')
    return render(request, 'checkout.html')


def ThankYou(request):
    return render(request, 'thankyou.html')


def cart(request):
    cartItems = CartItems.objects.filter(user=request.user, ordered=False)
    cart = Cart.objects.filter(user=request.user).values()
    

    context = {
        'cartItems': cartItems,
        'cart': cart,
    }
    if request.method == 'POST':
        cartItem = CartItems.objects.get(
        user=request.user, ordered=False)

        order = Order.objects.filter(
                user=request.user, delivered=False, paid=False).values()
        
        print(order)


        # order = Order.objects.filter(
        #         user=request.user, delivered=False, paid=False)
        cart = Cart.objects.get(user=request.user)

        print(order)

        Order.objects.create(
            user=request.user,
            totalPrice=30,
            cart=cart,
        )

        for getting_Id in order:
            order_id = getting_Id['id']
        order_id
        print(order_id)

        Codes.objects.filter(user = request.user, addToCart = True, ordered = False).update(order_id=order_id,ordered = True)


            

      
        

        CartItems.objects.filter(user=request.user, id=cartItem.id).update(
            ordered=True,
            orderId=order_id,
        )
        Cart.objects.filter(user=request.user).update(total_price=0)
        redirect('/')


    return render(request, 'cart.html', context)
