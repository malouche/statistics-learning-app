import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def calculate_range(data):
    """Calculate the range with step-by-step explanation"""
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val
    
    steps = f"""
    ### Range Calculation
    
    The range is the difference between the largest and smallest values in the dataset.
    
    **Formula**: $R = \\text{{max}} - \\text{{min}}$
    
    **Step 1**: Find the minimum value
    min = {min_val}
    
    **Step 2**: Find the maximum value
    max = {max_val}
    
    **Step 3**: Calculate the range
    $R = {max_val} - {min_val} = {range_val}$
    """
    
    return range_val, steps

def calculate_variance(data, is_population=False):
    """Calculate the variance with step-by-step explanation"""
    n = len(data)
    mean_val = sum(data) / n
    
    # Calculate sum of squared deviations
    deviations = [x - mean_val for x in data]
    squared_devs = [dev ** 2 for dev in deviations]
    sum_squared_devs = sum(squared_devs)
    
    # Calculate variance
    if is_population:
        divisor = n
        variance = sum_squared_devs / n
        formula = r"\sigma^2 = \frac{\sum_{i=1}^{N}(x_i - \mu)^2}{N}"
        notation = "σ²"
    else:
        divisor = n - 1
        variance = sum_squared_devs / (n - 1)
        formula = r"s^2 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n-1}"
        notation = "s²"
    
    # Create a table for the calculation
    calc_table = pd.DataFrame({
        "x_i": data,
        "x_i - mean": deviations,
        "(x_i - mean)²": squared_devs
    })
    
    # Alternative calculation method
    sum_x = sum(data)
    sum_x_squared = sum([x ** 2 for x in data])
    alt_variance = (sum_x_squared - (sum_x ** 2) / n) / divisor
    
    steps = f"""
    ### {'Population' if is_population else 'Sample'} Variance Calculation
    
    The variance measures the average squared deviation from the mean.
    
    **Formula**: ${formula}$
    
    **Step 1**: Calculate the mean
    $\\text{{mean}} = \\frac{{\\sum_{{i=1}}^{{{n}}} x_i}}{{{n}}} = \\frac{{{sum(data)}}}{{{n}}} = {mean_val:.6f}$
    
    **Step 2**: Calculate deviations from the mean and square them
    
    {calc_table.to_markdown(index=False)}
    
    **Step 3**: Sum the squared deviations
    $\\sum_{{i=1}}^{{{n}}} (x_i - \\text{{mean}})^2 = {sum_squared_devs:.6f}$
    
    **Step 4**: Divide by {'N' if is_population else 'n-1'}
    ${notation} = \\frac{{{sum_squared_devs:.6f}}}{{{divisor}}} = {variance:.6f}$
    
    #### Alternative Calculation Method (Computational Formula)
    
    This method can be more efficient for computation:
    
    **Formula**: ${notation} = \\frac{{\\sum_{{i=1}}^{{{n}}} x_i^2 - \\frac{{(\\sum_{{i=1}}^{{{n}}} x_i)^2}}{{{n}}}}}{{{divisor}}}$
    
    **Step 1**: Calculate $\\sum_{{i=1}}^{{{n}}} x_i = {sum_x:.6f}$
    
    **Step 2**: Calculate $\\sum_{{i=1}}^{{{n}}} x_i^2 = {sum_x_squared:.6f}$
    
    **Step 3**: Apply the formula:
    ${notation} = \\frac{{{sum_x_squared:.6f} - \\frac{{{sum_x:.6f}^2}}{{{n}}}}}{{{divisor}}} = \\frac{{{sum_x_squared:.6f} - \\frac{{{sum_x ** 2:.6f}}}{{{n}}}}}{{{divisor}}} = {alt_variance:.6f}$
    """
    
    return variance, steps

