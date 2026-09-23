# EXECUTIVE SUMMARY: ValueAI Risk Stratification & Agentic AI Intelligence Platform

**Project:** ValueAI Risk Stratification & Agentic AI Platform
**Author:** Antony Henry Oduor Onyango
**Date:** September 2026
**Purpose:** Demonstrate an end-to-end data science capability spanning big-data engineering, statistical analysis, predictive modelling, segmentation, forecasting, simulation, explainable AI, and GenAI-enabled decision support.

---

## 1. BUSINESS PROBLEM

Value-based programs require organizations to transform large and complex datasets into actionable insights that support proactive intervention, resource allocation, risk management, and improved business performance.

The ValueAI project was developed as an end-to-end analytical solution to demonstrate how fragmented claims data can be transformed into:

* Risk-stratified population segments.
* Predictive estimates of 30-day readmission risk.
* Statistical projections of future healthcare costs.
* Quantitative uncertainty estimates through simulation.
* Explainable model outputs for stakeholder interpretation.
* Natural-language access to verified analytical findings through an Agentic AI interface.

The project deliberately combines statistical modelling, data mining, visualization, big-data processing, and practical GenAI into a single analytical workflow.

---

## 2. DATA & BIG-DATA ENGINEERING

The project uses the CMS Synthetic Medicare Public Use Files (SynPUF), a synthetic and de-identified dataset suitable for demonstrating healthcare analytics workflows without processing real patient identities.

Using **PySpark**, the pipeline ingested, cleaned, transformed, and integrated multiple claims sources, including:

* Beneficiary summary data.
* Inpatient claims.
* Outpatient claims.
* Prescription drug events.
* Carrier claims data where applicable.

The resulting analytical workflow processed **more than 6.5 million records** and produced optimized **Parquet** datasets for downstream modelling.

The pipeline was designed to handle practical data-engineering issues encountered during implementation, including:

* Missing legacy source files.
* Schema differences between source datasets.
* Null and invalid values.
* Duplicate submission risks.
* Non-positive cost observations.
* Data-quality validation requirements.
* Train/validation/test dataset separation.

This established the foundation required for scalable statistical analysis and machine-learning workflows.

---

## 3. STATISTICAL MODELLING & DATA MINING

### Population Segmentation

A **Gaussian Mixture Model (GMM)** was developed to identify distinct population segments based on utilization and risk-related characteristics.

The clustering workflow included feature preparation, scaling, model fitting, cluster profiling, and evaluation using the **Silhouette Score**.

The resulting model achieved a Silhouette Score of approximately **0.35**, providing a quantitative basis for interpreting the resulting population segments.

Cluster profiles were subsequently made available to the downstream analytical and Agentic AI components.

### Predictive Modelling

An **XGBoost classification model** was developed to predict 30-day readmission risk.

The modelling workflow included:

* Feature engineering.
* Label construction.
* Train/validation/test separation.
* Model training.
* Performance evaluation.
* Feature-importance analysis.
* SHAP-based explainability.

The evaluated model achieved approximately:

* **AUC: 0.95**
* **Accuracy: 87.7%**

SHAP analysis was incorporated to help explain which model features contributed most strongly to predictions, supporting communication of analytical findings to non-technical stakeholders.

Importantly, model explanations were treated as measures of predictive contribution rather than evidence of causal relationships.

---

## 4. TIME-SERIES ANALYSIS & ECONOMETRIC PROJECTIONS

A time-series forecasting workflow was developed to project healthcare cost patterns.

The project evaluated an **ARIMA(1,1,1)** model using an out-of-sample holdout period and compared its performance against a naive forecasting baseline.

The final evaluation demonstrated approximately a **14.9% RMSE improvement over the selected naive baseline**.

During model development, the underlying synthetic dataset was also examined for structural changes in the later observation period. A decline in late-period synthetic claim volume was identified and documented rather than being treated as an unquestioned representation of real-world future behaviour.

This provided an important analytical control against producing misleading projections from artificial data characteristics.

---

## 5. MONTE CARLO SIMULATION & UNCERTAINTY ANALYSIS

A Monte Carlo simulation was developed to estimate the distribution of potential future healthcare admission costs.

The workflow:

1. Loaded historical admission-cost observations.
2. Validated and filtered non-positive cost values before fitting.
3. Fitted a log-normal distribution to eligible historical costs.
4. Generated repeated simulated cost outcomes.
5. Produced a 12-month projection.
6. Quantified uncertainty using a **95% prediction interval**.
7. Saved the resulting projection and supporting metadata for downstream use.

The simulation complements point forecasting by providing a distribution of possible outcomes rather than relying solely on a single expected value.

---

## 6. DATA QUALITY, GOVERNANCE & AUDITABILITY

Data quality was treated as a core component of the analytical workflow rather than a separate final-stage activity.

The project includes automated validation through **Great Expectations**, together with documented data-governance and audit considerations.

Several implementation issues were identified and resolved during development, including:

* Missing beneficiary source data.
* Invalid/non-positive cost observations affecting distribution fitting.
* Time-series model complexity relative to the available observations.
* Potential hallucination risk when using an LLM to communicate quantitative model results.

