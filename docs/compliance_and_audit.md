# ValueAI Project — Data Governance, Compliance & Audit Log

**Project:** ValueAI End-to-End Risk Stratification & Analytics Platform
**Data Source:** CMS Medicare Synthetic Public Use Files (SynPUF)
**Primary Processing:** Python, PySpark, Parquet
**Models:** XGBoost, Gaussian Mixture Model (GMM), ARIMA, Monte Carlo simulation
**Explainability:** SHAP
**Agentic AI:** LangGraph + local Qwen 2.5 7B via Ollama
**Current Phase:** Phase 4 — MLOps, Visualization & Stakeholder Communication
**Document Date:** 2026-09-22
**Status:** Project governance and issue-resolution record

---

## 1. Purpose

This document records the data-quality, analytical-governance, model-interpretation, and GenAI controls applied during development of the ValueAI project.

The objective is to demonstrate that analytical results are:

* traceable to the underlying data and processing pipeline;
* reproducible from versioned code and generated artifacts;
* interpreted within the limitations of the available data;
* separated from unsupported causal or clinical conclusions;
* documented when data or modelling issues are discovered;
* communicated with appropriate caveats.

This is a **portfolio project governance record**, not a legal compliance certification or production healthcare compliance assessment.

---

# 2. Data Source & Privacy Handling

## 2.1 Source

The project uses the **CMS Medicare Synthetic Public Use Files (SynPUF)** available as public-use data.

The local pipeline processes beneficiary, inpatient, outpatient, carrier, and prescription drug event data.

The available beneficiary files used in the current pipeline are:

* 2008 Beneficiary Summary File
* 2009 Beneficiary Summary File

Claims data covers the corresponding available SynPUF sample data used by the project.

The processed dataset contains more than **6.5 million claim-related records** across the source files processed by the pipeline.

---

## 2.2 Data Sensitivity

The project uses public-use synthetic/de-identified source data rather than a production healthcare database.

No real patient-identifying information was intentionally introduced into the project.

The project therefore does **not** constitute:

* a HIPAA compliance certification;
* a GDPR compliance certification;
* a production healthcare security assessment;
* authorization to process real Protected Health Information (PHI).

Any production implementation using real healthcare data would require additional legal, security, access-control, encryption, retention, audit, and organizational controls.

---

## 2.3 Identifier Handling

The SynPUF data contains synthetic beneficiary identifiers such as `DESYNPUF_ID`.

These identifiers are treated as analytical keys rather than real-world patient identities.

The project does not attempt to map synthetic identifiers to real individuals.

---

# 3. Data Storage & Processing Controls

## 3.1 Raw Data

Raw source files are stored under:

```text
data/raw/synpuf/
```

The current project contains:

* beneficiary summary files;
* inpatient claims;
* outpatient claims;
* prescription drug events;
* carrier claims.

Raw source files are retained separately from processed analytical datasets.

---

## 3.2 Processed Data

Processed datasets are stored under:

```text
data/processed/
```

The pipeline generates Parquet datasets including:

* `full_dataset.parquet`
* `train.parquet`
* `val.parquet`
* `test.parquet`
* `clustered_dataset.parquet`

Parquet with Snappy compression is used for analytical storage and efficient downstream processing.

---

## 3.3 Local Development Environment

The current project is developed locally using Python and PySpark.

The architecture is designed so that the analytical pipeline can subsequently be adapted to cloud infrastructure.

AWS/SageMaker should therefore be considered a **target deployment architecture**, unless an actual cloud deployment is separately documented.

No claim is made here that the current project is running in production on AWS SageMaker.

---

# 4. Data Quality Controls

The project includes explicit data validation and quality-handling steps.

Relevant implementation files include:

```text
src/data/make_dataset.py
src/data/validate_data.py
src/data/monte_carlo_simulation.py
```

Generated analytical artifacts are stored under:

```text
data/processed/
docs/
models/
```

The pipeline separates raw ingestion, transformation, feature engineering, model training, evaluation, and generated outputs.

---

# 5. Data Quality & Issue Resolution Log

The following issues were encountered during project development and were addressed through changes to the pipeline or analytical methodology.

