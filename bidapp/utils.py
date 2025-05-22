import pandas as pd
import random
import time
import numpy as np
import uuid
import os
import logging
from django.conf import settings

# 获取logger
logger = logging.getLogger(__name__)

def optimize_bid(lists, m_value):
    """
    Placeholder for the bid optimization algorithm.
    In a real implementation, this would contain the actual algorithm logic.

    Args:
        lists: A list of lists containing the input values
        m_value: The M value for optimization

    Returns:
        float: The recommended bid
    """
    # This is a simple placeholder implementation
    # Replace with actual algorithm logic

    # Calculate average of each list
    averages = [sum(lst) / len(lst) if lst else 0 for lst in lists]

    # Apply a simple formula using the averages and M value
    # This is just a placeholder - replace with actual algorithm
    recommended_bid = sum(averages) * m_value / len(averages) if averages else 0

    return round(recommended_bid, 2)

def process_excel_data(df, processed_data):
    """
    Process the Excel data based on user inputs.

    Args:
        df: Pandas DataFrame containing the Excel data
        processed_data: List of dictionaries containing user inputs
            Example: [
                {
                    'num': 5.0,
                    'reduc': 0.95,
                    'ranges': [
                        {'start': 1.0, 'end': 10.0, 'min': 0.8, 'max': 0.9},
                        {'start': 50.0, 'end': 100.0, 'min': 1.0, 'max': 2.0}
                    ]
                }
            ]

    Returns:
        DataFrame: Processed DataFrame with new columns
    """
    # Make a copy to avoid modifying the original
    processed_df = df.copy()

    # 检查DataFrame是否包含必要的列（控制价和数量）
    required_cols = ['控制价', '数量']
    for col in required_cols:
        if col not in processed_df.columns:
            raise ValueError(f"Excel文件缺少必要的列: {col}")

    # 计算合价（控制价*数量）
    processed_df['合价'] = processed_df['控制价'] * processed_df['数量']

    # 计算合价占总价的比例
    total_price = processed_df['合价'].sum()
    processed_df['占比'] = processed_df['合价'] / total_price * 100

    # 初始化方案计数器，用于跟踪当前方案编号
    scheme_counter = 1

    # 处理每个NUM组的数据
    for group in processed_data:
        num_value = int(group['num'])  # 需要生成的新列数量
        reduc = float(group['reduc'])  # 下浮比例
        ranges = group['ranges']  # 区间设置

        # 为每个NUM值生成新列
        for _ in range(num_value):
            # 设置不同的随机种子，确保每个方案生成不同的随机值
            # 使用当前时间和方案索引生成不同的种子
            # 确保种子值在允许的范围内
            seed_value = (int(time.time() * 1000) + scheme_counter * 100) % (2**32 - 1)
            random.seed(seed_value)

            # 使用递增的方案编号
            column_name = f'方案{scheme_counter}'

            # 初始化新列，默认复制原控制价
            processed_df[column_name] = processed_df['控制价'].copy()

            # 为每个区间应用随机系数
            for range_setting in ranges:
                start_percentile = range_setting['start']
                end_percentile = range_setting['end']
                min_factor = range_setting['min']
                max_factor = range_setting['max']

                # 按占比对行进行排序，找出排名在指定百分比区间内的行
                # 首先创建一个排序后的数据副本
                sorted_df = processed_df.sort_values(by='占比', ascending=False).copy()

                # 计算总行数
                total_rows = len(sorted_df)

                # 计算开始和结束的行索引（基于百分比）
                start_idx = int(total_rows * start_percentile / 100)
                end_idx = int(total_rows * end_percentile / 100)

                # 确保索引在有效范围内
                start_idx = max(0, start_idx)
                end_idx = min(total_rows, end_idx)

                # 获取这些行的原始索引
                selected_indices = sorted_df.index[start_idx:end_idx]
                mask_count = len(selected_indices)
                logger.debug(f"Selected {mask_count} rows for range {start_percentile}-{end_percentile}%")
                if mask_count > 0:
                    # 为这些行生成随机系数
                    random_factors = []
                    for _ in range(mask_count):
                        # 每次生成一个随机数，增加随机性
                        random_factors.append(random.uniform(min_factor, max_factor))

                    # 将生成的随机系数应用到数据中
                    for idx, factor in zip(selected_indices, random_factors):
                        # 应用随机系数并保留两位小数
                        processed_df.loc[idx, column_name] = round(processed_df.loc[idx, '控制价'] * factor, 2)

            # 计算新方案的合价
            processed_df[f'方案{scheme_counter}合价'] = processed_df[column_name] * processed_df['数量']

            # 调整系数以确保总价符合下浮比例要求
            current_total = processed_df[f'方案{scheme_counter}合价'].sum()
            target_total = total_price * reduc
            adjustment_factor = target_total / current_total

            # 应用调整系数
            processed_df[column_name] = (processed_df[column_name] * adjustment_factor).round(2)  # 将方案单价固定为两位小数
            processed_df[f'方案{scheme_counter}合价'] = processed_df[column_name] * processed_df['数量']

            # 增加方案计数器
            scheme_counter += 1

    return processed_df

