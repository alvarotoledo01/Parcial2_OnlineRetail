from dagster import Definitions, load_assets_from_modules
from dagster_mlflow import mlflow_tracking
import os
from dotenv import load_dotenv
from online_retail.assets import (
    agglomerative,
    clean_dataset,
    dbscan,
    gaussian_mixture,
    load_dataset,
    create_features,
    kmeans,
    summarize,
)

# Load environment variables from .env file
load_dotenv()
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")

assets = load_assets_from_modules(
    [
        load_dataset,
        clean_dataset,
        create_features,
        kmeans,
        agglomerative,
        gaussian_mixture,
        dbscan,
        summarize,
    ]
)

defs = Definitions(
    assets=assets,
    resources={
        "mlflow_kmeans": mlflow_tracking.configured(
            {
                "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
                "experiment_name": "kmeans_experiment1",
            }
        ),
        "mlflow_agglomerative": mlflow_tracking.configured(
            {
                "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
                "experiment_name": "agglomerative_experiment",
            }
        ),
        "mlflow_gaussian_mixture": mlflow_tracking.configured(
            {
                "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
                "experiment_name": "gaussian_mixture_experiment",
            }
        ),
        "mlflow_dbscan": mlflow_tracking.configured(
            {
                "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
                "experiment_name": "dbscan_experiment",
            }
        ),
    },
)
