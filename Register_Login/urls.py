from django.urls import path,re_path
from django.contrib.auth import views
from Register_Login.views import Register, activate_user, email_activated, logOut, signIn,email_sent,profile


app_name = 'Register_Login'

urlpatterns = [
    path('register', view = Register, name='Register'),
    path('login', view = signIn, name='login'),
    path('logOut',view = logOut, name='logOut'),
    path('email_sent', view = email_sent, name='email_sent'),
    path(route='activate/<token>', view=activate_user, name='activate'),
    path('profile', view = profile, name='profile'),
    path('email_activated', view = email_activated, name='email_activated'),
]
