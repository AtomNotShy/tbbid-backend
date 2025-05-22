"""
DEPRECATED - 此文件中的路由配置已被移动到urls目录下的各个模块中

请使用main_urls.py作为主入口，它包含了对以下文件的引用：
- urls/project_urls.py - 项目相关路由
- urls/bid_urls.py - 投标相关路由
- urls/company_urls.py - 公司相关路由
- urls/auth_urls.py - 用户认证路由
- urls/list_simulator_urls.py - 清单模拟器路由
- urls/excel_processor_urls.py - Excel处理器路由
- urls/bid_optimizer_urls.py - 投标优化器路由

本文件将在未来版本中废弃
"""

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('bid-optimizer/', views.bid_optimizer, name='bid_optimizer'),
#     path('excel-processor/', views.excel_processor, name='excel_processor'),
#     path('download-excel/<int:file_id>/', views.download_excel, name='download_excel'),
#     path('api/projects/', views.projects_list, name='projects_list'),
#     path('api/projects/<str:project_id>/', views.project_detail, name='project_detail'),
#     path('api/bid_sections/', views.bid_sections_list, name='bid_sections_list'),
#     path('api/bids/<int:pk>/', views.bid_detail, name='bid_detail'),
#     path('api/bid_results/', views.bid_result, name='bid_result'),
#     path('api/bid_results/<int:pk>/', views.bid_result_detail, name='bid_result_detail'),
#     path('api/today_update_count/', views.today_update_count, name='today_update_count'),
#     path('api/company-search/', views.company_search, name='company_search'),
#     path('api/company-bids/', views.company_bids, name='company_bids'),
#     path('api/send_sms_code/', views.send_sms_code, name='send_sms_code'),
#     path('api/register/', views.register, name='register'),
#     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/user-info/', views.user_info, name='user_info'),
#     path('api/logout/', views.logout, name='logout'),
#     path('api/list-simulator/', views.list_simulator_api, name='list_simulator_api'),
# ]

