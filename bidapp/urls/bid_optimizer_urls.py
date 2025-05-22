from django.urls import path
from ..apis.bid_optimizer import bid_optimizer

urlpatterns = [
    path('bid-optimizer/', bid_optimizer, name='bid_optimizer'),
]
