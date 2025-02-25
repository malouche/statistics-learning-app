import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from modules.measures_variability import calculate_iqr

def plot_histogram(data, bins='auto', kde=True):
    """Create a histogram with optional kernel density estimation"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate bin edges if 'auto'
    if bins == 'auto':
        if len(data) < 20:
            bins = min(int(np.sqrt(len(data))), 10)
        else:
            bins = 'sturges'  # Use Sturges' formula for bin count
    
    # Plot histogram
    sns.histplot(data, bins=bins, kde=kde, ax=ax)
    
    # Add mean and median lines
    mean_val = np.mean(data)
    median_val = np.median(data)
    
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='green', linestyle=':', linewidth=2, label=f'Median: {median_val:.2f}')
    
    # Add annotations
    ax.set_title('Histogram of Data', fontsize=14)
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend()
    
    return fig

def plot_boxplot(data):
    """Create a box plot with annotations for key components"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create box plot
    bp = ax.boxplot(data, patch_artist=True, vert=False)
    
    # Customize box plot appearance
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    for whisker in bp['whiskers']:
        whisker.set_color('gray')
        whisker.set_linestyle('--')
    for cap in bp['caps']:
        cap.set_color('gray')
    for median in bp['medians']:
        median.set_color('red')
        median.set_linewidth(2)
    for flier in bp['fliers']:
        flier.set_marker('o')
        flier.set_markerfacecolor('red')
        flier.set_markeredgecolor('black')
        flier.set_markersize(8)
    
    # Calculate five-number summary for annotations
    min_val = min(data)
    q1, q3 = np.percentile(data, [25, 75])
    median_val = np.median(data)
    max_val = max(data)
    iqr = q3 - q1
    
    # Add annotations
    ax.set_title('Box Plot of Data', fontsize=14)
    ax.set_xlabel('Value', fontsize=12)
    
    # Add summary stats as text
    summary_text = (
        f"Minimum: {min_val:.2f}\n"
        f"Q1: {q1:.2f}\n"
        f"Median: {median_val:.2f}\n"
        f"Q3: {q3:.2f}\n"
        f"Maximum: {max_val:.2f}\n"
        f"IQR: {iqr:.2f}"
    )
    
    ax.text(
        max_val + (max_val - min_val) * 0.05, 
        1.15, 
        summary_text,
        bbox=dict(facecolor='white', alpha=0.5, boxstyle='round'),
        verticalalignment='top'
    )
    
    # Check for outliers and mark them
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = [x for x in data if x < lower_fence or x > upper_fence]
    
    # Add outlier zone indicators
    if min_val < lower_fence:
        ax.axvspan(min_val - (max_val - min_val) * 0.05, lower_fence, alpha=0.2, color='red')
    if max_val > upper_fence:
        ax.axvspan(upper_fence, max_val + (max_val - min_val) * 0.05, alpha=0.2, color='red')
    
    # Add labels for box plot components
    y_pos = 1.05
    ax.annotate(
        'Minimum', xy=(min_val, 1), xytext=(min_val, y_pos),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
        ha='center', va='bottom'
    )
    
    ax.annotate(
        'Q1', xy=(q1, 1), xytext=(q1, y_pos),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
        ha='center', va='bottom'
    )
    
    ax.annotate(
        'Median', xy=(median_val, 1), xytext=(median_val, y_pos),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
        ha='center', va='bottom'
    )
    
    ax.annotate(
        'Q3', xy=(q3, 1), xytext=(q3, y_pos),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
        ha='center', va='bottom'
    )
    
    ax.annotate(
        'Maximum', xy=(max_val, 1), xytext=(max_val, y_pos),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3'),
        ha='center', va='bottom'
    )
    
    return fig

