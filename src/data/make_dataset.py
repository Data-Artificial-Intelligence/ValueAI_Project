import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.window import Window


# =============================================================================
# PROJECT ROOT
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# =============================================================================
# LOGGING
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =============================================================================
# WINDOWS SPARK CONFIGURATION
# =============================================================================
if os.name == "nt":
    # Force Spark to use this project's virtual environment
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    # Hadoop home used by Spark on Windows
    hadoop_home = Path.home() / ".hadoop"
    hadoop_bin = hadoop_home / "bin"

    winutils_path = hadoop_bin / "winutils.exe"
    hadoop_dll_path = hadoop_bin / "hadoop.dll"

    if not winutils_path.exists():
        raise FileNotFoundError(
            f"winutils.exe not found at {winutils_path}. "
            "Install the Hadoop 3.5.0 Windows binary before running the pipeline."
        )

    if not hadoop_dll_path.exists():
        raise FileNotFoundError(
            f"hadoop.dll not found at {hadoop_dll_path}. "
            "Install the Hadoop 3.5.0 Windows native library."
        )

    # Tell Hadoop where its Windows binaries live
    os.environ["HADOOP_HOME"] = str(hadoop_home)
    os.environ["hadoop.home.dir"] = str(hadoop_home)

    # Make Hadoop binaries available to Windows processes
    os.environ["PATH"] = (
        str(hadoop_bin)
        + os.pathsep
        + os.environ.get("PATH", "")
    )

    # Use forward slashes for Java/JVM native-library paths.
    # This avoids Windows backslash escaping issues in JVM options.
    hadoop_home_java = hadoop_home.as_posix()
    hadoop_bin_java = hadoop_bin.as_posix()
    

# =============================================================================
# 1. SPARK SESSION - Local mode for dev, cluster mode for AWS EMR/SageMaker
# =============================================================================
def create_spark_session(
    app_name: str = "ValueAI_SynPUF_Pipeline"
) -> SparkSession:
    """Create a Spark session configured for either local dev or AWS cluster."""

    # Detect environment: switch to YARN on AWS
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    master = "yarn" if is_aws else "local[*]"

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.sql.session.timeZone", "UTC")
        .config(
            "spark.sql.shuffle.partitions",
            "8" if not is_aws else "200"
        )
        .config("spark.driver.memory", "4g")
        .config("spark.sql.adaptive.enabled", "true")
        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )
    )

    # Windows-only JVM configuration
    if os.name == "nt":
        builder = (
            builder
            .config(
                "spark.driver.extraJavaOptions",
                f"-Dhadoop.home.dir={hadoop_home_java} "
                f"-Djava.library.path={hadoop_bin_java}"
            )
            .config(
                "spark.executor.extraJavaOptions",
                f"-Dhadoop.home.dir={hadoop_home_java} "
                f"-Djava.library.path={hadoop_bin_java}"
            )
        )

    if is_aws:
        # AWS S3 credentials picked up from IAM role automatically
        builder = builder.config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.InstanceProfileCredentialsProvider"
        )

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    logger.info(
        f"Spark session created on master: {master}"
    )

    return spark


# =============================================================================
# 2. DATA INGESTION - Read raw SynPUF CSVs
# =============================================================================
def load_beneficiary_data(
    spark: SparkSession,
    data_path: Path
) -> DataFrame:
    """Dynamically load and union all available beneficiary summary files."""

    pattern = "*Beneficiary_Summary_File_Sample_1.csv"

    files = list(data_path.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No beneficiary files found matching {pattern} in {data_path}"
        )

    dfs = []

    for path in files:
        # Extract year from filename
        year = int(path.stem.split("_")[2])

        df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(str(path))
            .withColumn("source_year", F.lit(year))
        )

        dfs.append(df)

        logger.info(
            f"Loaded {path.name}: {df.count()} rows"
        )

    from functools import reduce

    final_df = reduce(
        lambda df1, df2: df1.unionByName(
            df2,
            allowMissingColumns=True
        ),
        dfs
    )

    logger.info(
        f"Total beneficiary records loaded across "
        f"{len(dfs)} years: {final_df.count()}"
    )

    return final_df


def load_claims_data(
    spark: SparkSession,
    data_path: Path,
    claim_type: str
) -> DataFrame:
    """Load inpatient, outpatient, carrier, or drug claims."""

    file_map = {
        "inpatient":
            "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv",

        "outpatient":
            "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv",

        "carrier":
            "DE1_0_2008_to_2010_Carrier_Claims_Sample_1.csv",

        "drug":
            "DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv",
    }

    path = data_path / file_map[claim_type]

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(path))
    )

    logger.info(
        f"Loaded {claim_type} claims: {df.count()} rows"
    )

    return df


