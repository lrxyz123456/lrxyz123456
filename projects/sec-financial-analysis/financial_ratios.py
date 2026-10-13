import os

import pandas as pd


def load_csv(folder="data/processed"):
    files = {
        "income": "income_statement.csv",
        "balance_sheet": "balance_sheet.csv",
        "cash_flow": "cash_flow.csv",
    }

    data = {}
    for key, filename in files.items():
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist")

        frame = pd.read_csv(path)
        frame = frame.loc[:, ~frame.columns.duplicated()]
        frame["date"] = pd.to_datetime(frame["date"])

        for column in frame.columns:
            if column not in {"date", "form"}:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")

        frame = frame.drop_duplicates(subset="date")
        data[key] = frame

    return data["income"], data["balance_sheet"], data["cash_flow"]


def compute_ratios(income, balance_sheet, cash_flow):
    income = income.sort_values("date").copy()
    balance_sheet = balance_sheet.sort_values("date").copy()
    cash_flow = cash_flow.sort_values("date").copy()

    if {"revenue"}.issubset(income.columns):
        income["revenue_growth"] = income["revenue"].pct_change(fill_method=None)
    else:
        income["revenue_growth"] = pd.NA

    if {"net_income", "revenue"}.issubset(income.columns):
        income["net_income_margin"] = income["net_income"] / income["revenue"]
    else:
        income["net_income_margin"] = pd.NA

    if {"total_liabilities", "total_assets"}.issubset(balance_sheet.columns):
        balance_sheet["debt_to_assets"] = (
            balance_sheet["total_liabilities"] / balance_sheet["total_assets"]
        )
    else:
        balance_sheet["debt_to_assets"] = pd.NA

    merged_cash = cash_flow.merge(
        balance_sheet[["date", "cash"]].rename(columns={"cash": "balance_sheet_cash"}),
        on="date",
        how="left",
    )
    merged_cash["cash_runway_months"] = (
        merged_cash["balance_sheet_cash"]
        / merged_cash["operating_cash_flow"].abs()
        * 12
    )

    features = income.merge(
        balance_sheet[
            ["date", "cash", "total_assets", "total_liabilities", "debt_to_assets"]
        ],
        on="date",
        how="outer",
    )
    features = features.merge(
        cash_flow[
            ["date", "operating_cash_flow", "investing_cash_flow", "financing_cash_flow"]
        ],
        on="date",
        how="outer",
    )
    features = features.merge(
        merged_cash[["date", "cash_runway_months"]],
        on="date",
        how="left",
    )

    return features.sort_values("date").reset_index(drop=True)


def save_features(frame, filename="features_dataset.csv", folder="data/processed"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    frame.to_csv(path, index=False)
    print(f"Saved features dataset to {path}")


if __name__ == "__main__":
    income_df, balance_sheet_df, cash_flow_df = load_csv()
    features_df = compute_ratios(income_df, balance_sheet_df, cash_flow_df)
    save_features(features_df)
    print(features_df.tail())
