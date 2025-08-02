from dagster import AssetExecutionContext, asset
import pandas as pd
from sklearn.mixture import GaussianMixture
from online_retail.assets.utils import create_pca_graph, execute_clustering


@asset(
    description="Apply Gaussian Mixture Model clustering",
    group_name="Clustering",
    required_resource_keys={"mlflow_gaussian_mixture"},
)
def gaussian_mixture(
    context: AssetExecutionContext, create_features: pd.DataFrame
) -> dict:
    # get a copy of the dataframe
    df = create_features.copy()

    # initialize the Gaussian Mixture model
    context.log.info("Starting Gaussian Mixture Model clustering")
    model = GaussianMixture(n_components=2, random_state=42)
    mlflow = context.resources.mlflow_gaussian_mixture

    # execute clustering
    results = execute_clustering(mlflow, model, df, "gaussian_mixture")

    # create pca graph
    create_pca_graph(df, results["labels"], mlflow, "gaussian_mixture", context)

    return results