def calculate_std_dev(data, is_population=False):
    """Calculate the standard deviation with step-by-step explanation"""
    variance, variance_steps = calculate_variance(data, is_population)
    std_dev = np.sqrt(variance)
    
    if is_population:
        notation = "σ"
        var_notation = "σ²"
    else:
        notation = "s"
        var_notation = "s²"
    
    steps = f"""
    ### {'Population' if is_population else 'Sample'} Standard Deviation Calculation
    
    The standard deviation is the square root of the variance.
    
    **Formula**: ${notation} = \\sqrt{{{var_notation}}}$
    
    **Step 1**: Calculate the variance (as shown above)
    ${var_notation} = {variance:.6f}$
    
    **Step 2**: Take the square root
    ${notation} = \\sqrt{{{variance:.6f}}} = {std_dev:.6f}$
    
    #### Why we use Standard Deviation
    
    - The variance is in squared units, which can be difficult to interpret
    - The standard deviation returns to the original units of measurement
    - We can use the standard deviation with the Empirical Rule for normally distributed data
    """
    
    return std_dev, steps, variance_steps

def calculate_iqr(data):
    """Calculate the interquartile range with step-by-step explanation"""
    n = len(data)
    sorted_data = sorted(data)
    
    # Calculate positions of quartiles
    q1_pos = 0.25 * (n + 1)
    q3_pos = 0.75 * (n + 1)
    
    # Calculate Q1
    q1_int = int(q1_pos)
    q1_frac = q1_pos - q1_int
    
    if q1_frac == 0:
        q1 = sorted_data[q1_int - 1]  # Adjust for 0-indexed list
        q1_calc = f"The {q1_int}th value in the sorted data: {q1}"
    else:
        q1_lower = sorted_data[q1_int - 1]  # Adjust for 0-indexed list
        q1_upper = sorted_data[q1_int]  # Adjust for 0-indexed list
        q1 = q1_lower + q1_frac * (q1_upper - q1_lower)
        q1_calc = f"Between positions {q1_int} and {q1_int + 1}: {q1_lower} + {q1_frac:.2f} × ({q1_upper} - {q1_lower}) = {q1}"
    
    # Calculate Q3
    q3_int = int(q3_pos)
    q3_frac = q3_pos - q3_int
    
    if q3_frac == 0:
        q3 = sorted_data[q3_int - 1]  # Adjust for 0-indexed list
        q3_calc = f"The {q3_int}th value in the sorted data: {q3}"
    else:
        q3_lower = sorted_data[q3_int - 1]  # Adjust for 0-indexed list
        q3_upper = sorted_data[q3_int]  # Adjust for 0-indexed list
        q3 = q3_lower + q3_frac * (q3_upper - q3_lower)
        q3_calc = f"Between positions {q3_int} and {q3_int + 1}: {q3_lower} + {q3_frac:.2f} × ({q3_upper} - {q3_lower}) = {q3}"
    
    # Calculate IQR
    iqr = q3 - q1
    
    steps = f"""
    ### Interquartile Range (IQR) Calculation
    
    The IQR is the range of the middle 50% of the data.
    
    **Formula**: $IQR = Q_3 - Q_1$
    
    **Step 1**: Sort the data
    {sorted_data}
    
    **Step 2**: Find the position of Q1 (first quartile)
    Position of Q1 = 0.25 × (n + 1) = 0.25 × ({n} + 1) = {q1_pos}
    
    **Step 3**: Calculate Q1
    {q1_calc}
    
    **Step 4**: Find the position of Q3 (third quartile)
    Position of Q3 = 0.75 × (n + 1) = 0.75 × ({n} + 1) = {q3_pos}
    
    **Step 5**: Calculate Q3
    {q3_calc}
    
    **Step 6**: Calculate the IQR
    $IQR = Q_3 - Q_1 = {q3} - {q1} = {iqr}$
    """
    
    return iqr, steps, q1, q3

def calculate_cv(data):
    """Calculate the coefficient of variation with step-by-step explanation"""
    n = len(data)
    mean_val = sum(data) / n
    variance, _ = calculate_variance(data, is_population=False)
    std_dev = np.sqrt(variance)
    cv = (std_dev / mean_val) * 100
    
    steps = f"""
    ### Coefficient of Variation (CV) Calculation
    
    The CV measures the relative variability in relation to the mean.
    
    **Formula**: $CV = \\frac{{s}}{{\\bar{{x}}}} \\times 100\\%$
    
    **Step 1**: Calculate the mean
    $\\bar{{x}} = \\frac{{\\sum_{{i=1}}^{{{n}}} x_i}}{{{n}}} = \\frac{{{sum(data)}}}{{{n}}} = {mean_val:.6f}$
    
    **Step 2**: Calculate the standard deviation
    $s = {std_dev:.6f}$ (as calculated earlier)
    
    **Step 3**: Calculate the CV
    $CV = \\frac{{{std_dev:.6f}}}{{{mean_val:.6f}}} \\times 100\\% = {cv:.2f}\\%$
    
    #### Interpretation of CV
    
    - The CV is a unitless measure
    - It allows for comparison of variability between different datasets, even when they have different units or different means
    - Lower CV values indicate lower relative variability
    - Typically expressed as a percentage
    """
    
    return cv, steps

