"""
ValueAI Healthcare Value Intelligence Assistant
Phase 3 - GenAI & Agentic AI

Enterprise-style Streamlit interface for the LangGraph
data science assistant.
"""

from pathlib import Path
import hashlib
import json
import sys

import pandas as pd
import streamlit as st

from src.ai_agent.agent_graph import invoke_agent
from src.ai_agent.agent_tools import analyze_high_risk_cluster
import src.ai_agent.agent_graph as agent_graph_module
import src.ai_agent.agent_tools as agent_tools_module


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_METADATA_PATH = (
    PROJECT_ROOT / "models" / "classification_metadata.json"
)

MODEL_PATH = (
    PROJECT_ROOT / "models" / "classification_model.pkl"
)

CLUSTER_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "clustered_dataset.parquet"
)

SHAP_PATH = (
    PROJECT_ROOT / "docs" / "shap_feature_importance.csv"
)

TIME_SERIES_PATH = (
    PROJECT_ROOT / "models" / "timeseries_model.pkl"
)

MONTE_CARLO_PATH = (
    PROJECT_ROOT / "data" / "processed" / "monte_carlo_results.json"
)


# ============================================================
# AGENT DIAGNOSTICS
# ============================================================

def file_sha256(path: Path) -> str:
    """
    Return SHA-256 hash for a file.

    Used temporarily to prove exactly which source files
    Streamlit has loaded.
    """

    if not path.exists():
        return "FILE NOT FOUND"

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


AGENT_GRAPH_PATH = Path(
    agent_graph_module.__file__
).resolve()

