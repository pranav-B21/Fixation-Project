import numpy as np
import pandas as pd

# Function to match intervals based on proximity of start times
def match_intervals(gt_data, output_data):
    matched_pairs = []
    for _, gt_row in gt_data.iterrows():
        # Find the closest interval in the output data based on the sum of absolute differences of Onset and Offset times
        closest_output = output_data.iloc[((output_data['Onset'] - gt_row['Onset']).abs() + 
                                           (output_data['Offset'] - gt_row['Offset']).abs()).idxmin()]
        matched_pairs.append((gt_row, closest_output))
    return matched_pairs

# Load the datasets
child_roi = pd.read_csv('parent_roi_2.csv')
correlated_fixations = pd.read_csv('correlatedFixations2.csv')

# Adjust timestamps for the 30-second flag
child_roi['Onset'] -= 30
child_roi['Offset'] -= 30

# Match intervals from ground truth and output
matched_intervals = match_intervals(child_roi[['Onset', 'Offset']], correlated_fixations)

# Extract lengths of matched intervals
matched_gt_lengths = np.array([gt['Offset'] - gt['Onset'] for gt, _ in matched_intervals])
matched_output_lengths = np.array([out['Offset'] - out['Onset'] for _, out in matched_intervals])

# Calculate the correlation coefficient
correlation_coefficient = np.corrcoef(matched_gt_lengths, matched_output_lengths)[0, 1] if len(matched_gt_lengths) > 1 else 0

print(f"Correlation Coefficient: {correlation_coefficient}")
