import numpy as np

class BidOptimizerAggressive:
    def __init__(self, other_prices, my_company_count):
        self.other_prices = sorted(other_prices)
        self.my_company_count = my_company_count
        self.a_range = list(range(95, 101))  # A in [95, 100]

    def compute_base_price(self, a, my_bids=None):
        """Compute the evaluation base price given A and optional my bids."""
        all_prices = self.other_prices + (my_bids if my_bids else [])
        if len(all_prices) > 5:
            trimmed = sorted(all_prices)[1:-1]  # remove highest and lowest
        else:
            trimmed = all_prices
        average = np.mean(trimmed)
        return average * a / 100

    def score(self, bid, base_price):
        ratio_diff = (bid - base_price) / base_price
        if abs(ratio_diff) < 0.001:
            return 35
        elif bid > base_price:
            return max(0, 35 - ratio_diff / 0.01 * 1)
        else:
            return max(0, 35 - abs(ratio_diff) / 0.01 * 0.5)

    def find_optimal_bids_aggressive(self):
        """Generate x bids using an aggressive strategy."""
        stable_ranges = []

        for a in self.a_range:
            base_price = self.compute_base_price(a)
            # Introduce a more aggressive spread: base_price with ± 1%-2% range
            aggressive_range = (base_price * 0.98, base_price * 1.02)  # Extending range more aggressively
            stable_ranges.append(aggressive_range)

        # Find intersection of all aggressive ranges
        lower = max(r[0] for r in stable_ranges)
        upper = min(r[1] for r in stable_ranges)

        if lower > upper:
            # No stable range found, fallback: use central tendency of each A
            mid_bids = [self.compute_base_price(a) for a in self.a_range]
            lower = min(mid_bids)
            upper = max(mid_bids)
        print(f"lower: {lower:.4f}, upper: {upper:.4f}")

        # More aggressive bid distribution: split x prices across a wider range
        aggressive_bids = np.linspace(lower, upper, self.my_company_count).tolist()

        # Apply more spread by introducing slight randomness into the bid values
        #spread_bids = [bid * (1 + np.random.uniform(-0.01, 0.01)) for bid in aggressive_bids]
        spread_bids = [bid * (1 + np.random.uniform(-0.01, 0.01)) for bid in aggressive_bids]


        # Round the final bid values to 2 decimal places
        rounded_bids = [round(bid, 4) for bid in spread_bids]
        return rounded_bids
