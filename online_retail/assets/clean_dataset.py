from dagster import AssetExecutionContext, asset
import pandas as pd


@asset(
    description="Clean dataset for online retail transactions",
    group_name="Preprocessing",
)
def clean_data(context: AssetExecutionContext, load_data: pd.DataFrame):
    clean_df = load_data.copy()
    context.log.info("Dataset before cleaning: %s", clean_df.shape)

    # Clean by InvoiceNo
    clean_df = clean_df[clean_df["InvoiceNo"].str.match(r"^\d{6}$")]

    # Clean by StockCode
    stockcode_mask = clean_df["StockCode"].str.match(r"^\d{5}[a-zA-Z]*$") | clean_df[
        "StockCode"
    ].isin(["PADS"])
    clean_df = clean_df[stockcode_mask]

    # Clean by CustomerId
    clean_df = clean_df[clean_df["CustomerID"].notna()]

    # Clean by UnitPrice
    clean_df = clean_df[clean_df["UnitPrice"] > 0]

    # Clean by Canceled Invoices
    canceled_invoices = get_canceled_invoices(clean_df)
    clean_df = clean_df[~clean_df["InvoiceNo"].isin(canceled_invoices)]

    context.log.info("Dataset after cleaning: %s", clean_df.shape)

    return clean_df


def get_canceled_invoices(df: pd.DataFrame) -> list[str]:
    sales = df[df["Quantity"] > 0].copy()
    returns = df[df["Quantity"] < 0].copy()

    returns["InvoiceNo_clean"] = returns["InvoiceNo"].str.replace("C", "", n=1)
    returns["OriginalQuantity"] = -returns["Quantity"]

    matches = pd.merge(
        sales,
        returns,
        left_on=["CustomerID", "StockCode", "Quantity", "UnitPrice"],
        right_on=["CustomerID", "StockCode", "OriginalQuantity", "UnitPrice"],
        suffixes=("_sale", "_return"),
    )

    matches = matches[
        matches["InvoiceDate_sale"] < matches["InvoiceDate_return"]
    ].copy()

    matches = matches.sort_values(by=["InvoiceDate_return", "InvoiceNo_return"])
    unique_matches = matches.groupby("InvoiceNo_return").first().reset_index()

    return (
        pd.concat(
            [unique_matches["InvoiceNo_return"], unique_matches["InvoiceNo_sale"]]
        )
        .unique()
        .tolist()
    )
