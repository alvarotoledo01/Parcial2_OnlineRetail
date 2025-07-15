from dagster import AssetExecutionContext, asset
import pandas as pd
from sklearn.preprocessing import StandardScaler


@asset(
    description="Create features for online retail transactions",
    group_name="Feature_Engineering",
)
def create_features(
    context: AssetExecutionContext, clean_data: pd.DataFrame
) -> pd.DataFrame:
    df = clean_data.copy()

    # Crear columna 'Total'
    df["Total"] = df["Quantity"] * df["UnitPrice"]

    # Agrupar por CustomerID y calcular RFM
    aggregated_df = df.groupby(by="CustomerID", as_index=False).agg(
        Monetary=("Total", "sum"),
        Frequency=("InvoiceNo", "nunique"),
        LastInvoiceDate=("InvoiceDate", "max"),
    )

    # Convertir a datetime y calcular 'Recency'
    aggregated_df["LastInvoiceDate"] = pd.to_datetime(aggregated_df["LastInvoiceDate"])
    max_date = aggregated_df["LastInvoiceDate"].max()
    aggregated_df["Recency"] = (max_date - aggregated_df["LastInvoiceDate"]).dt.days

    # Filtrar outliers (por arriba) usando regla de Tukey
    monetary_threshold = get_outlier_thresholds(aggregated_df["Monetary"])
    frequency_threshold = get_outlier_thresholds(aggregated_df["Frequency"])

    is_outlier = (aggregated_df["Monetary"] > monetary_threshold) | (
        aggregated_df["Frequency"] > frequency_threshold
    )

    non_outliers = aggregated_df[~is_outlier].copy()

    # Escalar variables RFM
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(
        non_outliers[["Monetary", "Frequency", "Recency"]]
    )

    # Crear nuevo DataFrame escalado
    scaled_df = pd.DataFrame(
        scaled_data,
        columns=["Monetary", "Frequency", "Recency"],
        index=non_outliers.index,
    )

    context.log.info("Created and scaled data")
    context.log.info(scaled_df.describe())

    return scaled_df


def get_outlier_thresholds(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q3 + 1.5 * iqr
