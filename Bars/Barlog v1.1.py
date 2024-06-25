import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# Recognize Excel files with filenames starting with 'barlog' in immediate filepath
files = glob.glob("barlog*.xlsx")

# Read from all Excel files into a single DataFrame
data_frames = [pd.read_excel(file) for file in files]
df = pd.concat(data_frames, ignore_index=True)

# Calculate standard deviations
std_dev = {
    "Input": [1.00E+04, 5.00E+03, 7.00E+03, 8.00E+03],
    "Pre exposure": [2.00E+04, 3.00E+04, 1.50E+04, 2.00E+04],
    "Bacteria + Disinfectant": [5.00E+02, 2.00E+04, 1.00E+04, 3.00E+04],
    "Bacteria + Dried": [5.00E+02, 5.00E+02, 5.00E+04, 3.00E+04]
}

std_df = pd.DataFrame(std_dev)

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))

# Bar width, duh
bar_width = 0.2

# Set positions of the bars on the x-axis
r1 = np.arange(len(df['Time']))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Create the bars with error bars
ax.bar(r1, df['Input'], color='b', width=bar_width, edgecolor='grey', label='Input', yerr=std_df['Input'], capsize=5)
ax.bar(r2, df['Pre exposure'], color='g', width=bar_width, edgecolor='grey', label='Pre exposure', yerr=std_df['Pre exposure'], capsize=5)
ax.bar(r3, df['Bacteria + Disinfectant'], color='r', width=bar_width, edgecolor='grey', label='Bacteria + Disinfectant', yerr=std_df['Bacteria + Disinfectant'], capsize=5)
ax.bar(r4, df['Bacteria + Dried'], color='c', width=bar_width, edgecolor='grey', label='Bacteria + Dried', yerr=std_df['Bacteria + Dried'], capsize=5)

# Add xticks on the middle of the group bars
ax.set_xlabel('Time in Days', fontweight='bold')
ax.set_xticks([r + bar_width*1.5 for r in range(len(df['Time']))])
ax.set_xticklabels(df['Time'])

# Add y-axis label
ax.set_ylabel('CFU/mL')

# Add logarithmic scale
ax.set_yscale('log')

# Move legend outside of the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.subplots_adjust(right=0.75)  # Adjust plot to make space for the legend

plt.title('Bacterial Growth Over Time')
plt.show()
