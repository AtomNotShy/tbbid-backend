from django.urls import path
from ..apis.auth import send_sms_code, register, user_info, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('send_sms_code/', send_sms_code, name='send_sms_code'),
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', user_info, name='user_info'),
    path('logout/', logout, name='logout'),
]
