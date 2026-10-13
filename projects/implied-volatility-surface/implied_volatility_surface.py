import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

strike_prices = [70, 80, 90, 95, 100, 105, 110, 120, 130]
exp_dates = np.array([7, 30, 90, 180])

IV = [
    [55, 48, 42, 36, 32, 34, 38, 45, 52],
    [38, 32, 27, 23, 20, 21, 23, 28, 35],
    [32, 28, 25, 22, 19, 20, 22, 25, 29],
    [28, 25, 23, 21, 19, 19.5, 21, 23, 26]
]

strikes_grid, exp_grid = np.meshgrid(strike_prices, exp_dates)
iv_grid = np.array(IV)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    strikes_grid,
    exp_grid / 365,
    iv_grid,
    cmap='viridis',
    edgecolor='none',
    alpha=0.9
)

# ATM line
atm_iv = iv_grid[:, 6]
ax.plot(
    [100] * len(exp_dates),
    exp_dates / 365,
    atm_iv,
    color='red', alpha=1, linewidth=3, linestyle='--', label='ATM IV'
)

ax.set_xlabel('Strike Price')
ax.set_ylabel('Time to Expiration (years)')
ax.set_zlabel('Implied Volatility (%)')
ax.set_title('Implied Volatility Surface')

fig.colorbar(surf, shrink=0.6, aspect=10)
ax.view_init(elev=25, azim=135)
ax.legend()

plt.show()