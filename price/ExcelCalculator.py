import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_price_list(file_path):
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path,index_col=None)

        # 计算合价
        df['合价'] = df['数量'] * df['控制价']

        # 计算总价
        total_price = df['合价'].sum()

        # 计算比例
        df['比例'] = df['合价'] / total_price * 100  # 转换为百分比

        # 创建折线图
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")

        # 绘制折线图
        plt.plot(range(len(df)), df['比例'], marker='o')

        # 设置图表属性
        plt.title('price')
        plt.xlabel('label')
        plt.ylabel('part(%)')

        # 旋转x轴标签，防止重叠
        plt.xticks(rotation=45)

        # 添加网格线
        plt.grid(True, linestyle='--', alpha=0.7)

        # 保存图表
        plt.tight_layout()
        plt.savefig('价格比例分析.png')

        # 显示结果
        print("\n数据分析结果:")
        print(f"总价: {total_price:.2f}")
        print("\n前5行数据示例:")
        print(df[['数量', '控制价', '合价', '比例']].head())

        return df

    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"处理数据时发生错误: {str(e)}")
        return None

if __name__ == '__main__':

    # 使用示例
    file_path = "清单限价.xlsx"
    result_df = analyze_price_list(file_path)

    if result_df is not None:
        # 将结果保存到新的Excel文件
        result_df.to_excel('价格分析结果.xlsx', index=False)
        print("\n分析结果已保存到 '价格分析结果.xlsx'")
        print("折线图已保存为 '价格比例分析.png'")