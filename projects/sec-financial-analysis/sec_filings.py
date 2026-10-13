import requests
import pandas as pd
import os

SEC_HEADERS = {
    "User-Agent": "YourName your@email.com"
}

def get_company_facts(cik: str):
    cik = cik.zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(url, headers=SEC_HEADERS)
    response.raise_for_status()
    return response.json()

def extract_financials(facts, key, columns_map):
    """
    facts: SEC JSON
    key: 'Revenues', 'NetIncomeLoss', 'CashAndCashEquivalentsAtCarryingValue', etc.
    columns_map: {'val':'field_name', 'end':'date', 'form':'form'}
    """
    try:
        data = facts["facts"]["us-gaap"][key]["units"]["USD"]
    except KeyError:
        print(f"{key} not found for this company")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    df = df[list(columns_map.keys())]
    df = df.rename(columns=columns_map)
    return df

def save_to_csv(df, filename, folder="ingestion/data/processed"):
    if df.empty:
        return
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        df.to_csv(path, mode='a', index=False, header=False)
    else:
        df.to_csv(path, index=False)
    print(f"Saved {filename} to {folder}")

if __name__ == "__main__":
    cik = "0000909832"  # Apple
    facts = get_company_facts(cik)
    
    # Income Statement
    income_df = extract_financials(
        facts, 
        key="Revenues",
        columns_map={"end":"date", "val":"revenue", "form":"form"}
    )
    net_income_df = extract_financials(
        facts,
        key="NetIncomeLoss",
        columns_map={"end":"date", "val":"net_income", "form":"form"}
    )
    income_df = pd.merge(income_df, net_income_df, on=["date","form"], how="outer")
    save_to_csv(income_df, "income_statement.csv")
    
    # Balance Sheet
    cash_df = extract_financials(
        facts,
        key="CashAndCashEquivalentsAtCarryingValue",
        columns_map={"end":"date", "val":"cash", "form":"form"}
    )
    assets_df = extract_financials(
        facts,
        key="Assets",
        columns_map={"end":"date", "val":"total_assets", "form":"form"}
    )
    liabilities_df = extract_financials(
        facts,
        key="Liabilities",
        columns_map={"end":"date", "val":"total_liabilities", "form":"form"}
    )
    bs_df = cash_df.merge(assets_df, on=["date","form"], how="outer").merge(liabilities_df, on=["date","form"], how="outer")
    save_to_csv(bs_df, "balance_sheet.csv")
    
    # Cash Flow Statement
    ocf_df = extract_financials(
        facts,
        key="NetCashProvidedByUsedInOperatingActivities",
        columns_map={"end":"date", "val":"operating_cash_flow", "form":"form"}
    )
    icf_df = extract_financials(
        facts,
        key="NetCashProvidedByUsedInInvestingActivities",
        columns_map={"end":"date", "val":"investing_cash_flow", "form":"form"}
    )
    fcf_df = extract_financials(
        facts,
        key="NetCashProvidedByUsedInFinancingActivities",
        columns_map={"end":"date", "val":"financing_cash_flow", "form":"form"}
    )
    cf_df = ocf_df.merge(icf_df, on=["date","form"], how="outer").merge(fcf_df, on=["date","form"], how="outer")
    save_to_csv(cf_df, "cash_flow.csv")
