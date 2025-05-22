import os
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from ..forms import ExcelProcessorMainForm, NumGroupForm, NumRangeForm
from ..utils import process_excel_file


def excel_processor(request):
    """Excel处理器页面视图"""
    if request.method == 'POST':
        main_form = ExcelProcessorMainForm(request.POST, request.FILES)

        try:
            # 验证Excel文件
            if not main_form.is_valid():
                raise ValueError("Invalid Excel file")

            # 处理NUM组数据
            processed_data = []
            num_values = request.POST.getlist('num_value')
            reduc_values = request.POST.getlist('reduc')  # 新增获取reduc值

            # 检查是否有NUM值提交
            if not num_values:
                raise ValueError("No NUM values submitted")

            for group_index, (num_value, reduc_value) in enumerate(zip(num_values, reduc_values)):
                try:
                    # 验证NUM值和reduc值
                    num_form = NumGroupForm({
                        'num_value': num_value,
                        'reduc': reduc_value
                    })
                    if not num_form.is_valid():
                        continue

                    ranges = []
                    # 获取当前NUM组的所有范围数据
                    range_data = zip(
                        request.POST.getlist(f'start[{group_index}][]', []),
                        request.POST.getlist(f'end[{group_index}][]', []),
                        request.POST.getlist(f'min_value[{group_index}][]', []),
                        request.POST.getlist(f'max_value[{group_index}][]', [])
                    )

                    for start, end, min_val, max_val in range_data:
                        range_form = NumRangeForm({
                            'start': start,
                            'end': end,
                            'min_value': min_val,
                            'max_value': max_val
                        })

                        if range_form.is_valid():
                            ranges.append({
                                'start': range_form.cleaned_data['start'],
                                'end': range_form.cleaned_data['end'],
                                'min': range_form.cleaned_data['min_value'],
                                'max': range_form.cleaned_data['max_value']
                            })

                    if ranges:  # 只添加有效范围的NUM组
                        processed_data.append({
                            'num': float(num_value),
                            'reduc': float(reduc_value),  # 添加reduc值到结果中
                            'ranges': ranges
                        })
                except ValueError as e:
                    messages.warning(request, f'Error processing NUM group {group_index + 1}: {str(e)}')

            if not processed_data:
                raise ValueError("No valid data submitted")
            
            # 使用工具函数处理Excel文件
            result = process_excel_file(request.FILES['excel_file'], processed_data)
            
            # 将相对路径编码到URL中
            file_path_b64 = base64.b64encode(result['relative_path'].encode()).decode()
            download_url = reverse('excel_processor') + f'?download={file_path_b64}'

            return render(request, 'bidapp/excel_processor.html', {
                'excel_form': ExcelProcessorMainForm(),
                'num_group_form': NumGroupForm(),
                'num_range_form': NumRangeForm(),
                'processed_data': result['result_html'],
                'download_url': download_url,
                'original_filename': result['original_filename']
            })

        except Exception as e:
            messages.error(request, f'处理数据时出错: {str(e)}')

    # 处理文件下载请求
    download_param = request.GET.get('download')
    if download_param:
        try:
            # 解码文件路径
            relative_path = base64.b64decode(download_param).decode()
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    return response
        except Exception as e:
            messages.error(request, f'下载文件时出错: {str(e)}')
            
    return render(request, 'bidapp/excel_processor.html', {
        'excel_form': ExcelProcessorMainForm(),
        'num_group_form': NumGroupForm(),
        'num_range_form': NumRangeForm()
    })
