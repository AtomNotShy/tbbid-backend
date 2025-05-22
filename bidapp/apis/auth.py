import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from ..serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def send_sms_code(request):
    """发送短信验证码"""
    phone = request.data.get('phone')
    if not phone:
        return Response({'error': '手机号不能为空'}, status=400)
    
    code = str(random.randint(1000, 9999))
    print(f"发送验证码 {code} 到手机号 {phone}")  # 实际环境应替换为真正的短信发送
    cache.set(f'sms_code_{phone}', code, timeout=300)  # 5分钟有效
    
    return Response({'msg': '验证码已发送'})


@api_view(['POST'])
def register(request):
    """用户注册"""
    username = request.data.get('username')
    password = request.data.get('password')
    phone = request.data.get('phone')
    company = request.data.get('company')
    sms_code = request.data.get('sms_code')

    if not all([username, password, phone, company, sms_code]):
        return Response({'error': '所有字段均不能为空'}, status=400)

    # 手机号格式校验
    phone_validator = RegexValidator(r'^1\d{10}$', '手机号格式不正确')
    try:
        phone_validator(phone)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

    real_code = cache.get(f'sms_code_{phone}')
    if not real_code or real_code != sms_code:
        return Response({'error': '验证码错误或已过期'}, status=400)

    # 手机号唯一性校验
    if User.objects.filter(phone=phone).exists():
        return Response({'error': '手机号已注册'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        phone=phone,
        company=company,
        membership_level='free',
        membership_start=timezone.now(),
        membership_end=timezone.now() + timedelta(days=365)
    )
    return Response({'msg': '注册成功'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """获取用户信息"""
    user = request.user  # 直接用当前登录用户
    data = UserSerializer(user).data
    return Response({'user': data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """用户登出"""
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'error': '缺少 refresh token'}, status=400)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'msg': '登出成功'})
    except Exception as e:
        return Response({'error': 'Token 无效或已失效'}, status=400)
