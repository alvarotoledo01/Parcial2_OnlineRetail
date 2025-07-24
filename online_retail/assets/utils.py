from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def execute_clustering(mlflow, model, data, run_name):
    # fit and predict using the clustering model
    labels = model.fit_predict(data)

    # change run name
    mlflow.set_tag("mlflow.runName", run_name)

    # log the params and metrics
    sil = silhouette_score(data, labels)
    ch = calinski_harabasz_score(data, labels)
    db = davies_bouldin_score(data, labels)
    mlflow.log_params(model.get_params())

    n_clusters = get_number_of_clusters(labels)

    mlflow.log_metric("n_clusters", n_clusters)
    mlflow.log_metric("sil", sil)
    mlflow.log_metric("ch", ch)
    mlflow.log_metric("db", db)

    return {
        "silhouette_score": sil,
        "calinski_harabasz_score": ch,
        "davies_bouldin_score": db,
        "n_clusters": n_clusters,
        "labels": labels,
    }


def create_pca_graph(data, labels, mlflow, cluster_name, context):

    # ensure there is a dir
    os.makedirs("mlartifacts", exist_ok=True)
    pca_path = os.path.join("mlartifacts", f"{cluster_name}_pca.png")

    # perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data)

    # create a scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(
        principal_components[:, 0],
        principal_components[:, 1],
        c=labels,
        cmap="viridis",
        marker="o",
    )
    plt.title(f"PCA of {cluster_name} Clustering Results")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.colorbar(label="Cluster Label")
    plt.savefig(pca_path)
    plt.close()

    # log the PCA graph
    mlflow.log_artifact(pca_path)


def get_number_of_clusters(labels):
    if hasattr(labels, "n_clusters"):
        return labels.n_clusters
    elif hasattr(labels, "n_components"):
        return labels.n_components
    else:
        return len(set(labels)) - (1 if -1 in labels else 0)
