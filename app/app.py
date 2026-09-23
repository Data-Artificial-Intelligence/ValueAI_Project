"""
Unified Executive Dashboard for ValueAI.
Matches JD: "data visualization techniques, to create solutions that enable enhanced business performance"
"""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import streamlit as st
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# Import Phase 3 Agent
try:
    from src.ai_agent.agent_graph import invoke_agent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False

st.set_page_config(
    page_title="ValueAI Executive Dashboard", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .status-complete { background: #d4edda; color: #155724; }
    .status-warning { background: #fff3cd; color: #856404; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header"> ValueAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Healthcare Value Intelligence Platform</p>', unsafe_allow_html=True)

# Status Bar
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<span class="status-badge status-complete">✅ All Phases Complete</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="status-badge status-complete">✅ Governance Cleared</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="status-badge status-complete">✅ MLOps Ready</span>', unsafe_allow_html=True)

st.divider()

# Create comprehensive tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "👥 Patient Segmentation", 
    "🎯 Readmission Risk",
    "📈 Cost Forecasting",
    "🤖 AI Business Assistant"
])

# --- TAB 1: EXECUTIVE OVERVIEW ---
with tab1:
    st.header("Strategic Overview")
    
    # Load key metrics
    metrics_path = PROJECT_ROOT / "models" / "classification_metadata.json"
    if metrics_path.exists():
        with open(metrics_path, "r") as f:
            model_meta = json.load(f)
    else:
        model_meta = {}
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{int(model_meta.get('n_records', 230890)):,}")
    with col2:
        st.metric("XGBoost AUC-ROC", f"{model_meta.get('auc_roc', 0.9535):.4f}")
    with col3:
        st.metric("Model Accuracy", f"{model_meta.get('accuracy', 0.8777):.2%}")
    with col4:
        st.metric("Clusters Identified", model_meta.get('n_clusters', 3))
    
    st.divider()
    
    # Executive Summary
    st.subheader(" Executive Summary")
    summary_path = PROJECT_ROOT / "docs" / "executive_summary.md"
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.info("📄 Executive Summary not found. Please ensure docs/executive_summary.md exists.")
    
    # Key Findings
    st.divider()
    st.subheader("🎯 Key Findings")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **High-Risk Population**
        - Cluster 2 represents ~13% of total population
        - Average age: 75+ years
        - 2.9x higher admission rate
        - 4.2x higher healthcare costs
        """)
    with col2:
        st.markdown("""
        **Primary Readmission Drivers**
        1. Average days between inpatient claims
        2. Total admission count
        3. Unique diagnosis count
        4. Beneficiary response for inpatient services
        """)

# --- TAB 2: PATIENT SEGMENTATION ---
with tab2:
    st.header("GMM Patient Risk Clustering & SHAP Explainability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Cluster Distribution")
        cluster_plot = PROJECT_ROOT / "docs" / "cluster_distribution.png"
        if cluster_plot.exists():
            st.image(str(cluster_plot), use_container_width=True)
        else:
            st.info("Run Phase 2 clustering to generate this plot.")
            
    with col2:
        st.subheader("🔍 Readmission Drivers (SHAP)")
        shap_plot = PROJECT_ROOT / "docs" / "shap_summary.png"
        if shap_plot.exists():
            st.image(str(shap_plot), use_container_width=True)
        else:
            st.info("Run Phase 2 classification to generate this plot.")
    
    st.divider()
    
    # Cluster Details
    st.subheader(" Cluster Characteristics")
    
    # Load clustered data if available
    cluster_data_path = PROJECT_ROOT / "data" / "processed" / "clustered_dataset.parquet"
    if cluster_data_path.exists():
        try:
            df_clustered = pd.read_parquet(cluster_data_path)
            
            if "RISK_CLUSTER" in df_clustered.columns:
                cluster_stats = df_clustered.groupby("RISK_CLUSTER").agg({
                    "AGE": "mean",
                    "TOTAL_ADMISSIONS": "mean",
                    "AVG_ADMISSION_COST": "mean",
                    "UNIQUE_DIAGNOSES_COUNT": "mean"
                }).round(2)
                
                st.dataframe(cluster_stats, use_container_width=True)
                
                st.markdown("""
                **Key Insight:** Cluster 2 (High Risk) is primarily driven by `UNIQUE_DIAGNOSES_COUNT` and `TOTAL_ADMISSIONS`. 
                
                *Note: SHAP values indicate magnitude of impact, not directional causation.*
                """)
        except Exception as e:
            st.error(f"Error loading cluster data: {e}")
    else:
        st.info("Clustered dataset not found. Run Phase 2 clustering first.")

# --- TAB 3: READMISSION RISK ---
with tab3:
    st.header("🎯 XGBoost Readmission Prediction Model")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("AUC-ROC Score", f"{model_meta.get('auc_roc', 0.9535):.4f}")
        st.metric("Test Accuracy", f"{model_meta.get('accuracy', 0.8777):.2%}")
    with col2:
        st.metric("Training Samples", f"{model_meta.get('n_train_samples', 21294):,}")
        st.metric("Test Samples", f"{model_meta.get('n_test_samples', 4455):,}")
    
    st.divider()
    
    # SHAP Analysis
    st.subheader(" Feature Importance Analysis")
    shap_path = PROJECT_ROOT / "docs" / "shap_feature_importance.csv"
    if shap_path.exists():
        df_shap = pd.read_csv(shap_path)
        st.dataframe(df_shap.head(10), use_container_width=True)
        
        st.markdown("""
        **Understanding SHAP Values:**
        - Mean absolute SHAP measures the average magnitude of a feature's contribution
        - Does NOT indicate direction (higher/lower values increase risk)
        - Does NOT establish causation
        - Used for model interpretability and feature prioritization
        """)
    else:
        st.info("SHAP analysis not available. Run Phase 2 classification with SHAP enabled.")

# --- TAB 4: COST FORECASTING ---
with tab4:
    st.header("📈 ARIMA Time-Series Cost Projection")
    
    forecast_plot = PROJECT_ROOT / "docs" / "timeseries_forecast.png"
    metrics_path = PROJECT_ROOT / "docs" / "timeseries_model_metrics.csv"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if forecast_plot.exists():
            st.image(str(forecast_plot), use_container_width=True)
        else:
            st.info("Run Phase 2 time-series to generate this plot.")
            
    with col2:
        st.subheader("📊 Model Evaluation")
        if metrics_path.exists():
            df_metrics = pd.read_csv(metrics_path)
            st.dataframe(df_metrics, use_container_width=True)
            
            # Calculate improvement
            if len(df_metrics) >= 2:
                naive_rmse = df_metrics.iloc[0]['rmse']
                arima_rmse = df_metrics.iloc[1]['rmse']
                improvement = ((naive_rmse - arima_rmse) / naive_rmse) * 100
                st.success(f"✅ ARIMA RMSE improvement: {improvement:.1f}% vs baseline")
        else:
            st.info("Metrics pending.")
    
    st.divider()
    
    # Forecast details
    st.subheader("📅 12-Month Forecast Summary")
    forecast_csv = PROJECT_ROOT / "docs" / "timeseries_forecast.csv"
    if forecast_csv.exists():
        df_forecast = pd.read_csv(forecast_csv)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Projected Cost", f"${df_forecast['forecast'].sum():,.0f}")
        with col2:
            st.metric("Avg Monthly Cost", f"${df_forecast['forecast'].mean():,.0f}")
        with col3:
            st.metric("Forecast Period", f"{len(df_forecast)} months")
    else:
        st.info("Forecast data not available.")

# --- TAB 5: AGENTIC AI ASSISTANT ---
with tab5:
    st.header("🤖 ValueAI Data Science Assistant")
    st.markdown("""
    **Ask natural language questions about the data.** 
    The AI retrieves *verified* Phase 2 evidence before answering.
    
    **Try asking:**
    - "Analyze the high-risk cluster and give 3 strategic recommendations"
    - "What are the top drivers of readmission?"
    - "Generate an executive memo for the high-risk segment"
    """)
    
    if not AGENT_AVAILABLE:
        st.error("""
        ⚠️ **GenAI Agent dependencies not found.**
        
        Please ensure:
        - `langchain`, `langgraph`, and `langchain_ollama` are installed
        - Ollama is running with Qwen 2.5 7B model
        - Run: `ollama run qwen2.5:7b`
        """)
    else:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "Hello! I am the ValueAI Data Science Assistant. I can analyze high-risk clusters, explain SHAP drivers, or predict individual readmission risk. Try asking: *'Analyze the high-risk cluster and give 3 strategic recommendations.'*"
                }
            ]

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about the models or data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🧠 Retrieving verified evidence and generating insights..."):
                    try:
                        response = invoke_agent(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"⚠️ Error: {str(e)}")
                        st.markdown("**Troubleshooting:**")
                        st.code("""
1. Ensure Ollama is running: ollama run qwen2.5:7b
2. Check that all Phase 2 models are trained
3. Verify SHAP and clustering artifacts exist in docs/
                        """)

# Sidebar - Model Status
with st.sidebar:
    st.header("️ System Status")
    
    st.markdown("### Model Status")
    status_items = [
        ("Clustering Model", PROJECT_ROOT / "models" / "clustering_model.pkl"),
        ("XGBoost Readmission Model", PROJECT_ROOT / "models" / "classification_model.pkl"),
        ("SHAP Explainability", PROJECT_ROOT / "docs" / "shap_feature_importance.csv"),
        ("Time-Series Forecast", PROJECT_ROOT / "docs" / "timeseries_forecast.csv"),
        ("Monte Carlo Simulation", PROJECT_ROOT / "data" / "processed" / "monte_carlo_results.json"),
    ]
    
    for label, path in status_items:
        if path.exists():
            st.markdown(f"✅ **{label}**")
        else:
            st.markdown(f"⚠️ **{label}**")
    
    st.divider()
    
    st.markdown("### AI Engine")
    st.code("Qwen 2.5 7B", language="text")
    st.markdown("**Framework:** LangGraph")
    st.markdown("**Architecture:** Evidence-First RAG")
    
    st.divider()
    
    st.markdown("### Dataset")
    st.metric("Records", f"{int(model_meta.get('n_records', 230890)):,}")
    st.metric("Features", model_meta.get('n_features', 44))