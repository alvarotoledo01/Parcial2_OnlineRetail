from dagster import AssetExecutionContext, asset
import pandas as pd


@asset(
    description="Summarize clustering results",
    group_name="Clustering",
)
def summarize(
    context: AssetExecutionContext,
    kmeans: dict,
    agglomerative: dict,
    dbscan: dict,
    gaussian_mixture: dict,
):
    context.log.info("Summarizing clustering results")

    results_df = pd.DataFrame(
        {
            "Algorithm": ["KMeans", "Agglomerative", "DBSCAN", "Gaussian Mixture"],
            "Number of Clusters": [
                kmeans["n_clusters"],
                agglomerative["n_clusters"],
                dbscan["n_clusters"],
                gaussian_mixture["n_clusters"],
            ],
            "Silhouette Score": [
                kmeans["silhouette_score"],
                agglomerative["silhouette_score"],
                dbscan["silhouette_score"],
                gaussian_mixture["silhouette_score"],
            ],
            "Calinsky-Harabasz Score": [
                kmeans["calinski_harabasz_score"],
                agglomerative["calinski_harabasz_score"],
                dbscan["calinski_harabasz_score"],
                gaussian_mixture["calinski_harabasz_score"],
            ],
            "Davies-Bouldin Score": [
                kmeans["davies_bouldin_score"],
                agglomerative["davies_bouldin_score"],
                dbscan["davies_bouldin_score"],
                gaussian_mixture["davies_bouldin_score"],
            ],
        }
    )

    context.log.info("Clustering results summary created")
    context.log.info(results_df)
