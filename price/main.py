from BidOptimizer import BidOptimizer
from BidOptimizerAggressive import BidOptimizerAggressive


other_prices = [0.9971, 0.997, 0.9962, 0.9959, 0.9956, 0.9948, 0.994, 0.9938, 0.9935, 0.9932, 
                0.9928, 0.9921, 0.9916, 0.9916, 0.9913, 0.9909, 0.9906, 0.9903, 0.9898, 0.9896, 
                0.9894, 0.9891, 0.9889, 0.9887, 0.9884, 0.9878, 0.9875, 0.9871, 0.9864, 0.9847, 
                0.9739, 0.9523, 0.9512, 0.944, 0.938, 0.9377, 0.9372, 0.928, 0.9232, 0.9181, 
                0.9092, 0.9, 0.8952, 0.8878, 0.8812]

real_prices = [0.9816, 0.9783, 0.9739]

# Example usage

my_company_count = 5

print("其他公司报价：", other_prices)
print("我公司数量：", my_company_count)
print("真实报价：", real_prices)

# Create an instance of BidOptimizer
optimizer = BidOptimizer(other_prices=other_prices, my_company_count=my_company_count)
my_bids = optimizer.find_optimal_bids()
print("建议报价：", my_bids)

# Create an instance of BidOptimizerAggressive
aggressive_optimizer = BidOptimizerAggressive(other_prices=other_prices, my_company_count=my_company_count)
aggressive_bids = aggressive_optimizer.find_optimal_bids_aggressive()
print("激进报价建议：", aggressive_bids)