The project maintains supporting documentation covering data definitions, analytical outputs, model metadata, and governance considerations.

Where source-data limitations were identified, they were documented rather than hidden from downstream analysis.

---

## 7. GENAI & AGENTIC AI DECISION SUPPORT

The third phase extended the analytical platform with a practical **Agentic AI** interface.

A **LangGraph** workflow was integrated with a locally hosted **Qwen 2.5 7B** model through Ollama.

The objective was not to allow the LLM to independently invent analytical conclusions, but to create a natural-language interface over verified analytical outputs.

### Evidence-First Architecture

The Agentic AI workflow retrieves verified analytical artifacts before generating its response.

Available evidence includes:

* GMM cluster profiles.
* SHAP feature-importance results.
* Time-series forecast outputs.
* Model evaluation information.
* Other validated project artifacts.

This architecture separates:

**Analytical computation → Evidence retrieval → Natural-language interpretation**

rather than asking the LLM to independently calculate or invent quantitative findings.

This provides a practical approach for reducing hallucination risk when exposing data-science outputs to non-technical users.

### Stakeholder Interaction

The system supports natural-language questions such as:

* Which population segment has the highest observed risk characteristics?
* What factors contribute most strongly to the readmission model?
* What does the cost forecast indicate?
* What strategic considerations arise from the model outputs?

The assistant can also synthesize verified analytical evidence into structured business-oriented responses.

---

## 8. STAKEHOLDER COMMUNICATION & VISUALIZATION

The project incorporates **Streamlit** to provide a stakeholder-facing interface for analytical results.

The existing analytical artifacts include visualizations covering:

* Population cluster distribution.
* SHAP feature importance.
* Time-series forecasts.
* Monte Carlo cost projections.

The platform is designed to bridge the gap between technical analytical outputs and business stakeholders by presenting model findings in an accessible format.

This reflects the broader objective of the project: **turning advanced analytical methods into usable business intelligence rather than producing models in isolation.**

---

## 9. KEY ANALYTICAL OUTPUTS

| Capability              | Implementation           | Output                                |
|-------------------------|--------------------------|---------------------------------------|
| Big-data processing     | PySpark                  | 6.5M+ claims records processed        |
| Data transformation     | PySpark / Parquet        | Reusable analytical datasets          |
| Population segmentation | Gaussian Mixture Model   | Risk/utilization clusters             |
| Predictive modelling    | XGBoost                  | 30-day readmission classifier         |
| Model explainability    | SHAP                     | Feature contribution analysis         |
| Time-series analysis    | ARIMA(1,1,1)             | Cost projection                       |
| Forecast evaluation     | Holdout + naive baseline | 14.9% RMSE improvement                |
| Uncertainty modelling   | Monte Carlo simulation   | 95% prediction interval               |
| Data quality            | Great Expectations       | Automated validation                  |
| GenAI                   | Qwen 2.5 7B              | Natural-language analytical interface |
| Agent orchestration     | LangGraph                | Evidence-first analytical workflow    |
| Visualization           | Streamlit / Matplotlib   | Stakeholder-facing analytical views   |

---

## 10. BUSINESS VALUE

The ValueAI platform demonstrates how a data-science function can move from raw data to decision support through a connected analytical lifecycle:

**Large-scale data → Data quality → Feature engineering → Statistical modelling → Prediction → Segmentation → Forecasting → Explainability → GenAI interpretation → Stakeholder insight**

The resulting capability can support business use cases such as:

* Population risk stratification.
* Targeted resource allocation.
* Identification of high-utilization segments.
* Readmission-risk analysis.
* Cost projection and scenario analysis.
* Executive analytical reporting.
* Self-service access to verified data-science findings.

The recommendations generated by the system are intended to support business decision-making and should be validated against the organization's actual operational, clinical, financial, regulatory, and strategic requirements before implementation.

---

## 11. LIMITATIONS & ANALYTICAL CONTROLS

The project uses **synthetic Medicare claims data**, meaning its analytical findings should not be interpreted as direct evidence about real-world patient populations or actual healthcare outcomes.

Accordingly:

* Model performance metrics describe this project's evaluation dataset.
* Forecasts should not be treated as real-world financial projections.
* Correlation or predictive contribution should not be interpreted as causation.
* Synthetic-data artefacts were explicitly considered during time-series analysis.
* Business recommendations require validation against real organizational data before operational deployment.

These controls are important to ensure that analytical sophistication does not create false confidence in the underlying evidence.

---

## 12. CONCLUSION

ValueAI demonstrates practical capability across the principal areas required of a modern Data Scientist & Analytics function:

**advanced statistical modelling, data mining, large-scale data processing, visualization, predictive analytics, segmentation, sampling and simulation, time-series forecasting, explainable machine learning, stakeholder communication, and practical GenAI/Agentic AI implementation.**

The project establishes a reusable technical foundation for extending analytical models into governed, stakeholder-facing decision-support capabilities while maintaining traceability between business questions, data, models, evidence, and recommendations.
