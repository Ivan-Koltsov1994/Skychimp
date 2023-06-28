from django.urls import path

from main.apps import MainConfig
from main.views import IndexView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, set_is_active, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, SendingListView, SendingDetailView, SendingCreateView, SendingUpdateView, SendingDeleteView, \
    AttemptListView, AttemptDetailView, set_status_sending, SearchResultsView

app_name = MainConfig.name


urlpatterns = [

    path('', IndexView.as_view(), name='Index'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='clients_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='clients_update'),
    path('customer/delete/<int:pk>/', ClientDeleteView.as_view(), name='clients_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('sending/', SendingListView.as_view(), name='sending_list'),
    path('sending/<int:pk>/', SendingDetailView.as_view(), name='sending_view'),
    path('sending/create/', SendingCreateView.as_view(), name='sending_create'),
    path('sending/update/<int:pk>/', SendingUpdateView.as_view(), name='sending_update'),
    path('sending/delete/<int:pk>/', SendingDeleteView.as_view(), name='sending_delete'),
    path('attempt/', AttemptListView.as_view(), name='attempt_list'),
    path('attempt/<int:pk>/', AttemptDetailView.as_view(), name='attempt_view'),

    path('set_status_sending/<int:pk>', set_status_sending, name='set_status_sending'),
    path('set_is_active/<int:pk>', set_is_active, name='set_is_active'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
            ]