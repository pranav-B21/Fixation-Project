import re
import math
import pandas as pd

# function to convert complex time strings into total seconds for easier calculation
def parse_time_to_seconds_fixed(time_str):
    # split the time string into components
    parts = re.split('[:.]', time_str)
    days = int(parts[0])
    hours = int(parts[1])
    minutes = int(parts[2])
    seconds = int(parts[3])
    # extract milliseconds and adjust the string split by '/'
    milliseconds_part = parts[4].split('/')[0]
    milliseconds = int(milliseconds_part)
    # calculate total seconds
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds

# calculates the Euclidean distance between two points
def calculate_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# detects fixations based on distance and time thresholds
def detect_fixations(data, distance_threshold=50, time_threshold=0.1):
    fixations = []
    current_fixation = [data[0]]
    current_fixation_start = data[0]['timestamp_seconds']

    for i in range(1, len(data)):
        prev_point = data[i-1]
        current_point = data[i]
        # calculate distance between the previous and current point
        distance = calculate_euclidean_distance(float(prev_point['pupilX']), float(prev_point['pupilY']),
                                                float(current_point['pupilX']), float(current_point['pupilY']))
        
        if distance <= distance_threshold:
            current_fixation.append(current_point)
        else:
            # check if the current fixation duration meets the minimum threshold
            if current_fixation[-1]['timestamp_seconds'] - current_fixation_start >= time_threshold:
                fixations.append((current_fixation_start, current_fixation[-1]['timestamp_seconds']))
            # reset fixation list
            current_fixation = [current_point]
            current_fixation_start = current_point['timestamp_seconds']

    # check the last group of points collected as a fixation
    if current_fixation and (current_fixation[-1]['timestamp_seconds'] - current_fixation_start >= time_threshold):
        fixations.append((current_fixation_start, current_fixation[-1]['timestamp_seconds']))

    return fixations

# correlates detected fixations with known regions of interest (ROI)
def correlate_fixations_with_roi(fixations, roi_data):
    fixation_outputs = []

    for start, end in fixations:
        # find overlaps with the ROIs
        overlaps = roi_data[(roi_data['Onset (s)'] <= end) & (roi_data['Offset (s)'] >= start)]
        if overlaps.empty:
            # if no overlaps, it's a non-ROI fixation
            fixation_outputs.append({'Onset (s)': start, 'Offset (s)': end})
        else:
            # if there are overlaps, record the fixation
            fixation_outputs.append({'Onset (s)': start, 'Offset (s)': end})

    return fixation_outputs

# read eye tracking data from a text file
#file_path = 'child_eye_1.txt'
file_path = 'child_eye_2.txt'
with open(file_path, 'r') as file:
    child_eye_data = file.readlines()

# parse the eye tracking data
parsed_data = []
columns = ['recordFrameCount', 'sceneFrameCount', 'avg_fps', 'sceneQTtime', 'porQTtime', 
           'porX', 'porY', 'pupilX', 'pupilY', 'cornealRefX', 'cornealRefY', 'diameterW', 'diameterH']
for line in child_eye_data[7:]:
    if line.strip():
        parts = line.split()
        data_point = {col: parts[i] for i, col in enumerate(columns)}
        data_point['timestamp_seconds'] = parse_time_to_seconds_fixed(data_point['sceneQTtime'])
        parsed_data.append(data_point)

# detect fixations based on the parsed data
detected_fixations = detect_fixations(parsed_data)

# load ROI data from a CSV file
#roi_data = pd.read_csv('child_roi_1.csv', names=['Onset (s)', 'Offset (s)'])
roi_data = pd.read_csv('child_roi_2.csv', names=['Onset (s)', 'Offset (s)'])

# correlate detected fixations with ROI data
correlated_fixations = correlate_fixations_with_roi(detected_fixations, roi_data)

# output correlated fixations to a CSV file
correlated_fixations_df = pd.DataFrame(correlated_fixations)
#output_file_path = 'correlated_fixations_1.csv'
output_file_path = 'correlated_fixations_2.csv'
correlated_fixations_df.to_csv(output_file_path, index=False)

print("complete!")
