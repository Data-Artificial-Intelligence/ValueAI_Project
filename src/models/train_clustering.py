"""
Clustering Model for Patient Risk Segmentation.
Matches JD: "clustering, pattern analysis, segmentation analysis, customer profiling"

Note for SageMaker: In a cloud environment, this script is executed as a SageMaker 
Training Job. The joblib.dump step is replaced by saving the model artifact to S3 
and registering it in the SageMaker Model Registry.
"""
import sys
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger
logger = get_logger(__name__)

def run_clustering():
    logger.info("Starting Clustering Model Training...")
    
    # 1. Load Data
    data_path = PROJECT_ROOT / "data" / "processed" / "full_dataset.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df)} records for clustering.")
    
    # 2. Select Features for Segmentation
    cluster_features = [
        "AGE", "TOTAL_ADMISSIONS", "AVG_ADMISSION_COST", 
        "UNIQUE_DIAGNOSES_COUNT", "AVG_LENGTH_OF_STAY",
        "INPATIENT_CLAIM_COUNT", "OUTPATIENT_CLAIM_COUNT", "DRUG_CLAIM_COUNT"
    ]
    
    available_features = [f for f in cluster_features if f in df.columns]
    X = df[available_features].fillna(0)
    
    # 3. Scale Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Train Gaussian Mixture Model (GMM)
    n_components = 3
    gmm = GaussianMixture(n_components=n_components, random_state=42, n_init=10)
    cluster_labels = gmm.fit_predict(X_scaled)
    
    # 5. Evaluate
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    logger.info(f"Silhouette Score for {n_components} clusters: {silhouette_avg:.4f}")
    
    # 6. Analyze Cluster Profiles
    df["RISK_CLUSTER"] = cluster_labels
    cluster_profile = df.groupby("RISK_CLUSTER")[available_features].mean()
    logger.info("Cluster Profiles (Mean Values):\n" + str(cluster_profile))
    
    # 7. Save Outputs
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(gmm, models_dir / "clustering_model.pkl")
    joblib.dump(scaler, models_dir / "clustering_scaler.pkl")
    
    clustered_df_path = PROJECT_ROOT / "data" / "processed" / "clustered_dataset.parquet"
    df.to_parquet(clustered_df_path, index=False)
    logger.info(f"Saved clustered dataset to {clustered_df_path}")
    
    # Plot Cluster Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x="RISK_CLUSTER", data=df, palette="viridis", hue="RISK_CLUSTER", legend=False)
    plt.title("Patient Risk Cluster Distribution")
    plt.xlabel("Cluster ID")
    plt.ylabel("Number of Patients")
    plt.savefig(PROJECT_ROOT / "docs" / "cluster_distribution.png", dpi=150)
    plt.close()
    logger.info("Saved cluster distribution plot to docs/cluster_distribution.png")
    
    logger.info("Clustering Model Training Complete.")

if __name__ == "__main__":
    run_clustering()