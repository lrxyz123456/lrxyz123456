import random
import matplotlib.pyplot as plt

num_of_runs = 100

# STRATEGY SIM
def run_strategy(
    days = 100,
    window = 3,
    start_price = 100,
    mu = -0.00,
    sigma = 0.02,
):
    prices = [start_price]
    cash = 0
    position = 0
    buy_price = 0
    sell_price = 0

    buy_day = []
    buy_price_list = []
    sell_day = []
    sell_price_list = []

    for i in range(days-1):
        x = random.gauss(mu, sigma)
        new_price = prices[-1]*(1+x)
        prices.append(new_price)

    for i in range(len(prices)):
        if i < window - 1:
            continue
        avg = sum(prices[i-window+1 : i+1])/window
        # BUY SIGNAL
        if prices[i] > avg and position == 0:
            position = 1
            buy_price = prices[i]
            buy_price_list.append(prices[i])
            buy_day.append(i)
        # SELL SIGNAL
        elif prices[i] < avg and position == 1:
            position = 0
            sell_price = prices[i]
            cash += sell_price - buy_price
            sell_day.append(i)
            sell_price_list.append(prices[i])
            buy_price = 0


    return buy_price_list, sell_price_list, buy_day, sell_day, prices, cash

# MONTE CARLO DISTRIBUTION
all_pnls = []
all_prices = []

all_buy_days = []
all_buy_prices = []
all_sell_days = []
all_sell_prices = []

BnS_example = None

for i in  range(num_of_runs):
    buy_price_list, sell_price_list, buy_day, sell_day, prices, cash = run_strategy()
    all_pnls.append(cash)
    all_prices.append(prices)
    if i == 0:
        BnS_example = prices
        all_buy_days = buy_day
        all_sell_days = sell_day
        all_buy_prices = buy_price_list
        all_sell_prices = sell_price_list

fig, axs = plt.subplots(4, 1, figsize=(10, 12))

# MONTE CARLO
for path in all_prices:
    axs[0].plot(path, alpha=0.5)

axs[0].set_title("Monte Carlo Price Paths")
axs[0].set_xlabel("DAYS")
axs[0].set_ylabel("PRICE")

# EXAMPLE BnS
axs[1].plot(BnS_example)
axs[1].set_title("Example Simulation")
axs[1].set_xlabel("DAYS")
axs[1].set_ylabel("PRICE")
axs[1].scatter(all_buy_days, all_buy_prices, color='green', marker='^', s=25, label='Buy')
axs[1].scatter(all_sell_days, all_sell_prices, color='red', marker='v', s=25, label='Sell')

# HISTOGRAM
axs[2].hist(all_pnls, bins=50)
axs[2].set_title("PnL")
axs[2].set_xlabel("PnL")
axs[2].set_ylabel("Frequency")

profitable_runs = len([p for p in all_pnls if p > 0])
profit_rate = profitable_runs / len(all_pnls)
mean_pnl = sum(all_pnls) / len(all_pnls)


# TEXT
axs[3].axis("off")
axs[3].text(
    0.5, 0.5,
    f"Runs: {num_of_runs}\nMean PnL: {round(mean_pnl, 2)}\nProfitable Runs: {profitable_runs}\nProfit Rate: {round(profit_rate*100, 2)}",
    ha = "center",
    va = "center",
    fontsize=12
)
plt.tight_layout()
plt.legend()
plt.show()