import streamlit as st
import pandas as pd
import numpy as np

def data_input_sidebar():
    """Create sidebar for data input and return the entered data"""
    with st.sidebar:
        st.header("Data Input")
        st.markdown("Enter up to 30 observations. Each value must be a number.")
        
        input_method = st.radio(
            "Choose input method:",
            ["Manual Entry", "Sample Datasets"],
            index=0
        )
        
        if input_method == "Manual Entry":
            col1, col2 = st.columns(2)
            
            with col1:
                n_values = st.number_input(
                    "Number of observations:",
                    min_value=1,
                    max_value=30,
                    value=5,
                    step=1
                )
            
            with col2:
                separator = st.selectbox(
                    "Input separator:",
                    options=["One per line", "Comma", "Space", "Tab"],
                    index=0
                )
            
            if separator == "One per line":
                placeholder = "\n".join([f"Value {i+1}" for i in range(min(5, n_values))])
                input_data = st.text_area(
                    "Enter values (one per line):",
                    height=min(200, n_values * 40),
                    placeholder=placeholder
                )
                if input_data:
                    try:
                        data = [float(x.strip()) for x in input_data.split("\n") if x.strip()]
                    except ValueError:
                        st.error("❌ All values must be numbers. Please check your input.")
                        return None
            else:
                sep_map = {"Comma": ",", "Space": " ", "Tab": "\t"}
                sep = sep_map[separator]
                placeholder = f"e.g.: 10{sep}20{sep}30{sep}40{sep}50"
                input_data = st.text_input(
                    f"Enter values separated by {separator.lower()}:",
                    placeholder=placeholder
                )
                if input_data:
                    try:
                        data = [float(x.strip()) for x in input_data.split(sep) if x.strip()]
                    except ValueError:
                        st.error("❌ All values must be numbers. Please check your input.")
                        return None
                else:
                    data = []
        else:  # Sample datasets
            dataset = st.selectbox(
                "Choose a sample dataset:",
                [
                    "Walking Shoe Prices ($)",
                    "Milk Purchases (quarts)",
                    "Sodium Content in Cheese (mg)",
                    "Faculty Ages",
                    "Flower Petals"
                ]
            )
            
            sample_data = {
                "Walking Shoe Prices ($)": [40, 60, 65, 65, 65, 68, 68, 70, 70, 70, 70, 70, 70, 74, 75, 75, 90, 95],
                "Milk Purchases (quarts)": [0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5],
                "Sodium Content in Cheese (mg)": [260, 290, 300, 320, 330, 340, 340, 520],
                "Faculty Ages": [34, 48, 70, 63, 52, 52, 35, 50, 37, 43, 53, 43, 52, 44, 42, 31, 36, 48, 43, 26],
                "Flower Petals": [5, 12, 6, 8, 14]
            }
            
            data = sample_data[dataset]
            st.success(f"✅ Loaded {len(data)} observations from '{dataset}'")
            
            # Display the loaded data
            st.write("Preview:")
            st.write(data)
        
        # Data validation and stats
        if 'data' in locals() and len(data) > 0:
            if len(data) > 30:
                st.warning("⚠️ Maximum 30 observations allowed. Using only the first 30.")
                data = data[:30]
            
            st.write(f"**Current data:** {len(data)} observations")
            
            if st.button("Clear Data"):
                data = []
                st.experimental_rerun()
            
            return data
        else:
            return None