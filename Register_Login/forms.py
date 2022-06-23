from django import forms
from Register_Login.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class RegisterForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2','city')
        error_messages = {
            'email': {
                'unique': _("This entry has been registered before."),
            },
        }

class LoginForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class CompleteProfile(forms.ModelForm):
    class Meta:
        pass




