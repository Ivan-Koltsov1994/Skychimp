from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from main.forms import FormStyleMixin
from users.models import User


class UserChangeForm(FormStyleMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone')

    # Cкрываем пароль  при заполнении
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class UserRegisterForm(FormStyleMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2','country',)
