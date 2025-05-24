from django.urls import path
from ..apis.company import company_search, company_bids, company_wins, company_achievements, achievement_detail, company_manager_performances
from ..serializers import UserSerializer

urlpatterns = [
    path('company-search/', company_search, name='company_search'),
    path('company-bids/', company_bids, name='company_bids'),
    path('company-wins/', company_wins, name='company_wins'),
    path('company-achievements/', company_achievements, name='company_achievements'),
    path('company-achievement/<int:pk>/', achievement_detail, name='achievement_detail'),
    path('company-manager-performances/', company_manager_performances, name='company_manager_performances'),
]
