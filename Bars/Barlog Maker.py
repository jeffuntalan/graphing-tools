# BioAssets BarLog Maker v1.6 updated June 26, 2024
# This script reads an Excel file with multiple sheets containing data for a disinfectant residue assay.
# Install dependencies by running 'pip install pandas matplotlib numpy' in the terminal.

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change only the values to the right of the colons. This will be used for the legend labels.
legend_labels = {
    'input': 'Positive Control',
    'pre_exposure': 'Positive Control (Liquid)',
    'post_exposure': 'Sample (Dry)',
    'post_exposure_liquid': 'Sample (Liquid)'
}

# Recognize the Excel file with the prefix "barlog" in the current directory
file_list = [file for file in os.listdir() if file.startswith('barlog') and file.endswith('.xlsx')]

if len(file_list) == 0:
    print("No matching Excel file found starting with 'barlog' and ending with '.xlsx'.")
    exit()

file_path = file_list[0]  # Take the first matching file found

# Read the Excel file
xls = pd.ExcelFile(file_path)

# Scan sheet
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name, header=[0, 1])
    
    # Calculate averages and standard deviations
    averages = df.groupby(level=0, axis=1).mean()
    std_devs = df.groupby(level=0, axis=1).std()

    # Assign data for plotting
    days = [1, 7, 14, 21]
    input_means = averages['Input'].values.flatten()
    pre_exposure_means = averages['Pre-exposure'].values.flatten()
    post_exposure_means = averages['Post-exposure'].values.flatten()
    post_exposure_liquid_means = averages['Post-exposure-Liquid'].values.flatten()

    input_std = std_devs['Input'].values.flatten()
    pre_exposure_std = std_devs['Pre-exposure'].values.flatten()
    post_exposure_std = std_devs['Post-exposure'].values.flatten()
    post_exposure_liquid_std = std_devs['Post-exposure-Liquid'].values.flatten()
    
    # Plot bars with log scale on y-axis
    bar_width = 0.2
    index = np.arange(len(days))

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(index - bar_width, input_means, bar_width, label=legend_labels['input'], yerr=input_std, capsize=5, alpha=0.7)
    bars2 = ax.bar(index, pre_exposure_means, bar_width, label=legend_labels['pre_exposure'], yerr=pre_exposure_std, capsize=5, alpha=0.7)
    bars3 = ax.bar(index + bar_width, post_exposure_means, bar_width, label=legend_labels['post_exposure'], yerr=post_exposure_std, capsize=5, alpha=0.7)
    bars4 = ax.bar(index + 2*bar_width, post_exposure_liquid_means, bar_width, label=legend_labels['post_exposure_liquid'], yerr=post_exposure_liquid_std, capsize=5, alpha=0.7)

    # Threshold value for marking bars
    threshold = 2000
    marked_bars = []

    # Annotate bars that meet the threshold with an asterisk
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            if height <= threshold:
                ax.annotate('*', xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=20, color='red')
                marked_bars.append(bar)

    # Annotate standard deviation values in exponential form on top of each bar, with rotation
    show_std_dev = False  # Toggle for standard deviation values
    if show_std_dev:
        for bars, std_devs in zip([bars1, bars2, bars3, bars4], [input_std, pre_exposure_std, post_exposure_std, post_exposure_liquid_std]):
            for bar, std_dev in zip(bars, std_devs):
                height = bar.get_height()
                ax.annotate(f'{std_dev:.2e}', xy=(bar.get_x() + bar.get_width() / 2, height), 
                            xytext=(-8, 2), textcoords="offset points", ha='center', va='bottom', fontsize=6, rotation=90)

    ax.set_xlabel('Number of Day(s)') # Set the x-axis label
    ax.set_ylabel('Mean CFU/ml') # Set the y-axis label
    
    # Set the title of the plot to the sheet name
    title = f'Disinfectant Residue Assay - {sheet_name}'
    ax.set_title(title)
    
    ax.set_xticks(index)
    ax.set_xticklabels(days)

    # Set y-axis to log scale
    ax.set_yscale('log')
    ax.set_yticks([1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7])

    # Position the legend outside of the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Add notes text below the graph
    notes_text = "Notes: Bars marked with an asterisk (*) are less then or equal to 2,000 CFU/ml."
    plt.figtext(0.77, 0.38, notes_text, ha="left", fontsize=8, wrap=True)
    plt.tight_layout()
    
    # Save the figure and show the plot
    filename = f"{title.replace(' ', '_')}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.show()
