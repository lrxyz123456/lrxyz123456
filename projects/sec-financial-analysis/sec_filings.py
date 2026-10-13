import os

import pandas as pd
import requests


SEC_HEADERS = {
    "User-Agent": os.getenv("SEC_USER_AGENT", "Your Name your.email@example.com")
}


def get_company_facts(cik: str):
    cik = cik.zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(url, headers=SEC_HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_financials(facts, key, columns_map):
    try:
        data = facts["facts"]["us-gaap"][key]["units"]["USD"]
    except KeyError:
        print(f"{key} not found for this company")
        return pd.DataFrame()

    frame = pd.DataFrame(data)
    frame = frame[list(columns_map.keys())]
    return frame.rename(columns=columns_map)


def save_to_csv(frame, filename, folder="data/processed"):
    if frame.empty:
        return

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    frame.to_csv(path, index=False)
    print(f"Saved {filename} to {folder}")


def build_statements(cik="0000320193"):
    """Download selected company facts. Default CIK is Apple Inc."""
    facts = get_company_facts(cik)

    revenue = extract_financials(
        facts,
        key="Revenues",
        columns_map={"end": "date", "val": "revenue", "form": "form"},
    )
    net_income = extract_financials(
        facts,
        key="NetIncomeLoss",
        columns_map={"end": "date", "val": "net_income", "form": "form"},
    )
    income = pd.merge(revenue, net_income, on=["date", "form"], how="outer")

    cash = extract_financials(
        facts,
        key="CashAndCashEquivalentsAtCarryingValue",
        columns_map={"end": "date", "val": "cash", "form": "form"},
    )
    assets = extract_financials(
        facts,
        key="Assets",
        columns_map={"end": "date", "val": "total_assets", "form": "form"},
    )
    liabilities = extract_financials(
        facts,
        key="Liabilities",
        columns_map={"end": "date", "val": "total_liabilities", "form": "form"},
    )
    balance_sheet = cash.merge(assets, on=["date", "form"], how="outer").merge(
        liabilities, on=["date", "form"], how="outer"
    )

    operating_cf = extract_financials(
        facts,
        key="NetCashProvidedByUsedInOperatingActivities",
        columns_map={"end": "date", "val": "operating_cash_flow", "form": "form"},
    )
    investing_cf = extract_financials(
        facts,
        key="NetCashProvidedByUsedInInvestingActivities",
        columns_map={"end": "date", "val": "investing_cash_flow", "form": "form"},
    )
    financing_cf = extract_financials(
        facts,
        key="NetCashProvidedByUsedInFinancingActivities",
        columns_map={"end": "date", "val": "financing_cash_flow", "form": "form"},
    )
    cash_flow = operating_cf.merge(investing_cf, on=["date", "form"], how="outer").merge(
        financing_cf, on=["date", "form"], how="outer"
    )

    save_to_csv(income, "income_statement.csv")
    save_to_csv(balance_sheet, "balance_sheet.csv")
    save_to_csv(cash_flow, "cash_flow.csv")


if __name__ == "__main__":
    build_statements()
