from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from Register_Login.views import Register, activate_user, email_activated, logOut, signIn,email_sent,profile,password_reset_emailing


app_name = 'Register_Login'

urlpatterns = [
    path('register', view = Register, name='Register'),
    path('login', view = signIn, name='login'),
    path('logOut',view = logOut, name='logOut'),
    path('email_sent', view = email_sent, name='email_sent'),
    path(route='activate/<token>', view=activate_user, name='activate'),
    path('profile', view = profile, name='profile'),
    path('email_activated', view = email_activated, name='email_activated'),



    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),



    path('password_reset/done/', view = password_reset_emailing ,name='password_reset_emailing'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),


    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

