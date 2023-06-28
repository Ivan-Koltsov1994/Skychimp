from django import forms

from main.models import Clients, Message


class FormStyleMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForms(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'


class MessageForms(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'