def measures_variability_tab(data):
    """Display the measures of variability tab content"""
    st.header("📊 Measures of Variability")
    st.write("Learn how to calculate various measures of spread with step-by-step explanations.")
    
    # Select measure to explore
    measure = st.radio(
        "Select a measure to explore:",
        ["Range", "Variance", "Standard Deviation", "Interquartile Range (IQR)", "Coefficient of Variation (CV)", "Compare All"],
        horizontal=True
    )
    
    # Display the current data
    sorted_data = sorted(data)
    st.write("**Current data (sorted):**", sorted_data)
    
    # Create columns for displaying results
    if measure == "Compare All":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Range")
            range_val, _ = calculate_range(data)
            st.metric("Range", f"{range_val:.4f}")
            
            st.subheader("IQR")
            iqr_val, _, q1, q3 = calculate_iqr(data)
            st.metric("IQR", f"{iqr_val:.4f}")
        
        with col2:
            is_population = st.checkbox("Treat as population data")
            
            st.subheader("Variance")
            variance, _ = calculate_variance(data, is_population)
            st.metric("Variance", f"{variance:.4f}")
            
            st.subheader("CV")
            cv, _ = calculate_cv(data)
            st.metric("CV", f"{cv:.2f}%")
        
        with col3:
            st.subheader("Standard Deviation")
            std_dev, _, _ = calculate_std_dev(data, is_population)
            st.metric("Standard Deviation", f"{std_dev:.4f}")
            
            st.write("**Empirical Rule:**")
            if len(data) > 10:  # Only show if reasonable amount of data
                mean_val = sum(data) / len(data)
                st.write(f"- ~68% between {mean_val - std_dev:.4f} and {mean_val + std_dev:.4f}")
                st.write(f"- ~95% between {mean_val - 2*std_dev:.4f} and {mean_val + 2*std_dev:.4f}")
                st.write(f"- ~99.7% between {mean_val - 3*std_dev:.4f} and {mean_val + 3*std_dev:.4f}")
        
        # Display calculation steps
        with st.expander("Show Calculation Steps", expanded=True):
            range_val, range_steps = calculate_range(data)
            variance, var_steps = calculate_variance(data, is_population)
            std_dev, std_steps, _ = calculate_std_dev(data, is_population)
            iqr_val, iqr_steps, _, _ = calculate_iqr(data)
            cv, cv_steps = calculate_cv(data)
            
            st.markdown(range_steps)
            st.markdown("---")
            st.markdown(var_steps)
            st.markdown("---")
            st.markdown(std_steps)
            st.markdown("---")
            st.markdown(iqr_steps)
            st.markdown("---")
            st.markdown(cv_steps)
    
    elif measure == "Range":
        range_val, steps = calculate_range(data)
        st.metric("Range", f"{range_val:.4f}")
        st.markdown(steps)
        st.markdown("""
        #### About the Range
        
        The range is the simplest measure of variability. It's useful for a quick assessment of the spread of the data, but it has limitations:
        - Only uses the minimum and maximum values
        - Very sensitive to outliers
        - Doesn't provide information about how the data are distributed between the extremes
        """)
    
    elif measure == "Variance":
        is_population = st.checkbox("Treat as population data")
        variance, steps = calculate_variance(data, is_population)
        st.metric("Variance", f"{variance:.6f}")
        st.markdown(steps)
        st.markdown("""
        #### About the Variance
        
        The variance provides a measure of the average squared deviation from the mean. Key points:
        - Large deviations from the mean contribute more to the variance (squaring makes positive/negative deviations contribute equally)
        - The units are squared (e.g., if measuring height in cm, variance is in cm²)
        - The sample variance divides by (n-1) instead of n to provide an unbiased estimate of the population variance
        """)
    
    elif measure == "Standard Deviation":
        is_population = st.checkbox("Treat as population data")
        std_dev, steps, var_steps = calculate_std_dev(data, is_population)
        st.metric("Standard Deviation", f"{std_dev:.6f}")
        st.markdown(steps)
        
        with st.expander("Show Variance Calculation"):
            st.markdown(var_steps)
        
        st.subheader("The Empirical Rule")
        if len(data) > 10:  # Only show if reasonable amount of data
            mean_val = sum(data) / len(data)
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("For approximately normal distributions:")
                st.write(f"- ~68% between {mean_val - std_dev:.4f} and {mean_val + std_dev:.4f}")
                st.write(f"- ~95% between {mean_val - 2*std_dev:.4f} and {mean_val + 2*std_dev:.4f}")
                st.write(f"- ~99.7% between {mean_val - 3*std_dev:.4f} and {mean_val + 3*std_dev:.4f}")
            
            with col2:
                # Create a simplified normal distribution visualization
                fig, ax = plt.subplots(figsize=(8, 4))
                x = np.linspace(mean_val - 4*std_dev, mean_val + 4*std_dev, 1000)
                y = stats.norm.pdf(x, mean_val, std_dev)
                
                ax.plot(x, y, 'k', linewidth=2)
                
                # Shade the regions
                x1 = np.linspace(mean_val - std_dev, mean_val + std_dev, 100)
                ax.fill_between(x1, stats.norm.pdf(x1, mean_val, std_dev), alpha=0.4, color='blue', label='68%')
                
                x2 = np.linspace(mean_val - 2*std_dev, mean_val + 2*std_dev, 100)
                ax.fill_between(x2, stats.norm.pdf(x2, mean_val, std_dev), alpha=0.3, color='green', label='95%')
                
                x3 = np.linspace(mean_val - 3*std_dev, mean_val + 3*std_dev, 100)
                ax.fill_between(x3, stats.norm.pdf(x3, mean_val, std_dev), alpha=0.2, color='red', label='99.7%')
                
                ax.axvline(mean_val, color='black', linestyle='--')
                ax.axvline(mean_val + std_dev, color='blue', linestyle=':')
                ax.axvline(mean_val - std_dev, color='blue', linestyle=':')
                ax.axvline(mean_val + 2*std_dev, color='green', linestyle=':')
                ax.axvline(mean_val - 2*std_dev, color='green', linestyle=':')
                ax.axvline(mean_val + 3*std_dev, color='red', linestyle=':')
                ax.axvline(mean_val - 3*std_dev, color='red', linestyle=':')
                
                plt.legend()
                plt.title('Empirical Rule Visualization')
                st.pyplot(fig)
    
    elif measure == "Interquartile Range (IQR)":
        iqr_val, steps, q1, q3 = calculate_iqr(data)
        st.metric("IQR", f"{iqr_val:.4f}")
        st.markdown(steps)
        
        st.subheader("Outlier Detection using IQR")
        lower_fence = q1 - 1.5 * iqr_val
        upper_fence = q3 + 1.5 * iqr_val
        
        outliers = [x for x in data if x < lower_fence or x > upper_fence]
        
        st.write(f"Lower fence: Q₁ - 1.5×IQR = {q1:.4f} - 1.5×{iqr_val:.4f} = {lower_fence:.4f}")
        st.write(f"Upper fence: Q₃ + 1.5×IQR = {q3:.4f} + 1.5×{iqr_val:.4f} = {upper_fence:.4f}")
        
        if outliers:
            st.write(f"**Potential outliers:** {sorted(outliers)}")
        else:
            st.write("**No potential outliers detected.**")
        
        st.markdown("""
        #### About the IQR
        
        The interquartile range (IQR) is a robust measure of variability:
        - Not influenced by outliers (unlike the range)
        - Describes the middle 50% of the data
        - Used in box plots and for outlier detection
        - Especially useful for skewed distributions
        """)
    
    elif measure == "Coefficient of Variation (CV)":
        cv, steps = calculate_cv(data)
        st.metric("CV", f"{cv:.2f}%")
        st.markdown(steps)
        st.markdown("""
        #### About the Coefficient of Variation (CV)
        
        The CV provides a standardized, unitless measure of relative dispersion:
        - Allows comparing variability across datasets with different units or scales
        - Expressed as a percentage
        - Useful for comparing precision of different measurement methods
        - Limited usefulness for data with means close to zero
        """)