def plot_stem_and_leaf(data):
    """Create a stem and leaf plot"""
    # Convert data to integers for simplified display
    factor = 1
    if all(x == int(x) for x in data):
        # Data is already integers
        stem_factor = 10
        leaf_factor = 1
    else:
        # Find a good scaling factor
        max_decimals = max([len(str(x).split('.')[-1]) if '.' in str(x) else 0 for x in data])
        stem_factor = 10
        leaf_factor = 10 ** max_decimals
        data = [round(x * leaf_factor) for x in data]
    
    # Create stems and leaves
    stems = {}
    for value in sorted(data):
        stem = value // stem_factor
        leaf = value % stem_factor
        
        if stem not in stems:
            stems[stem] = []
        stems[stem].append(leaf)
    
    # Format the stem and leaf plot
    stem_leaf_text = "Stem | Leaf\n-----------\n"
    for stem in sorted(stems.keys()):
        leaves = stems[stem]
        leaf_str = ' '.join([str(leaf) for leaf in sorted(leaves)])
        stem_leaf_text += f"{stem:4} | {leaf_str}\n"
    
    stem_leaf_text += "\nKey: "
    if leaf_factor == 1 and stem_factor == 10:
        stem_leaf_text += f"{stem}|{leaves[0]} = {stem*stem_factor + leaves[0]}"
    else:
        stem_leaf_text += f"{stem}|{leaves[0]} = {(stem*stem_factor + leaves[0])/leaf_factor:.{max_decimals}f}"
    
    return stem_leaf_text