def simulate_list(input_param):
    # 这里写你的业务逻辑，举例返回模拟数据
    # input_param 可以是字符串、dict等，按你的前端传参格式
    return {
        "list": [
            {"name": "分项1", "price": 1000},
            {"name": "分项2", "price": 2000}
        ],
        "total": 3000
    }

def generate_result_html(processed_data, processed_df):
    """生成结果HTML的辅助函数"""
    # 第一部分: 用户输入参数表格
    result_html = """
        <div class="mt-4">
            <h4>处理参数</h4>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>NUM Value</th>
                        <th>Reduc Value</th>
                        <th>Ranges</th>
                    </tr>
                </thead>
                <tbody>
    """

    for item in processed_data:
        ranges_html = "<ul>"
        for r in item['ranges']:
            ranges_html += f"""
                <li>Start-End: [{r['start']}, {r['end']}],
                    Min-Max: [{r['min']}, {r['max']}]</li>
            """
        ranges_html += "</ul>"

        result_html += f"""
            <tr>
                <td>{item['num']}</td>
                <td>{item['reduc']}</td>
                <td>{ranges_html}</td>
            </tr>
        """

    result_html += """
                </tbody>
            </table>
        </div>
    """

    # 第二部分: 处理后的数据表格
    # 选择要显示的列
    display_columns = []

    # 序号、项目编码、项目名称、单位列
    id_columns = ['序号', '项目编码', '项目名称', '单位']
    # 去除不存在的列
    id_columns = [col for col in id_columns if col in processed_df.columns]

    # 基本列
    base_columns = ['控制价', '数量', '合价', '占比']
    # 去除不存在的列
    base_columns = [col for col in base_columns if col in processed_df.columns]

    # 获取所有方案列（不包含合价列）
    scheme_columns = [col for col in processed_df.columns if col.startswith('方案') and not col.endswith('合价')]

    # 将方案列按照数字大小排序
    scheme_columns.sort(key=lambda x: int(x.replace('方案', '')))

    # 如果有其他列，也显示出来，但排除已经包含的列和合价列
    other_columns = [col for col in processed_df.columns
                    if col not in id_columns + base_columns + scheme_columns
                    and not col.endswith('合价')
                    and not col.startswith('方案')]

    # 按照指定顺序组合列：序号/项目编码/项目名称/单位 -> 控制价/数量/合价/占比 -> 方案列
    display_columns = id_columns + base_columns + other_columns + scheme_columns

    # 选择要显示的列并格式化
    display_df = processed_df[display_columns].copy()

    # 格式化数值列
    for col in display_df.select_dtypes(include=[np.number]).columns:
        if col == '占比':
            # 占比列保留四位小数
            display_df[col] = display_df[col].round(4)
        else:
            # 其他数值列保留两位小数
            display_df[col] = display_df[col].round(2)

    # 添加处理后的数据表格
    result_html += f"""
        <div class="mt-4">
            <h4>处理后的数据</h4>
            {display_df.to_html(classes='table table-striped table-hover')}
        </div>

        <div class="mt-4">
            <h4>总价比较</h4>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>项目</th>
                        <th>金额</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>原始总价</td>
                        <td>{processed_df['合价'].sum():.2f}</td>
                    </tr>
    """

    # 添加每个方案的总价
    # 获取所有方案合价列
    scheme_total_columns = [col for col in processed_df.columns if col.startswith('方案') and col.endswith('合价')]

    # 按照方案编号排序
    scheme_total_columns.sort(key=lambda x: int(x.replace('方案', '').replace('合价', '')))

    # 为每个方案添加总价行
    for column_name in scheme_total_columns:
        # 提取方案编号
        scheme_num = column_name.replace('方案', '').replace('合价', '')

        # 找到对应的reduc值
        # 首先需要确定这个方案属于哪个NUM组
        scheme_int = int(scheme_num)
        reduc = None

        # 计算每个组的方案范围
        start_scheme = 1
        for item in processed_data:
            num_value = int(item['num'])
            end_scheme = start_scheme + num_value - 1

            # 如果当前方案在这个组的范围内，使用这个组的reduc值
            if start_scheme <= scheme_int <= end_scheme:
                reduc = float(item['reduc'])
                break

            # 更新下一组的起始方案编号
            start_scheme = end_scheme + 1

        # 如果找不到对应的reduc值，使用默认值
        if reduc is None:
            reduc = 0.9  # 使用更合理的默认值

        total = processed_df[column_name].sum()
        result_html += f"""
            <tr>
                <td>方案{scheme_num}总价 (下浮{(1-reduc)*100:.0f}%)</td>
                <td>{total:.2f}</td>
            </tr>
        """

    result_html += """
                </tbody>
            </table>
        </div>
    """

    return result_html