# =============================================================================
# 3. DATA CLEANING
# =============================================================================
def clean_beneficiary_data(df: DataFrame) -> DataFrame:
    """Standardize dates, handle missing values, derive age."""

    df = (
        df

        # CMS SynPUF uses yyyyMMdd
        .withColumn(
            "BENE_BIRTH_DT",
            F.to_date("BENE_BIRTH_DT", "yyyyMMdd")
        )

        .withColumn(
            "BENE_DEATH_DT",
            F.to_date("BENE_DEATH_DT", "yyyyMMdd")
        )

        # Age at end of study
        .withColumn(
            "AGE",
            F.floor(
                F.datediff(
                    F.lit("2010-12-31"),
                    F.col("BENE_BIRTH_DT")
                ) / 365.25
            )
        )

        # Impute missing race
        .withColumn(
            "RACE",
            F.coalesce(
                F.col("BENE_RACE_CD"),
                F.lit(2)
            )
        )

        .drop("BENE_RACE_CD")

        # Flag deceased beneficiaries
        .withColumn(
            "IS_DECEASED",
            F.col("BENE_DEATH_DT").isNotNull()
        )

        # Keep valid ages
        .filter(
            (F.col("AGE") >= 18) &
            (F.col("AGE") <= 110)
        )
    )

    logger.info(
        f"Cleaned beneficiary data: {df.count()} rows"
    )

    return df


def clean_claims_dates(
    df: DataFrame,
    claim_type: str
) -> DataFrame:
    """Standardize date columns across all claim types."""

    date_cols = {
        "inpatient": [
            "CLM_ADMSN_DT",
            "CLM_THRU_DT",
            "NCH_BENE_DSCHRG_DT"
        ],

        "outpatient": [
            "CLM_FROM_DT",
            "CLM_THRU_DT"
        ],

        "carrier": [
            "CLM_FROM_DT",
            "CLM_THRU_DT"
        ],

        "drug": [
            "SRVC_DT"
        ],
    }

    for col_name in date_cols.get(claim_type, []):

        if col_name in df.columns:

            df = df.withColumn(
                col_name,
                F.to_date(
                    F.col(col_name),
                    "yyyyMMdd"
                )
            )

    return df


# =============================================================================
# 4. FEATURE ENGINEERING
# =============================================================================
def build_readmission_target(
    inpatient_df: DataFrame
) -> DataFrame:
    """
    Create 30-day readmission target variable.

    A readmission = another inpatient admission
    within 30 days of discharge.
    """

    window_spec = (
        Window
        .partitionBy("DESYNPUF_ID")
        .orderBy("CLM_ADMSN_DT")
        .rowsBetween(1, 1)
    )

    df = (
        inpatient_df

        .filter(
            F.col("CLM_ADMSN_DT").isNotNull()
        )

        .filter(
            F.col("NCH_BENE_DSCHRG_DT").isNotNull()
        )

        .withColumn(
            "next_admission_date",
            F.lead(
                "CLM_ADMSN_DT"
            ).over(window_spec)
        )

        .withColumn(
            "days_to_next_admission",
            F.datediff(
                F.col("next_admission_date"),
                F.col("NCH_BENE_DSCHRG_DT")
            )
        )

        .withColumn(
            "IS_30DAY_READMISSION",
            (
                (F.col("days_to_next_admission") <= 30) &
                (F.col("days_to_next_admission") >= 0)
            )
        )

        .drop(
            "next_admission_date",
            "days_to_next_admission"
        )
    )

    readmit_rate = (
        df
        .groupBy("IS_30DAY_READMISSION")
        .count()
        .collect()
    )

    logger.info(
        f"Readmission target distribution: {readmit_rate}"
    )

    return df


def build_comorbidity_features(
    inpatient_df: DataFrame
) -> DataFrame:
    """
    Count unique ICD-9 diagnosis codes per beneficiary.

    SynPUF has 10 diagnosis columns:
    ICD9_DGNS_CD, ICD9_DGNS_2_CD, ... ICD9_DGNS_10_CD
    """

    diag_cols = [
        c
        for c in inpatient_df.columns
        if c.startswith("ICD9_DGNS_")
        or c == "ICD9_DGNS_CD"
    ]

    df_long = (
        inpatient_df
        .select(
            "DESYNPUF_ID",
            F.explode(
                F.array(
                    *[
                        F.col(c)
                        for c in diag_cols
                    ]
                )
            ).alias("DIAGNOSIS_CD")
        )
        .filter(
            F.col("DIAGNOSIS_CD").isNotNull()
        )
    )

    comorbidity_counts = (
        df_long
        .groupBy("DESYNPUF_ID")
        .agg(
            F.countDistinct(
                "DIAGNOSIS_CD"
            ).alias(
                "UNIQUE_DIAGNOSES_COUNT"
            )
        )
    )

    return comorbidity_counts


