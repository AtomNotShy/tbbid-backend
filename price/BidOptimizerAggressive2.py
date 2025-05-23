import numpy as np

class BidOptimizer:
    def __init__(self, other_prices, my_company_count):
        self.other_prices = sorted(other_prices)
        self.my_company_count = my_company_count
        self.a_range = list(range(95, 101))  # A in [95, 100]

    def compute_base_price(self, a):
        """计算评标基准价"""
        all_prices = self.other_prices
        if len(all_prices) > 5:
            trimmed = sorted(all_prices)[1:-1]  # 去掉最高和最低
        else:
            trimmed = all_prices
        average = np.mean(trimmed)
        return average * a / 100

    def score(self, bid, base_price):
        """计算每个报价的得分"""
        ratio_diff = (bid - base_price) / base_price
        if abs(ratio_diff) < 0.001:
            return 35  # 满分
        elif bid > base_price:
            return max(0, 35 - ratio_diff / 0.01 * 1)  # 超过基准价，每高1%扣1分
        else:
            return max(0, 35 - abs(ratio_diff) / 0.01 * 0.5)  # 低于基准价，每低1%扣0.5分

    def find_optimal_bids(self):
        """生成3个报价，使其有较高概率接近目标得分"""
        stable_ranges = []
        for a in self.a_range:
            base_price = self.compute_base_price(a)
            # 基准价的±2%波动范围，确保报价接近基准价
            aggressive_range = (base_price * 0.98, base_price * 1.02)  # 基准价±2%
            stable_ranges.append(aggressive_range)

        # 获取所有可能的区间并选择合理的区间范围
        lower = max(r[0] for r in stable_ranges)
        upper = min(r[1] for r in stable_ranges)

        if lower > upper:
            # 如果没有稳定的区间，使用每个A下的基准价生成价格
            mid_bids = [self.compute_base_price(a) for a in self.a_range]
            lower = min(mid_bids)
            upper = max(mid_bids)
        print(f"lower: {lower:.4f}, upper: {upper:.4f}")

        # 在范围内生成x个报价，并加入一些波动
        aggressive_bids = np.linspace(lower, upper, self.my_company_count).tolist()

        # 引入一定的随机性，确保报价有波动
        final_bids = [bid * (1 + np.random.uniform(-0.01, 0.01)) for bid in aggressive_bids]

        return final_bids


# 示例：其他公司的报价
other_prices = [
    0.9971, 0.997, 0.9962, 0.9959, 0.9956, 0.9948, 0.994, 0.9938, 0.9935, 0.9932, 
    0.9928, 0.9921, 0.9916, 0.9916, 0.9913, 0.9909, 0.9906, 0.9903, 0.9898, 0.9896, 
    0.9894, 0.9891, 0.9889, 0.9887, 0.9884, 0.9878, 0.9875, 0.9871, 0.9864, 0.9847, 
    0.9739, 0.9523, 0.9512, 0.944, 0.938, 0.9377, 0.9372, 0.928, 0.9232, 0.9181, 
    0.9092, 0.9, 0.8952, 0.8878, 0.8812
]

# 假设你的公司有3个报价
optimizer = BidOptimizer(other_prices, my_company_count=3)
my_bids = optimizer.find_optimal_bids()
print("我的公司报价：", my_bids)
