import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# Recognize Excel files with filenames starting with 'barlog' in the immediate filepath
files = glob.glob("barlog*.xlsx")

# Read from all Excel files into a single DataFrame
data_frames = [pd.read_excel(file) for file in files]
df = pd.concat(data_frames, ignore_index=True)

# Calculate mean and standard deviations for each category
mean_values = df.groupby('Time').mean()
std_dev = df.groupby('Time').std()

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))

# Bar width
bar_width = 0.2

# Set positions of the bars on the x-axis
r1 = np.arange(len(mean_values))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Create the bars with error bars
bars1 = ax.bar(r1, mean_values['Input'], color='b', width=bar_width, edgecolor='grey', label='Input', yerr=std_dev['Input'], capsize=5)
bars2 = ax.bar(r2, mean_values['Pre exposure'], color='g', width=bar_width, edgecolor='grey', label='Pre exposure', yerr=std_dev['Pre exposure'], capsize=5)
bars3 = ax.bar(r3, mean_values['Bacteria + Disinfectant'], color='r', width=bar_width, edgecolor='grey', label='Bacteria + Disinfectant', yerr=std_dev['Bacteria + Disinfectant'], capsize=5)
bars4 = ax.bar(r4, mean_values['Bacteria + Dried'], color='c', width=bar_width, edgecolor='grey', label='Bacteria + Dried', yerr=std_dev['Bacteria + Dried'], capsize=5)

# Function to add error bar values
def add_error_bar_values(bars, errors):
    for bar, err in zip(bars, errors):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height + err, f'{err:.1f}', ha='center', va='bottom', fontsize=8)

# Add error bar values
add_error_bar_values(bars1, std_dev['Input'])
add_error_bar_values(bars2, std_dev['Pre exposure'])
add_error_bar_values(bars3, std_dev['Bacteria + Disinfectant'])
add_error_bar_values(bars4, std_dev['Bacteria + Dried'])

# Add xticks on the middle of the group bars
ax.set_xlabel('Time in Days', fontweight='bold')
ax.set_xticks([r + bar_width*1.5 for r in range(len(mean_values))])
ax.set_xticklabels(mean_values.index)

# Add y-axis label
ax.set_ylabel('CFU/mL')

# Add logarithmic scale
ax.set_yscale('log')

# Move legend outside of the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)  # Adjust plot to make space for the legend

plt.title('Bacterial Growth Over Time')
plt.show()
