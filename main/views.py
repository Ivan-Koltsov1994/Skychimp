from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Post
from main.forms import ClientForms, MessageForms
from main.models import Sending, Clients, Message, Attempt
from main.services import send_email_to_clients


# Create your views here.

class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Sending.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_posts'] = Post.objects.all().order_by('?')[:3]
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Clients
    extra_context = {
        'object_list': Clients.objects.all(),
        'title': 'Все клиенты'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        if self.request.user.has_perm('main.can_view_client'):
            return queryset
        return Clients.objects.filter(created_by=self.request.user)


class ClientDetailView(DetailView):
    model = Clients
    extra_context = {
        'title': 'Детали клиента'
    }


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientForms
    success_url = reverse_lazy('main:clients_list')


class ClientUpdateView(UpdateView):
    model = Clients
    form_class = ClientForms

    def get_success_url(self):
        return reverse('main:clients_detail', args=[str(self.object.pk)])


class ClientDeleteView(DeleteView):
    model = Clients
    success_url = reverse_lazy('main:clients_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'message_list': Message.objects.all(),
        'title': 'Все Сообщения'
    }


class MessageDetailView(DetailView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForms
    success_url = reverse_lazy('main:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body',)

    def get_success_url(self):
        return reverse('main:message_view', args=[str(self.object.pk)])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    extra_context = {
        'object_list': Sending.objects.all(),
        'title': 'Все Рассылки'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('main.can_view_sending'):
            return queryset
        return Sending.objects.filter(created=self.request.user)


class SendingDetailView(DetailView):
    model = Sending

    def test_func(self):
        return self.request.user.has_perm(perm='main.set_sending_status')


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    fields = ('message', 'frequency', 'status', 'created')
    success_url = reverse_lazy('main:sending_list')

    # При установке флага отправки сообщения 1 раз - отправляем сообщение сразу
    send_email_to_clients(Sending.ONCE)


class SendingUpdateView(UpdateView):
    model = Sending
    fields = ('message', 'frequency', 'status',)

    def get_success_url(self):
        return reverse('main:sending_view', args=[str(self.object.pk)])


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('main:sending_list')


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    extra_context = {
        'object_list': Attempt.objects.all(),
        'title': 'Статистика рассылок'
    }


class AttemptDetailView(DetailView):
    model = Attempt
    extra_context = {
        'title': 'Детали рассылки'
    }


def set_is_active(request, pk):
    clients_item = get_object_or_404(Clients, pk=pk)
    if clients_item.is_active:
        clients_item.is_active = False
    else:
        clients_item.is_active = True
    clients_item.save()
    return redirect(reverse('main:clients_list'))


def set_status_sending(pk):
    sending_item = get_object_or_404(Sending, pk=pk)
    if sending_item.status == Sending.CREATED:
        sending_item.status = Sending.COMPLETED
        sending_item.save()
    else:
        sending_item.status = Sending.CREATED
        sending_item.save()
    return redirect(reverse('main:sending_list'))
