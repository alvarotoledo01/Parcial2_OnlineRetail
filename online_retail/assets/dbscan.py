from dagster import AssetExecutionContext, asset
import pandas as pd
from sklearn.cluster import DBSCAN
from online_retail.assets.utils import create_pca_graph, execute_clustering


@asset(
    description="Apply DBSCAN clustering",
    group_name="Clustering",
    required_resource_keys={"mlflow_dbscan"},
)
def dbscan(context: AssetExecutionContext, create_features: pd.DataFrame) -> dict:
    # get a copy of the dataframe
    df = create_features.copy()

    # initialize the DBSCAN model
    context.log.info("Starting DBSCAN clustering")
    model = DBSCAN(eps=0.9, min_samples=5)
    mlflow = context.resources.mlflow_dbscan

    # execute clustering
    results = execute_clustering(mlflow, model, df, "dbscan")

    # create pca graph
    create_pca_graph(df, model.labels_, mlflow, "dbscan", context)

    return results
