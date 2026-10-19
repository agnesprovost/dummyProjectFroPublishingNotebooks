import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from market_demo import estimate_parameters, generate_prices, log_returns, simulate_gbm


class MarketDemoTests(unittest.TestCase):
    def test_price_generation_is_reproducible_and_includes_initial_price(self):
        first = generate_prices(n_days=20, seed=123)
        second = generate_prices(n_days=20, seed=123)
        self.assertTrue(first.equals(second))
        self.assertEqual(len(first), 21)
        self.assertEqual(first.iloc[0], 100.0)
        self.assertTrue((first > 0).all())

    def test_returns_and_parameter_estimates_are_finite(self):
        returns = log_returns(generate_prices(n_days=100, seed=3))
        self.assertEqual(len(returns), 100)
        estimates = estimate_parameters(returns)
        self.assertTrue(np.isfinite(list(estimates.values())).all())
        self.assertGreaterEqual(estimates["volatility"], 0)

    def test_simulation_shape_and_starting_price(self):
        paths = simulate_gbm(50.0, n_days=12, drift=0.03, volatility=0.2, n_paths=8, seed=5)
        self.assertEqual(paths.shape, (13, 8))
        self.assertTrue(np.all(paths.iloc[0].to_numpy() == 50.0))
        self.assertTrue(np.isfinite(paths.to_numpy()).all())

    def test_rejects_invalid_prices_and_parameters(self):
        with self.assertRaises(ValueError):
            generate_prices(initial_price=0)
        with self.assertRaises(ValueError):
            log_returns(generate_prices(n_days=5) * 0)
        with self.assertRaises(ValueError):
            log_returns(pd.Series([100.0, np.inf]))
        with self.assertRaises(ValueError):
            estimate_parameters(pd.Series([0.1]))
        with self.assertRaises(ValueError):
            simulate_gbm(100, n_days=0, drift=0.05, volatility=0.2)


if __name__ == "__main__":
    unittest.main()
