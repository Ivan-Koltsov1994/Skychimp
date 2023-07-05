import secrets

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView

from config import settings
from users.forms import UserChangeForm, UserRegisterForm
from users.models import User
from users.services import confirm_account


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    success_url = reverse_lazy('main:Index')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = f'/users/page_after_registration/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_token = None

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.token = secrets.token_urlsafe(18)[:15]
            confirm_account(self.object)
            self.object.save()
            self.user_token = self.object.token
            self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Метод создает уникальный URL для подтверждения регистрации"""
        new_url = super().get_success_url()
        token = self.object.token
        return str(new_url) + str(token)


def page_after_registration(request, token):
    """Поcле отправки запроса на верификацию отправляет на страницу ожидания подтверждения пароля"""
    if request.method == 'POST':
        obj = get_object_or_404(User, token=token)
        confirm_account(obj)
    return render(request, 'users/page_after_registration.html')


def activate_user(request, token):
    """Метод активирует деактивированного пользователя"""
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()
        return redirect('users:login')
    return render(request, 'users/user_not_found.html')


def generate_new_password(request):
    """Метод генерирует новый пароль и отправляет на почту пользователя"""
    pass_ch = secrets.token_urlsafe(18)[:12]
    send_mail(
        subject='Смена пароля',
        message=f'Ваш новый пароль {pass_ch}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    # print(pass_ch)
    request.user.set_password(pass_ch)
    request.user.save()
    return redirect(reverse('users:login'))