| ID      | Issue                                                                                                                                      | Date       | Resolution                                                                                                                                                        | Status     |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------|------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| AUD-001 | Expected/attempted 2010 beneficiary source file was unavailable at the attempted CMS source location and returned HTTP 404                 | 2026-09-21 | Pipeline was revised to use the available 2008 and 2009 beneficiary files rather than depending on the unavailable file                                           | Resolved   |
| AUD-002 | Non-positive admission-cost observations affected assumptions required for log-normal Monte Carlo modelling                                | 2026-09-22 | Monte Carlo preprocessing excludes non-positive values before fitting the log-normal distribution                                                                 | Resolved   |
| AUD-003 | Seasonal time-series specification was inappropriate given the limited historical observation window and introduced an overfitting concern | 2026-09-22 | Model simplified to ARIMA(1,1,1); out-of-sample holdout evaluation and a naive baseline were added                                                                | Resolved   |
| AUD-004 | Free-form LLM generation could introduce unsupported quantitative claims                                                                   | 2026-09-22 | Implemented deterministic Evidence-First routing in LangGraph so analytical tools produce verified evidence before the local LLM generates the narrative response | Controlled |

---

# 6. AUD-001 — Source File Availability

### Observation

During data acquisition, an attempted source location for the 2010 beneficiary summary file returned an HTTP 404 response.

### Risk

A pipeline dependent on a specific unavailable file could fail during reproducibility or future execution.

### Corrective Action

The ingestion process was adapted to work with the available SynPUF beneficiary files:

```text
2008
2009
```

The pipeline therefore does not treat the unavailable 2010 beneficiary file as a required input.

### Evidence

Available source files are retained under:

```text
data/raw/synpuf/
```

The current project contains:

```text
DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv
DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv
```

### Status

**Resolved**

---

# 7. AUD-002 — Admission Cost Data Quality

### Observation

The admission-cost data contained non-positive observations.

A log-normal distribution requires positive observations, so directly fitting the distribution to non-positive values would violate the modelling assumption.

### Risk

Including invalid values could distort the fitted distribution and produce an invalid Monte Carlo projection.

### Corrective Action

The Monte Carlo preprocessing step filters out non-positive cost observations before fitting the log-normal distribution.

The resulting simulation is therefore based only on observations satisfying the distribution's positivity requirement.

### Analytical Limitation

Excluding non-positive observations is a modelling treatment rather than proof that those records are erroneous.

A production implementation would require investigation of the business meaning and source-system lineage of such values before deciding whether they should be corrected, excluded, imputed, or represented using another statistical model.

### Evidence

Generated outputs:

```text
data/processed/monte_carlo_results.json
data/processed/monte_carlo_projection.png
```

Implementation:

```text
src/data/monte_carlo_simulation.py
```

### Status

**Resolved for the current portfolio modelling workflow**

---

# 8. AUD-003 — Time-Series Model Specification

### Observation

An initial seasonal time-series approach raised an overfitting concern because the available historical series contained only a limited number of observations.

The underlying synthetic claims data also exhibits a pronounced decline toward the end of the available period.

### Risk

A complex seasonal model could fit historical patterns that are not sufficiently supported by the available observation window and could give misleading confidence in the forecast.

### Corrective Action

The time-series model was simplified to:

```text
ARIMA(1,1,1)
```

The evaluation workflow also includes:

* an out-of-sample holdout period;
* comparison against a naive baseline;
* model evaluation metrics;
* forecast output;
* documentation of the observed late-period decline.

### Evidence

```text
src/models/train_timeseries.py

data/processed/timeseries_model.pkl

docs/timeseries_forecast.csv
docs/timeseries_forecast.png
docs/timeseries_holdout_evaluation.csv
docs/timeseries_model_metadata.json
docs/timeseries_model_metrics.csv
```

### Interpretation Limitation

The observed late-period decline is a characteristic of the available synthetic dataset.

It should not automatically be interpreted as a real-world healthcare utilization trend.

Forecast results should therefore be interpreted in the context of the source data and its limited historical window.

### Status

**Resolved**

---

# 9. AUD-004 — GenAI Hallucination & Evidence Governance

## 9.1 Risk

A conventional LLM workflow can generate plausible-sounding quantitative statements that are not supported by the underlying analytical results.

This is particularly important when communicating:

* model metrics;
* cluster sizes;
* feature importance;
* patient predictions;
* financial projections;
* business recommendations.

---

## 9.2 Control Architecture

The project implements an **Evidence-First Agentic AI architecture**.

The workflow is:

```text
User Question
      ↓
Deterministic Evidence Router
      ↓
Verified Analytical Tool
      ↓
Evidence Package
      ↓
Qwen 2.5 7B
      ↓
Executive Business Response
```

Relevant implementation files:

```text
src/ai_agent/agent_graph.py
src/ai_agent/agent_tools.py
src/ai_agent/streamlit_app.py
```

The agent can retrieve evidence from deterministic analytical functions for:

* high-risk cluster analysis;
* SHAP feature importance;
* model metadata;
* individual readmission-risk prediction.

