# """
# DEPRECATED - 此文件中的函数已被移动到apis目录下的各个模块中
#
# 请使用以下模块中的相应函数：
# - apis/project.py - 项目相关API
# - apis/bid.py - 投标相关API
# - apis/company.py - 公司信息API
# - apis/auth.py - 用户认证API
# - apis/list_simulator.py - 清单模拟器API
# - apis/excel_processor.py - Excel处理器API
# - apis/bid_optimizer.py - 投标优化器API
#
# 本文件将在未来版本中废弃
# """
#
# import json
# import pandas as pd
# import numpy as np
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, JsonResponse
# from django.contrib import messages
# from .forms import ExcelProcessorMainForm, NumGroupForm, NumRangeForm
# from .models import Project, Bid, BidRank, BidSection, CompanyInfo, EmployeeInfo, ExcelProcessing
# from .utils import optimize_bid, process_excel_data, simulate_list, list_simulator_from_excel, process_excel_file, generate_result_html
# from price.BidOptimizer import BidOptimizer
# from .serializers import ProjectSerializer, BidSectionSerializer, BidSerializer, BidRankSerializer, CompanyInfoSerializer, EmployeeInfoSerializer, UserSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.utils import timezone
# from datetime import datetime, timedelta
# from django.db import models
# from django.core.cache import cache
# import random
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.validators import RegexValidator
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def projects_list(request):
#     projects = Project.objects.all().order_by('-time_show')[:10]
#     serializer = ProjectSerializer(projects, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def project_detail(request, project_id):
#     project = get_object_or_404(Project, project_id=project_id)
#     html_content = project.notice_content
#     bid_sections = BidSection.objects.filter(project_id=project.project_id)
#     bid_sections_data = BidSectionSerializer(bid_sections, many=True).data
#     return Response({
#         "bid_sections": bid_sections_data,
#         "html_content": html_content
#     })
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def bid_sections_list(request):
#     bid_sections = BidSection.objects.all().order_by('-bid_open_time')[:10]
#     serializer = BidSectionSerializer(bid_sections, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def bid_detail(request, pk):
#     from .models import Bid
#     from .serializers import BidSerializer
#     try:
#         bid_section = BidSection.objects.get(pk=pk)
#         section_id = bid_section.section_id
#         project_id = bid_section.project_id_id
#         lot_ctl_amt = bid_section.lot_ctl_amt
#         bids = Bid.objects.filter(section_id=section_id, project_id=project_id)
#     except Bid.DoesNotExist:
#         return Response({'detail': 'Not found.'}, status=404)
#     serializer = BidSerializer(bids, many=True)
#     # 为每个投标对象增加lot_ctl_amt字段
#     data = serializer.data
#     for item in data:
#         item['lot_ctl_amt'] = lot_ctl_amt
#     return Response(data)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def bid_result(request):
#     from .models import BidRank
#     from .serializers import BidRankSerializer
#     bid_ranks = BidRank.objects.all().order_by('-open_time')[:6]
#     serializer = BidRankSerializer(bid_ranks, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def bid_result_detail(request, pk):
#     from .models import BidRank
#     from .serializers import BidRankSerializer
#     try:
#         bid_rank = BidRank.objects.get(pk=pk)
#         project_id = bid_rank.project_id
#         section_id = bid_rank.section_id
#         all_ranks = BidRank.objects.filter(project_id=project_id, section_id=section_id).order_by('rank')
#     except BidRank.DoesNotExist:
#         return Response({'detail': 'Not found.'}, status=404)
#     serializer = BidRankSerializer(all_ranks, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def today_update_count(request):
#     from .models import Project, Bid, BidRank
#     today = timezone.now().date()
#     project_count = Project.objects.filter(time_show__date=today).count()
#     bid_count = Bid.objects.filter(bid_open_time__date=today).count()
#     bid_result_count = BidRank.objects.filter(open_time__date=today).count()
#     return Response({
#         'project_count': project_count,
#         'bid_count': bid_count,
#         'bid_result_count': bid_result_count
#     })
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def company_search(request):
#     from .models import CompanyInfo, EmployeeInfo
#     from .serializers import CompanyInfoSerializer, EmployeeInfoSerializer
#     query = request.GET.get('query', '').strip()
#     if not query:
#         return Response([])
#     companies = CompanyInfo.objects.filter(
#         models.Q(name__icontains=query) |
#         models.Q(corp_code__icontains=query) |
#         models.Q(corp__icontains=query)
#     )[:20]
#     company_data = []
#     for company in companies:
#         data = CompanyInfoSerializer(company).data
#         employees = EmployeeInfo.objects.filter(corp_code=company.corp_code)
#         data['employees'] = EmployeeInfoSerializer(employees, many=True).data
#         company_data.append(data)
#     return Response(company_data)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def company_bids(request):
#     from .models import Bid, CompanyInfo
#     from .serializers import BidSerializer
#     corp_code = request.GET.get('corp_code', '').strip()
#     page = int(request.GET.get('page', 1))
#     PAGE_SIZE = 20
#     if not corp_code:
#         return Response({'results': [], 'count': 0})
#     # 先查公司名称
#     try:
#         company = CompanyInfo.objects.get(corp_code=corp_code)
#         company_name = company.name
#     except CompanyInfo.DoesNotExist:
#         return Response({'results': [], 'count': 0})
#     # 用公司名称查投标记录
#     bids = Bid.objects.filter(bidder_name__icontains=company_name)
#     total = bids.count()
#     bids = bids.order_by('-bid_open_time')[(page-1)*PAGE_SIZE:page*PAGE_SIZE]
#     serializer = BidSerializer(bids, many=True)
#     return Response({'results': serializer.data, 'count': total})
#
#
#
#
# def home(request):
#     # Get top 20 companies by successful bids
#     success_ranking = CompanyInfo.objects.all().order_by('-win_count')[:20]
#     # Get top 20 companies by total bids
#     total_ranking = CompanyInfo.objects.all().order_by('-bid_count')[:20]
#
#     return render(request, 'bidapp/home.html', {
#         'success_ranking': success_ranking,
#         'total_ranking': total_ranking
#     })
#
# def bid_optimizer(request):
#     if request.method == 'POST':
#         min_values = request.POST.getlist('min[]')
#         max_values = request.POST.getlist('max[]')
#         num_values = request.POST.getlist('num[]')
#         m_value = int(request.POST.get('m_value'))
#         # Process the input lists
#         input_lists = []
#         for min_val, max_val, num_val in zip(min_values, max_values, num_values):
#             random_floats = np.random.uniform(low=float(min_val), high=float(max_val), size=int(num_val)).tolist()
#             input_lists += np.round(random_floats, 4).tolist()
#         sorted(input_lists)
#         # Example: Calculate a recommended bid (replace with your logic)
#         optimizer = BidOptimizer(other_prices=input_lists, my_company_count=m_value)
#         my_bids = optimizer.find_optimal_bids()
#
#         return render(request, 'bidapp/bid_optimizer.html', {
#             'result': {
#                 'recommended_bid': my_bids,
#                 'input_lists': input_lists,
#                 'm_value':m_value
#             }
#         })
#
#     return render(request, 'bidapp/bid_optimizer.html')
#
# def excel_processor(request):
#     if request.method == 'POST':
#         main_form = ExcelProcessorMainForm(request.POST, request.FILES)
#
#         try:
#             # 验证Excel文件
#             if not main_form.is_valid():
#                 raise ValueError("Invalid Excel file")
#
#             # 处理NUM组数据
#             processed_data = []
#             num_values = request.POST.getlist('num_value')
#             reduc_values = request.POST.getlist('reduc')  # 新增获取reduc值
#
#             # 检查是否有NUM值提交
#             if not num_values:
#                 raise ValueError("No NUM values submitted")
#
#             for group_index, (num_value, reduc_value) in enumerate(zip(num_values, reduc_values)):
#                 try:
#                     # 验证NUM值和reduc值
#                     num_form = NumGroupForm({
#                         'num_value': num_value,
#                         'reduc': reduc_value
#                     })
#                     if not num_form.is_valid():
#                         continue
#
#                     ranges = []
#                     # 获取当前NUM组的所有范围数据
#                     range_data = zip(
#                         request.POST.getlist(f'start[{group_index}][]', []),
#                         request.POST.getlist(f'end[{group_index}][]', []),
#                         request.POST.getlist(f'min_value[{group_index}][]', []),
#                         request.POST.getlist(f'max_value[{group_index}][]', [])
#                     )
#
#                     for start, end, min_val, max_val in range_data:
#                         range_form = NumRangeForm({
#                             'start': start,
#                             'end': end,
#                             'min_value': min_val,
#                             'max_value': max_val
#                         })
#
#                         if range_form.is_valid():
#                             ranges.append({
#                                 'start': range_form.cleaned_data['start'],
#                                 'end': range_form.cleaned_data['end'],
#                                 'min': range_form.cleaned_data['min_value'],
#                                 'max': range_form.cleaned_data['max_value']
#                             })
#
#                     if ranges:  # 只添加有效范围的NUM组
#                         processed_data.append({
#                             'num': float(num_value),
#                             'reduc': float(reduc_value),  # 添加reduc值到结果中
#                             'ranges': ranges
#                         })
#                 except ValueError as e:
#                     messages.warning(request, f'Error processing NUM group {group_index + 1}: {str(e)}')
#
#             if not processed_data:
#                 raise ValueError("No valid data submitted")
#
#             # 使用工具函数处理Excel文件
#             result = process_excel_file(request.FILES['excel_file'], processed_data)
#
#             # 生成直接下载链接，不经过数据库存储
#             from django.urls import reverse
#             from django.utils.http import urlencode
#             import base64
#             import json
#
#             # 将相对路径编码到URL中（临时方案，实际使用应通过session或缓存存储）
#             file_path_b64 = base64.b64encode(result['relative_path'].encode()).decode()
#             download_url = reverse('excel_processor') + f'?download={file_path_b64}'
#
#             return render(request, 'bidapp/excel_processor.html', {
#                 'excel_form': ExcelProcessorMainForm(),
#                 'num_group_form': NumGroupForm(),
#                 'num_range_form': NumRangeForm(),
#                 'processed_data': result['result_html'],
#                 'download_url': download_url,
#                 'original_filename': result['original_filename']
#             })
#
#         except Exception as e:
#             messages.error(request, f'处理数据时出错: {str(e)}')
#
#     # 处理文件下载请求
#     download_param = request.GET.get('download')
#     if download_param:
#         try:
#             import base64
#             from django.conf import settings
#             import os
#
#             # 解码文件路径
#             relative_path = base64.b64decode(download_param).decode()
#             file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
#
#             if os.path.exists(file_path):
#                 filename = os.path.basename(file_path)
#                 with open(file_path, 'rb') as f:
#                     response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#                     response['Content-Disposition'] = f'attachment; filename={filename}'
#                     return response
#         except Exception as e:
#             messages.error(request, f'下载文件时出错: {str(e)}')
#
#     return render(request, 'bidapp/excel_processor.html', {
#         'excel_form': ExcelProcessorMainForm(),
#         'num_group_form': NumGroupForm(),
#         'num_range_form': NumRangeForm()
#     })
#
#
# def download_excel(request, file_id):
#     excel_processing = get_object_or_404(ExcelProcessing, id=file_id)
#
#     if excel_processing.processed_file:
#         file_path = excel_processing.processed_file.path
#         with open(file_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = f'attachment; filename={excel_processing.original_filename}_processed.xlsx'
#             return response
#
#     messages.error(request, 'Processed file not found.')
#     return redirect('excel_processor')
#
# @api_view(['POST'])
# def send_sms_code(request):
#     phone = request.data.get('phone')
#     if not phone:
#         return Response({'error': '手机号不能为空'}, status=400)
#     code = str(random.randint(1000, 9999))
#     print(f"发送验证码 {code} 到手机号 {phone}")
#     cache.set(f'sms_code_{phone}', code, timeout=300)  # 5分钟有效
#     return Response({'msg': '验证码已发送'})
#
# @api_view(['POST'])
# def register(request):
#     from django.core.cache import cache
#     username = request.data.get('username')
#     password = request.data.get('password')
#     phone = request.data.get('phone')
#     company = request.data.get('company')
#     sms_code = request.data.get('sms_code')
#
#     if not all([username, password, phone, company, sms_code]):
#         return Response({'error': '所有字段均不能为空'}, status=400)
#
#     # 手机号格式校验
#     phone_validator = RegexValidator(r'^1\d{10}$', '手机号格式不正确')
#     try:
#         phone_validator(phone)
#     except Exception as e:
#         return Response({'error': str(e)}, status=400)
#
#     real_code = cache.get(f'sms_code_{phone}')
#     if not real_code or real_code != sms_code:
#         return Response({'error': '验证码错误或已过期'}, status=400)
#
#     # 手机号唯一性校验
#     if User.objects.filter(phone=phone).exists():
#         return Response({'error': '手机号已注册'}, status=400)
#     if User.objects.filter(username=username).exists():
#         return Response({'error': '用户名已存在'}, status=400)
#
#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         phone=phone,
#         company=company,
#         membership_level='free',
#         membership_start=timezone.now(),
#         membership_end=timezone.now() + timedelta(days=365)
#     )
#     return Response({'msg': '注册成功'})
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_info(request):
#     user = request.user  # 直接用当前登录用户
#     data = UserSerializer(user).data
#     return Response({'user': data})
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     refresh_token = request.data.get('refresh')
#     if not refresh_token:
#         return Response({'error': '缺少 refresh token'}, status=400)
#     try:
#         token = RefreshToken(refresh_token)
#         token.blacklist()
#         return Response({'msg': '登出成功'})
#     except Exception as e:
#         return Response({'error': 'Token 无效或已失效'}, status=400)
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # 或 AllowAny，按需设置
# def list_simulator_api(request):
#     # 支持Excel文件上传
#     if 'file' in request.FILES:
#         try:
#             # 解析价格组参数
#             price_groups = None
#             if 'price_groups' in request.data:
#                 try:
#                     if isinstance(request.data['price_groups'], str):
#                         import json
#                         price_groups = json.loads(request.data['price_groups'])
#                     else:
#                         price_groups = request.data['price_groups']
#                 except Exception as e:
#                     return Response({'error': f'价格组参数格式错误: {str(e)}'}, status=400)
#
#             # 生成临时文件名
#             from datetime import datetime
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#
#             # 检查是否请求包含完整数据
#             include_full_data = False
#             if 'include_full_data' in request.data:
#                 include_full_data_param = request.data.get('include_full_data')
#                 include_full_data = (
#                     include_full_data_param == 'true' or
#                     include_full_data_param == True or
#                     include_full_data_param == '1' or
#                     include_full_data_param == 1
#                 )
#
#             # 处理文件并生成结果
#             result = list_simulator_from_excel(request.FILES['file'], price_groups, include_full_data)
#
#             # 确保结果中没有非法JSON值(NaN, inf)
#             def clean_json_values(obj):
#                 import math
#                 import decimal
#                 if isinstance(obj, dict):
#                     return {k: clean_json_values(v) for k, v in obj.items()}
#                 elif isinstance(obj, list):
#                     return [clean_json_values(item) for item in obj]
#                 elif isinstance(obj, float):
#                     if math.isnan(obj) or math.isinf(obj):
#                         return 0
#                     return obj
#                 elif isinstance(obj, decimal.Decimal):
#                     return float(obj)
#                 else:
#                     return obj
#
#             result = clean_json_values(result)
#
#             # 如果需要生成下载文件
#             if price_groups and len(price_groups) > 0:
#                 # 此处可添加生成下载文件的逻辑
#                 # 例如，保存到media目录并返回URL
#                 from django.conf import settings
#                 import os
#                 import pandas as pd
#
#                 # 保存目录路径
#                 processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_files')
#                 if not os.path.exists(processed_dir):
#                     os.makedirs(processed_dir)
#
#                 # 保存处理后的DataFrame为Excel文件
#                 filename = f"list_simulator_{timestamp}.xlsx"
#                 file_path = os.path.join(processed_dir, filename)
#
#                 # 获取原始数据
#                 df_original = pd.read_excel(request.FILES['file'])
#
#                 # 使用process_excel_data处理
#                 processed_data_format = []
#                 for group in price_groups:
#                     processed_data_format.append({
#                         'num': group['numValue'],
#                         'reduc': group['reduc'],
#                         'ranges': [
#                             {
#                                 'start': r['start'],
#                                 'end': r['end'],
#                                 'min': r['min'],
#                                 'max': r['max']
#                             }
#                             for r in group['ranges']
#                         ]
#                     })
#                 processed_df = process_excel_data(df_original, processed_data_format)
#
#                 # 保存结果到Excel
#                 processed_df.to_excel(file_path, index=False)
#
#                 # 添加下载URL到结果
#                 result['downloadUrl'] = request.build_absolute_uri(
#                     os.path.join(settings.MEDIA_URL, 'processed_files', filename)
#                 )
#
#             return Response(result)
#         except Exception as e:
#             import traceback
#             traceback.print_exc()
#             return Response({'error': str(e)}, status=400)
#
#     # 兼容原有字符串输入
#     input_param = request.data.get('input')
#     result = simulate_list(input_param)
#     return Response(result)
