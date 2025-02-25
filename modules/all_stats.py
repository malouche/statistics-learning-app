import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from modules.measures_center import calculate_mean, calculate_median, calculate_mode
from modules.measures_variability import (
    calculate_range, calculate_variance, calculate_std_dev, 
    calculate_iqr, calculate_cv
)
from modules.visualization import plot_histogram, plot_boxplot

def generate_five_number_summary(data):
    """Generate the five-number summary for the dataset"""
    sorted_data = sorted(data)
    min_val = min(sorted_data)
    max_val = max(sorted_data)
    
    # Calculate median
    median_val, _ = calculate_median(data)
    
    # Calculate quartiles
    iqr_val, _, q1, q3 = calculate_iqr(data)
    
    return {
        "Minimum": min_val,
        "Q1": q1,
        "Median": median_val,
        "Q3": q3,
        "Maximum": max_val,
        "IQR": iqr_val
    }

def generate_descriptive_stats(data, is_population=False):
    """Generate comprehensive descriptive statistics for the dataset"""
    n = len(data)
    mean_val, _ = calculate_mean(data)
    median_val, _ = calculate_median(data)
    mode_vals, _, _ = calculate_mode(data)
    
    if mode_vals:
        mode_str = ", ".join([str(x) for x in sorted(mode_vals)])
    else:
        mode_str = "No mode"
    
    range_val, _ = calculate_range(data)
    variance, _ = calculate_variance(data, is_population)
    std_dev, _, _ = calculate_std_dev(data, is_population)
    iqr_val, _, q1, q3 = calculate_iqr(data)
    cv, _ = calculate_cv(data)
    
    # Additional statistics
    skewness = pd.Series(data).skew()
    kurtosis = pd.Series(data).kurtosis()
    
    # Calculate percentiles
    percentiles = {
        "10th": np.percentile(data, 10),
        "25th": q1,
        "50th": median_val,
        "75th": q3,
        "90th": np.percentile(data, 90)
    }
    
    return {
        "Count": n,
        "Mean": mean_val,
        "Median": median_val,
        "Mode": mode_str,
        "Range": range_val,
        "Variance": variance,
        "Standard Deviation": std_dev,
        "IQR": iqr_val,
        "CV": f"{cv:.2f}%",
        "Skewness": skewness,
        "Kurtosis": kurtosis,
        "Percentiles": percentiles,
        "Min": min(data),
        "Max": max(data),
        "Q1": q1,
        "Q3": q3,
        "Is Population": is_population
    }

def create_summary_dataframe(stats):
    """Create a formatted summary dataframe from statistics"""
    # Basic stats
    basic_stats = {
        "Statistic": [
            "Count", "Minimum", "Maximum", "Range", 
            "Mean", "Median", "Mode",
            "Variance", "Standard Deviation", "CV"
        ],
        "Value": [
            stats["Count"],
            stats["Min"],
            stats["Max"],
            stats["Range"],
            stats["Mean"],
            stats["Median"],
            stats["Mode"],
            stats["Variance"],
            stats["Standard Deviation"],
            stats["CV"]
        ]
    }
    
    # Quartiles and percentiles
    quartile_stats = {
        "Statistic": [
            "10th Percentile",
            "25th Percentile (Q1)",
            "50th Percentile (Median)",
            "75th Percentile (Q3)",
            "90th Percentile",
            "IQR (Q3-Q1)"
        ],
        "Value": [
            stats["Percentiles"]["10th"],
            stats["Q1"],
            stats["Median"],
            stats["Q3"],
            stats["Percentiles"]["90th"],
            stats["IQR"]
        ]
    }
    
    # Shape statistics
    shape_stats = {
        "Statistic": ["Skewness", "Kurtosis"],
        "Value": [stats["Skewness"], stats["Kurtosis"]]
    }
    
    # Create dataframes
    basic_df = pd.DataFrame(basic_stats)
    quartile_df = pd.DataFrame(quartile_stats)
    shape_df = pd.DataFrame(shape_stats)
    
    return basic_df, quartile_df, shape_df

