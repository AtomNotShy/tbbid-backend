from django.urls import path
from ..apis.bid import bid_sections_list, bid_detail, bid_result, bid_result_detail

urlpatterns = [
    path('bid_sections/', bid_sections_list, name='bid_sections_list'),
    path('bids/<int:pk>/', bid_detail, name='bid_detail'),
    path('bid_results/', bid_result, name='bid_result'),
    path('bid_results/<int:pk>/', bid_result_detail, name='bid_result_detail'),
]
