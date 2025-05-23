import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def analyze_price_list(file_path):
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path, index_col=None)

        # 计算合价
        df['合价'] = df['数量'] * df['控制价']

        # 计算总价
        total_price = df['合价'].sum()

        # 计算比例
        df['比例'] = df['合价'] / total_price * 100  # 转换为百分比

        # 按比例排序
        df_sorted = df.sort_values('比例', ascending=True)

        # 将数据分成100组
        df_sorted['分组'] = pd.qcut(range(len(df_sorted)), q=100, labels=range(1, 101))

        # 计算每组的平均比例
        group_means = df_sorted.groupby('分组')['比例'].mean().reset_index()

        # 创建折线图
        plt.figure(figsize=(15, 8))
        sns.set_style("whitegrid")

        # 绘制分组后的折线图
        plt.plot(group_means['分组'], group_means['比例'], marker='o', linewidth=2)

        # 设置图表属性
        plt.title('项目比例分布图（分100组）', fontsize=14)
        plt.xlabel('分组', fontsize=12)
        plt.ylabel('平均占比 (%)', fontsize=12)

        # 添加网格线
        plt.grid(True, linestyle='--', alpha=0.7)

        # 保存图表
        plt.tight_layout()
        plt.savefig('价格比例分析_分组.png', dpi=300, bbox_inches='tight')

        # 显示结果
        print("\n数据分析结果:")
        print(f"总价: {total_price:.2f}")
        print("\n分组统计示例（前5组）:")
        print(group_means.head())

        # 保存详细结果到Excel
        df_sorted.to_excel('价格分析结果_排序.xlsx', index=False)

        # 保存分组统计结果
        group_means.to_excel('价格分析结果_分组统计.xlsx', index=False)

        print("\n分析结果已保存到:")
        print("1. '价格分析结果_排序.xlsx' (完整排序数据)")
        print("2. '价格分析结果_分组统计.xlsx' (分组统计结果)")
        print("3. '价格比例分析_分组.png' (分组折线图)")

        return df_sorted, group_means

    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"处理数据时发生错误: {str(e)}")
        return None

if __name__ == '__main__':

    # 使用示例
    file_path = "清单限价.xlsx"
    result_df, group_stats = analyze_price_list(file_path)