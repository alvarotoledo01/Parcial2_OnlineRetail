# Online Retail Customer Segmentation

## Descripción

Este proyecto realiza segmentación de clientes utilizando análisis RFM (Recency, Frequency, Monetary) con múltiples algoritmos de clustering. El pipeline está implementado con Dagster y el tracking de experimentos con MLflow.

## Configuración del Entorno

### 1. Crear el entorno de Conda

```bash
conda env create -f environment.yml
conda activate online_retail
```

### 2. Configurar MLflow (Opcional)

Crear un archivo `.env` en la raíz del proyecto:

```bash
# Para uso local (por defecto si no se especifica)
MLFLOW_TRACKING_URI=file:./mlruns

# Para usar un servidor MLflow remoto
MLFLOW_TRACKING_URI=http://192.168.1.108:5000"
```

**Nota**: Si no creas el archivo `.env`, el sistema usará automáticamente `file:./mlruns` para almacenamiento local.

### 3. Ejecutar el Pipeline

```bash
# Desde la raíz del proyecto
dagster dev
```

Esto levantará la interfaz web de Dagster en `http://localhost:3000` donde podrás:

- Visualizar el pipeline completo
- Ejecutar assets individuales o todo el pipeline
- Monitorear el progreso y logs
- Ver los resultados de clustering y métricas en MLflow

## Estructura del Proyecto

- `online_retail/assets/` - Assets de Dagster (carga, limpieza, clustering)
- `online_retail/resources/` - Configuración de recursos (MLflow)
- `environment.yml` - Especificación del entorno de Conda
- `.env` - Variables de entorno (crear manualmente)

## Algoritmos de Clustering Incluidos

- K-Means
- Agglomerative Clustering
- Gaussian Mixture Model
- DBSCAN

Cada algoritmo genera métricas de evaluación (Silhouette Score, Calinski-Harabasz, Davies-Bouldin) y visualizaciones PCA.
