import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    
    # Convert values to appropriate types for display
    freq_table = freq_table.astype({"Value": float, "Frequency": int})
    
    # Create a more visually appealing markdown table
    has_decimals = any(x != int(x) for x in freq_table['Value'])
    value_format = ".2f" if has_decimals else ""
    
    # Build an improved markdown table
    freq_table_md = """| Value | Frequency | Bar Chart |\n|------:|----------:|:----------|\n"""
    
    max_freq = max(freq_table['Frequency'])
    bar_scale = 20  # Maximum number of characters for the full bar
    
    # Add rows with special formatting for mode values
    for _, row in freq_table.iterrows():
        value = row['Value']
        frequency = row['Frequency']
        is_mode = value in mode_values
        
        # Format the value based on whether it's an integer or float
        if has_decimals:
            value_str = f"{value:.2f}"
        else:
            value_str = f"{int(value)}"
        
        # Create a bar representing the frequency
        bar_length = int((frequency / max_freq) * bar_scale)
        bar = "█" * bar_length
        
        # Add bold formatting if this is a mode value
        if is_mode:
            freq_table_md += f"| **{value_str}** | **{frequency}** | **{bar}** |\n"
        else:
            freq_table_md += f"| {value_str} | {frequency} | {bar} |\n"
    
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
    
    return mode_values, steps, freq_table

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
            mode_values, mode_steps, _ = calculate_mode(data)
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
        mode_values, steps, freq_df = calculate_mode(data)
        if mode_values:
            mode_display = ", ".join([str(x) for x in sorted(mode_values)])
        else:
            mode_display = "No mode"
        st.metric("Mode", mode_display)
        st.markdown(steps)
        
        # Display frequency distribution in a nice format
        st.write("")
        st.write("**Interactive Frequency Distribution:**")
        
        # Display with conditional formatting and custom column config
        st.dataframe(
            freq_df,
            column_config={
                "Value": st.column_config.NumberColumn(
                    "Value",
                    format="%.2f" if any(x != int(x) for x in freq_df['Value']) else "%d"
                ),
                "Frequency": st.column_config.NumberColumn(
                    "Frequency", 
                    format="%d"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add a bar chart visualization of the frequencies
        if not freq_df.empty:
            st.write("**Frequency Visualization:**")
            
            # Create a horizontal bar chart
            chart_data = freq_df.copy()
            
            # Highlight the mode values
            chart_colors = []
            for val in chart_data['Value']:
                if val in mode_values:
                    chart_colors.append("#1f77b4")  # Highlight color
                else:
                    chart_colors.append("#aec7e8")  # Regular color
            
            # Plot the bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Sort by frequency for better visualization
            chart_data_sorted = chart_data.sort_values(by="Frequency")
            
            # Convert values to strings for the chart
            is_float = any(x != int(x) for x in chart_data_sorted['Value'])
            if is_float:
                value_labels = [f"{x:.2f}" for x in chart_data_sorted['Value']]
            else:
                value_labels = [f"{int(x)}" for x in chart_data_sorted['Value']]
            
            # Create the horizontal bar chart
            bars = ax.barh(value_labels, chart_data_sorted['Frequency'], color=chart_colors)
            
            # Highlight mode value bars
            for i, val in enumerate(chart_data_sorted['Value']):
                if val in mode_values:
                    bars[i].set_edgecolor('black')
                    bars[i].set_linewidth(2)
            
            # Add frequency labels on the bars
            for i, v in enumerate(chart_data_sorted['Frequency']):
                ax.text(v + 0.1, i, str(v), va='center')
            
            # Set labels and title
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Value')
            ax.set_title('Frequency Distribution')
            
            # Display the chart
            st.pyplot(fig)
    
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