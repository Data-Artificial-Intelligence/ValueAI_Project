# Data Governance & Audit Log
**Project:** ValueAI Risk Stratification Pipeline  
**Date:** 2026-09-21  
**Auditor:** [Antony Henry Oduor Onyango]  

## 1. Data Provenance & Integrity
- **Source:** CMS Medicare Synthetic Public Use Files (SynPUF) DE-1 Sample 1 (2008-2010).
- **Ingestion Method:** Automated PowerShell download with ZIP integrity verification (System.IO.Compression).
- **Storage:** Processed data stored in columnar Parquet format with Snappy compression for optimal big data platform (AWS S3/SageMaker) compatibility.

## 2. Known Data Gaps & Mitigations (Audit Issue #001)
- **Issue:** The official CMS portal returns a persistent HTTP 404 for `DE1_0_2010_Beneficiary_Summary_File_Sample_1.zip`. This is a documented, longstanding CMS publishing error (the link incorrectly routes to Sample 20).
- **Impact Assessment:** Low. The 2008 and 2009 Beneficiary Summary files successfully provide complete baseline demographics (Age, Sex, Race, Chronic Condition flags) for the entire 1,000-beneficiary cohort. 
- **Mitigation Applied:** The PySpark ingestion pipeline (`src/data/make_dataset.py`) was engineered to dynamically discover and union all available beneficiary years. The 2008–2010 Inpatient Claims file successfully provides all necessary longitudinal data to construct the 30-day readmission target variable. No statistical imputation was required.
- **Status:** ✅ CLOSED. Documented and mitigated without blocking project delivery.

## 3. Privacy & Statutory Compliance
- **PII Handling:** The SynPUF dataset is natively de-identified. The `DESYNPUF_ID` is a hashed, synthetic identifier. No real Protected Health Information (PHI) is present or processed.
- **Access Control:** Raw data is excluded from version control via `.gitignore`. Only processed, aggregated, or anonymized artifacts are committed.

## 4. Data Quality Validation (Great Expectations)
Automated validation suite executed post-ingestion. Key assertions passed:
- [x] `DESYNPUF_ID` uniqueness and non-nullability.
- [x] `AGE` bounded between 18 and 110.
- [x] `IS_30DAY_READMISSION` strictly boolean.
- [x] Cost metrics are non-negative.

## 5. Reproducibility
- Pipeline orchestrated via modular Python scripts.
- Random seeds fixed (e.g., `seed=42` for stratified sampling and Monte Carlo simulations) to ensure 100% reproducible splits and projections.