def process_excel_file(excel_file, processed_data):
    """
    处理Excel文件，生成处理后的DataFrame和下载文件，返回相关信息
    
    Args:
        excel_file: 上传的Excel文件对象
        processed_data: 处理参数列表
        
    Returns:
        dict: 包含处理结果的字典
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        
        # 处理Excel数据
        processed_df = process_excel_data(df, processed_data)
        
        # 生成结果HTML
        result_html = generate_result_html(processed_data, processed_df)
        
        # 生成文件名并准备保存路径
        # 创建存储目录（如果不存在）
        processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_files')
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
        
        # 生成唯一文件名
        filename = f"{uuid.uuid4().hex}.xlsx"
        file_path = os.path.join(processed_dir, filename)
        
        # 将处理后的数据保存到Excel文件
        # 选择要保存的列，排除合价列
        
        # 序号、项目编码、项目名称、单位列
        id_columns = ['序号', '项目编码', '项目名称', '单位']
        # 去除不存在的列
        id_columns = [col for col in id_columns if col in processed_df.columns]
        
        # 基本列
        base_columns = ['控制价', '数量', '合价', '占比']
        # 去除不存在的列
        base_columns = [col for col in base_columns if col in processed_df.columns]
        
        # 获取所有方案列（不包含合价列）
        scheme_columns = [col for col in processed_df.columns if col.startswith('方案') and not col.endswith('合价')]
        
        # 将方案列按照数字大小排序
        scheme_columns.sort(key=lambda x: int(x.replace('方案', '')))
        
        # 如果有其他列，也显示出来，但排除已经包含的列和合价列
        other_columns = [col for col in processed_df.columns
                        if col not in id_columns + base_columns + scheme_columns
                        and not col.endswith('合价')
                        and not col.startswith('方案')]
        
        # 按照指定顺序组合列：序号/项目编码/项目名称/单位 -> 控制价/数量/合价/占比 -> 方案列
        export_columns = id_columns + base_columns + other_columns + scheme_columns
        
        # 去除不存在的列
        export_columns = [col for col in export_columns if col in processed_df.columns]
        
        # 创建要导出的数据副本
        export_df = processed_df[export_columns].copy()
        
        # 格式化占比列为四位小数
        if '占比' in export_df.columns:
            export_df['占比'] = export_df['占比'].round(4)
        
        # 导出到Excel
        export_df.to_excel(file_path, index=False)
        
        # 相对路径
        relative_path = os.path.join('processed_files', filename)
        
        return {
            'result_html': result_html,
            'processed_df': processed_df,
            'file_path': file_path,
            'relative_path': relative_path,
            'filename': filename,
            'original_filename': excel_file.name
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise ValueError(f'处理Excel文件时出错: {str(e)}')

def list_simulator_from_excel(file, price_groups=None, include_full_data=False):
    """
    将上传的Excel文件按照价格组参数进行模拟计算
    
    Args:
        file: 上传的Excel文件对象
        price_groups: 价格组参数，格式如:
            [
                {
                    'numValue': 5,
                    'reduc': 0.95,
                    'ranges': [
                        {'start': 1, 'end': 10, 'min': 0.8, 'max': 1.2},
                        ...
                    ]
                },
                ...
            ]
        include_full_data: 是否在结果中包含完整的Excel数据
    
    Returns:
        dict: 包含处理后的清单和总价
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file)
        
        # 替换无效值（inf, -inf, NaN）为有效值
        df = df.replace([float('inf'), float('-inf')], 0)
        df = df.fillna(0)  # 替换NaN为0
        
        # 如果没有价格组参数，使用简单处理逻辑
        if not price_groups:
            # 简单示例：假设有"分项名称"和"单价"两列
            if '分项名称' not in df.columns or '单价' not in df.columns:
                raise ValueError('Excel文件缺少"分项名称"或"单价"列')
            result_list = []
            total = 0
            for _, row in df.iterrows():
                name = row['分项名称']
                price = float(row['单价'])
                # 确保价格是有效值
                if not pd.isna(price) and not np.isinf(price):
                    result_list.append({'name': name, 'price': price})
                    total += price
                else:
                    result_list.append({'name': name, 'price': 0})
            return {'list': result_list, 'total': total}
        
        # 使用完整的process_excel_data处理逻辑
        # 转换price_groups格式为process_excel_data需要的格式
        processed_data = []
        for group in price_groups:
            processed_data.append({
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
        
        # 检查必要列
        required_cols = ['控制价', '数量']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            alt_cols = {
                '控制价': ['单价', '价格', 'price'],
                '数量': ['quantity', 'qty']
            }
            # 尝试找替代列
            for missing in missing_cols:
                for alt in alt_cols.get(missing, []):
                    if alt in df.columns:
                        df[missing] = df[alt]
                        break
            
            # 再次检查
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f'Excel文件缺少必要列: {", ".join(missing_cols)}')
        
        # 处理Excel数据
        processed_df = process_excel_data(df, processed_data)
        
        # 清理无效浮点值以避免JSON序列化问题
        processed_df = processed_df.replace([float('inf'), float('-inf')], 0)
        processed_df = processed_df.fillna(0)
        
        # 返回结果数据
        result_list = []
        for idx, row in processed_df.iterrows():
            # 使用最后一个方案的价格
            scheme_cols = [col for col in processed_df.columns if col.startswith('方案') and not col.endswith('合价')]
            if scheme_cols:
                last_scheme = sorted(scheme_cols)[-1]
                name = row.get('项目名称', row.get('分项名称', f'项目 {idx}'))
                try:
                    price = float(row[last_scheme])
                    # 确保价格是有效的JSON值
                    if pd.isna(price) or np.isinf(price):
                        price = 0
                except (ValueError, TypeError):
                    price = 0
                result_list.append({'name': str(name), 'price': price})
        
        # 计算总价
        total_col = f'{last_scheme}合价' if f'{last_scheme}合价' in processed_df.columns else '合价' 
        try:
            total = float(processed_df[total_col].sum()) if total_col in processed_df.columns else sum(item['price'] for item in result_list)
            # 确保总价是有效的JSON值
            if pd.isna(total) or np.isinf(total):
                total = 0
        except (ValueError, TypeError):
            total = 0
        
        result = {
            'list': result_list,
            'total': total,
        }
        
        # 如果需要完整数据，添加到结果中
        if include_full_data:
            # 准备列名和数据
            columns = processed_df.columns.tolist()
            
            # 转换DataFrame为简单的行列列表格式
            data = []
            for _, row in processed_df.iterrows():
                row_data = []
                for col in columns:
                    value = row[col]
                    # 确保所有值都是JSON兼容的
                    if pd.isna(value) or (isinstance(value, float) and np.isinf(value)):
                        value = 0
                    # 转换numpy类型为Python内置类型
                    elif hasattr(value, 'item'):
                        value = value.item()
                    row_data.append(value)
                data.append(row_data)
            
            result['fullExcelData'] = {
                'columns': columns,
                'data': data
            }
            
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise ValueError(f'处理Excel文件失败: {str(e)}')
