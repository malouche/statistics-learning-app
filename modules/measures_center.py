import streamlit as st
import numpy as np
import pandas as pd

def calculate_mean(data):
    """Calculate the mean with step-by-step explanation"""
    n = len(data)
    sum_data = sum(data)
    mean_value = sum_data / n
    
    steps = f"""
    ### Mean Calculation
    
    The mean of a set of measurements is the sum of the measurements divided by the total number of measurements.
    
    **Formula**: $\\bar{{x}} = \\frac{{\\sum_{{i=1}}^{{n}} x_i}}{{n}}$
    
    **Step 1**: Sum all measurements
    $\\sum_{{i=1}}^{{{n}}} x_i = {' + '.join([str(x) for x in data])} = {sum_data}$
    
    **Step 2**: Divide by the number of measurements (n = {n})
    $\\bar{{x}} = \\frac{{{sum_data}}}{{{n}}} = {mean_value:.6f}$
    """
    
    return mean_value, steps

def calculate_median(data):
    """Calculate the median with step-by-step explanation"""
    n = len(data)
    sorted_data = sorted(data)
    position = 0.5 * (n + 1)
    pos_int = int(position)
    pos_frac = position - pos_int
    
    if pos_frac == 0:
        median_value = sorted_data[pos_int - 1]  # Adjust for 0-indexed list
        calculation = f"The {pos_int}th value in the sorted data: {median_value}"
    else:
        lower_value = sorted_data[pos_int - 1]  # Adjust for 0-indexed list
        upper_value = sorted_data[pos_int]  # Adjust for 0-indexed list
        median_value = lower_value + pos_frac * (upper_value - lower_value)
        calculation = f"Between positions {pos_int} and {pos_int + 1}: {lower_value} + {pos_frac:.2f} × ({upper_value} - {lower_value}) = {median_value}"
    
    steps = f"""
    ### Median Calculation
    
    The median is the middle value when the measurements are ranked from smallest to largest.
    
    **Step 1**: Sort the data
    {sorted_data}
    
    **Step 2**: Find the position of the median
    Position = 0.5 × (n + 1) = 0.5 × ({n} + 1) = {position}
    
    **Step 3**: Determine the median
    {calculation}
    """
    
    return median_value, steps

def calculate_mode(data):
    """Calculate the mode with step-by-step explanation"""
    # Count occurrences of each value
    value_counts = {}
    for x in data:
        if x in value_counts:
            value_counts[x] += 1
        else:
            value_counts[x] = 1
    
    # Find the maximum frequency
    max_count = max(value_counts.values())
    
    # If all values appear once, there is no mode
    if max_count == 1:
        mode_values = []
        mode_type = "No mode"
    else:
        # Find all values with the maximum frequency
        mode_values = [x for x, count in value_counts.items() if count == max_count]
        if len(mode_values) == 1:
            mode_type = "Unimodal"
        elif len(mode_values) == 2:
            mode_type = "Bimodal"
        else:
            mode_type = "Multimodal"
    
    # Generate frequency table
    freq_table = pd.DataFrame({
        "Value": list(value_counts.keys()),
        "Frequency": list(value_counts.values())
    }).sort_values("Value").reset_index(drop=True)
    
    # Create a markdown table instead of HTML
    freq_table_md = "| Value | Frequency |\n| ---: | ---: |\n"
    
    # Add rows with highlighting for the mode values
    for _, row in freq_table.iterrows():
        freq_table_md += f"| {row['Value']} | {row['Frequency']} |\n"
    
    # Generate explanation
    if mode_values:
        mode_str = ", ".join([str(x) for x in sorted(mode_values)])
        result = f"{mode_str} (each appears {max_count} times)"
    else:
        result = "No mode (all values appear only once)"
    
    steps = f"""
    ### Mode Calculation
    
    The mode is the value(s) that appear most frequently in the dataset.
    
    **Step 1**: Count the frequency of each value
    
    {freq_table_md}
    
    **Step 2**: Identify the value(s) with the highest frequency
    Maximum frequency: {max_count}
    
    **Step 3**: Determine the mode
    Mode type: {mode_type}
    Result: {result}
    """
    
    return mode_values, steps

