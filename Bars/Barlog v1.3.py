import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Find the Excel file starting with 'barlog' and ending with '.xlsx'
file_list = [file for file in os.listdir() if file.startswith('barlog') and file.endswith('.xlsx')]

if len(file_list) == 0:
    print("No matching Excel file found starting with 'barlog' and ending with '.xlsx'.")
    exit()

file_path = file_list[0]  # Take the first matching file found

# Step 2: Read the Excel file
df = pd.read_excel(file_path, header=[0, 1])

# Step 3: Calculate averages and standard deviations
averages = df.groupby(level=0, axis=1).mean()
std_devs = df.groupby(level=0, axis=1).std()

# Step 4: Prepare data for plotting
days = [1, 7, 14, 21]
input_means = averages['Input'].values.flatten()
pre_exposure_means = averages['Pre-exposure'].values.flatten()
post_exposure_means = averages['Post-exposure'].values.flatten()
post_exposure_liquid_means = averages['Post-exposure-Liquid'].values.flatten()

input_std = std_devs['Input'].values.flatten()
pre_exposure_std = std_devs['Pre-exposure'].values.flatten()
post_exposure_std = std_devs['Post-exposure'].values.flatten()
post_exposure_liquid_std = std_devs['Post-exposure-Liquid'].values.flatten()

# Step 5: Plotting with logarithmic scale on y-axis
bar_width = 0.2
index = np.arange(len(days))

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(index - bar_width, input_means, bar_width, label='Input', yerr=input_std, capsize=5, alpha=0.7)
bars2 = ax.bar(index, pre_exposure_means, bar_width, label='Pre-exposure', yerr=pre_exposure_std, capsize=5, alpha=0.7)
bars3 = ax.bar(index + bar_width, post_exposure_means, bar_width, label='Post-exposure', yerr=post_exposure_std, capsize=5, alpha=0.7)
bars4 = ax.bar(index + 2*bar_width, post_exposure_liquid_means, bar_width, label='Post-exposure-Liquid', yerr=post_exposure_liquid_std, capsize=5, alpha=0.7)

show_std_dev = True  # Toggle this flag to show or hide standard deviation values

# Annotate standard deviation values in exponential form on top of each bar, with rotation
if show_std_dev:
    for bars, std_devs in zip([bars1, bars2, bars3, bars4], [input_std, pre_exposure_std, post_exposure_std, post_exposure_liquid_std]):
        for bar, std_dev in zip(bars, std_devs):
            height = bar.get_height()
            ax.annotate(f'{std_dev:.2e}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(-8, 2),
                        textcoords="offset points", ha='center', va='bottom', fontsize=6, rotation=90)

ax.set_xlabel('Number of Day(s)')
ax.set_ylabel('Mean CFU/ml')
ax.set_title('Disinfectant Residue Assay')
ax.set_xticks(index)
ax.set_xticklabels(days)

# Set y-axis to logarithmic scale
ax.set_yscale('log')

# Position the legend outside of the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.show()