def plot_normal_probability(data):
    """Create a normal probability plot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create QQ plot
    stats.probplot(data, plot=ax)
    
    ax.set_title('Normal Probability Plot', fontsize=14)
    
    # Add a reference line
    x = np.array(ax.get_xlim())
    y = x * ax.get_lines()[0].get_xydata()[:,1].std() + np.mean(data)
    ax.plot(x, y, 'r--', linewidth=2)
    
    return fig

def plot_compare_distribution(data):
    """Create a plot comparing the data distribution to a normal distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the data distribution
    sns.histplot(data, kde=True, stat='density', label='Data Distribution', ax=ax)
    
    # Overlay a normal distribution
    x = np.linspace(min(data) - 1, max(data) + 1, 1000)
    y = stats.norm.pdf(x, np.mean(data), np.std(data))
    ax.plot(x, y, 'r-', linewidth=2, label='Normal Distribution')
    
    # Add mean and standard deviation lines
    mean_val = np.mean(data)
    std_dev = np.std(data)
    
    ax.axvline(mean_val, color='green', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvline(mean_val + std_dev, color='blue', linestyle=':', linewidth=2, label=f'Mean + SD: {mean_val + std_dev:.2f}')
    ax.axvline(mean_val - std_dev, color='blue', linestyle=':', linewidth=2, label=f'Mean - SD: {mean_val - std_dev:.2f}')
    
    ax.set_title('Data Distribution vs Normal Distribution', fontsize=14)
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.legend()
    
    return fig

def visualization_tab(data):
    """Display the visualization tab content"""
    st.header("📈 Visualization")
    st.write("Explore different ways to visualize your data for better insights.")
    
    # Select visualization type
    viz_type = st.radio(
        "Select visualization type:",
        ["Histogram", "Box Plot", "Stem-and-Leaf Plot", "Normal Probability Plot", "Distribution Comparison"],
        horizontal=True
    )
    
    # Display the visualization
    if viz_type == "Histogram":
        st.subheader("Histogram")
        
        col1, col2 = st.columns(2)
        with col1:
            bins = st.select_slider(
                "Number of bins:",
                options=list(range(1, 21)) + ["auto"],
                value="auto"
            )
        
        with col2:
            kde = st.checkbox("Show density curve", value=True)
        
        if bins != "auto":
            bins = int(bins)
        
        fig = plot_histogram(data, bins=bins, kde=kde)
        st.pyplot(fig)
        
        st.markdown("""
        ### About Histograms
        
        A histogram displays the distribution of your data by grouping values into bins and showing the frequency of values in each bin.
        
        **Key features:**
        - Shows the overall shape of the distribution (e.g., symmetric, skewed, bimodal)
        - Reveals peaks and gaps in the data
        - Helps identify potential outliers
        - The density curve (KDE) provides a smoothed version of the distribution
        
        **Interpreting histograms:**
        - **Symmetric**: Values are evenly distributed around the center
        - **Right-skewed**: Tail extends to the right, median < mean
        - **Left-skewed**: Tail extends to the left, median > mean
        - **Bimodal**: Two peaks, suggesting two subgroups in the data
        """)
    
    elif viz_type == "Box Plot":
        st.subheader("Box Plot")
        
        fig = plot_boxplot(data)
        st.pyplot(fig)
        
        st.markdown("""
        ### About Box Plots
        
        A box plot (or box-and-whisker plot) provides a visual summary of the distribution based on the five-number summary.
        
        **Key components:**
        - **Box**: Represents the interquartile range (IQR), from Q1 (25th percentile) to Q3 (75th percentile)
        - **Line inside box**: Median (50th percentile)
        - **Whiskers**: Extend to the most extreme data points within 1.5 × IQR from the box
        - **Points beyond whiskers**: Potential outliers
        
        **Advantages of box plots:**
        - Compact representation of the data distribution
        - Good for comparing multiple distributions side by side
        - Robust against outliers (uses quartiles rather than mean)
        - Clearly identifies potential outliers
        """)
    
    elif viz_type == "Stem-and-Leaf Plot":
        st.subheader("Stem-and-Leaf Plot")
        
        stem_leaf_text = plot_stem_and_leaf(data)
        st.text(stem_leaf_text)
        
        st.markdown("""
        ### About Stem-and-Leaf Plots
        
        A stem-and-leaf plot organizes data by separating each value into a "stem" (typically the first digit or digits) and a "leaf" (typically the last digit).
        
        **Key features:**
        - Preserves the original data values (unlike a histogram)
        - Shows the shape of the distribution
        - Easy to read individual values
        - Compact representation for small to medium datasets
        
        **Reading a stem-and-leaf plot:**
        - Each row has a stem value followed by all leaf values for that stem
        - To reconstruct the original values, combine each stem with each of its leaves
        - The values are typically sorted within each stem
        """)
    
    elif viz_type == "Normal Probability Plot":
        st.subheader("Normal Probability Plot")
        
        fig = plot_normal_probability(data)
        st.pyplot(fig)
        
        st.markdown("""
        ### About Normal Probability Plots
        
        A normal probability plot (or Q-Q plot) is used to assess whether data follows a normal distribution.
        
        **Key features:**
        - Plots the actual data quantiles against theoretical quantiles from a normal distribution
        - The closer the points are to a straight line, the more normally distributed the data is
        
        **Interpreting the plot:**
        - **Points follow the line**: Data is approximately normally distributed
        - **S-shaped curve**: Data has longer tails than a normal distribution
        - **Inverted S-shape**: Data has shorter tails than a normal distribution
        - **Points above the line on right, below on left**: Right-skewed distribution
        - **Points below the line on right, above on left**: Left-skewed distribution
        """)
    
    elif viz_type == "Distribution Comparison":
        st.subheader("Distribution Comparison")
        
        fig = plot_compare_distribution(data)
        st.pyplot(fig)
        
        st.markdown("""
        ### About Distribution Comparison
        
        This plot compares your actual data distribution to a theoretical normal distribution with the same mean and standard deviation.
        
        **Key features:**
        - Shows histogram of your data with a density curve
        - Overlays a normal distribution curve for comparison
        - Marks the mean and one standard deviation in each direction
        
        **What to look for:**
        - How closely the actual distribution (blue) matches the theoretical normal distribution (red)
        - Deviations from normality: skewness, multiple peaks, or heavy tails
        - The spread of the data compared to the standard deviation
        """)
