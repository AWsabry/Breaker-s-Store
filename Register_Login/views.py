# Importing Django Libraries required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

# Importing the utilts file
from Register_Login.utils import AccessTokenGenerator

# Importing setting from the main project
from Breakers_Store import settings


# Importing Models
from Register_Login.models import AccessToken, Profile
# from cart_and_orders.models import Cart

# Importing Forms
from Register_Login.forms import CompleteProfile, LoginForm, RegisterForm


# Email Confirm SignUp
def send_tracking(user):
    print(user)
    user = Profile.objects.filter(id=user.id).first()
    last_token = user.token.filter(
        user=user, expires__gt=timezone.now()).first()
    if not last_token:
        access_token = user.token.create(user=user)
        return (access_token.token, 0)
    return (False, (last_token.expires - timezone.now()).total_seconds())

# Checking the token availablity & creating the cart


def token_check(user):
    token, time_tosend = send_tracking(user=user)
    if token:
        # Cart.objects.create(
        #             user=user,
        #         )
        return (token, time_tosend)
    return (None, time_tosend)


def send_activate_mail(request, user):
    token, time_tosend = token_check(user)
    if token:
        print(token)
        domain = get_current_site(request)
        subject = _('Activate user account')
        body = render_to_string('activate.html', {
            'user': user,
            'domain': domain,
            'token': token,
        })
        email = EmailMessage(
            subject, body, settings.EMAIL_HOST_USER, [user.email])
        print(email)
        email.send()

        messages.success(request, _('There are an mail has been sent.'))
    else:
        messages.error(request, _('Please varify the account (an email have been sent) please wait %(time_tosend)8.0f') % {
                       'time_tosend': time_tosend}, extra_tags='danger')


# This function is to create a new user profile & be saved in the models
@csrf_exempt
def Register(request):
    if request.user.is_authenticated:
        return redirect('categories_and_products:index')
    else:
        if request.method == 'POST':
            print("Method is Post")
            form = RegisterForm(request.POST)
            email = form.data.get('email')
            first_name, last_name, username = form.data.get(
                'first_name'), form.data.get('last_name'), form.data.get('username')
            password = form.data.get('password1')
            city = form.data.get('city')
            Age, PhoneNumber = form.data.get(
                'Age'), form.data.get('PhoneNumber'),

            print(form.errors)
           
            user = Profile.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    username=username,
                    city=city,
                    Age=Age,
                    PhoneNumber=PhoneNumber,
            )
            print('user is created')
            # send_activate_mail(request, user)
            print(user)           
            return redirect('Register_Login:email_sent')
       
        else:
            print("Error")
            form = RegisterForm()
        return render(request, "Register.html",  {
        })


# Confirming sending email to user
def email_sent(request):
    return render(request, "email_sent.html")

# Logout Page


def activate_user(request, token):
    token = AccessToken.objects.filter(token=token).first()
    
    if token:
        last_token = AccessToken.objects.filter(user=token.user, expires__gt=timezone.now()).first()
        
        if last_token == token:
            
            if AccessTokenGenerator().check_token(token.user, token.token):       
                token.user.is_active = True
                token.user.save()
                return HttpResponse('activated')
            return HttpResponse('already activated')
        return HttpResponse('timeout')

    return  HttpResponse('None found token')
    

def logOut(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'LogOut.html',)

# Login View


def signIn(request):
    form = LoginForm(request.POST, request.FILES)
    if request.user.is_authenticated:
        return redirect('categories_and_products:index')
    else:
        if request.method == 'POST':
            if form.is_valid():
                print("Post")
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(request, email=email, password=password)
                user_login(request, user)
                messages.success(request, "You Have been logged successfully!")
                return HttpResponseRedirect('/')
        return render(request, 'signIn.html', {'form': form})


def completeProfile(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        city = form.data.get('city')
        Age, phone_number, ProfilePic = form.data.get(
            'age'), form.data.get('phone_number'), form.data.get('ProfilePic')

        Profile.objects.filter(user=request.user).update(
            city=city,
            Age=Age,
            ProfilePic=ProfilePic,
            PhoneNumber=phone_number,
        )
        return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'completeProfile.html')