def measures_center_tab(data):
    """Display the measures of center tab content"""
    st.header("📏 Measures of Center")
    st.write("Learn how to calculate the mean, median, and mode with step-by-step explanations.")
    
    # Select measure to explore
    measure = st.radio(
        "Select a measure to explore:",
        ["Mean", "Median", "Mode", "Compare All"],
        horizontal=True
    )
    
    # Display the current data
    sorted_data = sorted(data)
    st.write("**Current data (sorted):**", sorted_data)
    
    # Create columns for displaying results
    if measure == "Compare All":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Mean")
            mean_value, mean_steps = calculate_mean(data)
            st.metric("Mean", f"{mean_value:.4f}")
        
        with col2:
            st.subheader("Median")
            median_value, median_steps = calculate_median(data)
            st.metric("Median", f"{median_value:.4f}")
        
        with col3:
            st.subheader("Mode")
            mode_values, mode_steps = calculate_mode(data)
            if mode_values:
                mode_display = ", ".join([str(x) for x in sorted(mode_values)])
            else:
                mode_display = "No mode"
            st.metric("Mode", mode_display)
        
        # Display all steps
        with st.expander("Show Calculation Steps", expanded=True):
            st.markdown(mean_steps)
            st.markdown("---")
            st.markdown(median_steps)
            st.markdown("---")
            st.markdown(mode_steps)
    
    elif measure == "Mean":
        mean_value, steps = calculate_mean(data)
        st.metric("Mean", f"{mean_value:.4f}")
        st.markdown(steps)
    
    elif measure == "Median":
        median_value, steps = calculate_median(data)
        st.metric("Median", f"{median_value:.4f}")
        st.markdown(steps)
    
    elif measure == "Mode":
        mode_values, steps = calculate_mode(data)
        if mode_values:
            mode_display = ", ".join([str(x) for x in sorted(mode_values)])
        else:
            mode_display = "No mode"
        st.metric("Mode", mode_display)
        st.markdown(steps)
        
        # Highlight the mode values in a separate section
        if mode_values:
            st.write("**Mode values highlighted:**")
            
            # Create a dataframe with mode values highlighted
            freq_df = pd.DataFrame()
            value_counts = {}
            for x in data:
                if x in value_counts:
                    value_counts[x] += 1
                else:
                    value_counts[x] = 1
                    
            freq_df = pd.DataFrame({
                "Value": list(value_counts.keys()),
                "Frequency": list(value_counts.values())
            }).sort_values("Value").reset_index(drop=True)
            
            # Use st.dataframe with styling to highlight the mode
            def highlight_mode(row):
                if row["Value"] in mode_values:
                    return ['background-color: #e6f3ff; font-weight: bold;'] * 2
                return [''] * 2
            
            st.dataframe(freq_df.style.apply(highlight_mode, axis=1))
    
    # Provide context about when to use each measure
    with st.expander("When to use each measure of center"):
        st.markdown("""
        ### When to use each measure of center:
        
        - **Mean**: Best for symmetrical distributions. Sensitive to outliers.
          - Use when you need to account for all values in the dataset
          - Common in statistical analyses and many mathematical operations
          
        - **Median**: Best for skewed distributions or data with outliers.
          - Less affected by extreme values than the mean
          - Good for income, home prices, and other skewed distributions
          
        - **Mode**: Best for categorical data or when you need the most common value.
          - Most useful for discrete data with clear frequencies
          - Can have multiple modes or no mode at all
        
        **Rule of thumb for skewed distributions:**
        - If skewed right (tail extends to the right): Mean > Median
        - If skewed left (tail extends to the left): Mean < Median
        - If symmetric: Mean ≈ Median
        """)