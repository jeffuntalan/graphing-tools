import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Recognize the Excel file with the prefix "barlog" in the current directory
file_list = [file for file in os.listdir() if file.startswith('barlog') and file.endswith('.xlsx')]

if len(file_list) == 0:
    print("No matching Excel file found starting with 'barlog' and ending with '.xlsx'.")
    exit()

file_path = file_list[0]  # Take the first matching file found

# Read the Excel file
xls = pd.ExcelFile(file_path)

# Scan sheets
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

    # Plot bars with logarithmic scale on y-axis
    bar_width = 0.2
    index = np.arange(len(days))

    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(index - bar_width, input_means, bar_width, label='Input', yerr=input_std, capsize=5, alpha=0.7)
    bars2 = ax.bar(index, pre_exposure_means, bar_width, label='Pre-exposure', yerr=pre_exposure_std, capsize=5, alpha=0.7)
    bars3 = ax.bar(index + bar_width, post_exposure_means, bar_width, label='Post-exposure', yerr=post_exposure_std, capsize=5, alpha=0.7)
    bars4 = ax.bar(index + 2*bar_width, post_exposure_liquid_means, bar_width, label='Post-exposure-Liquid', yerr=post_exposure_liquid_std, capsize=5, alpha=0.7)

    show_std_dev = False  # Toggle for standard deviation values

    # Annotate standard deviation values in exponential form on top of each bar, with rotation
    if show_std_dev:
        for bars, std_devs in zip([bars1, bars2, bars3, bars4], [input_std, pre_exposure_std, post_exposure_std, post_exposure_liquid_std]):
            for bar, std_dev in zip(bars, std_devs):
                height = bar.get_height()
                ax.annotate(f'{std_dev:.2e}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(-8, 2),
                            textcoords="offset points", ha='center', va='bottom', fontsize=6, rotation=90)

    ax.set_xlabel('Number of Day(s)')
    ax.set_ylabel('Mean CFU/ml')
    
    # Set the title of the plot to the sheet name
    ax.set_title(f'Disinfectant Residue Assay - {sheet_name}')
    
    ax.set_xticks(index)
    ax.set_xticklabels(days)

    # Set y-axis to logarithmic scale
    ax.set_yscale('log')

    # Position the legend outside of the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.show()
