import pandas as pd
import numpy as np

def optimal_bid(n, x, competitor_prices, num_simulations=10000):
    """
    计算最优投标报价
    :param n: 总投标公司数量
    :param x: 已知竞争对手数量
    :param competitor_prices: 已知的x家报价列表(列表长度必须等于x)
    :param num_simulations: 蒙特卡洛模拟次数,默认10000次
    :return: 最优报价，最高期望得分
    """
    # 生成候选报价范围（基于已知报价的80%~120%区间，步长0.1%）
    min_price = min(competitor_prices)
    max_price = max(competitor_prices)
    price_range = max_price - min_price
    q_candidates = np.linspace(min_price*0.8, max_price*1.2, 10000)
    
    best_q = None
    best_score = -np.inf

    # 蒙特卡洛模拟A值
    A_values = [100, 99, 98, 97, 96, 95]  # 直接使用5个A值
    for q in q_candidates:
        total_scores = []
        for A in A_values:
            # 构造完整报价列表
            controlled_prices = [q] * (n - x)
            all_prices = np.concatenate([competitor_prices, controlled_prices])
            
            # 计算基准价
            if len(all_prices) > 5:
                sorted_prices = np.sort(all_prices)
                trimmed = sorted_prices[1:-1]  # 去掉最高最低
                avg = np.mean(trimmed)
            else:
                avg = np.mean(all_prices)
                
            benchmark = avg * A / 100  # 基准价计算

            # 计算当前报价得分
            if q > benchmark:
                deviation = (q - benchmark) / benchmark
                score = 35 - deviation * 100 * 1
            else:
                deviation = (benchmark - q) / benchmark
                score = 35 - deviation * 100 * 0.5
                
            score = np.clip(score, 0, 35)  # 确保在0-35分之间
            total_scores.append(score)
        
        # 计算期望得分
        expected_score = np.mean(total_scores)
        if expected_score > best_score:
            best_score = expected_score
            best_q = q
            
    return best_q, best_score


sorted_prices = np.sort(np.random.normal(loc=96.84, scale=0.01, size=5))

def generate_quote_matrix_v2(n, x, competitor_prices, optimal_price):
    """
    生成差异化受控报价的投标矩阵
    :param n: 总投标公司数
    :param x: 已知竞争对手数
    :param competitor_prices: 已知报价列表
    :param optimal_price: 算法计算基准价
    :return: 报价矩阵，差异化报价列表
    """
    # 生成受控报价
    controlled_num = n - x
    variations = np.random.uniform(-0.02, 0.02, controlled_num)  # 生成±2%的随机波动
    controlled_prices = [optimal_price * (1 + var) for var in variations]
    # controlled_prices = np.random.normal(loc=optimal_price, scale=0.02, size=controlled_num).tolist()  # 正态分布生成报价
    # 强制差异化（确保最小1%差异）
    for i in range(1, controlled_num):
        min_diff = 0.01 * optimal_price # 最小差异1%
        while abs(controlled_prices[i] - controlled_prices[i-1]) < min_diff:
            controlled_prices[i] += np.random.choice([-1,1]) * min_diff * 0.5
    
    # 构建完整矩阵
    all_prices = competitor_prices + controlled_prices
    df = pd.DataFrame({
        '投标公司': [f'公司{i+1}' for i in range(controlled_num)],
        '报价(万元)': controlled_prices,
        '报价类型': ['受控报价']*(controlled_num)
    }).sort_values('报价(万元)')
    
    # 计算动态基准价
    benchmark = np.mean(sorted(all_prices)[1:-1]) if n>5 else np.mean(all_prices)
    A = np.random.uniform(0.95, 1)  # A值随机因子
    benchmark *= A
    
    return df.round(2), benchmark.round(2), A

# 示例使用（网页1的案例数据）
if __name__ == "__main__":
    
    # 输入参数
    other_prices = [0.9971, 0.997, 0.9962, 0.9959, 0.9956, 0.9948, 0.994, 0.9938, 0.9935, 0.9932, 
                0.9928, 0.9921, 0.9916, 0.9916, 0.9913, 0.9909, 0.9906, 0.9903, 0.9898, 0.9896, 
                0.9894, 0.9891, 0.9889, 0.9887, 0.9884, 0.9878, 0.9875, 0.9871, 0.9864, 0.9847, 
                0.9739, 0.9523, 0.9512, 0.944, 0.938, 0.9377, 0.9372, 0.928, 0.9232, 0.9181, 
                0.9092, 0.9, 0.8952, 0.8878, 0.8812]
    competitor_quotes = []  # 已知报价
    known_competitors = len(other_prices)
    for i in other_prices:
        competitor_quotes.append(i*100)
        
    total_bidders = 3 + known_competitors # 总投标公司数
    
    optimal_price, score = optimal_bid(total_bidders, known_competitors, competitor_quotes, num_simulations=1000)
    print(f"最优报价：{optimal_price:.2f}万元，预计得分：{score:.2f}")

    # 生成报价矩阵
    matrix, benchmark, A = generate_quote_matrix_v2(
        n=total_bidders,
        x=known_competitors,
        competitor_prices=competitor_quotes,
        optimal_price=optimal_price
    )
    
    print("差异化报价矩阵：")
    print(matrix)
    print(f"\n智能基准价：{benchmark}万元, 随机值A：{A:.2f}")