"""
ValueAI Agent Tools
===================

Tool layer for the Phase 3 Agentic AI Data Science Assistant.

All quantitative evidence is loaded dynamically from Phase 2 artifacts.
No patient statistics, cluster statistics, or SHAP rankings are
hardcoded into the returned analytical evidence.
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from langchain.tools import tool


# ---------------------------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLUSTERED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "clustered_dataset.parquet"
)

SHAP_PATH = PROJECT_ROOT / "docs" / "shap_feature_importance.csv"

MODEL_PATH = PROJECT_ROOT / "models" / "classification_model.pkl"

METADATA_PATH = PROJECT_ROOT / "models" / "classification_metadata.json"


# ---------------------------------------------------------------------------
# HIGH-RISK CLUSTER ANALYSIS
# ---------------------------------------------------------------------------

@tool
def analyze_high_risk_cluster() -> str:
    """
    Analyze the high-risk patient cluster using the actual Phase 2
    clustered dataset and actual Phase 2 SHAP feature-importance results.

    Returns:
    - total population
    - high-risk cluster population
    - high-risk cluster percentage
    - observed patient/utilization characteristics
    - top SHAP model-importance drivers

    Important:
    SHAP values returned by this tool are mean absolute SHAP values.
    They describe feature-importance magnitude only and do not provide
    directional or causal evidence.

    Use this tool whenever the user asks about:
    - the high-risk cluster
    - patient segmentation
    - cluster characteristics
    - high-risk population size
    - utilization characteristics
    - readmission drivers in the context of the high-risk cluster
    """

    if not CLUSTERED_DATA_PATH.exists():
        return "ERROR: clustered_dataset.parquet was not found."

    if not SHAP_PATH.exists():
        return "ERROR: shap_feature_importance.csv was not found."

    try:
        # ---------------------------------------------------------------
        # LOAD CLUSTERED DATA
        # ---------------------------------------------------------------

        df = pd.read_parquet(CLUSTERED_DATA_PATH)

        if "RISK_CLUSTER" not in df.columns:
            return (
                "ERROR: RISK_CLUSTER column is missing from clustered dataset."
            )

        total_population = len(df)

        if total_population == 0:
            return "ERROR: clustered dataset contains no records."

        # The Phase 2 project definition identifies Cluster 2 as the
        # high-risk cluster.
        high_risk_cluster_id = 2

        high_risk = df[
            df["RISK_CLUSTER"] == high_risk_cluster_id
        ].copy()

        if high_risk.empty:
            return (
                "ERROR: High-risk cluster 2 contains no records. "
                "Inspect the Phase 2 clustering output before continuing."
            )

        population_size = len(high_risk)

        population_percentage = (
            population_size / total_population
        ) * 100

        # ---------------------------------------------------------------
        # OBSERVED CLUSTER PROFILE
        # ---------------------------------------------------------------

        metrics = {
            "average_age": "AGE",
            "average_admissions": "TOTAL_ADMISSIONS",
            "average_admission_cost": "AVG_ADMISSION_COST",
            "average_diagnoses": "UNIQUE_DIAGNOSES_COUNT",
            "average_length_of_stay": "AVG_LENGTH_OF_STAY",
            "average_inpatient_claims": "INPATIENT_CLAIM_COUNT",
            "average_outpatient_claims": "OUTPATIENT_CLAIM_COUNT",
            "average_drug_claims": "DRUG_CLAIM_COUNT",
        }

        profile = {}

        for label, column in metrics.items():

            if column not in high_risk.columns:
                profile[label] = None
                continue

            numeric_values = pd.to_numeric(
                high_risk[column],
                errors="coerce",
            )

            value = numeric_values.mean()

            if pd.notna(value):
                profile[label] = float(value)
            else:
                profile[label] = None

        # ---------------------------------------------------------------
        # LOAD ACTUAL SHAP RANKINGS
        # ---------------------------------------------------------------

        shap_df = pd.read_csv(SHAP_PATH)

        required_shap_columns = {
            "feature",
            "mean_abs_shap_rank",
            "mean_abs_shap",
        }

        missing_columns = (
            required_shap_columns - set(shap_df.columns)
        )

        if missing_columns:
            return (
                "ERROR: SHAP file is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        # Validate numerical columns before using them.
        shap_df["mean_abs_shap_rank"] = pd.to_numeric(
            shap_df["mean_abs_shap_rank"],
            errors="coerce",
        )

        shap_df["mean_abs_shap"] = pd.to_numeric(
            shap_df["mean_abs_shap"],
            errors="coerce",
        )

        shap_df = shap_df.dropna(
            subset=[
                "mean_abs_shap_rank",
                "mean_abs_shap",
            ]
        )

        shap_df = shap_df.sort_values(
            "mean_abs_shap_rank"
        )

        # Return enough rankings for the agent to understand the
        # complete ordering, while explicitly identifying the top three.
        top_shap = shap_df.head(10).copy()

        shap_drivers = []

        for _, row in top_shap.iterrows():

            shap_drivers.append(
                {
                    "rank": int(row["mean_abs_shap_rank"]),
                    "feature": str(row["feature"]),
                    "mean_abs_shap": float(row["mean_abs_shap"]),
                }
            )

        # Explicit top-three evidence.
        top_three = shap_drivers[:3]

        # ---------------------------------------------------------------
        # STRUCTURED EVIDENCE
        # ---------------------------------------------------------------

        evidence = {
            "analysis_type": "High-risk cluster evidence",

            "cluster_definition": (
                "The high-risk cluster is Cluster 2 as defined by "
                "the Phase 2 patient segmentation analysis."
            ),

            "population": {
                "total_dataset_records": total_population,
                "high_risk_population": population_size,
                "high_risk_percentage": round(
                    population_percentage,
                    2,
                ),
            },

            "clinical_utilization_profile": profile,

            "shap_analysis": {
                "source": "Phase 2 SHAP feature-importance artifact",
                "value_type": "mean absolute SHAP",
                "top_three": top_three,
                "top_ten": shap_drivers,
                "interpretation": (
                    "Mean absolute SHAP values measure the average "
                    "magnitude of a feature's contribution to the "
                    "model's predictions. They do not indicate whether "
                    "higher or lower feature values increase predicted "
                    "risk, and they do not establish causation."
                ),
                "direction_available": False,
                "causal_evidence_available": False,
            },

            "evidence_separation": {
                "observed_data": (
                    "Cluster population and cluster profile metrics "
                    "are descriptive statistics calculated from the "
                    "clustered dataset."
                ),
                "model_importance": (
                    "SHAP rankings describe feature contribution "
                    "magnitude within the readmission model."
                ),
                "causal_evidence": (
                    "No causal evidence is provided by this tool."
                ),
            },

            "recommendation_guidance": (
                "Business recommendations may use observed cluster "
                "characteristics as evidence for potential interventions. "
                "SHAP importance may identify areas worthy of further "
                "investigation, but SHAP importance alone must not be "
                "used to claim that changing a feature will reduce "
                "readmission, cost, or utilization."
            ),
        }

        return json.dumps(
            evidence,
            indent=2,
        )

    except Exception as exc:
        return f"ERROR analyzing high-risk cluster: {exc}"


# ---------------------------------------------------------------------------
# SHAP FEATURE IMPORTANCE
# ---------------------------------------------------------------------------

@tool
def get_shap_feature_importance(top_n: int = 10) -> str:
    """
    Return the actual numerical SHAP feature-importance rankings
    generated by the Phase 2 XGBoost model.

    The artifact contains mean absolute SHAP values.

    Use this when the user asks:
    - which variables drive readmission predictions
    - top model drivers
    - SHAP rankings
    - feature importance

    Important:
    These values provide magnitude/ranking only.
    They do not establish direction or causation.
    """

    if not SHAP_PATH.exists():
        return "ERROR: shap_feature_importance.csv was not found."

    try:
        top_n = max(
            1,
            min(
                int(top_n),
                44,
            ),
        )

        shap_df = pd.read_csv(SHAP_PATH)

        required_columns = {
            "feature",
            "mean_abs_shap_rank",
            "mean_abs_shap",
        }

        missing_columns = (
            required_columns - set(shap_df.columns)
        )

        if missing_columns:
            return (
                "ERROR: SHAP file is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        shap_df["mean_abs_shap_rank"] = pd.to_numeric(
            shap_df["mean_abs_shap_rank"],
            errors="coerce",
        )

        shap_df["mean_abs_shap"] = pd.to_numeric(
            shap_df["mean_abs_shap"],
            errors="coerce",
        )

        shap_df = shap_df.dropna(
            subset=[
                "mean_abs_shap_rank",
                "mean_abs_shap",
            ]
        )

        shap_df = shap_df.sort_values(
            "mean_abs_shap_rank"
        ).head(top_n)

        results = []

        for _, row in shap_df.iterrows():

            results.append(
                {
                    "rank": int(row["mean_abs_shap_rank"]),
                    "feature": str(row["feature"]),
                    "mean_abs_shap": float(row["mean_abs_shap"]),
                }
            )

        return json.dumps(
            {
                "source": "Phase 2 SHAP analysis",

                "value_type": "mean absolute SHAP",

                "features": results,

                "interpretation": (
                    "Higher mean absolute SHAP values indicate greater "
                    "average contribution magnitude to the model's "
                    "predictions. These values provide feature "
                    "importance/ranking only. They do not establish "
                    "whether higher or lower feature values increase "
                    "predicted risk and do not provide causal evidence."
                ),

                "direction_available": False,

                "causal_evidence_available": False,
            },
            indent=2,
        )

    except Exception as exc:
        return f"ERROR reading SHAP importance: {exc}"


# ---------------------------------------------------------------------------
# MODEL METADATA
# ---------------------------------------------------------------------------

@tool
def get_model_metadata() -> str:
    """
    Return metadata describing the trained Phase 2 readmission model,
    including its target, feature schema, evaluation metrics, and
    SHAP sample size.

    Use this when the user asks about:
    - model performance
    - model target
    - model features
    - training/evaluation information
    - model schema
    """

    if not METADATA_PATH.exists():
        return "ERROR: classification_metadata.json was not found."

    try:
        metadata = json.loads(
            METADATA_PATH.read_text(
                encoding="utf-8"
            )
        )

        return json.dumps(
            metadata,
            indent=2,
        )

    except Exception as exc:
        return f"ERROR reading model metadata: {exc}"


# ---------------------------------------------------------------------------
# INDIVIDUAL READMISSION PREDICTION
# ---------------------------------------------------------------------------

@tool
def predict_readmission_risk(
    patient_features_json: str,
) -> str:
    """
    Predict 30-day readmission probability using the trained Phase 2
    XGBoost model.

    Input must be JSON containing the model's expected feature names.

    The tool validates the supplied schema and does not silently invent
    missing clinical values.

    This tool should only be used when the required patient feature
    values are actually supplied by the user.
    """

    if not MODEL_PATH.exists():
        return "ERROR: classification_model.pkl was not found."

    try:
        model = joblib.load(MODEL_PATH)

        data = json.loads(
            patient_features_json
        )

        if not isinstance(data, dict):
            return (
                "ERROR: Input must be a JSON object of "
                "feature names and values."
            )

        if not hasattr(model, "feature_names_in_"):
            return (
                "ERROR: Trained model does not expose "
                "feature_names_in_. Prediction schema cannot "
                "be validated safely."
            )

        expected_features = list(
            model.feature_names_in_
        )

        supplied_features = set(
            data.keys()
        )

        expected_feature_set = set(
            expected_features
        )

        missing_features = sorted(
            expected_feature_set - supplied_features
        )

        unexpected_features = sorted(
            supplied_features - expected_feature_set
        )

        if missing_features:
            return json.dumps(
                {
                    "status": "validation_error",
                    "message": (
                        "Prediction requires all model features. "
                        "No missing features were automatically filled."
                    ),
                    "missing_features": missing_features,
                },
                indent=2,
            )

        if unexpected_features:
            return json.dumps(
                {
                    "status": "validation_error",
                    "message": (
                        "Input contains features not used by "
                        "the trained model."
                    ),
                    "unexpected_features": unexpected_features,
                },
                indent=2,
            )

        input_df = pd.DataFrame(
            [
                [
                    data[feature]
                    for feature in expected_features
                ]
            ],
            columns=expected_features,
        )

        prediction_probability = float(
            model.predict_proba(input_df)[0][1]
        )

        prediction = int(
            model.predict(input_df)[0]
        )

        return json.dumps(
            {
                "status": "success",

                "predicted_class": prediction,

                "predicted_30_day_readmission_probability": round(
                    prediction_probability,
                    6,
                ),

                "predicted_30_day_readmission_percentage": round(
                    prediction_probability * 100,
                    2,
                ),

                "model": "XGBoost classification model",

                "target": "IS_30DAY_READMISSION",

                "interpretation_note": (
                    "This is a model prediction for the supplied "
                    "feature values. It is not a diagnosis and does "
                    "not establish causation."
                ),
            },
            indent=2,
        )

    except json.JSONDecodeError:
        return (
            "ERROR: patient_features_json is not valid JSON."
        )

    except Exception as exc:
        return f"ERROR making readmission prediction: {exc}"


# ---------------------------------------------------------------------------
# TOOL COLLECTION
# ---------------------------------------------------------------------------

TOOLS = [
    analyze_high_risk_cluster,
    get_shap_feature_importance,
    get_model_metadata,
    predict_readmission_risk,
]