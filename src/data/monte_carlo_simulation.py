
"""
Monte Carlo simulation for cost uncertainty modeling.

Matches JD:
"build econometric and statistical models... simulations"

The simulation fits a log-normal distribution to positive historical
healthcare costs and projects future monthly costs with uncertainty bounds.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from src.utils.logger import get_logger


logger = get_logger(__name__)


def run_monte_carlo_projection(
    n_simulations: int = 10_000,
    projection_horizon_months: int = 12,
    confidence_level: float = 0.95,
    output_path: Path = None
) -> dict:
    """
    Run Monte Carlo simulation to project future healthcare costs.

    Historical positive admission costs are modeled using a log-normal
    distribution. Non-positive costs are excluded because a log-normal
    distribution is defined only for positive values.
    """

    # -------------------------------------------------------------------------
    # OUTPUT PATH
    # -------------------------------------------------------------------------
    if output_path is None:
        output_path = (
            Path(__file__).parents[2]
            / "data"
            / "processed"
        )

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # -------------------------------------------------------------------------
    # LOAD HISTORICAL DATA
    # -------------------------------------------------------------------------
    logger.info("Loading historical admission costs...")

    df = pd.read_parquet(
        output_path / "full_dataset.parquet"
    )

    if "AVG_ADMISSION_COST" not in df.columns:
        raise ValueError(
            "AVG_ADMISSION_COST column not found in full_dataset.parquet"
        )

    historical_costs = (
        pd.to_numeric(
            df["AVG_ADMISSION_COST"],
            errors="coerce"
        )
        .dropna()
        .to_numpy()
    )

    if len(historical_costs) == 0:
        raise ValueError(
            "No historical cost data available for simulation"
        )

    # -------------------------------------------------------------------------
    # VALIDATE HISTORICAL COSTS
    # -------------------------------------------------------------------------
    total_cost_records = len(historical_costs)

    non_positive_mask = historical_costs <= 0
    non_positive_count = int(
        np.sum(non_positive_mask)
    )

    positive_costs = historical_costs[
        ~non_positive_mask
    ]

    logger.info(
        f"Historical cost records: {total_cost_records:,}"
    )

    logger.info(
        f"Non-positive cost records excluded: {non_positive_count:,}"
    )

    logger.info(
        f"Positive cost records used for fitting: {len(positive_costs):,}"
    )

    if len(positive_costs) < 10:
        raise ValueError(
            "Fewer than 10 positive historical cost observations "
            "are available for fitting the log-normal distribution."
        )

    # -------------------------------------------------------------------------
    # FIT LOG-NORMAL DISTRIBUTION
    # -------------------------------------------------------------------------
    #
    # Log-normal modeling requires strictly positive values.
    #
    log_costs = np.log(
        positive_costs
    )

    mu = float(
        np.mean(log_costs)
    )

    sigma = float(
        np.std(log_costs)
    )

    if not np.isfinite(mu) or not np.isfinite(sigma):
        raise ValueError(
            "Invalid log-normal parameters. "
            f"mu={mu}, sigma={sigma}"
        )

    if sigma <= 0:
        raise ValueError(
            "Log-normal standard deviation is zero. "
            "Historical costs do not contain enough variation."
        )

    logger.info(
        f"Fitted log-normal distribution: "
        f"mu={mu:.4f}, sigma={sigma:.4f}"
    )

    # -------------------------------------------------------------------------
    # MONTE CARLO SIMULATION
    # -------------------------------------------------------------------------
    logger.info(
        f"Running {n_simulations:,} simulations "
        f"over {projection_horizon_months} months..."
    )

    np.random.seed(42)

    all_projections = np.zeros(
        (
            n_simulations,
            projection_horizon_months
        )
    )

    # Healthcare cost trend assumption:
    # approximately 5% annual growth.
    trend = np.linspace(
        1.0,
        1.05,
        projection_horizon_months
    )

    for sim in range(n_simulations):

        monthly_costs = np.random.lognormal(
            mean=mu,
            sigma=sigma,
            size=projection_horizon_months
        )

        all_projections[sim] = (
            monthly_costs * trend
        )

    # -------------------------------------------------------------------------
    # CALCULATE PROJECTION STATISTICS
    # -------------------------------------------------------------------------
    mean_projection = np.mean(
        all_projections,
        axis=0
    )

    lower_percentile = (
        (1 - confidence_level)
        / 2
        * 100
    )

    upper_percentile = (
        (1 + confidence_level)
        / 2
        * 100
    )

    lower_bound = np.percentile(
        all_projections,
        lower_percentile,
        axis=0
    )

    upper_bound = np.percentile(
        all_projections,
        upper_percentile,
        axis=0
    )

    total_cost_mean = float(
        np.sum(mean_projection)
    )

    total_cost_ci = (
        float(np.sum(lower_bound)),
        float(np.sum(upper_bound))
    )

    # -------------------------------------------------------------------------
    # RESULTS
    # -------------------------------------------------------------------------
    results = {
        "mean_monthly_projection":
            mean_projection.tolist(),

        "lower_bound":
            lower_bound.tolist(),

        "upper_bound":
            upper_bound.tolist(),

        "total_cost_mean":
            total_cost_mean,

        "total_cost_ci_lower":
            total_cost_ci[0],

        "total_cost_ci_upper":
            total_cost_ci[1],

        "n_simulations":
            n_simulations,

        "projection_horizon_months":
            projection_horizon_months,

        "confidence_level":
            confidence_level,

        "log_normal_mu":
            mu,

        "log_normal_sigma":
            sigma,

        "historical_cost_records":
            total_cost_records,

        "excluded_non_positive_costs":
            non_positive_count,

        "positive_cost_records_used":
            len(positive_costs),
    }

    # -------------------------------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------------------------------
    results_df = pd.DataFrame(
        {
            "mean_monthly_projection":
                mean_projection,

            "lower_bound":
                lower_bound,

            "upper_bound":
                upper_bound,
        }
    )

    results_df.to_json(
        output_path / "monte_carlo_results.json",
        orient="index"
    )

    # -------------------------------------------------------------------------
    # PLOT
    # -------------------------------------------------------------------------
    months = np.arange(
        1,
        projection_horizon_months + 1
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        months,
        mean_projection,
        linewidth=2,
        label="Mean Projection"
    )

    plt.fill_between(
        months,
        lower_bound,
        upper_bound,
        alpha=0.3,
        label=(
            f"{int(confidence_level * 100)}% "
            "Confidence Interval"
        )
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Projected Cost ($)"
    )

    plt.title(
        f"Monte Carlo Cost Projection "
        f"({n_simulations:,} Simulations)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        output_path / "monte_carlo_projection.png",
        dpi=150
    )

    plt.close()

    # -------------------------------------------------------------------------
    # FINAL LOGGING
    # -------------------------------------------------------------------------
    logger.info(
        "Monte Carlo simulation complete"
    )

    logger.info(
        f"Total projected cost: "
        f"${total_cost_mean:,.2f}"
    )

    logger.info(
        f"{int(confidence_level * 100)}% CI: "
        f"(${total_cost_ci[0]:,.2f}, "
        f"${total_cost_ci[1]:,.2f})"
    )

    return results


if __name__ == "__main__":
    run_monte_carlo_projection()

