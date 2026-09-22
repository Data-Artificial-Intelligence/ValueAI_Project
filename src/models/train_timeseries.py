"""
Time-Series & Econometric Forecasting Model.

Matches JD:
"time-series analysis, econometrics, projections"

Methodology:
1. Aggregate inpatient claims into monthly healthcare costs.
2. Restrict the real dataset to complete 2008-2010 monthly observations.
3. Reserve the final 6 months as an out-of-sample holdout period.
4. Compare a naive baseline against an ARIMA model.
5. Evaluate using RMSE, MAE, and MAPE.
6. Refit the ARIMA model on the complete historical dataset.
7. Produce a 12-month forward forecast with 95% confidence intervals.
8. Save the trained model, forecast, evaluation metrics, and visualization.

This implementation intentionally avoids seasonal ARIMA because the available
historical series contains only 36 monthly observations. Estimating a full
12-month seasonal model with such a small sample can produce unstable
parameters and unreliable forecasts.
"""

import sys
import logging
import warnings
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "synpuf"
    / "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
)

DOCS_DIR = PROJECT_ROOT / "docs"
MODELS_DIR = PROJECT_ROOT / "models"

FORECAST_HORIZON = 12
HOLDOUT_MONTHS = 6

# ARIMA specification.
#
# With only 36 observations, a simple non-seasonal ARIMA is more defensible
# than a 12-month seasonal ARIMA.
ARIMA_ORDER = (1, 1, 1)


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_monthly_claim_costs():
    """
    Load and aggregate inpatient claims into monthly total costs.

    Returns
    -------
    pandas.DataFrame
        Columns:
            ds : monthly timestamp
            y  : total monthly claim cost
    """

    logger.info("Loading historical inpatient claims...")

    if not RAW_DATA_FILE.exists():
        logger.warning(
            "Raw inpatient claims not found. "
            "Using synthetic monthly data for demonstration."
        )

        dates = pd.date_range(
            start="2008-01-01",
            end="2010-12-01",
            freq="MS"
        )

        np.random.seed(42)

        # Synthetic data intentionally uses a moderate trend, annual
        # seasonality and random noise.
        trend = np.linspace(10_000_000, 15_000_000, len(dates))

        seasonality = (
            1_000_000
            * np.sin(
                2 * np.pi * np.arange(len(dates)) / 12
            )
        )

        noise = np.random.normal(
            loc=0,
            scale=300_000,
            size=len(dates)
        )

        monthly_costs = trend + seasonality + noise

        df = pd.DataFrame(
            {
                "ds": dates,
                "y": monthly_costs,
            }
        )

        return df

    logger.info("Reading raw inpatient claims CSV...")

    try:
        df_raw = pd.read_csv(RAW_DATA_FILE)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to read inpatient claims file: {exc}"
        ) from exc

    required_columns = [
        "CLM_ADMSN_DT",
        "CLM_PMT_AMT",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df_raw.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required columns missing from inpatient claims file: "
            + ", ".join(missing_columns)
        )

    logger.info(
        f"Raw inpatient claim records: {len(df_raw):,}"
    )

    # Convert admission date.
    df_raw["CLM_ADMSN_DT"] = pd.to_datetime(
        df_raw["CLM_ADMSN_DT"],
        format="%Y%m%d",
        errors="coerce"
    )

    # Convert payment amount to numeric.
    df_raw["CLM_PMT_AMT"] = pd.to_numeric(
        df_raw["CLM_PMT_AMT"],
        errors="coerce"
    )

    # Remove unusable records.
    df_raw = df_raw.dropna(
        subset=[
            "CLM_ADMSN_DT",
            "CLM_PMT_AMT",
        ]
    )

    logger.info(
        f"Usable claim records after cleaning: {len(df_raw):,}"
    )

    # Convert every admission date to month-start.
    df_raw["ds"] = (
        df_raw["CLM_ADMSN_DT"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Aggregate total monthly claim payments.
    df = (
        df_raw
        .groupby("ds", as_index=False)["CLM_PMT_AMT"]
        .sum()
        .rename(columns={"CLM_PMT_AMT": "y"})
        .sort_values("ds")
        .reset_index(drop=True)
    )

    # -----------------------------------------------------------------------
    # Important:
    #
    # The source contains Nov-Dec 2007 partial/ramp-up observations.
    # The intended analytical period is Jan 2008-Dec 2010.
    # -----------------------------------------------------------------------

    start_date = pd.Timestamp("2008-01-01")
    end_date = pd.Timestamp("2010-12-01")

    df = df[
        (df["ds"] >= start_date)
        & (df["ds"] <= end_date)
    ].copy()

    # Create a complete monthly index.
    expected_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="MS"
    )

    df = (
        df
        .set_index("ds")
        .reindex(expected_dates)
        .rename_axis("ds")
        .reset_index()
    )

    # Missing months indicate no recorded claims in that month.
    # For a monthly total-cost series, this is treated as zero.
    missing_months = df["y"].isna().sum()

    if missing_months > 0:
        logger.warning(
            f"Found {missing_months} missing monthly observations. "
            "Filling missing monthly costs with zero."
        )

        df["y"] = df["y"].fillna(0)

    # Validate final data.
    if len(df) < HOLDOUT_MONTHS + 12:
        raise ValueError(
            "Insufficient historical observations for time-series modeling."
        )

    if not np.isfinite(df["y"]).all():
        raise ValueError(
            "Monthly cost series contains non-finite values."
        )

    logger.info(
        f"Monthly time series: {len(df)} observations"
    )

    logger.info(
        f"Historical period: "
        f"{df['ds'].min().strftime('%Y-%m')} to "
        f"{df['ds'].max().strftime('%Y-%m')}"
    )

    logger.info(
        f"Monthly cost range: "
        f"${df['y'].min():,.2f} to ${df['y'].max():,.2f}"
    )

    return df


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def calculate_metrics(actual, predicted):
    """
    Calculate standard forecasting evaluation metrics.
    """

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    mae = mean_absolute_error(
        actual,
        predicted
    )

    # MAPE is undefined when actual values are zero.
    non_zero_mask = actual != 0

    if non_zero_mask.any():
        mape = (
            np.mean(
                np.abs(
                    (
                        actual[non_zero_mask]
                        - predicted[non_zero_mask]
                    )
                    / actual[non_zero_mask]
                )
            )
            * 100
        )
    else:
        mape = np.nan

    return {
        "RMSE": rmse,
        "MAE": mae,
        "MAPE": mape,
    }


# ---------------------------------------------------------------------------
# Model Training
# ---------------------------------------------------------------------------

def fit_arima(series):
    """
    Fit the configured ARIMA model.

    Warnings are suppressed during fitting because statsmodels can emit
    convergence warnings on small samples. The model fit itself is still
    checked for successful completion.
    """

    logger.info(
        f"Fitting ARIMA{ARIMA_ORDER}..."
    )

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=UserWarning
        )

        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning
        )

        fitted_model = ARIMA(
            series,
            order=ARIMA_ORDER
        ).fit()

    return fitted_model


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def run_timeseries():

    logger.info(
        "Starting Time-Series Forecasting Model..."
    )

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------------------------
    # 1. Load and prepare monthly data
    # -----------------------------------------------------------------------

    df = load_monthly_claim_costs()

    logger.info(
        f"Time series data shape: {df.shape}"
    )

    # -----------------------------------------------------------------------
    # 2. Holdout split
    #
    # Final 6 months are never used during model training.
    # This provides a genuine out-of-sample evaluation.
    # -----------------------------------------------------------------------

    train = df.iloc[:-HOLDOUT_MONTHS].copy()
    test = df.iloc[-HOLDOUT_MONTHS:].copy()

    logger.info(
        f"Training observations: {len(train)}"
    )

    logger.info(
        f"Holdout observations: {len(test)}"
    )

    logger.info(
        f"Training period: "
        f"{train['ds'].min().strftime('%Y-%m')} to "
        f"{train['ds'].max().strftime('%Y-%m')}"
    )

    logger.info(
        f"Holdout period: "
        f"{test['ds'].min().strftime('%Y-%m')} to "
        f"{test['ds'].max().strftime('%Y-%m')}"
    )

    # -----------------------------------------------------------------------
    # 3. Naive baseline
    #
    # Forecast every holdout month using the final observed training value.
    # This is important because ARIMA should demonstrate value beyond a
    # simple baseline.
    # -----------------------------------------------------------------------

    logger.info(
        "Evaluating naive last-value baseline..."
    )

    naive_prediction = np.repeat(
        train["y"].iloc[-1],
        len(test)
    )

    naive_metrics = calculate_metrics(
        test["y"],
        naive_prediction
    )

    logger.info(
        f"Naive Baseline RMSE: "
        f"${naive_metrics['RMSE']:,.2f}"
    )

    logger.info(
        f"Naive Baseline MAE: "
        f"${naive_metrics['MAE']:,.2f}"
    )

    logger.info(
        f"Naive Baseline MAPE: "
        f"{naive_metrics['MAPE']:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 4. Train ARIMA using only training data
    # -----------------------------------------------------------------------

    fitted_train_model = fit_arima(
        train["y"]
    )

    logger.info(
        "ARIMA model fitted successfully."
    )

    # -----------------------------------------------------------------------
    # 5. Forecast the holdout period
    # -----------------------------------------------------------------------

    logger.info(
        f"Generating {HOLDOUT_MONTHS}-month holdout forecast..."
    )

    holdout_forecast_result = (
        fitted_train_model.get_forecast(
            steps=HOLDOUT_MONTHS
        )
    )

    holdout_prediction = (
        holdout_forecast_result
        .predicted_mean
        .to_numpy()
    )

    # -----------------------------------------------------------------------
    # 6. Evaluate ARIMA
    # -----------------------------------------------------------------------

    arima_metrics = calculate_metrics(
        test["y"],
        holdout_prediction
    )

    logger.info(
        f"ARIMA Test RMSE: "
        f"${arima_metrics['RMSE']:,.2f}"
    )

    logger.info(
        f"ARIMA Test MAE: "
        f"${arima_metrics['MAE']:,.2f}"
    )

    logger.info(
        f"ARIMA Test MAPE: "
        f"{arima_metrics['MAPE']:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 7. Compare ARIMA against baseline
    # -----------------------------------------------------------------------

    if (
        np.isfinite(arima_metrics["RMSE"])
        and np.isfinite(naive_metrics["RMSE"])
        and naive_metrics["RMSE"] != 0
    ):
        rmse_improvement = (
            (
                naive_metrics["RMSE"]
                - arima_metrics["RMSE"]
            )
            / naive_metrics["RMSE"]
        ) * 100
    else:
        rmse_improvement = np.nan

    logger.info(
        f"ARIMA RMSE improvement vs naive baseline: "
        f"{rmse_improvement:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 8. Save evaluation metrics
    # -----------------------------------------------------------------------

    metrics_df = pd.DataFrame(
        [
            {
                "model": "Naive Last Value",
                "rmse": naive_metrics["RMSE"],
                "mae": naive_metrics["MAE"],
                "mape_percent": naive_metrics["MAPE"],
            },
            {
                "model": f"ARIMA{ARIMA_ORDER}",
                "rmse": arima_metrics["RMSE"],
                "mae": arima_metrics["MAE"],
                "mape_percent": arima_metrics["MAPE"],
            },
        ]
    )

    metrics_path = (
        DOCS_DIR
        / "timeseries_model_metrics.csv"
    )

    metrics_df.to_csv(
        metrics_path,
        index=False
    )

    logger.info(
        f"Saved evaluation metrics to {metrics_path}"
    )

    # -----------------------------------------------------------------------
    # 9. Create holdout evaluation dataset
    # -----------------------------------------------------------------------

    holdout_df = test[
        ["ds", "y"]
    ].copy()

    holdout_df["naive_forecast"] = naive_prediction
    holdout_df["arima_forecast"] = holdout_prediction

    holdout_path = (
        DOCS_DIR
        / "timeseries_holdout_evaluation.csv"
    )

    holdout_df.to_csv(
        holdout_path,
        index=False
    )

    logger.info(
        f"Saved holdout evaluation to {holdout_path}"
    )

    # -----------------------------------------------------------------------
    # 10. Refit ARIMA on ALL historical observations
    #
    # The holdout was only for honest evaluation.
    # Once evaluation is complete, we use all historical data to maximize
    # information available for the final production forecast.
    # -----------------------------------------------------------------------

    logger.info(
        "Refitting ARIMA on complete historical dataset..."
    )

    final_model = fit_arima(
        df["y"]
    )

    logger.info(
        "Final ARIMA model fitted successfully."
    )

    # -----------------------------------------------------------------------
    # 11. Generate 12-month future forecast
    # -----------------------------------------------------------------------

    logger.info(
        f"Generating {FORECAST_HORIZON}-month future forecast..."
    )

    forecast_result = (
        final_model.get_forecast(
            steps=FORECAST_HORIZON
        )
    )

    forecast_mean = (
        forecast_result
        .predicted_mean
        .to_numpy()
    )

    conf_int = (
        forecast_result
        .conf_int()
        .to_numpy()
    )

    forecast_dates = pd.date_range(
        start=(
            df["ds"].iloc[-1]
            + pd.DateOffset(months=1)
        ),
        periods=FORECAST_HORIZON,
        freq="MS"
    )

    forecast_df = pd.DataFrame(
        {
            "ds": forecast_dates,
            "forecast": forecast_mean,
            "lower_ci": conf_int[:, 0],
            "upper_ci": conf_int[:, 1],
        }
    )

    # Ensure forecasts cannot contain non-finite values.
    if not np.isfinite(
        forecast_df[
            [
                "forecast",
                "lower_ci",
                "upper_ci",
            ]
        ].to_numpy()
    ).all():

        raise ValueError(
            "Final forecast contains non-finite values."
        )

    # -----------------------------------------------------------------------
    # 12. Log forecast summary
    # -----------------------------------------------------------------------

    logger.info(
        "Future forecast summary:"
    )

    logger.info(
        f"Total projected cost over "
        f"{FORECAST_HORIZON} months: "
        f"${forecast_df['forecast'].sum():,.2f}"
    )

    logger.info(
        f"Average projected monthly cost: "
        f"${forecast_df['forecast'].mean():,.2f}"
    )

    logger.info(
        f"Minimum projected monthly cost: "
        f"${forecast_df['forecast'].min():,.2f}"
    )

    logger.info(
        f"Maximum projected monthly cost: "
        f"${forecast_df['forecast'].max():,.2f}"
    )

    # -----------------------------------------------------------------------
    # 13. Save forecast
    # -----------------------------------------------------------------------

    forecast_path = (
        DOCS_DIR
        / "timeseries_forecast.csv"
    )

    forecast_df.to_csv(
        forecast_path,
        index=False
    )

    logger.info(
        f"Saved forecast to {forecast_path}"
    )

    # -----------------------------------------------------------------------
    # 14. Create visualization
    # -----------------------------------------------------------------------

    logger.info(
        "Creating time-series forecast visualization..."
    )

    plt.figure(
        figsize=(14, 7)
    )

    # Complete historical series.
    plt.plot(
        df["ds"],
        df["y"],
        label="Historical Monthly Cost",
        linewidth=2
    )

    # Holdout actuals.
    plt.plot(
        test["ds"],
        test["y"],
        label="Holdout Actuals",
        linewidth=2
    )

    # Holdout ARIMA forecast.
    plt.plot(
        test["ds"],
        holdout_prediction,
        linestyle="--",
        label="ARIMA Holdout Forecast",
        linewidth=2
    )

    # Future forecast.
    plt.plot(
        forecast_df["ds"],
        forecast_df["forecast"],
        linestyle="--",
        label="12-Month Future Forecast",
        linewidth=2
    )

    # Future confidence interval.
    plt.fill_between(
        forecast_df["ds"],
        forecast_df["lower_ci"],
        forecast_df["upper_ci"],
        alpha=0.2,
        label="95% Confidence Interval"
    )

    # Separate historical data from future projection.
    plt.axvline(
        df["ds"].iloc[-1],
        linestyle=":",
        linewidth=2,
        label="Forecast Start"
    )

    plt.title(
        "Healthcare Monthly Cost Forecast - ARIMA"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Total Monthly Claim Cost ($)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plot_path = (
        DOCS_DIR
        / "timeseries_forecast.png"
    )

    plt.savefig(
        plot_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    logger.info(
        f"Saved time-series forecast plot to {plot_path}"
    )

    # -----------------------------------------------------------------------
    # 15. Save final model
    # -----------------------------------------------------------------------

    model_path = (
        MODELS_DIR
        / "timeseries_model.pkl"
    )

    joblib.dump(
        final_model,
        model_path
    )

    logger.info(
        f"Saved final ARIMA model to {model_path}"
    )

    # -----------------------------------------------------------------------
    # 16. Save model metadata
    #
    # This makes the artifact easier to understand if it is later moved
    # into an ML platform such as SageMaker.
    # -----------------------------------------------------------------------

    metadata = {
        "model_type": "ARIMA",
        "order": ARIMA_ORDER,
        "historical_start": df["ds"].min().strftime("%Y-%m-%d"),
        "historical_end": df["ds"].max().strftime("%Y-%m-%d"),
        "historical_observations": int(len(df)),
        "holdout_months": HOLDOUT_MONTHS,
        "forecast_horizon_months": FORECAST_HORIZON,
        "naive_rmse": float(naive_metrics["RMSE"]),
        "naive_mae": float(naive_metrics["MAE"]),
        "naive_mape_percent": float(naive_metrics["MAPE"]),
        "arima_rmse": float(arima_metrics["RMSE"]),
        "arima_mae": float(arima_metrics["MAE"]),
        "arima_mape_percent": float(arima_metrics["MAPE"]),
        "arima_rmse_improvement_vs_naive_percent": (
            float(rmse_improvement)
            if np.isfinite(rmse_improvement)
            else None
        ),
        "forecast_total": float(
            forecast_df["forecast"].sum()
        ),
        "forecast_average_monthly": float(
            forecast_df["forecast"].mean()
        ),
    }

    metadata_path = (
        DOCS_DIR
        / "timeseries_model_metadata.json"
    )

    import json

    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2
        )

    logger.info(
        f"Saved model metadata to {metadata_path}"
    )

    # -----------------------------------------------------------------------
    # 17. Final status
    # -----------------------------------------------------------------------

    logger.info(
        "Time-Series Forecasting Complete."
    )

    logger.info(
        "Outputs generated:"
    )

    logger.info(
        f"  Model: {model_path}"
    )

    logger.info(
        f"  Forecast: {forecast_path}"
    )

    logger.info(
        f"  Evaluation metrics: {metrics_path}"
    )

    logger.info(
        f"  Holdout predictions: {holdout_path}"
    )

    logger.info(
        f"  Plot: {plot_path}"
    )

    logger.info(
        f"  Metadata: {metadata_path}"
    )


if __name__ == "__main__":
    run_timeseries()