def build_utilization_features(
    claims_df: DataFrame,
    claim_type: str
) -> DataFrame:
    """
    Build rolling averages and time-since-last-event
    per beneficiary.
    """

    date_col_map = {
        "inpatient": "CLM_ADMSN_DT",
        "outpatient": "CLM_FROM_DT",
        "carrier": "CLM_FROM_DT",
        "drug": "SRVC_DT"
    }

    date_col = date_col_map.get(
        claim_type,
        "CLM_FROM_DT"
    )

    # Determine cost column
    if "CLM_PMT_AMT" in claims_df.columns:
        cost_col = "CLM_PMT_AMT"

    elif "TOT_RX_CST_AMT" in claims_df.columns:
        cost_col = "TOT_RX_CST_AMT"

    else:
        cost_col = None

    window_spec = (
        Window
        .partitionBy("DESYNPUF_ID")
        .orderBy(date_col)
        .rowsBetween(-3, -1)
    )

    df = claims_df.filter(
        F.col(date_col).isNotNull()
    )

    if cost_col:

        df = (
            df

            .withColumn(
                "ROLLING_AVG_COST_3",
                F.avg(cost_col).over(window_spec)
            )

            .withColumn(
                "ROLLING_MAX_COST_3",
                F.max(cost_col).over(window_spec)
            )
        )

    # Time since previous claim
    df = df.withColumn(
        "DAYS_SINCE_LAST_CLAIM",
        F.datediff(
            F.col(date_col),
            F.lag(date_col).over(
                Window
                .partitionBy("DESYNPUF_ID")
                .orderBy(date_col)
            )
        )
    )

    agg_cols = [
        F.count("*").alias(
            f"{claim_type.upper()}_CLAIM_COUNT"
        ),

        (
            F.avg("ROLLING_AVG_COST_3").alias(
                f"AVG_{claim_type.upper()}_COST"
            )
            if cost_col
            else F.lit(None)
        ),

        F.avg(
            "DAYS_SINCE_LAST_CLAIM"
        ).alias(
            f"AVG_DAYS_BETWEEN_{claim_type.upper()}_CLAIMS"
        ),
    ]

    agg_cols = [
        c for c in agg_cols
        if c is not None
    ]

    return (
        df
        .groupBy("DESYNPUF_ID")
        .agg(*agg_cols)
    )


