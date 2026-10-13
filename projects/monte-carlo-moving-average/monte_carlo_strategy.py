import random
from collections import deque

import matplotlib.pyplot as plt


def run_strategy(days=1000, window=3, start_price=100, mu=0.0, sigma=0.02):
    """Run one moving-average strategy simulation on a synthetic price path."""
    prices = [start_price]
    cash = 0.0
    position = 0
    buy_price = 0.0

    buy_days, buy_prices = [], []
    sell_days, sell_prices = [], []

    for _ in range(days - 1):
        move = random.gauss(mu, sigma)
        prices.append(prices[-1] * (1 + move))

    moving_window = deque(prices[:window], maxlen=window)

    for day in range(window, len(prices)):
        average = sum(moving_window) / window
        price = prices[day]

        if price > average and position == 0:
            position = 1
            buy_price = price
            buy_days.append(day)
            buy_prices.append(price)

        elif price < average and position == 1:
            position = 0
            cash += price - buy_price
            sell_days.append(day)
            sell_prices.append(price)
            buy_price = 0.0

        moving_window.append(price)

    if position == 1:
        cash += prices[-1] - buy_price
        sell_days.append(len(prices) - 1)
        sell_prices.append(prices[-1])

    return {
        "prices": prices,
        "buy_days": buy_days,
        "buy_prices": buy_prices,
        "sell_days": sell_days,
        "sell_prices": sell_prices,
        "pnl": cash,
    }


def monte_carlo_simulation(num_runs=1000, days=1000, window=3):
    results = [run_strategy(days=days, window=window) for _ in range(num_runs)]
    return results


def plot_results(results, sample_paths=50):
    pnls = [result["pnl"] for result in results]
    example = results[0]

    fig, axes = plt.subplots(4, 1, figsize=(12, 14))

    for result in results[:sample_paths]:
        axes[0].plot(result["prices"], alpha=0.15)
    axes[0].set_title(f"Monte Carlo Price Paths (sample {min(sample_paths, len(results))})")
    axes[0].set_xlabel("Days")
    axes[0].set_ylabel("Price")

    axes[1].plot(example["prices"])
    axes[1].scatter(example["buy_days"], example["buy_prices"], marker="^", s=40, label="Buy")
    axes[1].scatter(example["sell_days"], example["sell_prices"], marker="v", s=40, label="Sell")
    axes[1].set_title("Example Simulation with Trades")
    axes[1].set_xlabel("Days")
    axes[1].set_ylabel("Price")
    axes[1].legend()

    axes[2].hist(pnls, bins=50)
    axes[2].set_title("Distribution of Total PnL")
    axes[2].set_xlabel("Total PnL")
    axes[2].set_ylabel("Frequency")

    mean_pnl = sum(pnls) / len(pnls)
    profitable_runs = sum(pnl > 0 for pnl in pnls)
    profit_rate = profitable_runs / len(pnls)

    axes[3].axis("off")
    axes[3].text(
        0.5,
        0.5,
        (
            f"Monte Carlo Runs: {len(results)}\n"
            f"Mean PnL: {mean_pnl:.2f}\n"
            f"Profitable Runs: {profitable_runs}\n"
            f"Profit Rate: {profit_rate * 100:.2f}%"
        ),
        ha="center",
        va="center",
        fontsize=12,
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    simulations = monte_carlo_simulation(num_runs=1000)
    plot_results(simulations)