The LLM is therefore used primarily for **interpretation and communication**, rather than independently calculating project metrics.

---

## 9.3 Evidence Interpretation Rules

The agent is explicitly instructed to distinguish between:

### Observed Data

Descriptive statistics directly calculated from the dataset.

Example:

```text
Cluster 2 contains 30,298 individuals.
```

### Model Importance

SHAP mean absolute values represent the magnitude of feature contribution to model output.

They do **not**, by themselves, establish:

* whether increasing the feature increases risk;
* whether decreasing the feature increases risk;
* causality.

### Model Prediction

A model-generated probability or classification is an output of the trained model.

It is not equivalent to a clinical diagnosis.

### Causal Evidence

The project does not claim that an observational association or model feature importance establishes causation.

---

## 9.4 Current GenAI Limitation

The Evidence-First architecture reduces the risk of unsupported quantitative evidence entering the LLM context, but it does not guarantee that every generated sentence will be interpreted correctly.

For example, SHAP magnitude can still be incorrectly described as directional if the generated narrative is not sufficiently constrained.

Therefore:

> Quantitative evidence should be validated against the deterministic analytical outputs before being treated as a final business or clinical conclusion.

A production implementation should add structured output validation or deterministic post-generation checks before responses are presented to decision-makers.

### Status

**Controlled — additional production-grade validation remains a future enhancement**

---

# 10. Model Governance

## 10.1 Classification Model

The project uses XGBoost for 30-day readmission classification.

Current recorded evaluation results include:

* ROC-AUC: approximately **0.95**
* Accuracy: approximately **87.7%**

The exact evaluation artifacts should remain the authoritative source for reported metrics.

Model metadata is stored under:

```text
models/classification_metadata.json
```

Model artifact:

```text
models/classification_model.pkl
```

---

## 10.2 Explainability

SHAP is used to provide model explainability.

The project stores:

```text
docs/shap_feature_importance.csv
docs/shap_summary.png
```

The current analysis identifies the most influential features by mean absolute SHAP magnitude.

These results are interpreted as **model explanations**, not causal relationships.

---

## 10.3 Clustering

A Gaussian Mixture Model (GMM) is used for population segmentation.

The clustering workflow stores:

```text
models/clustering_model.pkl
models/clustering_scaler.pkl
data/processed/clustered_dataset.parquet
docs/cluster_distribution.png
```

The current clustering evaluation reports a silhouette score of approximately:

```text
0.35
```

The high-risk segment designation refers to the segment identified through the project's analytical segmentation criteria.

It should not be interpreted as a clinical diagnosis.

---

## 10.4 Monte Carlo Simulation

Monte Carlo simulation is used to project healthcare admission-cost distributions.

The project produces:

```text
data/processed/monte_carlo_results.json
data/processed/monte_carlo_projection.png
```

The simulation reports a prediction interval based on the fitted historical cost distribution.

The projection is a statistical scenario estimate, not a guaranteed future financial outcome.

---

# 11. Statistical & Analytical Limitations

The following limitations are material to interpretation of the project.

### 11.1 Synthetic Data

The project uses CMS SynPUF public-use synthetic data.

Therefore, findings should not be presented as evidence of actual current healthcare utilization patterns in a real patient population.

### 11.2 Historical Coverage

The available data provides a limited historical window.

Consequently, time-series forecasts should not be interpreted as long-term structural forecasts without additional real-world data.

### 11.3 Observational Data

The project does not establish causal relationships between utilization variables and readmission.

### 11.4 Model Performance

Model performance metrics describe performance on the project's evaluation datasets.

They do not establish guaranteed performance after deployment to a different population or production environment.

### 11.5 SHAP Interpretation

SHAP feature importance identifies model contribution magnitude.

It does not independently establish feature direction, causation, or intervention effectiveness.

### 11.6 Cluster Interpretation

GMM clusters are analytical segments produced by the selected features, preprocessing, and model configuration.

They should not be interpreted as formally validated clinical risk categories.

---

# 12. Recommendations Governance

Recommendations generated by the project are treated as **analytical hypotheses for stakeholder consideration**, not guaranteed interventions.

A recommendation should therefore connect:

```text
Observed Evidence
        ↓
Analytical Interpretation
        ↓
Potential Business Action
        ↓
Proposed KPI
        ↓
Future Validation
```

The project does not claim that a particular intervention will reduce readmissions, costs, or utilization unless such an effect has been separately demonstrated through appropriate evaluation.

Potential operational KPIs should be defined and tested with real operational data before being assigned numerical targets.

---

# 13. Fairness & Responsible AI Considerations

