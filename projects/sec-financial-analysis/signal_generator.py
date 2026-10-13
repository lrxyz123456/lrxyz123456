import pandas as pd


def generate_signal(features_df):
    """Generate a simple rules-based directional signal from the latest feature row."""
    latest = features_df.sort_values("date").iloc[-1]

    scores = {"call": 0, "put": 0, "total": 0}

    if pd.notna(latest.get("revenue_growth")):
        scores["total"] += 1
        if latest["revenue_growth"] > 0.10:
            scores["call"] += 1
        elif latest["revenue_growth"] < 0:
            scores["put"] += 1

    if pd.notna(latest.get("net_income_margin")):
        scores["total"] += 1
        if latest["net_income_margin"] > 0.05:
            scores["call"] += 1
        elif latest["net_income_margin"] < 0:
            scores["put"] += 1

    if pd.notna(latest.get("cash_runway_months")):
        scores["total"] += 1
        if latest["cash_runway_months"] < 6:
            scores["put"] += 1

    if pd.notna(latest.get("debt_to_assets")):
        scores["total"] += 1
        if latest["debt_to_assets"] > 0.7:
            scores["put"] += 1

    if pd.notna(latest.get("operating_cash_flow")):
        scores["total"] += 1
        if latest["operating_cash_flow"] < 0:
            scores["put"] += 1

    if scores["call"] > scores["put"]:
        bias = "CALL"
        confidence = scores["call"] / scores["total"]
    elif scores["put"] > scores["call"]:
        bias = "PUT"
        confidence = scores["put"] / scores["total"]
    else:
        bias = "HOLD"
        confidence = 0.5 if scores["total"] > 0 else 0.0

    return {
        "bias": bias,
        "confidence": round(confidence, 2),
        "date": latest["date"],
    }


if __name__ == "__main__":
    features = pd.read_csv("data/processed/features_dataset.csv")
    features["date"] = pd.to_datetime(features["date"])
    print(generate_signal(features))
