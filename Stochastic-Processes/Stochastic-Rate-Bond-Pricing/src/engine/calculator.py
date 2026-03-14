import numpy as np


class CalculationModel:
    def __init__(self, n=10, T=10, r0=0.05, sigma=0.1):

        # Initialize base parameters for the binomial interest rate model
        self.n = n
        self.T = T
        self.r0 = r0
        self.sigma = sigma
        self.u = np.exp(sigma * T / n)  # Upward movement factor
        self.d = 1 / self.u  # Downward movement factor
        # Risk-neutral transition probability
        self.p = (np.exp(r0 * T / n) - self.d) / (self.u - self.d)
        self.q = 1 - self.p  # Complementary probability

        # Construct the short-rate binomial tree
        self.rate_tree = np.zeros((self.n + 1, self.n + 1))
        for i in range(self.n + 1):
            for j in range(i, self.n + 1):
                self.rate_tree[self.n - i, j] = (
                    self.r0 * (self.u**i) * (self.d ** (j - i))
                )

    def get_zcb_price(self, t=None):
        """
        Calculates the Zero-Coupon Bond (ZCB) price matrix up to time t.

        Args:
            t (int, optional): The maturity of the ZCB. Defaults to n.

        Returns:
            np.ndarray: A binomial tree representing the ZCB prices.
        """

        if t is None:
            t = self.n

        zcb_tree = np.zeros((t + 1, t + 1))
        zcb_tree[:, t] = 100  # Face value at maturity

        for j in range(t - 1, -1, -1):
            for i in range(t - j, t + 1):
                zcb_tree[i, j] = (
                    self.p * zcb_tree[i - 1, j + 1] + self.q * zcb_tree[i, j + 1]
                ) / (1 + self.rate_tree[i + self.n - t, j])

        return zcb_tree

    def get_forward_price(self, t):
        """
        Calculates the forward price on a Zero-Coupon Bond.

        Args:
            t (int): Forward contract execution time.

        Returns:
            float: The calculated forward price.
        """

        # Current price of the underlying ZCB maturing at n (ZCB_10)
        zcb_price_n = self.get_zcb_price()[-1, 0]

        # Current price of the ZCB maturing at the forward execution time t
        zcb_price_k = self.get_zcb_price(t=t)[-1, 0]

        forward_price = zcb_price_n / zcb_price_k * 100

        return forward_price

    def get_futures_price(self, asset_tree, k):
        """
        Calculates the futures price of an asset for a specific expiration time.

        Args:
            asset_tree (np.ndarray): A binomial tree representing the underlying asset's price.
            k (int): Futures expiration time.

        Returns:
            np.ndarray: A binomial tree representing the futures prices.
        """

        futures_price_tree = np.zeros((k + 1, k + 1))
        futures_price_tree[:, k] = asset_tree[-(k + 1) :, k]

        for j in range(k - 1, -1, -1):
            for i in range(k - j, k + 1):
                futures_price_tree[i, j] = (
                    self.p * futures_price_tree[i - 1, j + 1]
                    + self.q * futures_price_tree[i, j + 1]
                )

        return futures_price_tree

    def get_american_option_price(self, asset_tree, k=6, call=True, strike=70):
        """
        Calculates the price of an American-style option on an underlying asset.

        Args:
            asset_tree (np.ndarray): A binomial tree representing the underlying asset's price.
            k (int): Option expiration time.
            call (bool): True for a Call option, False for a Put option.
            strike (float): The strike price as a percentage.

        Returns:
            np.ndarray: A binomial tree representing the American option prices.
        """

        # Calculate intrinsic value at expiration based on option type (Call or Put)
        if call:
            american_option_tree = asset_tree - strike
        else:
            american_option_tree = strike - asset_tree

        american_option_tree[american_option_tree < 0] = 0

        for j in range(k - 1, -1, -1):
            for i in range(k - j, k + 1):
                american_option_tree[i, j] = max(
                    (
                        self.p * american_option_tree[i - 1, j + 1]
                        + self.q * american_option_tree[i, j + 1]
                    )
                    / np.exp(self.r0 * 100 * self.T / k),
                    american_option_tree[i, j],
                )

        return american_option_tree
