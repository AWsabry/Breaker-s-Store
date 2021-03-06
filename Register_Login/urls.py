from django.urls import path
from django.contrib.auth import views
from Register_Login.views import Register, activate_user, completeProfile, logOut, signIn,email_sent


app_name = 'Register_Login'

urlpatterns = [
    path('register', view = Register, name='Register'),
    path('login', view = signIn, name='login'),
    path('completeProfile', view = completeProfile, name='completeProfile'),
    path('logOut',view = logOut, name='logOut'),
    path('email_sent', view = email_sent, name='email_sent'),

    
    path(route='activate/<token>', view=activate_user, name='activate'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
