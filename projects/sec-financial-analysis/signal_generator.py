import pandas as pd

def generate_signal(features_df):
    """
    Takes the features DataFrame for a company and returns a signal and confidence.
    """
    # Pick the most recent date
    latest = features_df.sort_values("date").iloc[-1]

    rules = {
        "call": 0,
        "put": 0,
        "total": 0
    }

    # Rule 1: Revenue growth
    if pd.notna(latest.get("revenue_growth")):
        rules["total"] += 1
        if latest["revenue_growth"] > 0.10:
            rules["call"] += 1
        elif latest["revenue_growth"] < 0:
            rules["put"] += 1

    # Rule 2: Net income margin
    if pd.notna(latest.get("net_income_margin")):
        rules["total"] += 1
        if latest["net_income_margin"] > 0.05:
            rules["call"] += 1
        elif latest["net_income_margin"] < 0:
            rules["put"] += 1

    # Rule 3: Cash runway
    if pd.notna(latest.get("cash_runway_months")):
        rules["total"] += 1
        if latest["cash_runway_months"] < 6:
            rules["put"] += 1

    # Rule 4: Debt-to-assets
    if pd.notna(latest.get("debt_to_assets")):
        rules["total"] += 1
        if latest["debt_to_assets"] > 0.7:
            rules["put"] += 1

    # Rule 5: Operating cash flow
    if pd.notna(latest.get("operating_cash_flow")):
        rules["total"] += 1
        if latest["operating_cash_flow"] < 0:
            rules["put"] += 1

    # Determine bias
    if rules["call"] > rules["put"]:
        bias = "CALL"
        confidence = rules["call"] / rules["total"]
    elif rules["put"] > rules["call"]:
        bias = "PUT"
        confidence = rules["put"] / rules["total"]
    else:
        bias = "HOLD"
        confidence = 0.5 if rules["total"] > 0 else 0

    return {
        "bias": bias,
        "confidence": round(confidence, 2),
        "date": latest["date"]
    }

if __name__ == "__main__":
    df = pd.read_csv("ingestion/data/processed/features_dataset.csv")
    signal = generate_signal(df)
    print(signal)
