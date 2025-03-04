import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textwrap


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
    $\\displaystyle\\sum_{{i=1}}^{{{n}}} x_i = {' + '.join([str(x) for x in data])} = {sum_data}$
    
    **Step 2**: Divide by the number of measurements (n = {n})
    $\\bar{{x}} = \\displaystyle\\frac{{{sum_data}}}{{{n}}} = {mean_value:.6f}$
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
    """Calculate the mode with step-by-step explanation without displaying the frequency table."""
    # Count occurrences of each value
    value_counts = {}
    for x in data:
        value_counts[x] = value_counts.get(x, 0) + 1

    # Find the maximum frequency
    max_count = max(value_counts.values())
    
    # Determine mode and mode type
    if max_count == 1:
        mode_values = []
        mode_type = "No mode"
    else:
        mode_values = [x for x, count in value_counts.items() if count == max_count]
        if len(mode_values) == 1:
            mode_type = "Unimodal"
        elif len(mode_values) == 2:
            mode_type = "Bimodal"
        else:
            mode_type = "Multimodal"
    
    # Generate explanation without the frequency table
    if mode_values:
        mode_str = ", ".join(str(x) for x in sorted(mode_values, key=lambda x: float(x) if isinstance(x, (int, float)) or (isinstance(x, str) and x.replace('.', '', 1).isdigit()) else float('inf')))
        result = f"{mode_str} (each appears {max_count} times)"
    else:
        result = "No mode (all values appear only once)"
    
    steps = textwrap.dedent(f"""
    ### Mode Calculation

    **Step 1**: Count the frequency of each value.

    **Step 2**: Identify the value(s) with the highest frequency.  
    Maximum frequency: {max_count}

    **Step 3**: Determine the mode.  
    Mode type: {mode_type}  
    Result: {result}
    """)
    
    # Create frequency DataFrame
    freq_df = pd.DataFrame({
        "Value": list(value_counts.keys()),
        "Frequency": list(value_counts.values())
    })
    
    # Try to convert values to numeric for better sorting
    try:
        freq_df["Value"] = pd.to_numeric(freq_df["Value"])
    except (ValueError, TypeError):
        # If conversion fails, leave as is
        pass
        
    # Sort values and reset index
    freq_df = freq_df.sort_values(by="Value").reset_index(drop=True)
    
    return mode_values, steps, freq_df


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
            
            # Create a copy of the dataframe for visualization
            chart_data = freq_df.copy()
            
            # Sort by frequency for better visualization
            chart_data = chart_data.sort_values(by="Frequency")
            
            # Make sure values are numeric for comparison with mode_values when possible
            try:
                chart_data['Value'] = pd.to_numeric(chart_data['Value'])
            except (ValueError, TypeError):
                pass

            # Create color list for bars
            chart_colors = []
            for val in chart_data['Value']:
                try:
                    val_numeric = float(val) if isinstance(val, str) else val
                    mode_values_numeric = [float(mv) if isinstance(mv, str) else mv for mv in mode_values]
                    
                    if any(abs(val_numeric - mv_num) < 1e-10 for mv_num in mode_values_numeric):
                        chart_colors.append("#1f77b4")  # Highlight color for mode values
                    else:
                        chart_colors.append("#aec7e8")  # Regular color
                except (ValueError, TypeError):
                    chart_colors.append("#aec7e8")  # Default color if conversion fails
            
            # Format values for display
            try:
                # Check if values contain decimals
                is_float = any(isinstance(x, (float, np.float64)) and x != int(x) 
                               for x in chart_data['Value'] if pd.notna(x))
                
                if is_float:
                    value_labels = [f"{float(x):.2f}" if pd.notna(x) else "" for x in chart_data['Value']]
                else:
                    value_labels = [f"{int(float(x))}" if pd.notna(x) else "" for x in chart_data['Value']]
            except (ValueError, TypeError):
                # If conversion fails, use string representation
                value_labels = [str(x) for x in chart_data['Value']]
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.barh(value_labels, chart_data['Frequency'], color=chart_colors)
            
            # Highlight bars for mode values
            for i, val in enumerate(chart_data['Value']):
                try:
                    val_numeric = float(val) if isinstance(val, str) else val
                    mode_values_numeric = [float(mv) if isinstance(mv, str) else mv for mv in mode_values]
                    
                    if any(abs(val_numeric - mv_num) < 1e-10 for mv_num in mode_values_numeric):
                        bars[i].set_edgecolor('black')
                        bars[i].set_linewidth(2)
                except (ValueError, TypeError):
                    pass  # Skip if conversion fails
            
            # Add frequency labels on the bars
            for i, v in enumerate(chart_data['Frequency']):
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
