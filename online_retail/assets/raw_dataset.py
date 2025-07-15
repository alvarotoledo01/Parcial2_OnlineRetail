import os
from pathlib import Path
from dagster import AssetExecutionContext, asset
import pandas as pd


@asset(
    description="Raw dataset for online retail transactions",
    group_name="Ingestion",
)
def load_data(context: AssetExecutionContext):
    # Load the online retail dataset
    data_path = Path(__file__).joinpath("../../../data/Online Retail.xlsx").resolve()
    df = pd.read_excel(data_path, sheet_name=0)
    context.log.info("Loaded online retail dataset with shape: %s", df.shape)

    # Convert some columns to strings
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)

    return df
