from django.urls import path, include
from . import views  # 保留一些可能未移动的视图

# 主路由，包含所有子模块的路由
urlpatterns = [
        # 各功能模块API路由
    path('api/', include('bidapp.urls.project_urls')),
    path('api/', include('bidapp.urls.bid_urls')),
    path('api/', include('bidapp.urls.company_urls')),
    path('api/', include('bidapp.urls.auth_urls')),
    path('api/', include('bidapp.urls.list_simulator_urls')),
    
    # 工具页面路由
    path('', include('bidapp.urls.excel_processor_urls')),
    path('', include('bidapp.urls.bid_optimizer_urls')),
] 