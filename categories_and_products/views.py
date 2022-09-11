from django.shortcuts import redirect, render
from Register_Login.models import Profile
from cart_and_orders.emptying_cart import reset_all_users_cartItems_and_release_codes
from cart_and_orders.models import Cart, CartItems, Codes
from categories_and_products.forms import QuantityForm
from categories_and_products.models import Code_Categories, Game, Poster
from django.contrib import messages
from django.utils.translation import gettext as _

def index(request):

    reset_all_users_cartItems_and_release_codes(request)
    poster = Poster.objects.filter(active=True)
    code_categories = Code_Categories.objects.filter(active=True)
    games = Game.objects.filter(active=True,)
    steamGames = Game.objects.filter(active=True,gameName = "Steam Wallet Codes (TL)")

    context = {
        "code_categories": code_categories,
        'games': games,
        "steamGames" : steamGames,
        'poster' : poster
    }
    return render(request, 'index.html', context)


def games(request):
    reset_all_users_cartItems_and_release_codes(request)
    games = Game.objects.filter(active=True,)
    context = {
        'games': games
    }
    return render(request, 'games.html', context)


def store(request):
    reset_all_users_cartItems_and_release_codes(request)
    code_categories = Code_Categories.objects.filter(
        active=True).order_by('-codeCategory')
    codes = Codes.objects.filter(active = True, addToCart = False, ordered = False , user = None,codeCategory__active = True)
    print(codes)
    context = {
        # 'codes' : codes,
        'code_categories': code_categories,
    }
    return render(request, 'store.html', context)


def GamesCodes(request, Gameslug):
    reset_all_users_cartItems_and_release_codes(request)
    code_categories = Code_Categories.objects.filter(
        active=True, game__Gameslug=Gameslug)
    codes = Codes.objects.all()
    print(codes)

    context = {
        'codes' : codes,
        'code_categories': code_categories,
    }
    return render(request, "GamesCodes.html", context)


def searchedPage(request):
    reset_all_users_cartItems_and_release_codes(request)
    searched = request.GET.get('searched')
    print(type(searched))
    searching = Code_Categories.objects.all() if not str(searched) else Code_Categories.objects.filter(codeCategory__contains=searched)
    GamingSearch  = Game.objects.all() if not str(searched) else Game.objects.filter(gameName__contains = searched, active = True)
    print(searching)
    print(GamingSearch)
    context = {
        'searched' : searched,
        'searching' : searching,
        'GamingSearch' : GamingSearch,
     
    }
    return render(request, 'searchedPage.html', context)


def code_details(request, categoryslug):
    reset_all_users_cartItems_and_release_codes(request)
    quantityForm = QuantityForm(request.POST)
    Games = Game.objects.filter(active=True)

    # For Retrieving in HTML
    codeCategories = Code_Categories.objects.filter(
        categoryslug=categoryslug, active=True,)

    # For Getting Values
    codeCategory = Code_Categories.objects.get(
        categoryslug=categoryslug, active=True,)

    all_codes_in_category = Codes.objects.filter(codeCategory__categoryslug = categoryslug,addToCart = False).all().count()
    if request.method == "POST" and quantityForm.is_valid():
        if request.user.is_authenticated:

            Quantity = quantityForm.cleaned_data['Quantity']
            # order = Order.objects.filter(user=request.user, delivered=False, paid=False)


            cart = Cart.objects.get(user=request.user)

            totalOrderItemPrice = codeCategory.price * \
                quantityForm.cleaned_data['Quantity']

            if all_codes_in_category < Quantity:
                print("not Valid")
                messages.error(request, _(
                    '* You Ordered more than what in stock'), extra_tags='danger')

            # Printing till handeling messages
            # return redirect()

            else:
                # if the code category exist in the cart
                if CartItems.objects.filter(user=request.user, codeCategory__categoryslug=categoryslug, ordered=False).exists():
                    cartItem = CartItems.objects.get(
                        user=request.user, codeCategory__categoryslug=categoryslug, ordered=False)
                    new_added_codeCategory = quantityForm.cleaned_data['Quantity'] + cartItem.quantity

                    print("EXIST")

                    CartItems.objects.filter(user=request.user, codeCategory__categoryslug=categoryslug, ordered=False).update(
                        quantity=new_added_codeCategory,
                        totalOrderItemPrice=codeCategory.price * new_added_codeCategory,
                    )
                    cart.total_price += totalOrderItemPrice
                    cart.save()

                    # Adding the user to the codes he ordered
                    Code_Quantity_Control = Codes.objects.filter(active=True, codeCategory__categoryslug=categoryslug,addToCart = False).order_by('?').values('pk')[:Quantity]            
                    Codes.objects.filter(pk__in = Code_Quantity_Control).update(
                    user=request.user,addToCart = True)

                    messages.success(request, _('* Updated in Cart'),
                                     extra_tags='danger')
                    return redirect('cart_and_orders:cart')

                else:
                    # if the code category does not exist in the cart
                    CartItems.objects.create(
                        user=request.user,
                        cart=cart,
                        codeCategory=codeCategory,
                        ordered=False,
                        quantity=quantityForm.cleaned_data['Quantity'],
                        price=codeCategory.price,
                    )
                    cart.total_price += totalOrderItemPrice
                    cart.save()
                    Code_Quantity_Control = Codes.objects.filter(active=True, codeCategory__categoryslug=categoryslug,addToCart = False).order_by('?').values('pk')[:Quantity] 

                    Codes.objects.filter(pk__in = Code_Quantity_Control).update(
                    user=request.user,addToCart = True)

                    messages.success(request, _('* Added to cart'),
                                     extra_tags='danger')
                    return redirect('cart_and_orders:cart')
        else:
            messages.error(request, _('* Login First Please'),
                           extra_tags='danger')
            return redirect('Register_Login:login')


    context = {
        'categories': Games,
        'codeCategories': codeCategories,
        'form': quantityForm,
        'all_codes_in_category' : all_codes_in_category
    }
    print(all_codes_in_category)
    return render(request, "code_details.html", context)


def filtering_test(request):
    products = Codes.objects.filter(active=True, codeCategory="").values()
    print(products)
    return render(request, 'filter.html', {'products': products})