AGENT_TOOLS_PATH = Path(
    agent_tools_module.__file__
).resolve()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ValueAI | Healthcare Value Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LIGHT UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    div[data-testid="stMetric"] {
        padding: 0.25rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD MODEL METADATA
# ============================================================

@st.cache_data
def load_model_metadata():

    if not MODEL_METADATA_PATH.exists():
        return {}

    try:

        with open(
            MODEL_METADATA_PATH,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# ============================================================
# LOAD DATASET RECORD COUNT
# ============================================================

@st.cache_data
def load_dataset_record_count():

    if not CLUSTER_DATA_PATH.exists():
        return None

    try:

        df = pd.read_parquet(
            CLUSTER_DATA_PATH,
            columns=["RISK_CLUSTER"],
        )

        return len(df)

    except Exception:

        return None


# ============================================================
# LOAD CLUSTER COUNT
# ============================================================

@st.cache_data
def load_cluster_count():

    if not CLUSTER_DATA_PATH.exists():
        return None

    try:

        df = pd.read_parquet(
            CLUSTER_DATA_PATH,
            columns=["RISK_CLUSTER"],
        )

        return int(
            df["RISK_CLUSTER"].nunique()
        )

    except Exception:

        return None


# ============================================================
# INITIAL DATA LOAD
# ============================================================

metadata = load_model_metadata()

record_count = load_dataset_record_count()

cluster_count = load_cluster_count()


# ============================================================
# SESSION STATE
# ============================================================

default_prompt = (
    "Analyze the high-risk cluster. "
    "What are the top 3 drivers of readmission based on the SHAP values, "
    "and generate 3 strategic, value-based recommendations for the business?"
)


if "business_question" not in st.session_state:

    st.session_state["business_question"] = default_prompt


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## VALUEAI")

    st.caption("Healthcare Value Intelligence")

    st.divider()

    # --------------------------------------------------------
    # MODEL STATUS
    # --------------------------------------------------------

    st.markdown("### MODEL STATUS")

    status_items = [
        (
            "Clustering Model",
            CLUSTER_DATA_PATH.exists(),
        ),
        (
            "XGBoost Readmission Model",
            MODEL_PATH.exists(),
        ),
        (
            "SHAP Explainability",
            SHAP_PATH.exists(),
        ),
        (
            "Time-Series Forecast",
            TIME_SERIES_PATH.exists(),
        ),
        (
            "Monte Carlo Simulation",
            MONTE_CARLO_PATH.exists(),
        ),
    ]

    for label, available in status_items:

        if available:

            st.markdown(
                f"✓ **{label}**"
            )

        else:

            st.markdown(
                f"⚠ **{label}**"
            )

    st.divider()

    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    st.markdown("### DATASET")

    st.metric(
        "Records",
        f"{record_count:,}"
        if record_count is not None
        else "N/A",
    )

    st.metric(
        "Classification Features",
        metadata.get(
            "n_features",
            "N/A",
        ),
    )

    st.metric(
        "Clusters",
        cluster_count
        if cluster_count is not None
        else "N/A",
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    st.markdown("### READMISSION MODEL")

    auc = metadata.get(
        "test_auc_roc"
    )

    accuracy = metadata.get(
        "test_accuracy"
    )

    if auc is not None:

        st.metric(
            "Test AUC-ROC",
            f"{auc:.4f}",
        )

    if accuracy is not None:

        st.metric(
            "Test Accuracy",
            f"{accuracy:.4f}",
        )

    st.divider()

    # --------------------------------------------------------
    # AI ENGINE
    # --------------------------------------------------------

    st.markdown("### AI ENGINE")

    st.write("**Local LLM**")

    st.code(
        "Qwen 2.5 7B",
        language="text",
    )

    st.write("**Agent Framework**")

    st.code(
        "LangGraph",
        language="text",
    )

    st.write("**Inference**")

    st.code(
        "Local XGBoost",
        language="text",
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("VALUEAI")

st.caption(
    "Healthcare Value Intelligence Assistant"
)

st.divider()


# ============================================================
# TEMPORARY DEVELOPER DIAGNOSTICS
# ============================================================

with st.expander(
    "Developer Diagnostics",
    expanded=False,
):

    st.markdown(
        "### Runtime"
    )

    st.write(
        "Python executable:",
        sys.executable,
    )

    st.write(
        "Python version:",
        sys.version,
    )

    st.write(
        "Project root:",
        str(PROJECT_ROOT),
    )

    st.markdown(
        "### Imported Modules"
    )

    st.write(
        "Agent graph loaded from:",
        str(AGENT_GRAPH_PATH),
    )

    st.write(
        "Agent tools loaded from:",
        str(AGENT_TOOLS_PATH),
    )

    st.write(
        "agent_graph.py SHA-256:",
        file_sha256(AGENT_GRAPH_PATH),
    )

    st.write(
        "agent_tools.py SHA-256:",
        file_sha256(AGENT_TOOLS_PATH),
    )

    st.markdown(
        "### Analytical Artifacts"
    )

    st.write(
        "Clustered dataset:",
        str(CLUSTER_DATA_PATH),
    )

    st.write(
        "Clustered dataset exists:",
        CLUSTER_DATA_PATH.exists(),
    )

    st.write(
        "SHAP artifact:",
        str(SHAP_PATH),
    )

    st.write(
        "SHAP artifact exists:",
        SHAP_PATH.exists(),
    )

    st.write(
        "Classification model:",
        str(MODEL_PATH),
    )

    st.write(
        "Classification model exists:",
        MODEL_PATH.exists(),
    )

    st.markdown(
        "### Direct Analytical Tool Test"
    )

    st.caption(
        "This bypasses LangGraph and Qwen and directly executes "
        "analyze_high_risk_cluster()."
    )

    if st.button(
        "Test Analytical Tool Directly",
        key="diagnostic_tool_test",
    ):

        try:

            diagnostic_result = (
                analyze_high_risk_cluster.invoke({})
            )

            st.success(
                "Analytical tool executed successfully."
            )

            st.code(
                diagnostic_result,
                language="json",
            )

        except Exception as exc:

            st.error(
                "Direct analytical tool execution failed."
            )

            st.exception(exc)


# ============================================================
# BUSINESS QUESTION
# ============================================================

st.subheader(
    "Ask the Data Science Assistant"
)

st.caption(
    "Ask questions about patient segmentation, readmission risk, "
    "model drivers, utilization patterns, and business value."
)


# ============================================================
# QUICK ANALYSIS OPTIONS
# ============================================================

st.markdown(
    "### Quick Analysis"
)

quick_col1, quick_col2, quick_col3 = st.columns(3)


with quick_col1:

    if st.button(
        "High-Risk Cluster",
        use_container_width=True,
    ):

        st.session_state["business_question"] = (
            "Analyze the high-risk cluster. "
            "Describe its population and utilization profile, "
            "identify the top 3 model drivers based on mean absolute "
            "SHAP importance, and propose 3 evidence-grounded "
            "business interventions."
        )

        st.rerun()


with quick_col2:

    if st.button(
        "Model Drivers",
        use_container_width=True,
    ):

        st.session_state["business_question"] = (
            "What are the top 10 drivers of readmission according to "
            "the Phase 2 SHAP analysis? Explain what mean absolute SHAP "
            "importance tells us and clearly distinguish model "
            "importance from causation."
        )

        st.rerun()


with quick_col3:

    if st.button(
        "Business Memo",
        use_container_width=True,
    ):

        st.session_state["business_question"] = (
            "Generate an executive business memo for the high-risk "
            "cluster using the available analytical evidence. "
            "Include the population profile, top model drivers, "
            "what the data shows, 3 proposed strategic interventions, "
            "value mechanisms, KPIs, and model/data caveats."
        )

        st.rerun()


# ============================================================
# BUSINESS QUESTION INPUT
# ============================================================

prompt = st.text_area(
    "Business question",
    key="business_question",
    height=120,
    label_visibility="collapsed",
)


# ============================================================
# RUN ANALYSIS
# ============================================================

st.markdown("")

analyze_button = st.button(
    "Run Analysis",
    type="primary",
    use_container_width=True,
)


if analyze_button:

    if not prompt.strip():

        st.warning(
            "Please enter a business question."
        )

        st.stop()

    with st.spinner(
        "Analyzing Phase 2 evidence and generating executive insights..."
    ):

        try:

            response = invoke_agent(
                prompt.strip()
            )

        except Exception as exc:

            st.error(
                "The analysis could not be completed."
            )

            st.exception(exc)

            st.stop()

    st.session_state[
        "analysis_response"
    ] = response


# ============================================================
# DISPLAY EXECUTIVE MEMO
# ============================================================

if "analysis_response" in st.session_state:

    st.divider()

    st.subheader(
        "EXECUTIVE MEMO"
    )

    st.caption(
        "Generated from the ValueAI analytical tools and local "
        "Qwen 2.5 7B reasoning layer."
    )

    response = st.session_state[
        "analysis_response"
    ]

    with st.container(border=True):

        st.markdown(response)