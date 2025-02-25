import streamlit as st
import pandas as pd
import numpy as np

# Import modules for different functionalities
from modules.data_input import data_input_sidebar
from modules.measures_variability import measures_variability_tab
from modules.visualization import visualization_tab
from modules.all_stats import all_stats_tab
from modules.measures_center import calculate_mean, calculate_median, calculate_mode, measures_center_tab

# Set page config
st.set_page_config(
    page_title="Statistical Measures Learning App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-left: 10px;
        padding-right: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f3ff;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("📊 Statistical Measures Learning App")
st.markdown("""
This app helps you learn and practice statistical concepts from Chapter 2: "Describing Data with Numerical Measures".

Enter your data in the sidebar, then explore different tabs to see calculations for various statistical measures.
""")

# Sidebar for data input
data = data_input_sidebar()

# Main content with tabs
if data is not None and len(data) > 0:
    tab1, tab2, tab3, tab4 = st.tabs(["📏 Measures of Center", "📊 Measures of Variability", "📈 Visualization", "🧮 All Statistics"])
    
    with tab1:
        measures_center_tab(data)
    
    with tab2:
        measures_variability_tab(data)
    
    with tab3:
        visualization_tab(data)
    
    with tab4:
        all_stats_tab(data)
else:
    st.info("👈 Please enter your data in the sidebar to get started.")