Fairness is treated as a governance consideration for future validation rather than as a completed fairness certification.

The current project does **not** claim that the models have passed a formal demographic fairness audit.

A production healthcare deployment should evaluate, where legally and ethically appropriate:

* performance across relevant demographic groups;
* false-positive and false-negative rates;
* calibration across groups;
* feature and proxy-variable risks;
* potential disparities in intervention allocation;
* human oversight requirements.

Because the current dataset is synthetic and the project has not established a formal fairness evaluation framework, no claim of demographic fairness is made here.

---

# 14. Access, Secrets & Environment Configuration

Environment-specific configuration is separated from source code.

Project configuration files include:

```text
.env
.env.example
.gitignore
```

Secrets and environment-specific values should not be committed to source control.

The project's `.gitignore` should continue to exclude:

* credentials;
* API keys;
* local environment files where appropriate;
* virtual environments;
* generated caches;
* other machine-specific artifacts.

---

# 15. Reproducibility & Evidence Artifacts

The project maintains generated analytical artifacts alongside the source code.

### Data

```text
data/raw/
data/processed/
```

### Models

```text
models/
```

### Analytical Documentation

```text
docs/data_dictionary.md
docs/data_governance_audit.md
docs/compliance_and_audit.md
```

### Forecasting Evidence

```text
docs/timeseries_forecast.csv
docs/timeseries_forecast.png
docs/timeseries_holdout_evaluation.csv
docs/timeseries_model_metadata.json
docs/timeseries_model_metrics.csv
```

### Explainability Evidence

```text
docs/shap_feature_importance.csv
docs/shap_summary.png
```

### Simulation Evidence

```text
data/processed/monte_carlo_results.json
data/processed/monte_carlo_projection.png
```

### Model Artifacts

```text
models/classification_model.pkl
models/classification_metadata.json
models/clustering_model.pkl
models/clustering_scaler.pkl
models/timeseries_model.pkl
```

---

# 16. Project Audit Status

| Area                                | Current Status                     | Evidence                             |
|-------------------------------------|------------------------------------|--------------------------------------|
| Source-data availability            | Addressed                          | `data/raw/synpuf/`                   |
| Data preprocessing                  | Implemented                        | `src/data/make_dataset.py`           |
| Data validation                     | Implemented                        | `src/data/validate_data.py`          |
| Cost-distribution handling          | Addressed                          | `src/data/monte_carlo_simulation.py` |
| Classification modelling            | Implemented                        | `src/models/train_classification.py` |
| Clustering                          | Implemented                        | `src/models/train_clustering.py`     |
| Time-series modelling               | Implemented                        | `src/models/train_timeseries.py`     |
| SHAP explainability                 | Implemented                        | `docs/shap_feature_importance.csv`   |
| Agentic AI evidence routing         | Implemented                        | `src/ai_agent/agent_graph.py`        |
| GenAI evidence controls             | Implemented with known limitations | `src/ai_agent/agent_graph.py`        |
| Formal fairness audit               | Not completed                      | Future control                       |
| Production AWS/SageMaker deployment | Not completed                      | Future deployment                    |
| Production compliance certification | Not applicable                     | Portfolio project                    |

---

# 17. Future Production Controls

If the project were promoted from a portfolio prototype to a production healthcare analytics platform, the following controls would be required before deployment:

1. Formal data classification and privacy assessment.
2. Appropriate identity and access management.
3. Encryption at rest and in transit.
4. Centralized audit logging.
5. Model registry and model-version governance.
6. Dataset and feature lineage.
7. Automated data-quality thresholds and alerts.
8. Model drift monitoring.
9. Bias/fairness evaluation using an appropriate real-world population.
10. Human review for high-impact decisions.
11. Structured validation of LLM-generated responses.
12. Production monitoring and incident management.
13. Formal regulatory and organizational review.
14. Reproducible cloud deployment and infrastructure-as-code.
15. Formal model approval and change-control procedures.

---

# 18. Evidence-Based Governance Principle

The central governance principle of ValueAI is:

> **The analytical system produces the evidence; the AI explains the evidence.**

The LLM should not be treated as the authoritative source of numerical project results.

For quantitative claims, the authoritative sources are the deterministic analytical pipelines and their generated artifacts.

This separation is intended to improve:

* traceability;
* reproducibility;
* explainability;
* stakeholder communication;
* responsible GenAI usage;
* analytical integrity.

---

## Document Status

**Current status:** Governance documentation implemented for the portfolio project.

**Important limitation:** This document records development controls and issue resolution. It does not represent a formal regulatory, legal, clinical, security, or production-compliance certification.
