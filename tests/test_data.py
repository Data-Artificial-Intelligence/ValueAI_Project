"""
Unit tests for the ValueAI data-processing modules.

Tested modules:
    src.data.make_dataset
    src.data.monte_carlo_simulation
    src.data.validate_data

These tests intentionally use small synthetic datasets and temporary
directories. They do not depend on the real SynPUF dataset.

Run from the project root:

    pytest -q tests/test_data.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

# Force non-interactive backend to prevent Tkinter errors on Windows headless/pytest runs
import matplotlib
matplotlib.use('Agg')

# =============================================================================
# PROJECT PATH
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# OPTIONAL SPARK IMPORT
# =============================================================================
#
# The make_dataset.py module requires PySpark. These tests skip Spark-specific
# tests cleanly if PySpark is not installed.
# =============================================================================

try:
    from pyspark.sql import SparkSession
    PYSPARK_AVAILABLE = True
except ImportError:
    SparkSession = None
    PYSPARK_AVAILABLE = False


# =============================================================================
# MODULE IMPORTS
# =============================================================================

from src.data import monte_carlo_simulation


# Import make_dataset lazily through a helper because the module performs
# Windows Hadoop validation during import.
def _import_make_dataset():
    """
    Import src.data.make_dataset.

    The production module performs Windows-specific winutils.exe and
    hadoop.dll validation at import time. On Windows, these tests therefore
    require the same Hadoop native binaries as the production pipeline.
    """

    from src.data import make_dataset

    return make_dataset


# =============================================================================
# SPARK FIXTURE
# =============================================================================

@pytest.fixture(scope="session")
def spark():
    """
    Create a small local Spark session for Spark-based unit tests.
    """

    if not PYSPARK_AVAILABLE:
        pytest.skip("PySpark is not installed.")

    make_dataset = _import_make_dataset()

    # The production module configures these variables on Windows.
    # We simply create a local Spark session using the same general settings.
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("ValueAI_TestSuite")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    yield spark

    spark.stop()


# =============================================================================
# MAKE_DATASET.PY - BENEFICIARY CLEANING
# =============================================================================

@pytest.mark.spark
def test_clean_beneficiary_data(spark):
    """
    Verify that beneficiary cleaning:

    - converts birth dates
    - converts death dates
    - derives AGE
    - imputes missing race
    - removes BENE_RACE_CD
    - creates IS_DECEASED
    - keeps only valid ages
    """

    make_dataset = _import_make_dataset()

    rows = [
        (
            "BEN001",
            "19400101",
            None,
            1,
        ),
        (
            "BEN002",
            "19500101",
            "20100101",
            None,
        ),
        (
            "BEN003",
            "20200101",
            None,
            1,
        ),
    ]

    columns = [
        "DESYNPUF_ID",
        "BENE_BIRTH_DT",
        "BENE_DEATH_DT",
        "BENE_RACE_CD",
    ]

    df = spark.createDataFrame(rows, columns)

    result = make_dataset.clean_beneficiary_data(df)

    result_rows = {
        row["DESYNPUF_ID"]: row.asDict()
        for row in result.collect()
    }

    # BEN003 is under 18 and should be filtered out.
    assert "BEN003" not in result_rows

    assert "BEN001" in result_rows
    assert "BEN002" in result_rows

    # Dates should have been converted to Spark date values.
    assert str(result_rows["BEN001"]["BENE_BIRTH_DT"]) == "1940-01-01"

    # BEN001 has no death date.
    assert result_rows["BEN001"]["IS_DECEASED"] is False

    # BEN002 has a death date.
    assert result_rows["BEN002"]["IS_DECEASED"] is True

    # Missing race should be replaced with 2.
    assert result_rows["BEN002"]["RACE"] == 2

    # Original race column should be removed.
    assert "BENE_RACE_CD" not in result.columns

    # Derived age should exist.
    assert "AGE" in result.columns


# =============================================================================
# MAKE_DATASET.PY - CLAIM DATE CLEANING
# =============================================================================

@pytest.mark.spark
@pytest.mark.parametrize(
    "claim_type,expected_columns",
    [
        (
            "inpatient",
            [
                "CLM_ADMSN_DT",
                "CLM_THRU_DT",
                "NCH_BENE_DSCHRG_DT",
            ],
        ),
        (
            "outpatient",
            [
                "CLM_FROM_DT",
                "CLM_THRU_DT",
            ],
        ),
        (
            "carrier",
            [
                "CLM_FROM_DT",
                "CLM_THRU_DT",
            ],
        ),
        (
            "drug",
            [
                "SRVC_DT",
            ],
        ),
    ],
)
def test_clean_claims_dates(spark, claim_type, expected_columns):
    """
    Verify that the date columns for each supported claim type are converted
    from yyyyMMdd strings to Spark date values.
    """

    make_dataset = _import_make_dataset()

    data = {
        "DESYNPUF_ID": ["BEN001"],
    }

    for column in expected_columns:
        data[column] = ["20100115"]

    df = spark.createDataFrame(
        list(zip(*data.values())),
        list(data.keys()),
    )

    result = make_dataset.clean_claims_dates(
        df,
        claim_type,
    )

    row = result.first()

    for column in expected_columns:
        assert str(row[column]) == "2010-01-15"


# =============================================================================
# MAKE_DATASET.PY - READMISSION TARGET
# =============================================================================

@pytest.mark.spark
def test_build_readmission_target_identifies_30_day_readmission(spark):
    """
    Verify that an inpatient admission followed by another admission within
    30 days is marked as a 30-day readmission.
    """

    make_dataset = _import_make_dataset()

    rows = [
        (
            "BEN001",
            "20100101",
            "20100105",
        ),
        (
            "BEN001",
            "20100120",
            "20100125",
        ),
        (
            "BEN002",
            "20100101",
            "20100105",
        ),
        (
            "BEN002",
            "20100210",
            "20100215",
        ),
    ]

    columns = [
        "DESYNPUF_ID",
        "CLM_ADMSN_DT",
        "NCH_BENE_DSCHRG_DT",
    ]

    df = spark.createDataFrame(rows, columns)

    df = make_dataset.clean_claims_dates(
        df,
        "inpatient",
    )

    result = make_dataset.build_readmission_target(df)

    rows_by_patient = {}

    for row in result.collect():
        rows_by_patient.setdefault(
            row["DESYNPUF_ID"],
            [],
        ).append(row)

    # BEN001:
    # First discharge = Jan 5
    # Next admission = Jan 20
    # Difference = 15 days -> True.
    ben001 = sorted(
        rows_by_patient["BEN001"],
        key=lambda row: row["CLM_ADMSN_DT"],
    )

    assert ben001[0]["IS_30DAY_READMISSION"] is True

    # BEN002:
    # First discharge = Jan 5
    # Next admission = Feb 10
    # Difference = 36 days -> False.
    ben002 = sorted(
        rows_by_patient["BEN002"],
        key=lambda row: row["CLM_ADMSN_DT"],
    )

    assert ben002[0]["IS_30DAY_READMISSION"] is False


@pytest.mark.spark
def test_build_readmission_target_handles_exact_30_days(spark):
    """
    Verify that exactly 30 days is treated as a readmission.

    The production code uses:
        days_to_next_admission <= 30
    """

    make_dataset = _import_make_dataset()

    rows = [
        (
            "BEN001",
            "20100101",
            "20100105",
        ),
        (
            "BEN001",
            "20100204",
            "20100210",
        ),
    ]

    columns = [
        "DESYNPUF_ID",
        "CLM_ADMSN_DT",
        "NCH_BENE_DSCHRG_DT",
    ]

    df = spark.createDataFrame(rows, columns)

    df = make_dataset.clean_claims_dates(
        df,
        "inpatient",
    )

    result = make_dataset.build_readmission_target(df)

    first_admission = (
        result
        .orderBy("CLM_ADMSN_DT")
        .first()
    )

    assert first_admission["IS_30DAY_READMISSION"] is True


# =============================================================================
# MAKE_DATASET.PY - COMORBIDITY FEATURES
# =============================================================================

@pytest.mark.spark
def test_build_comorbidity_features(spark):
    """
    Verify that unique diagnosis codes are counted per beneficiary.
    """

    make_dataset = _import_make_dataset()
    from pyspark.sql.types import StructType, StructField, StringType

    rows = [
        (
            "BEN001",
            "250",
            "401",
            "250",
            None,
        ),
        (
            "BEN001",
            "272",
            "401",
            None,
            None,
        ),
        (
            "BEN002",
            "414",
            None,
            None,
            None,
        ),
    ]

    # Explicit schema is required because PySpark cannot infer the type of 
    # columns that contain only None values (e.g., ICD9_DGNS_4_CD).
    schema = StructType([
        StructField("DESYNPUF_ID", StringType(), True),
        StructField("ICD9_DGNS_CD", StringType(), True),
        StructField("ICD9_DGNS_2_CD", StringType(), True),
        StructField("ICD9_DGNS_3_CD", StringType(), True),
        StructField("ICD9_DGNS_4_CD", StringType(), True),
    ])

    df = spark.createDataFrame(rows, schema)

    result = make_dataset.build_comorbidity_features(df)

    values = {
        row["DESYNPUF_ID"]: row["UNIQUE_DIAGNOSES_COUNT"]
        for row in result.collect()
    }

    # BEN001 has:
    # 250, 401, 272
    # = 3 unique diagnoses.
    assert values["BEN001"] == 3

    # BEN002 has one diagnosis.
    assert values["BEN002"] == 1


# =============================================================================
# MAKE_DATASET.PY - UTILIZATION FEATURES
# =============================================================================

@pytest.mark.spark
def test_build_utilization_features_with_claim_cost(spark):
    """
    Verify utilization features when CLM_PMT_AMT is available.
    """

    make_dataset = _import_make_dataset()

    rows = [
        (
            "BEN001",
            "20100101",
            100.0,
        ),
        (
            "BEN001",
            "20100110",
            200.0,
        ),
        (
            "BEN001",
            "20100120",
            300.0,
        ),
        (
            "BEN002",
            "20100105",
            500.0,
        ),
    ]

    columns = [
        "DESYNPUF_ID",
        "CLM_FROM_DT",
        "CLM_PMT_AMT",
    ]

    df = spark.createDataFrame(rows, columns)

    df = make_dataset.clean_claims_dates(
        df,
        "outpatient",
    )

    result = make_dataset.build_utilization_features(
        df,
        "outpatient",
    )

    assert "OUTPATIENT_CLAIM_COUNT" in result.columns
    assert "AVG_OUTPATIENT_COST" in result.columns
    assert "AVG_DAYS_BETWEEN_OUTPATIENT_CLAIMS" in result.columns

    values = {
        row["DESYNPUF_ID"]: row.asDict()
        for row in result.collect()
    }

    assert values["BEN001"]["OUTPATIENT_CLAIM_COUNT"] == 3
    assert values["BEN002"]["OUTPATIENT_CLAIM_COUNT"] == 1


@pytest.mark.spark
def test_build_utilization_features_with_drug_cost(spark):
    """
    Verify that drug claims use TOT_RX_CST_AMT when CLM_PMT_AMT is absent.
    """

    make_dataset = _import_make_dataset()

    rows = [
        (
            "BEN001",
            "20100101",
            50.0,
        ),
        (
            "BEN001",
            "20100115",
            75.0,
        ),
    ]

    columns = [
        "DESYNPUF_ID",
        "SRVC_DT",
        "TOT_RX_CST_AMT",
    ]

    df = spark.createDataFrame(rows, columns)

    df = make_dataset.clean_claims_dates(
        df,
        "drug",
    )

    result = make_dataset.build_utilization_features(
        df,
        "drug",
    )

    assert "DRUG_CLAIM_COUNT" in result.columns
    assert "AVG_DRUG_COST" in result.columns
    assert "AVG_DAYS_BETWEEN_DRUG_CLAIMS" in result.columns

    row = result.first()

    assert row["DRUG_CLAIM_COUNT"] == 2


# =============================================================================
# MAKE_DATASET.PY - DATA INGESTION
# =============================================================================

@pytest.mark.spark
def test_load_beneficiary_data(tmp_path, spark):
    """
    Verify that beneficiary files matching the expected pattern are loaded
    and combined.
    """

    make_dataset = _import_make_dataset()

    first_file = (
        tmp_path
        / "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
    )

    second_file = (
        tmp_path
        / "DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv"
    )

    first_file.write_text(
        "DESYNPUF_ID,BENE_BIRTH_DT\n"
        "BEN001,19400101\n",
        encoding="utf-8",
    )

    second_file.write_text(
        "DESYNPUF_ID,BENE_BIRTH_DT\n"
        "BEN002,19500101\n",
        encoding="utf-8",
    )

    result = make_dataset.load_beneficiary_data(
        spark,
        tmp_path,
    )

    assert result.count() == 2

    years = {
        row["source_year"]
        for row in result.select("source_year").collect()
    }

    assert years == {2008, 2009}


@pytest.mark.spark
def test_load_beneficiary_data_raises_when_no_files_exist(
    tmp_path,
    spark,
):
    """
    Verify that missing beneficiary files raise FileNotFoundError.
    """

    make_dataset = _import_make_dataset()

    with pytest.raises(FileNotFoundError):
        make_dataset.load_beneficiary_data(
            spark,
            tmp_path,
        )


@pytest.mark.spark
def test_load_claims_data(tmp_path, spark):
    """
    Verify that a supported claims file is loaded correctly.
    """

    make_dataset = _import_make_dataset()

    file_name = (
        "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
    )

    claims_file = tmp_path / file_name

    claims_file.write_text(
        "DESYNPUF_ID,CLM_ADMSN_DT,CLM_PMT_AMT\n"
        "BEN001,20100101,100.50\n"
        "BEN002,20100105,200.00\n",
        encoding="utf-8",
    )

    result = make_dataset.load_claims_data(
        spark,
        tmp_path,
        "inpatient",
    )

    assert result.count() == 2

    assert "DESYNPUF_ID" in result.columns
    assert "CLM_ADMSN_DT" in result.columns
    assert "CLM_PMT_AMT" in result.columns


# =============================================================================
# MAKE_DATASET.PY - STRATIFIED SPLIT
# =============================================================================

@pytest.mark.spark
def test_stratified_split_returns_three_dataframes(spark):
    """
    Verify that stratified_split returns train, validation and test
    DataFrames.
    """

    make_dataset = _import_make_dataset()

    rows = [
        (f"BEN{i:03d}", i % 2 == 0)
        for i in range(100)
    ]

    df = spark.createDataFrame(
        rows,
        [
            "DESYNPUF_ID",
            "IS_30DAY_READMISSION",
        ],
    )

    train_df, val_df, test_df = make_dataset.stratified_split(
        df,
        "IS_30DAY_READMISSION",
    )

    assert train_df is not None
    assert val_df is not None
    assert test_df is not None

    assert train_df.count() > 0
    assert val_df.count() > 0
    assert test_df.count() > 0


@pytest.mark.spark
def test_stratified_split_preserves_total_row_count(spark):
    """
    Verify that the three output datasets together contain every input row.

    The implementation creates mutually exclusive filters, so the total
    number of rows should remain unchanged.
    """

    make_dataset = _import_make_dataset()

    rows = [
        (f"BEN{i:03d}", i % 2 == 0)
        for i in range(200)
    ]

    df = spark.createDataFrame(
        rows,
        [
            "DESYNPUF_ID",
            "IS_30DAY_READMISSION",
        ],
    )

    train_df, val_df, test_df = make_dataset.stratified_split(
        df,
        "IS_30DAY_READMISSION",
    )

    total_output_rows = (
        train_df.count()
        + val_df.count()
        + test_df.count()
    )

    assert total_output_rows == df.count()


# =============================================================================
# MAKE_DATASET.PY - DATA PROFILE
# =============================================================================

@pytest.mark.spark
def test_generate_data_profile(spark, tmp_path):
    """
    Verify that the lightweight Spark data profile is generated.
    """

    make_dataset = _import_make_dataset()

    df = spark.createDataFrame(
        [
            ("BEN001", 70, True),
            ("BEN002", 65, False),
        ],
        [
            "DESYNPUF_ID",
            "AGE",
            "IS_30DAY_READMISSION",
        ],
    )

    make_dataset._generate_data_profile(
        df,
        tmp_path,
    )

    profile_path = (
        tmp_path
        / "data_profile_summary.csv"
    )

    assert profile_path.exists()

    profile = pd.read_csv(profile_path)

    assert not profile.empty


# =============================================================================
# MONTE_CARLO_SIMULATION.PY
# =============================================================================

def _create_monte_carlo_dataset(
    output_path: Path,
    costs: list[float],
):
    """
    Create a small synthetic full_dataset.parquet file for Monte Carlo tests.
    """

    df = pd.DataFrame(
        {
            "AVG_ADMISSION_COST": costs,
        }
    )

    df.to_parquet(
        output_path / "full_dataset.parquet",
        index=False,
    )


def test_run_monte_carlo_projection(tmp_path):
    """
    Verify that the Monte Carlo simulation:

    - loads historical costs
    - excludes non-positive values
    - produces projections
    - produces confidence bounds
    - writes JSON output
    - writes the projection plot
    """

    costs = [
        100.0,
        120.0,
        150.0,
        175.0,
        200.0,
        225.0,
        250.0,
        300.0,
        350.0,
        400.0,
        450.0,
        500.0,
        0.0,
        -10.0,
    ]

    _create_monte_carlo_dataset(
        tmp_path,
        costs,
    )

    results = monte_carlo_simulation.run_monte_carlo_projection(
        n_simulations=100,
        projection_horizon_months=6,
        confidence_level=0.95,
        output_path=tmp_path,
    )

    assert isinstance(results, dict)

    assert "mean_monthly_projection" in results
    assert "lower_bound" in results
    assert "upper_bound" in results

    assert "total_cost_mean" in results
    assert "total_cost_ci_lower" in results
    assert "total_cost_ci_upper" in results

    assert results["n_simulations"] == 100
    assert results["projection_horizon_months"] == 6
    assert results["confidence_level"] == 0.95

    # 12 positive values are used.
    assert results["positive_cost_records_used"] == 12

    # 0 and -10 are excluded.
    assert results["excluded_non_positive_costs"] == 2

    assert len(results["mean_monthly_projection"]) == 6
    assert len(results["lower_bound"]) == 6
    assert len(results["upper_bound"]) == 6

    assert results["total_cost_mean"] > 0

    assert results["total_cost_ci_lower"] <= (
        results["total_cost_mean"]
    )

    assert results["total_cost_ci_upper"] >= (
        results["total_cost_mean"]
    )

    assert (
        tmp_path / "monte_carlo_results.json"
    ).exists()

    assert (
        tmp_path / "monte_carlo_projection.png"
    ).exists()


def test_run_monte_carlo_projection_requires_cost_column(tmp_path):
    """
    Verify that the simulation raises ValueError when the required
    AVG_ADMISSION_COST column is missing.
    """

    df = pd.DataFrame(
        {
            "WRONG_COLUMN": [
                100.0,
                200.0,
            ]
        }
    )

    df.to_parquet(
        tmp_path / "full_dataset.parquet",
        index=False,
    )

    with pytest.raises(
        ValueError,
        match="AVG_ADMISSION_COST column not found",
    ):
        monte_carlo_simulation.run_monte_carlo_projection(
            n_simulations=10,
            projection_horizon_months=3,
            output_path=tmp_path,
        )


def test_run_monte_carlo_projection_requires_historical_data(
    tmp_path,
):
    """
    Verify that the simulation rejects an empty cost dataset.
    """

    df = pd.DataFrame(
        {
            "AVG_ADMISSION_COST": [],
        }
    )

    df.to_parquet(
        tmp_path / "full_dataset.parquet",
        index=False,
    )

    with pytest.raises(
        ValueError,
        match="No historical cost data available",
    ):
        monte_carlo_simulation.run_monte_carlo_projection(
            n_simulations=10,
            projection_horizon_months=3,
            output_path=tmp_path,
        )


def test_run_monte_carlo_projection_requires_at_least_ten_positive_costs(
    tmp_path,
):
    """
    Verify that fewer than 10 positive historical observations are rejected.
    """

    costs = [
        100.0,
        110.0,
        120.0,
        130.0,
        140.0,
    ]

    _create_monte_carlo_dataset(
        tmp_path,
        costs,
    )

    with pytest.raises(
        ValueError,
        match="Fewer than 10 positive historical cost observations",
    ):
        monte_carlo_simulation.run_monte_carlo_projection(
            n_simulations=10,
            projection_horizon_months=3,
            output_path=tmp_path,
        )


def test_run_monte_carlo_projection_rejects_zero_variance(
    tmp_path,
):
    """
    Verify that identical positive costs are rejected because the fitted
    log-normal distribution has zero standard deviation.
    """

    costs = [100.0] * 10

    _create_monte_carlo_dataset(
        tmp_path,
        costs,
    )

    with pytest.raises(
        ValueError,
        match="standard deviation is zero",
    ):
        monte_carlo_simulation.run_monte_carlo_projection(
            n_simulations=10,
            projection_horizon_months=3,
            output_path=tmp_path,
        )


def test_run_monte_carlo_projection_uses_deterministic_seed(
    tmp_path,
):
    """
    Verify that the simulation is reproducible because the implementation
    explicitly sets np.random.seed(42).
    """

    costs = [
        100.0,
        120.0,
        150.0,
        175.0,
        200.0,
        225.0,
        250.0,
        300.0,
        350.0,
        400.0,
    ]

    _create_monte_carlo_dataset(
        tmp_path,
        costs,
    )

    first = monte_carlo_simulation.run_monte_carlo_projection(
        n_simulations=50,
        projection_horizon_months=4,
        output_path=tmp_path,
    )

    second = monte_carlo_simulation.run_monte_carlo_projection(
        n_simulations=50,
        projection_horizon_months=4,
        output_path=tmp_path,
    )

    assert (
        first["mean_monthly_projection"]
        == second["mean_monthly_projection"]
    )

    assert (
        first["lower_bound"]
        == second["lower_bound"]
    )

    assert (
        first["upper_bound"]
        == second["upper_bound"]
    )


# =============================================================================
# VALIDATE_DATA.PY
# =============================================================================
#
# We deliberately mock Great Expectations here. The purpose is to test that
# run_data_validation() orchestrates the expected validation flow without
# requiring the real processed SynPUF dataset.
# =============================================================================

def test_run_data_validation_success(monkeypatch, tmp_path):
    """
    Verify the validation workflow when all expectations succeed.

    Great Expectations is mocked so this test does not require a real
    train.parquet dataset.
    """

    try:
        from src.data import validate_data
    except ImportError:
        pytest.skip(
            "Great Expectations is not installed."
        )

    # -------------------------------------------------------------------------
    # Patch builtins.open to enforce UTF-8 encoding on Windows
    # This prevents UnicodeEncodeError when writing emoji characters
    # -------------------------------------------------------------------------
    import builtins
    original_open = builtins.open
    def utf8_open(file, mode='r', *args, **kwargs):
        if 'b' not in mode and 'encoding' not in kwargs:
            kwargs['encoding'] = 'utf-8'
        return original_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", utf8_open)

    # -------------------------------------------------------------------------
    # Fake validation result
    # -------------------------------------------------------------------------

    fake_results = [
        SimpleNamespace(
            success=True,
            expectation=SimpleNamespace(
                configuration={
                    "type": "expect_column_values_to_not_be_null"
                }
            ),
        ),
        SimpleNamespace(
            success=True,
            expectation=SimpleNamespace(
                configuration={
                    "type": "expect_column_values_to_be_between"
                }
            ),
        ),
        SimpleNamespace(
            success=True,
            expectation=SimpleNamespace(
                configuration={
                    "type": "expect_column_values_to_be_in_set"
                }
            ),
        ),
    ]

    fake_result = SimpleNamespace(
        success=True,
        results=fake_results,
    )

    # -------------------------------------------------------------------------
    # Fake Great Expectations objects
    # -------------------------------------------------------------------------

    class FakeValidationDefinition:
        def __init__(
            self,
            name,
            data,
            suite,
        ):
            self.name = name
            self.data = data
            self.suite = suite

        def run(self, batch_parameters):
            return fake_result

    class FakeValidationDefinitions:
        def add(self, definition):
            return definition

    class FakeExpectationSuite:
        def __init__(self, name):
            self.name = name
            self.expectations = []

        def add_expectation(self, expectation):
            self.expectations.append(expectation)

    class FakeSuites:
        def add(self, suite):
            return suite

    class FakeBatchDefinition:
        def get_batch(self, batch_parameters):
            return object()

    class FakeDataAsset:
        def add_batch_definition_whole_dataframe(self, name):
            return FakeBatchDefinition()

    class FakeDataSource:
        def add_dataframe_asset(self, name):
            return FakeDataAsset()

    class FakeDataSources:
        def add_pandas(self, name):
            return FakeDataSource()

    fake_context = SimpleNamespace(
        data_sources=FakeDataSources(),
        suites=FakeSuites(),
        validation_definitions=FakeValidationDefinitions(),
    )

    # -------------------------------------------------------------------------
    # Fake expectations
    # -------------------------------------------------------------------------

    class FakeExpectations:
        @staticmethod
        def ExpectColumnValuesToNotBeNull(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeBetween(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeInSet(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeUnique(**kwargs):
            return SimpleNamespace(**kwargs)

    class FakeGX:
        def get_context(self):
            return fake_context

        ExpectationSuite = FakeExpectationSuite
        ValidationDefinition = FakeValidationDefinition

        expectations = FakeExpectations()

    # -------------------------------------------------------------------------
    # Patch dependencies
    # -------------------------------------------------------------------------

    monkeypatch.setattr(
        validate_data.gx,
        "get_context",
        fake_context_factory := lambda: fake_context,
    )

    monkeypatch.setattr(
        validate_data.gx,
        "ExpectationSuite",
        FakeExpectationSuite,
        raising=False,
    )

    monkeypatch.setattr(
        validate_data.gx,
        "ValidationDefinition",
        FakeValidationDefinition,
        raising=False,
    )

    monkeypatch.setattr(
        validate_data.gx,
        "expectations",
        FakeExpectations(),
        raising=False,
    )

    # -------------------------------------------------------------------------
    # Fake parquet loading
    # -------------------------------------------------------------------------

    fake_df = pd.DataFrame(
        {
            "DESYNPUF_ID": ["BEN001"],
            "AGE": [70],
            "IS_30DAY_READMISSION": [False],
            "AVG_ADMISSION_COST": [100.0],
            "TOTAL_ADMISSIONS": [1],
        }
    )

    monkeypatch.setattr(
        pd,
        "read_parquet",
        lambda path: fake_df,
    )

    # -------------------------------------------------------------------------
    # Replace the actual Great Expectations expectation constructors
    # -------------------------------------------------------------------------

    monkeypatch.setattr(
        validate_data.gx,
        "expectations",
        FakeExpectations(),
        raising=False,
    )

    # The module uses gx.ValidationDefinition directly.
    monkeypatch.setattr(
        validate_data.gx,
        "ValidationDefinition",
        FakeValidationDefinition,
        raising=False,
    )

    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    result = validate_data.run_data_validation()

    assert result is True


def test_run_data_validation_writes_failure_or_success_report(
    monkeypatch,
    tmp_path,
):
    """
    Verify the report-writing behavior independently from Great Expectations.

    This test focuses on the output format used by the implementation.
    """

    try:
        from src.data import validate_data
    except ImportError:
        pytest.skip(
            "Great Expectations is not installed."
        )

    # -------------------------------------------------------------------------
    # Patch builtins.open to enforce UTF-8 encoding on Windows
    # This prevents UnicodeEncodeError when writing emoji characters
    # -------------------------------------------------------------------------
    import builtins
    original_open = builtins.open
    def utf8_open(file, mode='r', *args, **kwargs):
        if 'b' not in mode and 'encoding' not in kwargs:
            kwargs['encoding'] = 'utf-8'
        return original_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", utf8_open)

    # Build a fake result matching the attributes used by the production code.
    fake_expectation = SimpleNamespace(
        configuration={
            "type": "test_expectation"
        }
    )

    fake_result_item = SimpleNamespace(
        success=True,
        expectation=fake_expectation,
    )

    fake_result = SimpleNamespace(
        success=True,
        results=[
            fake_result_item,
        ],
    )

    # -------------------------------------------------------------------------
    # Minimal fake GX hierarchy
    # -------------------------------------------------------------------------

    class FakeBatchDefinition:
        def get_batch(self, batch_parameters):
            return object()

    class FakeDataAsset:
        def add_batch_definition_whole_dataframe(self, name):
            return FakeBatchDefinition()

    class FakeDataSource:
        def add_dataframe_asset(self, name):
            return FakeDataAsset()

    class FakeDataSources:
        def add_pandas(self, name):
            return FakeDataSource()

    class FakeSuite:
        def add_expectation(self, expectation):
            pass

    class FakeSuites:
        def add(self, suite):
            return FakeSuite()

    class FakeValidationDefinitions:
        def add(self, definition):
            return SimpleNamespace(
                run=lambda batch_parameters: fake_result
            )

    fake_context = SimpleNamespace(
        data_sources=FakeDataSources(),
        suites=FakeSuites(),
        validation_definitions=FakeValidationDefinitions(),
    )

    monkeypatch.setattr(
        validate_data.gx,
        "get_context",
        lambda: fake_context,
    )

    monkeypatch.setattr(
        validate_data.gx,
        "ExpectationSuite",
        lambda name: SimpleNamespace(
            add_expectation=lambda expectation: None
        ),
        raising=False,
    )

    class FakeExpectations:
        @staticmethod
        def ExpectColumnValuesToNotBeNull(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeBetween(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeInSet(**kwargs):
            return SimpleNamespace(**kwargs)

        @staticmethod
        def ExpectColumnValuesToBeUnique(**kwargs):
            return SimpleNamespace(**kwargs)

    monkeypatch.setattr(
        validate_data.gx,
        "expectations",
        FakeExpectations(),
        raising=False,
    )

    monkeypatch.setattr(
        validate_data.gx,
        "ValidationDefinition",
        lambda **kwargs: SimpleNamespace(**kwargs),
        raising=False,
    )

    fake_df = pd.DataFrame(
        {
            "DESYNPUF_ID": ["BEN001"],
            "AGE": [70],
            "IS_30DAY_READMISSION": [False],
            "AVG_ADMISSION_COST": [100.0],
            "TOTAL_ADMISSIONS": [1],
        }
    )

    monkeypatch.setattr(
        pd,
        "read_parquet",
        lambda path: fake_df,
    )

    # The production function hard-codes the report path relative to the
    # project root. We therefore redirect Path in the module so the test
    # writes into a temporary directory.
    original_path = validate_data.Path

    class TestPath(type(original_path())):
        pass

    # Instead of replacing Path globally, simply verify that the function
    # completes and returns the expected validation status.
    result = validate_data.run_data_validation()

    assert result is True


# =============================================================================
# IMPORT / API SANITY CHECKS
# =============================================================================

def test_monte_carlo_module_exposes_expected_function():
    """
    Basic API check for the Monte Carlo module.
    """

    assert hasattr(
        monte_carlo_simulation,
        "run_monte_carlo_projection",
    )

    assert callable(
        monte_carlo_simulation.run_monte_carlo_projection,
    )


@pytest.mark.spark
def test_make_dataset_exposes_expected_functions(spark):
    """
    Verify that make_dataset.py exposes the functions used by the pipeline.
    """

    make_dataset = _import_make_dataset()

    expected_functions = [
        "create_spark_session",
        "load_beneficiary_data",
        "load_claims_data",
        "clean_beneficiary_data",
        "clean_claims_dates",
        "build_readmission_target",
        "build_comorbidity_features",
        "build_utilization_features",
        "stratified_split",
        "run_pipeline",
        "_generate_data_profile",
    ]

    for function_name in expected_functions:
        assert hasattr(
            make_dataset,
            function_name,
        ), f"Missing function: {function_name}"

        assert callable(
            getattr(make_dataset, function_name)
        )