def all_stats_tab(data):
    """Display the all statistics tab content"""
    st.header("🧮 All Statistics")
    st.write("View a comprehensive summary of all statistical measures for your dataset.")
    
    # Set up page layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Calculate all statistics
        is_population = st.checkbox("Treat as population data")
        stats = generate_descriptive_stats(data, is_population)
        
        # Create and display summary tables
        basic_df, quartile_df, shape_df = create_summary_dataframe(stats)
        
        st.subheader("Basic Statistics")
        st.dataframe(basic_df, use_container_width=True)
        
        st.subheader("Quartiles and Percentiles")
        st.dataframe(quartile_df, use_container_width=True)
        
        st.subheader("Distribution Shape")
        st.dataframe(shape_df, use_container_width=True)
        
        # Interpretation of results
        st.subheader("Interpretation")
        
        # Interpret central tendency
        mean_val = stats["Mean"]
        median_val = stats["Median"]
        
        if abs(mean_val - median_val) < 0.05 * max(abs(mean_val), abs(median_val)):
            st.write("🔹 The mean and median are close, suggesting a **symmetric distribution**.")
        elif mean_val > median_val:
            st.write("🔹 The mean is greater than the median, indicating a **right-skewed (positively skewed) distribution**.")
        else:
            st.write("🔹 The mean is less than the median, indicating a **left-skewed (negatively skewed) distribution**.")
        
        # Interpret skewness
        skewness = stats["Skewness"]
        if abs(skewness) < 0.5:
            st.write(f"🔹 Skewness = {skewness:.4f}: The distribution is approximately **symmetric**.")
        elif skewness > 0:
            st.write(f"🔹 Skewness = {skewness:.4f}: The distribution has a **positive skew** (tail extends to the right).")
        else:
            st.write(f"🔹 Skewness = {skewness:.4f}: The distribution has a **negative skew** (tail extends to the left).")
        
        # Interpret kurtosis
        kurtosis = stats["Kurtosis"]
        if abs(kurtosis) < 0.5:
            st.write(f"🔹 Kurtosis = {kurtosis:.4f}: The distribution has a **normal peak** (mesokurtic).")
        elif kurtosis > 0:
            st.write(f"🔹 Kurtosis = {kurtosis:.4f}: The distribution has a **sharper peak** than normal (leptokurtic).")
        else:
            st.write(f"🔹 Kurtosis = {kurtosis:.4f}: The distribution has a **flatter peak** than normal (platykurtic).")
        
        # Interpret coefficient of variation
        cv_val = float(stats["CV"].replace("%", ""))
        if cv_val < 10:
            st.write(f"🔹 CV = {stats['CV']}: The data shows **low relative variability**.")
        elif cv_val < 30:
            st.write(f"🔹 CV = {stats['CV']}: The data shows **moderate relative variability**.")
        else:
            st.write(f"🔹 CV = {stats['CV']}: The data shows **high relative variability**.")
    
    with col2:
        # Display visualizations
        st.subheader("Visualizations")
        
        # Histogram
        st.write("**Histogram**")
        hist_fig = plot_histogram(data, bins='auto', kde=True)
        st.pyplot(hist_fig)
        
        # Box Plot
        st.write("**Box Plot**")
        box_fig = plot_boxplot(data)
        st.pyplot(box_fig)
        
        # Five number summary visualization
        st.write("**Five-Number Summary**")
        
        # Calculate five-number summary
        five_num = generate_five_number_summary(data)
        
        # Create a simple visual representation
        fig, ax = plt.subplots(figsize=(8, 2))
        
        # Plot the number line
        min_val = five_num["Minimum"]
        max_val = five_num["Maximum"]
        buffer = 0.05 * (max_val - min_val)
        
        ax.plot([min_val - buffer, max_val + buffer], [0, 0], 'k-', linewidth=2)
        
        # Plot the five points
        summary_points = [
            five_num["Minimum"],
            five_num["Q1"],
            five_num["Median"],
            five_num["Q3"],
            five_num["Maximum"]
        ]
        
        summary_labels = ["Min", "Q1", "Median", "Q3", "Max"]
        
        for i, (point, label) in enumerate(zip(summary_points, summary_labels)):
            ax.plot(point, 0, 'bo', markersize=10)
            ax.annotate(
                f"{label}: {point:.2f}",
                xy=(point, 0),
                xytext=(point, 0.1),
                ha='center',
                va='bottom',
                fontsize=10
            )
        
        # Add IQR visualization
        ax.plot([five_num["Q1"], five_num["Q3"]], [0, 0], 'g-', linewidth=6, alpha=0.5)
        ax.annotate(
            f"IQR: {five_num['IQR']:.2f}",
            xy=((five_num["Q1"] + five_num["Q3"]) / 2, 0),
            xytext=((five_num["Q1"] + five_num["Q3"]) / 2, -0.1),
            ha='center',
            va='top',
            fontsize=10
        )
        
        # Remove axes
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        st.pyplot(fig)