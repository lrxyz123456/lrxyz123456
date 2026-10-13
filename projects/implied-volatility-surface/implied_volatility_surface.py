import matplotlib.pyplot as plt
import numpy as np


strike_prices = np.array([70, 80, 90, 95, 100, 105, 110, 120, 130])
expiration_days = np.array([7, 30, 90, 180])

implied_volatility = np.array(
    [
        [55, 48, 42, 36, 32, 34, 38, 45, 52],
        [38, 32, 27, 23, 20, 21, 23, 28, 35],
        [32, 28, 25, 22, 19, 20, 22, 25, 29],
        [28, 25, 23, 21, 19, 19.5, 21, 23, 26],
    ]
)

strike_grid, expiration_grid = np.meshgrid(strike_prices, expiration_days)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

surface = ax.plot_surface(
    strike_grid,
    expiration_grid / 365,
    implied_volatility,
    cmap="viridis",
    edgecolor="none",
    alpha=0.9,
)

atm_index = int(np.where(strike_prices == 100)[0][0])
atm_iv = implied_volatility[:, atm_index]
ax.plot(
    [100] * len(expiration_days),
    expiration_days / 365,
    atm_iv,
    linewidth=3,
    linestyle="--",
    label="ATM IV",
)

ax.set_xlabel("Strike Price")
ax.set_ylabel("Time to Expiration (years)")
ax.set_zlabel("Implied Volatility (%)")
ax.set_title("Implied Volatility Surface")

fig.colorbar(surface, shrink=0.6, aspect=10)
ax.view_init(elev=25, azim=135)
ax.legend()

plt.show()
