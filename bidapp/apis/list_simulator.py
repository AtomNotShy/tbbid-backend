import json
import os
import math
import decimal
import pandas as pd
import traceback
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..utils import list_simulator_from_excel, process_excel_data, simulate_list


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 或 AllowAny，按需设置
def list_simulator_api(request):
    """清单模拟器API"""
    # 支持Excel文件上传
    if 'file' in request.FILES:
        try:
            # 解析价格组参数
            price_groups = None
            if 'price_groups' in request.data:
                try:
                    if isinstance(request.data['price_groups'], str):
                        price_groups = json.loads(request.data['price_groups'])
                    else:
                        price_groups = request.data['price_groups']
                except Exception as e:
                    return Response({'error': f'价格组参数格式错误: {str(e)}'}, status=400)
            
            # 生成临时文件名
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 检查是否请求包含完整数据
            include_full_data = False
            if 'include_full_data' in request.data:
                include_full_data_param = request.data.get('include_full_data')
                include_full_data = (
                    include_full_data_param == 'true' or 
                    include_full_data_param == True or 
                    include_full_data_param == '1' or 
                    include_full_data_param == 1
                )
            
            # 处理文件并生成结果
            result = list_simulator_from_excel(request.FILES['file'], price_groups, include_full_data)
            
            # 确保结果中没有非法JSON值(NaN, inf)
            result = clean_json_values(result)
            
            # 如果需要生成下载文件
            if price_groups and len(price_groups) > 0:
                # 保存目录路径
                processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_files')
                if not os.path.exists(processed_dir):
                    os.makedirs(processed_dir)
                
                # 保存处理后的DataFrame为Excel文件
                filename = f"list_simulator_{timestamp}.xlsx"
                file_path = os.path.join(processed_dir, filename)
                
                # 获取原始数据
                df_original = pd.read_excel(request.FILES['file'])
                
                # 使用process_excel_data处理
                processed_data_format = []
                for group in price_groups:
                    processed_data_format.append({
                        'num': group['numValue'],
                        'reduc': group['reduc'],
                        'ranges': [
                            {
                                'start': r['start'],
                                'end': r['end'],
                                'min': r['min'],
                                'max': r['max']
                            }
                            for r in group['ranges']
                        ]
                    })
                processed_df = process_excel_data(df_original, processed_data_format)
                
                # 保存结果到Excel
                processed_df.to_excel(file_path, index=False)
                
                # 添加下载URL到结果
                result['downloadUrl'] = request.build_absolute_uri(
                    os.path.join(settings.MEDIA_URL, 'processed_files', filename)
                )
            
            return Response(result)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=400)
    
    # 兼容原有字符串输入
    input_param = request.data.get('input')
    result = simulate_list(input_param)
    return Response(result)


def clean_json_values(obj):
    """清理JSON中的非法值（NaN, Infinity等）"""
    if isinstance(obj, dict):
        return {k: clean_json_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_values(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0
        return obj
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
