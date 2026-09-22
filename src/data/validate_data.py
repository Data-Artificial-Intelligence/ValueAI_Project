"""
Great Expectations validation suite for data quality adherence.
Matches JD: "100% adherence to policies, procedures and statutory guidelines"
"""
import great_expectations as gx
from pathlib import Path
from datetime import datetime


def run_data_validation():
    """Validate processed data against business rules."""
    context = gx.get_context()
    processed_path = Path(__file__).parents[2] / "data" / "processed"

    # Create data source
    data_source = context.data_sources.add_pandas(name="synpuf_processed")
    data_asset = data_source.add_dataframe_asset(name="train_data")

    # Read train data
    import pandas as pd
    df = pd.read_parquet(processed_path / "train.parquet")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("train_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    # Define expectations (business rules)
    expectation_suite = context.suites.add(gx.ExpectationSuite(name="synpuf_quality"))

    expectations = [
        # 1. No null beneficiary IDs (primary key integrity)
        gx.expectations.ExpectColumnValuesToNotBeNull(column="DESYNPUF_ID"),
        # 2. Age must be between 18 and 110
        gx.expectations.ExpectColumnValuesToBeBetween(column="AGE", min_value=18, max_value=110),
        # 3. Readmission target must be boolean
        gx.expectations.ExpectColumnValuesToBeInSet(column="IS_30DAY_READMISSION", value_set=[True, False]),
        # 4. Costs must be non-negative
        gx.expectations.ExpectColumnValuesToBeBetween(column="AVG_ADMISSION_COST", min_value=0, max_value=1_000_000),
        # 5. Claim counts must be non-negative
        gx.expectations.ExpectColumnValuesToBeBetween(column="TOTAL_ADMISSIONS", min_value=0, max_value=1000),
        # 6. No duplicate beneficiaries
        gx.expectations.ExpectColumnValuesToBeUnique(column="DESYNPUF_ID"),
    ]

    for exp in expectations:
        expectation_suite.add_expectation(exp)

    # Run validation
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="synpuf_train_validation",
            data=batch_definition,
            suite=expectation_suite,
        )
    )

    result = validation_definition.run(batch_parameters={"dataframe": df})

    # Save report
    report_path = Path(__file__).parents[2] / "docs" / "data_quality_report.md"
    with open(report_path, "w") as f:
        f.write(f"# Data Quality Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"## Results\n\n")
        f.write(f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n\n")
        f.write(f"**Statistics:**\n")
        f.write(f"- Evaluated: {result.results.__len__()} expectations\n")
        f.write(f"- Success Rate: {sum(1 for r in result.results if r.success) / len(result.results) * 100:.1f}%\n\n")
        f.write("## Expectation Details\n\n")
        for r in result.results:
            status = "✅" if r.success else "❌"
            f.write(f"- {status} {r.expectation.configuration.get('type', 'Unknown')}\n")

    print(f"📋 Data quality report saved to: {report_path}")
    return result.success


if __name__ == "__main__":
    success = run_data_validation()
    print(f"\nValidation {'PASSED ✅' if success else 'FAILED ❌'}")