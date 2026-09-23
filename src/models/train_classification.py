"""
Classification Model for 30-Day Readmission Prediction.

Matches JD:
"predictive statistical models, decision trees, classification"

Outputs:
- XGBoost classification model
- SHAP summary plot
- Machine-readable SHAP feature importance CSV
"""

import sys
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap

from pathlib import Path
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    classification_report
)

import xgboost as xgb


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger


logger = get_logger(__name__)


def run_classification():
    logger.info("Starting Classification Model Training...")

    # ------------------------------------------------------------------
    # 1. Load Data
    # ------------------------------------------------------------------

    data_path = PROJECT_ROOT / "data" / "processed"

    train_df = pd.read_parquet(data_path / "train.parquet")
    val_df = pd.read_parquet(data_path / "val.parquet")
    test_df = pd.read_parquet(data_path / "test.parquet")

    # ------------------------------------------------------------------
    # 2. Define Target and Excluded Columns
    # ------------------------------------------------------------------

    target = "IS_30DAY_READMISSION"

    exclude_cols = [
        "DESYNPUF_ID",
        "IS_30DAY_READMISSION",
        "BENE_BIRTH_DT",
        "BENE_DEATH_DT",
        "RISK_CLUSTER",
    ]

    # ------------------------------------------------------------------
    # 3. Remove Records With Unknown Target
    # ------------------------------------------------------------------

    train_df = train_df.dropna(subset=[target]).copy()
    val_df = val_df.dropna(subset=[target]).copy()
    test_df = test_df.dropna(subset=[target]).copy()

    logger.info(
        f"Labeled records - Train: {len(train_df):,}, "
        f"Validation: {len(val_df):,}, "
        f"Test: {len(test_df):,}"
    )

    # ------------------------------------------------------------------
    # 4. Encode Target
    # ------------------------------------------------------------------

    def encode_target(series):
        encoded = series.map({
            True: 1,
            False: 0,
            "True": 1,
            "False": 0,
            1: 1,
            0: 0,
        })

        if encoded.isna().any():
            invalid_values = series[encoded.isna()].unique()
            raise ValueError(
                f"Unexpected values found in {target}: "
                f"{invalid_values}"
            )

        return encoded.astype(int)

    train_df[target] = encode_target(train_df[target])
    val_df[target] = encode_target(val_df[target])
    test_df[target] = encode_target(test_df[target])

    # ------------------------------------------------------------------
    # 5. Select Numeric Features
    # ------------------------------------------------------------------

    numeric_dtypes = [
        "int64",
        "float64",
        "bool",
        "int32",
        "float32",
        "int16",
        "float16",
    ]

    features = [
        col
        for col in train_df.columns
        if (
            col not in exclude_cols
            and train_df[col].dtype in numeric_dtypes
        )
    ]

    if not features:
        raise ValueError("No numeric classification features were found.")

    logger.info(f"Classification features: {len(features)}")

    # ------------------------------------------------------------------
    # 6. Normalize Boolean Features
    # ------------------------------------------------------------------

    for col in features:
        if train_df[col].dtype == "bool":
            train_df[col] = train_df[col].astype(int)
            val_df[col] = val_df[col].astype(int)
            test_df[col] = test_df[col].astype(int)

    # ------------------------------------------------------------------
    # 7. Handle Missing Feature Values
    #
    # IMPORTANT:
    # Target values were already handled separately.
    # Only model features are imputed here.
    # ------------------------------------------------------------------

    train_df[features] = train_df[features].fillna(0)
    val_df[features] = val_df[features].fillna(0)
    test_df[features] = test_df[features].fillna(0)

    X_train = train_df[features]
    y_train = train_df[target]

    X_val = val_df[features]
    y_val = val_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    # ------------------------------------------------------------------
    # 8. Log Target Distribution
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # 9. Train XGBoost Classifier
    # ------------------------------------------------------------------

    logger.info("Training XGBoost Classifier...")

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="auc",
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[
            (X_train, y_train),
            (X_val, y_val),
        ],
        verbose=False,
    )

    # ------------------------------------------------------------------
    # 10. Evaluate Model
    # ------------------------------------------------------------------

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    auc_roc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, y_pred)

    logger.info(f"Test AUC-ROC: {auc_roc:.4f}")
    logger.info(f"Test Accuracy: {accuracy:.4f}")

    report = classification_report(
        y_test,
        y_pred,
        digits=4,
    )

    logger.info("Classification Report:\n" + report)

    # ------------------------------------------------------------------
    # 11. SHAP Explainability
    # ------------------------------------------------------------------

    logger.info("Calculating SHAP values for explainability...")

    explainer = shap.TreeExplainer(model)

    # Use a deterministic sample for explainability.
    #
    # This keeps SHAP computation manageable while preserving
    # reproducibility. The full test set is still used for evaluation.
    shap_sample_size = min(2000, len(X_test))

    X_shap = X_test.sample(
        n=shap_sample_size,
        random_state=42,
    )

    logger.info(
        f"Calculating SHAP values on {len(X_shap):,} test records..."
    )

    shap_explanation = explainer(X_shap)

    shap_values = np.asarray(shap_explanation.values)

    # XGBoost binary classification normally produces:
    #
    # (n_samples, n_features)
    #
    # Some SHAP versions/models can produce:
    #
    # (n_samples, n_features, n_outputs)
    #
    # Handle both safely.
    if shap_values.ndim == 3:
        if shap_values.shape[2] == 1:
            shap_values = shap_values[:, :, 0]
        else:
            # For binary classification, use the positive class.
            shap_values = shap_values[:, :, 1]

    if shap_values.ndim != 2:
        raise ValueError(
            f"Unexpected SHAP array shape: {shap_values.shape}"
        )

    # ------------------------------------------------------------------
    # 12. Calculate Numerical SHAP Feature Importance
    # ------------------------------------------------------------------

    mean_abs_shap = np.abs(shap_values).mean(axis=0)

    shap_importance = pd.DataFrame({
        "feature": X_shap.columns,
        "mean_abs_shap": mean_abs_shap,
    })

    shap_importance = shap_importance.sort_values(
        "mean_abs_shap",
        ascending=False,
    ).reset_index(drop=True)

    shap_importance["mean_abs_shap_rank"] = (
        np.arange(1, len(shap_importance) + 1)
    )

    shap_importance = shap_importance[
        [
            "feature",
            "mean_abs_shap_rank",
            "mean_abs_shap",
        ]
    ]

    # ------------------------------------------------------------------
    # 13. Save Machine-Readable SHAP Importance
    # ------------------------------------------------------------------

    docs_dir = PROJECT_ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    shap_csv_path = docs_dir / "shap_feature_importance.csv"

    shap_importance.to_csv(
        shap_csv_path,
        index=False,
    )

    logger.info(
        f"Saved numerical SHAP feature importance to "
        f"{shap_csv_path.relative_to(PROJECT_ROOT)}"
    )

    # Log top 10 features so we can verify them immediately.
    logger.info("Top SHAP features:")

    for _, row in shap_importance.head(10).iterrows():
        logger.info(
            f"  {int(row['mean_abs_shap_rank'])}. "
            f"{row['feature']} "
            f"(mean |SHAP|={row['mean_abs_shap']:.6f})"
        )

    # ------------------------------------------------------------------
    # 14. Save SHAP Summary Plot
    # ------------------------------------------------------------------

    plt.figure(figsize=(10, 6))

    shap.summary_plot(
        shap_values,
        X_shap,
        show=False,
    )

    plt.title(
        "SHAP Feature Importance for Readmission Prediction"
    )

    plt.tight_layout()

    shap_plot_path = docs_dir / "shap_summary.png"

    plt.savefig(
        shap_plot_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    logger.info(
        f"Saved SHAP summary plot to "
        f"{shap_plot_path.relative_to(PROJECT_ROOT)}"
    )

    # ------------------------------------------------------------------
    # 15. Save Model
    # ------------------------------------------------------------------

    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = models_dir / "classification_model.pkl"

    joblib.dump(
        model,
        model_path,
    )

    logger.info(
        f"Saved classification model to "
        f"{model_path.relative_to(PROJECT_ROOT)}"
    )

    # ------------------------------------------------------------------
    # 16. Save Model Metadata
    #
    # This will be useful later for the Phase 3 inference tool.
    # ------------------------------------------------------------------

    metadata = {
        "target": target,
        "features": features,
        "n_features": len(features),
        "test_auc_roc": float(auc_roc),
        "test_accuracy": float(accuracy),
        "shap_sample_size": int(shap_sample_size),
    }

    metadata_path = models_dir / "classification_metadata.json"

    import json

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(
            metadata,
            f,
            indent=2,
        )

    logger.info(
        f"Saved classification metadata to "
        f"{metadata_path.relative_to(PROJECT_ROOT)}"
    )

    # ------------------------------------------------------------------
    # 17. Completion
    # ------------------------------------------------------------------

    logger.info("Classification Model Training Complete.")


if __name__ == "__main__":
    run_classification()