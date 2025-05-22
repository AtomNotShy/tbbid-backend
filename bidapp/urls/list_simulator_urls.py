from django.urls import path
from ..apis.list_simulator import list_simulator_api

urlpatterns = [
    path('list-simulator/', list_simulator_api, name='list_simulator_api'),
]
