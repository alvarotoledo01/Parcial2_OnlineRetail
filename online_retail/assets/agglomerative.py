from dagster import AssetExecutionContext, asset
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from online_retail.assets.utils import create_pca_graph, execute_clustering


@asset(
    description="Apply Agglomerative clustering",
    group_name="Clustering",
    required_resource_keys={"mlflow_agglomerative"},
)
def agglomerative(
    context: AssetExecutionContext, create_features: pd.DataFrame
) -> dict:
    # get a copy of the dataframe
    df = create_features.copy()

    # initialize the Agglomerative model
    context.log.info("Starting Agglomerative clustering")
    model = AgglomerativeClustering(n_clusters=2, linkage="ward")
    mlflow = context.resources.mlflow_agglomerative

    # execute clustering
    results = execute_clustering(mlflow, model, df, "agglomerative")

    # create pca graph
    create_pca_graph(df, model.labels_, mlflow, "agglomerative", context)

    return results
