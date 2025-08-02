from dagster import AssetExecutionContext, asset
import pandas as pd
from sklearn.cluster import KMeans
from online_retail.assets.utils import create_pca_graph, execute_clustering


@asset(
    description="Apply KMeans clustering",
    group_name="Clustering",
    required_resource_keys={"mlflow_kmeans"},
)
def kmeans(context: AssetExecutionContext, create_features: pd.DataFrame) -> dict:
    # get a copy of the dataframe
    df = create_features.copy()

    # initialize the KMeans model
    context.log.info("Starting KMeans clustering")
    model = KMeans(n_clusters=3, random_state=42)
    mlflow = context.resources.mlflow_kmeans

    # execute clustering
    results = execute_clustering(mlflow, model, df, "kmeans")

    # create pca graph
    create_pca_graph(df, model.labels_, mlflow, "kmeans", context)

    return results
