import numpy as np
from django.shortcuts import render
from price.BidOptimizer import BidOptimizer


def bid_optimizer(request):
    """投标优化器页面视图"""
    if request.method == 'POST':
        min_values = request.POST.getlist('min[]')
        max_values = request.POST.getlist('max[]')
        num_values = request.POST.getlist('num[]')
        m_value = int(request.POST.get('m_value'))
        
        # 处理输入列表
        input_lists = []
        for min_val, max_val, num_val in zip(min_values, max_values, num_values):
            random_floats = np.random.uniform(
                low=float(min_val), 
                high=float(max_val), 
                size=int(num_val)
            ).tolist()
            input_lists += np.round(random_floats, 4).tolist()
        
        # 排序
        sorted(input_lists)
        
        # 计算推荐投标价
        optimizer = BidOptimizer(other_prices=input_lists, my_company_count=m_value)
        my_bids = optimizer.find_optimal_bids()

        return render(request, 'bidapp/bid_optimizer.html', {
            'result': {
                'recommended_bid': my_bids,
                'input_lists': input_lists,
                'm_value': m_value
            }
        })

    return render(request, 'bidapp/bid_optimizer.html')
