from django.contrib import admin
from main.models import Clients, Sending, Attempt, Message


@admin.register(Clients)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    list_filter = ('name',)


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'scheduled_time', 'frequency', 'status',)
    list_filter = ('created_at', 'scheduled_time', 'frequency', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at',)
    list_filter = ('created_at',)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('sending', 'sent_at', 'status', 'response',)
    list_filter = ('sending', 'sent_at', 'status', 'response',)


from django.contrib import admin

# Register your models here.