# =============================================================================
# 5. TRAIN / VALIDATION / TEST SPLIT
# =============================================================================
def stratified_split(
    df: DataFrame,
    target_col: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    """
    Split data into training, validation and test datasets.
    """

    train_df = df.filter(
        F.rand(seed=42) < train_ratio
    )

    remaining = df.filter(
        F.rand(seed=42) >= train_ratio
    )

    val_df = remaining.filter(
        F.rand(seed=43)
        < (val_ratio / (1 - train_ratio))
    )

    test_df = remaining.filter(
        F.rand(seed=43)
        >= (val_ratio / (1 - train_ratio))
    )

    logger.info(
        f"Split sizes - "
        f"Train: {train_df.count()}, "
        f"Val: {val_df.count()}, "
        f"Test: {test_df.count()}"
    )

    return train_df, val_df, test_df


# =============================================================================
# 6. MAIN PIPELINE ORCHESTRATOR
# =============================================================================
def run_pipeline():
    """Execute the full Phase 1 pipeline."""

    start_time = datetime.now()

    logger.info("=" * 60)
    logger.info("Starting ValueAI Phase 1 Pipeline")
    logger.info("=" * 60)

    spark = create_spark_session()

    raw_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "synpuf"
    )

    processed_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
    )

    processed_path.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        # ---------------------------------------------------------------------
        # INGESTION
        # ---------------------------------------------------------------------
        logger.info("[1/6] Loading raw data...")

        beneficiaries = load_beneficiary_data(
            spark,
            raw_path
        )

        inpatient = load_claims_data(
            spark,
            raw_path,
            "inpatient"
        )

        outpatient = load_claims_data(
            spark,
            raw_path,
            "outpatient"
        )

        drug = load_claims_data(
            spark,
            raw_path,
            "drug"
        )

        # ---------------------------------------------------------------------
        # CLEANING
        # ---------------------------------------------------------------------
        logger.info("[2/6] Cleaning data...")

        beneficiaries = clean_beneficiary_data(
            beneficiaries
        )

        inpatient = clean_claims_dates(
            inpatient,
            "inpatient"
        )

        outpatient = clean_claims_dates(
            outpatient,
            "outpatient"
        )

        drug = clean_claims_dates(
            drug,
            "drug"
        )

        # ---------------------------------------------------------------------
        # TARGET VARIABLE
        # ---------------------------------------------------------------------
        logger.info(
            "[3/6] Building readmission target..."
        )

        inpatient_with_target = (
            build_readmission_target(
                inpatient
            )
        )

        # ---------------------------------------------------------------------
        # FEATURE ENGINEERING
        # ---------------------------------------------------------------------
        logger.info(
            "[4/6] Engineering features..."
        )

        comorbidity = (
            build_comorbidity_features(
                inpatient
            )
        )

        inpatient_util = (
            build_utilization_features(
                inpatient,
                "inpatient"
            )
        )

        outpatient_util = (
            build_utilization_features(
                outpatient,
                "outpatient"
            )
        )

        drug_util = (
            build_utilization_features(
                drug,
                "drug"
            )
        )

        # ---------------------------------------------------------------------
        # JOIN FEATURE TABLES
        # ---------------------------------------------------------------------
        logger.info(
            "[5/6] Joining feature tables..."
        )

        admission_base = (
            inpatient_with_target
            .groupBy("DESYNPUF_ID")
            .agg(
                F.max(
                    "IS_30DAY_READMISSION"
                ).alias(
                    "IS_30DAY_READMISSION"
                ),

                F.count("*").alias(
                    "TOTAL_ADMISSIONS"
                ),

                F.avg(
                    "CLM_PMT_AMT"
                ).alias(
                    "AVG_ADMISSION_COST"
                ),

                F.avg(
                    "CLM_UTLZTN_DAY_CNT"
                ).alias(
                    "AVG_LENGTH_OF_STAY"
                ),
            )
        )

        final_df = (
            beneficiaries

            .join(
                admission_base,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                comorbidity,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                inpatient_util,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                outpatient_util,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                drug_util,
                "DESYNPUF_ID",
                "left"
            )
        )

        # Fill nulls with 0 for patients with no claims.
        # These columns are created by the joins above.
        fill_columns = [
            "TOTAL_ADMISSIONS",
            "UNIQUE_DIAGNOSES_COUNT",
            "INPATIENT_CLAIM_COUNT",
            "OUTPATIENT_CLAIM_COUNT",
            "DRUG_CLAIM_COUNT"
        ]

        final_df = final_df.fillna(
            0,
            subset=[
                c
                for c in fill_columns
                if c in final_df.columns
            ]
        )

        # ---------------------------------------------------------------------
        # STRATIFIED SPLIT & SAVE
        # ---------------------------------------------------------------------
        logger.info(
            "[6/6] Stratified sampling and saving..."
        )

        train_df, val_df, test_df = stratified_split(
            final_df,
            "IS_30DAY_READMISSION"
        )

        # Save train dataset
        (
            train_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "train.parquet"
                )
            )
        )

        # Save validation dataset
        (
            val_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "val.parquet"
                )
            )
        )

        # Save test dataset
        (
            test_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "test.parquet"
                )
            )
        )

        # Save complete dataset
        (
            final_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "full_dataset.parquet"
                )
            )
        )

        # ---------------------------------------------------------------------
        # DATA PROFILE
        # ---------------------------------------------------------------------
        _generate_data_profile(
            train_df,
            processed_path
        )

        elapsed = (
            datetime.now() - start_time
        ).total_seconds()

        logger.info(
            f"Pipeline completed in {elapsed:.1f} seconds"
        )

        logger.info(
            f"Processed data saved to: {processed_path}"
        )

    except Exception as e:

        logger.error(
            f"[ERROR] Pipeline failed: {e}",
            exc_info=True
        )

        raise

    finally:
        spark.stop()


# =============================================================================
# 7. DATA PROFILE
# =============================================================================
def _generate_data_profile(
    df: DataFrame,
    output_path: Path
):
    """
    Generate a lightweight Spark data profiling summary.
    """

    summary = df.summary().toPandas()

    summary.to_csv(
        output_path / "data_profile_summary.csv",
        index=False
    )

    logger.info(
        "Data profile saved to data_profile_summary.csv"
    )


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    run_pipeline()