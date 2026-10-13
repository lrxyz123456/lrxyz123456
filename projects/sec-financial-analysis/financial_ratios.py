import pandas as pd
import os

def load_csv(folder="ingestion/data/processed", nrows=None, chunked=False, chunksize=100_000):
    """
    Loads processed CSV files into DataFrames safely.
    Supports chunked loading for large files.
    """
    files = {
        "income": "income_statement.csv",
        "bs": "balance_sheet.csv",
        "cf": "cash_flow.csv"
    }

    dfs = {}
    for key, file in files.items():
        path = os.path.join(folder, file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist")

        if chunked:
            chunks = []
            for chunk in pd.read_csv(path, chunksize=chunksize, nrows=nrows):
                # Remove duplicate columns
                chunk = chunk.loc[:, ~chunk.columns.duplicated()]
                # Convert numeric columns
                for col in chunk.columns:
                    if col not in ["date", "form"]:
                        chunk[col] = pd.to_numeric(chunk[col], errors="coerce")
                # Convert date
                chunk["date"] = pd.to_datetime(chunk["date"])
                chunks.append(chunk)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(path, nrows=nrows)
            df = df.loc[:, ~df.columns.duplicated()]
            for col in df.columns:
                if col not in ["date", "form"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            df["date"] = pd.to_datetime(df["date"])

        # Ensure date is unique for safe merging
        df = df.drop_duplicates(subset="date")
        dfs[key] = df

    return dfs["income"], dfs["bs"], dfs["cf"]

def compute_ratios(income, bs, cf):
    """
    Computes financial ratios and merges data safely.
    """
    # Sort by date
    income = income.sort_values("date")
    bs = bs.sort_values("date")
    cf = cf.sort_values("date")

    # Revenue growth
    if "revenue" in income.columns:
        income["revenue_growth"] = income["revenue"].pct_change(fill_method=None)
    else:
        income["revenue_growth"] = pd.NA

    # Net income margin
    if "net_income" in income.columns and "revenue" in income.columns:
        income["net_income_margin"] = income["net_income"] / income["revenue"]
    else:
        income["net_income_margin"] = pd.NA

    # Debt to assets
    if "total_liabilities" in bs.columns and "total_assets" in bs.columns:
        bs["debt_to_assets"] = bs["total_liabilities"] / bs["total_assets"]
    else:
        bs["debt_to_assets"] = pd.NA

    # Cash runway (cash / |operating cash flow| * 12)
    cf_cols = ["date", "operating_cash_flow"]
    if "cash" in bs.columns:
        cf_merged = cf.merge(bs[["date", "cash"]].drop_duplicates("date").rename(columns={"cash": "bs_cash"}), 
                             on="date", how="left")
        cf_merged["cash_runway_months"] = cf_merged["bs_cash"] / cf_merged["operating_cash_flow"].abs() * 12
    else:
        cf_merged = cf.copy()
        cf_merged["cash_runway_months"] = pd.NA

    # Merge safely with selected columns only
    df = income.merge(
        bs[["date", "cash", "total_assets", "total_liabilities", "debt_to_assets"]].drop_duplicates("date"),
        on="date", how="outer"
    )
    df = df.merge(
        cf[["date", "operating_cash_flow", "investing_cash_flow", "financing_cash_flow"]].drop_duplicates("date"),
        on="date", how="outer"
    )
    df = df.merge(
        cf_merged[["date", "cash_runway_months"]].drop_duplicates("date"),
        on="date", how="left"
    )

    # Final sorting
    df = df.sort_values("date").reset_index(drop=True)

    return df

def save_features(df, filename="features_dataset.csv", folder="ingestion/data/processed"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
    print(f"Saved features dataset to {path}")

if __name__ == "__main__":
    # Load CSVs (use chunked=True if files are huge)
    income, bs, cf = load_csv(chunked=False)  # set chunked=True for large datasets

    # Compute ratios safely
    features_df = compute_ratios(income, bs, cf)

    # Save final features
    save_features(features_df)

    # Display last few rows
    print(features_df.tail())
