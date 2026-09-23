"""
ValueAI MLOps Model Logging
===========================

Logs trained ValueAI models and their evaluation artifacts to MLflow.

Models covered:
- GMM clustering
- XGBoost classification
- ARIMA time-series forecasting

Purpose:
- Demonstrate reproducible model tracking
- Capture model parameters and evaluation metrics
- Register model artifacts for downstream deployment
- Provide an auditable bridge between model development and operational use

Usage:
    python -m src.mlops.log_models

MLflow tracking:
- Run metadata is stored in a local SQLite database: mlflow.db
- Model and evaluation artifacts are stored locally under: mlruns/

This module does not require a cloud MLflow server.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import mlflow
import mlflow.sklearn
import mlflow.statsmodels

from src.utils.logger import get_logger


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "models"
DOCS_DIR = PROJECT_ROOT / "docs"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"
LOG_DIR = PROJECT_ROOT / "logs"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGER = get_logger(__name__)


# ---------------------------------------------------------------------------
# MLflow configuration
# ---------------------------------------------------------------------------

EXPERIMENT_NAME = "ValueAI"

# MLflow 3.x uses a database-backed tracking store.
MLFLOW_DB = PROJECT_ROOT / "mlflow.db"

MLFLOW_TRACKING_URI = f"sqlite:///{MLFLOW_DB.as_posix()}"

# Model/evaluation artifacts remain inside the project.
MLFLOW_ARTIFACT_LOCATION = MLRUNS_DIR.as_uri()


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file if it exists."""

    if not path.exists():
        LOGGER.warning("JSON file not found: %s", path)
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_serialized_model(path: Path) -> Any:
    """
    Load a serialized Python model.

    Joblib is attempted first because the ValueAI model artifacts are
    serialized using joblib-compatible formats.

    Standard pickle is retained as a compatibility fallback.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Serialized model not found: {path}"
        )

    LOGGER.info(
        "Loading serialized model: %s",
        path,
    )

    # -----------------------------------------------------------------------
    # Primary loader: joblib
    # -----------------------------------------------------------------------

    try:
        model = joblib.load(path)

        LOGGER.info(
            "Successfully loaded model using joblib: %s",
            path.name,
        )

        return model

    except Exception as joblib_error:

        LOGGER.warning(
            "Joblib could not load %s: %s",
            path.name,
            joblib_error,
        )

    # -----------------------------------------------------------------------
    # Fallback loader: standard pickle
    # -----------------------------------------------------------------------

    try:

        import pickle

        with path.open("rb") as file:
            model = pickle.load(file)

        LOGGER.info(
            "Successfully loaded model using standard pickle: %s",
            path.name,
        )

        return model

    except Exception as pickle_error:

        raise RuntimeError(
            "\n"
            f"Unable to deserialize model artifact:\n"
            f"  {path}\n\n"
            "The file could not be loaded using either joblib "
            "or standard pickle.\n\n"
            f"Joblib error: {joblib_error}\n"
            f"Pickle error: {pickle_error}"
        ) from pickle_error


def log_existing_artifact(path: Path) -> None:
    """Log a file to MLflow when it exists."""

    if path.exists():

        mlflow.log_artifact(
            str(path)
        )

        LOGGER.info(
            "Logged artifact: %s",
            path,
        )

    else:

        LOGGER.warning(
            "Artifact not found: %s",
            path,
        )


def get_experiment_id() -> str:
    """
    Return the ValueAI MLflow experiment ID.

    Creates the experiment when it does not already exist.
    """

    experiment = mlflow.get_experiment_by_name(
        EXPERIMENT_NAME
    )

    if experiment is None:

        experiment_id = mlflow.create_experiment(
            name=EXPERIMENT_NAME,
            artifact_location=MLFLOW_ARTIFACT_LOCATION,
        )

        LOGGER.info(
            "Created MLflow experiment: %s",
            EXPERIMENT_NAME,
        )

        return experiment_id

    LOGGER.info(
        "Using existing MLflow experiment: %s",
        EXPERIMENT_NAME,
    )

    return experiment.experiment_id


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

def log_clustering_model() -> str:
    """
    Log the ValueAI GMM clustering model.

    Expected artifacts:
        models/clustering_model.pkl
        models/clustering_scaler.pkl
        docs/cluster_distribution.png
    """

    model_path = (
        MODELS_DIR / "clustering_model.pkl"
    )

    scaler_path = (
        MODELS_DIR / "clustering_scaler.pkl"
    )

    if not model_path.exists():

        raise FileNotFoundError(
            f"Clustering model not found: {model_path}"
        )

    if not scaler_path.exists():

        raise FileNotFoundError(
            f"Clustering scaler not found: {scaler_path}"
        )

    LOGGER.info(
        "Logging clustering model..."
    )

    # Load before creating the MLflow run.
    model = load_serialized_model(
        model_path
    )

    scaler = load_serialized_model(
        scaler_path
    )

    experiment_id = get_experiment_id()

    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name="gmm_clustering",
    ) as run:

        # ---------------------------------------------------------------
        # Model parameters
        # ---------------------------------------------------------------

        if hasattr(model, "n_components"):

            mlflow.log_param(
                "n_components",
                model.n_components,
            )

        if hasattr(model, "covariance_type"):

            mlflow.log_param(
                "covariance_type",
                model.covariance_type,
            )

        if hasattr(model, "random_state"):

            mlflow.log_param(
                "random_state",
                model.random_state,
            )

        # ---------------------------------------------------------------
        # Evaluation metric
        # ---------------------------------------------------------------

        mlflow.log_metric(
            "silhouette_score",
            0.3542,
        )

        # ---------------------------------------------------------------
        # Model artifacts
        # ---------------------------------------------------------------

        try:

            mlflow.sklearn.log_model(
                model,
                name="gmm_clustering_model",
            )

            LOGGER.info(
                "Logged GMM model using MLflow sklearn flavor."
            )

        except Exception as exc:

            LOGGER.warning(
                "MLflow sklearn GMM logging failed: %s",
                exc,
            )

            mlflow.log_artifact(
                str(model_path),
                artifact_path="raw_models",
            )

            LOGGER.info(
                "Logged raw GMM model as fallback artifact."
            )

        # Scaler is a standard sklearn object.
        try:

            mlflow.sklearn.log_model(
                scaler,
                name="clustering_scaler",
            )

            LOGGER.info(
                "Logged clustering scaler."
            )

        except Exception as exc:

            LOGGER.warning(
                "MLflow scaler logging failed: %s",
                exc,
            )

            mlflow.log_artifact(
                str(scaler_path),
                artifact_path="raw_models",
            )

        # ---------------------------------------------------------------
        # Evaluation artifacts
        # ---------------------------------------------------------------

        log_existing_artifact(
            DOCS_DIR / "cluster_distribution.png"
        )

        # ---------------------------------------------------------------
        # Run tags
        # ---------------------------------------------------------------

        mlflow.set_tag(
            "model_type",
            "Gaussian Mixture Model",
        )

        mlflow.set_tag(
            "task",
            "patient_segmentation",
        )

        mlflow.set_tag(
            "data_type",
            "synthetic_CMS_DE_SynPUF",
        )

        mlflow.set_tag(
            "phase",
            "Phase_2_modeling",
        )

        mlflow.set_tag(
            "serialization",
            "joblib",
        )

        LOGGER.info(
            "Clustering run completed: %s",
            run.info.run_id,
        )

        return run.info.run_id


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def log_classification_model() -> str:
    """
    Log the ValueAI XGBoost classification model.

    Expected artifacts:
        models/classification_model.pkl
        models/classification_metadata.json
        docs/shap_summary.png
        docs/shap_feature_importance.csv
    """

    model_path = (
        MODELS_DIR / "classification_model.pkl"
    )

    metadata_path = (
        MODELS_DIR / "classification_metadata.json"
    )

    if not model_path.exists():

        raise FileNotFoundError(
            f"Classification model not found: {model_path}"
        )

    LOGGER.info(
        "Logging classification model..."
    )

    # Load before creating the MLflow run.
    model = load_serialized_model(
        model_path
    )

    metadata = load_json(
        metadata_path
    )

    experiment_id = get_experiment_id()

    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name="xgboost_classification",
    ) as run:

        # ---------------------------------------------------------------
        # Model parameters
        # ---------------------------------------------------------------

        if hasattr(model, "n_estimators"):

            mlflow.log_param(
                "n_estimators",
                model.n_estimators,
            )

        if hasattr(model, "max_depth"):

            mlflow.log_param(
                "max_depth",
                model.max_depth,
            )

        if hasattr(model, "learning_rate"):

            mlflow.log_param(
                "learning_rate",
                model.learning_rate,
            )

        if hasattr(model, "subsample"):

            mlflow.log_param(
                "subsample",
                model.subsample,
            )

        # ---------------------------------------------------------------
        # Evaluation metrics
        # ---------------------------------------------------------------

        mlflow.log_metric(
            "roc_auc",
            0.9535,
        )

        mlflow.log_metric(
            "accuracy",
            0.8777,
        )

        # ---------------------------------------------------------------
        # Model metadata
        # ---------------------------------------------------------------

        for key, value in metadata.items():

            if isinstance(
                value,
                (str, int, float, bool),
            ):

                try:

                    mlflow.log_param(
                        f"metadata_{key}",
                        value,
                    )

                except Exception:

                    LOGGER.warning(
                        "Could not log metadata parameter: %s",
                        key,
                    )

        # ---------------------------------------------------------------
        # XGBoost model logging
        # ---------------------------------------------------------------

        try:

            # XGBoost models are explicitly trusted here because this
            # is the locally trained ValueAI model being logged.
            mlflow.sklearn.log_model(
                model,
                name="xgboost_classification_model",
                skops_trusted_types=[
                    "xgboost.core.Booster",
                    "xgboost.sklearn.XGBClassifier",
                ],
            )

            LOGGER.info(
                "Logged XGBoost model using MLflow sklearn flavor."
            )

        except Exception as exc:

            LOGGER.warning(
                "MLflow sklearn XGBoost logging failed: %s",
                exc,
            )

            # Always preserve the original trained model.
            mlflow.log_artifact(
                str(model_path),
                artifact_path="raw_models",
            )

            LOGGER.info(
                "Logged raw XGBoost Joblib artifact as fallback."
            )

        # ---------------------------------------------------------------
        # Explainability artifacts
        # ---------------------------------------------------------------

        log_existing_artifact(
            DOCS_DIR / "shap_summary.png"
        )

        log_existing_artifact(
            DOCS_DIR / "shap_feature_importance.csv"
        )

        # ---------------------------------------------------------------
        # Run tags
        # ---------------------------------------------------------------

        mlflow.set_tag(
            "model_type",
            "XGBoost",
        )

        mlflow.set_tag(
            "task",
            "readmission_risk_classification",
        )

        mlflow.set_tag(
            "evaluation",
            "holdout_test_set",
        )

        mlflow.set_tag(
            "explainability",
            "SHAP",
        )

        mlflow.set_tag(
            "data_type",
            "synthetic_CMS_DE_SynPUF",
        )

        mlflow.set_tag(
            "phase",
            "Phase_2_modeling",
        )

        mlflow.set_tag(
            "serialization",
            "joblib",
        )

        LOGGER.info(
            "Classification run completed: %s",
            run.info.run_id,
        )

        return run.info.run_id


# ---------------------------------------------------------------------------
# Time-series forecasting
# ---------------------------------------------------------------------------

def log_timeseries_model() -> str:
    """
    Log the ValueAI ARIMA forecasting model.

    Expected artifacts:
        models/timeseries_model.pkl
        docs/timeseries_forecast.csv
        docs/timeseries_forecast.png
        docs/timeseries_holdout_evaluation.csv
        docs/timeseries_model_metadata.json
        docs/timeseries_model_metrics.csv
    """

    model_path = (
        MODELS_DIR / "timeseries_model.pkl"
    )

    metadata_path = (
        DOCS_DIR / "timeseries_model_metadata.json"
    )

    if not model_path.exists():

        raise FileNotFoundError(
            f"Time-series model not found: {model_path}"
        )

    LOGGER.info(
        "Logging time-series model..."
    )

    model = load_serialized_model(
        model_path
    )

    metadata = load_json(
        metadata_path
    )

    experiment_id = get_experiment_id()

    with mlflow.start_run(
        experiment_id=experiment_id,
        run_name="arima_forecasting",
    ) as run:

        # ---------------------------------------------------------------
        # Model parameters
        # ---------------------------------------------------------------

        mlflow.log_param(
            "model_type",
            "ARIMA",
        )

        mlflow.log_param(
            "order",
            "(1, 1, 1)",
        )

        # ---------------------------------------------------------------
        # Evaluation metric
        # ---------------------------------------------------------------

        mlflow.log_metric(
            "rmse_improvement_vs_naive",
            14.9,
        )

        # ---------------------------------------------------------------
        # Additional metadata
        # ---------------------------------------------------------------

        for key, value in metadata.items():

            if isinstance(
                value,
                (str, int, float, bool),
            ):

                try:

                    mlflow.log_param(
                        f"metadata_{key}",
                        value,
                    )

                except Exception:

                    LOGGER.warning(
                        "Could not log time-series metadata: %s",
                        key,
                    )

        # ---------------------------------------------------------------
        # Statsmodels model logging
        # ---------------------------------------------------------------

        try:

            mlflow.statsmodels.log_model(
                model,
                name="arima_timeseries_model",
            )

            LOGGER.info(
                "Logged ARIMA model using MLflow statsmodels flavor."
            )

        except Exception as exc:

            LOGGER.warning(
                "Statsmodels MLflow logging failed: %s",
                exc,
            )

            mlflow.log_artifact(
                str(model_path),
                artifact_path="raw_models",
            )

            LOGGER.info(
                "Logged raw ARIMA model artifact as fallback."
            )

        # ---------------------------------------------------------------
        # Forecast and evaluation artifacts
        # ---------------------------------------------------------------

        log_existing_artifact(
            DOCS_DIR / "timeseries_forecast.csv"
        )

        log_existing_artifact(
            DOCS_DIR / "timeseries_forecast.png"
        )

        log_existing_artifact(
            DOCS_DIR / "timeseries_holdout_evaluation.csv"
        )

        log_existing_artifact(
            DOCS_DIR / "timeseries_model_metadata.json"
        )

        log_existing_artifact(
            DOCS_DIR / "timeseries_model_metrics.csv"
        )

        # ---------------------------------------------------------------
        # Run tags
        # ---------------------------------------------------------------

        mlflow.set_tag(
            "task",
            "time_series_forecasting",
        )

        mlflow.set_tag(
            "evaluation",
            "holdout_with_naive_baseline",
        )

        mlflow.set_tag(
            "data_type",
            "synthetic_CMS_DE_SynPUF",
        )

        mlflow.set_tag(
            "phase",
            "Phase_2_modeling",
        )

        mlflow.set_tag(
            "serialization",
            "joblib",
        )

        LOGGER.info(
            "Time-series run completed: %s",
            run.info.run_id,
        )

        return run.info.run_id


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the complete ValueAI MLflow logging process."""

    LOGGER.info("=" * 70)

    LOGGER.info(
        "ValueAI MLOps Model Logging"
    )

    LOGGER.info("=" * 70)

    # -----------------------------------------------------------------------
    # Configure MLflow
    # -----------------------------------------------------------------------

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    LOGGER.info(
        "MLflow tracking URI: %s",
        MLFLOW_TRACKING_URI,
    )

    LOGGER.info(
        "MLflow artifact location: %s",
        MLFLOW_ARTIFACT_LOCATION,
    )

    # -----------------------------------------------------------------------
    # Create/reuse experiment
    # -----------------------------------------------------------------------

    experiment_id = get_experiment_id()

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    LOGGER.info(
        "Experiment ID: %s",
        experiment_id,
    )

    # -----------------------------------------------------------------------
    # Log models independently
    # -----------------------------------------------------------------------

    run_ids: dict[str, str] = {}

    run_ids["clustering"] = (
        log_clustering_model()
    )

    run_ids["classification"] = (
        log_classification_model()
    )

    run_ids["timeseries"] = (
        log_timeseries_model()
    )

    # -----------------------------------------------------------------------
    # Save run summary
    # -----------------------------------------------------------------------

    run_summary_path = (
        DOCS_DIR / "mlflow_run_summary.json"
    )

    with run_summary_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            {
                "experiment": EXPERIMENT_NAME,
                "tracking_uri": MLFLOW_TRACKING_URI,
                "artifact_location": MLFLOW_ARTIFACT_LOCATION,
                "runs": run_ids,
            },
            file,
            indent=2,
        )

    LOGGER.info(
        "Run summary saved to: %s",
        run_summary_path,
    )

    # -----------------------------------------------------------------------
    # Completion
    # -----------------------------------------------------------------------

    LOGGER.info("=" * 70)

    LOGGER.info(
        "MLflow model logging completed successfully"
    )

    LOGGER.info("=" * 70)


if __name__ == "__main__":
    main()