from django.urls import path
from ..apis.company import company_search, company_bids, company_wins

urlpatterns = [
    path('company-search/', company_search, name='company_search'),
    path('company-bids/', company_bids, name='company_bids'),
    path('company-wins/', company_wins, name='company_wins'),
]
