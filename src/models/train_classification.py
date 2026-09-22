"""
Classification Model for 30-Day Readmission Prediction.
Matches JD: "predictive statistical models, decision trees, classification"
"""
import sys
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from pathlib import Path
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger
logger = get_logger(__name__)

def run_classification():
    logger.info("Starting Classification Model Training...")
    
    # 1. Load Data
    data_path = PROJECT_ROOT / "data" / "processed"
    train_df = pd.read_parquet(data_path / "train.parquet")
    val_df = pd.read_parquet(data_path / "val.parquet")
    test_df = pd.read_parquet(data_path / "test.parquet")
    
    # 2. Define Features and Target
    target = "IS_30DAY_READMISSION"
    exclude_cols = [
        "DESYNPUF_ID",
        "IS_30DAY_READMISSION",
        "BENE_BIRTH_DT",
        "BENE_DEATH_DT",
        "RISK_CLUSTER"
    ]

    # Remove records where the readmission outcome is unknown.
    # None/NaN means the outcome cannot be used as a classification label.
    train_df = train_df.dropna(subset=[target]).copy()
    val_df = val_df.dropna(subset=[target]).copy()
    test_df = test_df.dropna(subset=[target]).copy()

    logger.info(
        f"Labeled records - Train: {len(train_df):,}, "
        f"Validation: {len(val_df):,}, "
        f"Test: {len(test_df):,}"
    )

    # Convert boolean readmission target to binary 0/1.
    # True = readmitted, False = not readmitted.
    def encode_target(series):
        return series.map({
            True: 1,
            False: 0,
            "True": 1,
            "False": 0,
            1: 1,
            0: 0
        }).astype(int)

    train_df[target] = encode_target(train_df[target])
    val_df[target] = encode_target(val_df[target])
    test_df[target] = encode_target(test_df[target])

    features = [
        col for col in train_df.columns
        if col not in exclude_cols
        and train_df[col].dtype in [
            "int64",
            "float64",
            "bool",
            "int32",
            "float32"
        ]
    ]

    logger.info(f"Classification features: {len(features)}")

    # Handle boolean feature columns for XGBoost compatibility
    for col in features:
        if train_df[col].dtype == "bool":
            train_df[col] = train_df[col].astype(int)
            val_df[col] = val_df[col].astype(int)
            test_df[col] = test_df[col].astype(int)

    # Fill missing values in FEATURES only.
    train_df[features] = train_df[features].fillna(0)
    val_df[features] = val_df[features].fillna(0)
    test_df[features] = test_df[features].fillna(0)

    X_train, y_train = train_df[features], train_df[target]
    X_val, y_val = val_df[features], val_df[target]
    X_test, y_test = test_df[features], test_df[target]

    logger.info(
        f"Target distribution - Train: "
        f"{y_train.value_counts().to_dict()}"
    )
    logger.info(
        f"Target distribution - Validation: "
        f"{y_val.value_counts().to_dict()}"
    )
    logger.info(
        f"Target distribution - Test: "
        f"{y_test.value_counts().to_dict()}"
    )

    # 3. Train XGBoost Model
    logger.info("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="auc"
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )
    
    # 4. Evaluate Model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, y_pred)
    
    logger.info(f"Test AUC-ROC: {auc_roc:.4f}")
    logger.info(f"Test Accuracy: {acc:.4f}")
    logger.info("Classification Report:\n" + classification_report(y_test, y_pred))
    
    # 5. SHAP Explainability
    logger.info("Calculating SHAP values for explainability...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # Plot SHAP summary
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_test, show=False)
    plt.title("SHAP Feature Importance for Readmission Prediction")
    plt.tight_layout()
    plt.savefig(PROJECT_ROOT / "docs" / "shap_summary.png", dpi=150)
    plt.close()
    logger.info("Saved SHAP summary plot to docs/shap_summary.png")
    
    # 6. Save Model
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, models_dir / "classification_model.pkl")
    logger.info("Saved classification model to models/classification_model.pkl")
    
    logger.info("Classification Model Training Complete.")

if __name__ == "__main__":
    run_classification()