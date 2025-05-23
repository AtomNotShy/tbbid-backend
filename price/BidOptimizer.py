class BidOptimizer:
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
        average = sum(trimmed) / len(trimmed)
        return average * a / 100

    def score(self, bid, base_price):
        ratio_diff = (bid - base_price) / base_price
        if abs(ratio_diff) < 0.001:
            return 35
        elif bid > base_price:
            return max(0, 35 - ratio_diff / 0.01 * 1)
        else:
            return max(0, 35 - abs(ratio_diff) / 0.01 * 0.5)

    def find_optimal_bids(self):
        """Generate x bids that have the best chance to score 35 across A=95~100."""
        stable_ranges = []

        for a in self.a_range:
            base_price = self.compute_base_price(a)
            best_bid = base_price
            # Add a small ±0.05% tolerance to account for floating point rounding
            stable_ranges.append((best_bid * 0.9995, best_bid * 1.0005))

        # Find intersection of all stable ranges
        lower = max(r[0] for r in stable_ranges)
        upper = min(r[1] for r in stable_ranges)

        if lower > upper:
            # No stable range found, fallback: use center ranges of each A
            mid_bids = [self.compute_base_price(a) for a in self.a_range]
            lower = min(mid_bids)
            upper = max(mid_bids)
        print(f"lower: {lower:.4f}, upper: {upper:.4f}")

        # Spread x prices evenly within [lower, upper]
        step = (upper - lower) / (self.my_company_count - 1) if self.my_company_count > 1 else 1
        bids = [round(lower + i * step, 4) for i in range(self.my_company_count)]
        return bids
