from django.shortcuts import redirect, render
from Register_Login.models import Profile
from categories_and_products.forms import QuantityForm
from categories_and_products.models import Code_Categories, Game, Codes
from django.core.paginator import Paginator

import datetime


def index(request):
    # x = Codes.objects.filter(active=True,).first()

    y = 2
    code_categories = Code_Categories.objects.filter(active=True)
    games = Game.objects.filter(active=True,)
    
    
    # x = Codes.objects.filter(active = True, category__categoryslug = 'pubg-code-200').order_by('?')[:y]

    context = {
            "code_categories": code_categories,
            'games': games,
        }
    print(x)
    return render(request, 'index.html', context)


def games(request):
    games = Game.objects.filter(active=True,)
    context = {
        'games': games
    }
    return render(request, 'games.html', context)



def store(request):
    code_categories = Code_Categories.objects.filter(active=True).order_by('-codeCategory')
    context = {
        'code_categories': code_categories
    }
    return render(request, 'store.html',context)



def GamesCodes(request, Gameslug):
    code_categories = Code_Categories.objects.filter(active=True,game__Gameslug=Gameslug)

    context = {

        'code_categories': code_categories,
    }
    return render(request, "GamesCodes.html", context)



def code_details(request, id):
    quantityForm = QuantityForm(request.POST)
    categories = Game.objects.filter(active=True,)
    codeCategories = Code_Categories.objects.filter(
        id=id, active=True,)

    # date = datetime.datetime.now().hour
    # cart = Cart.objects.get(user=request.user)
    # order = Order.objects.filter(user=request.user,)

    # cartItem = CartItems.objects.filter(user=request.user).values()

    # # orderData = Order.objects.filter(user=request.user).values()

    # product_data = Product.objects.get(slug=slug)

    # totalOrderPricelist = []
    # for totalPriceCheck in cartItem:
    #     totalOrderPricelist.append(totalPriceCheck['totalOrderItemPrice'])
    # total = sum(totalOrderPricelist)


    # # place = Order.objects.get(name='kansas')


    # print(total)
    # print(totalOrderPricelist)

  
    

    context = {

        'categories': categories,
        'codeCategories': codeCategories
    }
    # print(request.user)

    # if request.method == 'POST':
    #     if quantityForm.is_valid():
            
    #         totalOrderItemPrice = product_data.price * \
    #             quantityForm.cleaned_data['Quantity']

    #         print('Done')
    #         CartItems.objects.create(
    #             user=request.user,
    #             cart=cart,
    #             product=product_data,
    #             ordered=False,
    #             quantity=quantityForm.cleaned_data['Quantity'],
    #             totalOrderItemPrice=totalOrderItemPrice
    #         )
    #         print("Total Before added", totalOrderItemPrice)

    #         cart.total_price += totalOrderItemPrice
    #         cart.save()

    #         print("Cart_Total",cart.total_price)

    #         print(cart)

            # return redirect('cart_and_orders:checkout')
        
    return render(request, "code_details.html", context)


def filtering_test(request):
    products = Codes.objects.filter(active=True,category ="").values()
    print(products)
    return render(request, 'filter.html', {'products': products})
