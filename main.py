import re
import math
import pandas as pd

# function to convert complex time strings into total seconds for easier calculation
def parseTimeToSecondsFixed(timeStr):
    # split the time string into components
    parts = re.split('[:.]', timeStr)
    days = int(parts[0])
    hours = int(parts[1])
    minutes = int(parts[2])
    seconds = int(parts[3])
    # extract milliseconds and adjust the string split by '/'
    millisecondsPart = parts[4].split('/')[0]
    milliseconds = int(millisecondsPart)
    # calculate total seconds
    totalSeconds = days * 86400 + hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return totalSeconds

# calculates the Euclidean distance between two points
def calculateEuclideanDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# detects fixations based on distance and time thresholds
def detectFixations(data, distanceThreshold=50, timeThreshold=0.1):
    fixations = []
    currentFixation = [data[0]]
    currentFixationStart = data[0]['timestampSeconds']

    for i in range(1, len(data)):
        prevPoint = data[i-1]
        currentPoint = data[i]
        # calculate distance between the previous and current point
        distance = calculateEuclideanDistance(float(prevPoint['pupilX']), float(prevPoint['pupilY']),
                                                float(currentPoint['pupilX']), float(currentPoint['pupilY']))
        
        if distance <= distanceThreshold:
            currentFixation.append(currentPoint)
        else:
            # check if the current fixation duration meets the minimum threshold
            if currentFixation[-1]['timestampSeconds'] - currentFixationStart >= timeThreshold:
                fixations.append((currentFixationStart, currentFixation[-1]['timestampSeconds']))
            # reset fixation list
            currentFixation = [currentPoint]
            currentFixationStart = currentPoint['timestampSeconds']

    # check the last group of points collected as a fixation
    if currentFixation and (currentFixation[-1]['timestampSeconds'] - currentFixationStart >= timeThreshold):
        fixations.append((currentFixationStart, currentFixation[-1]['timestampSeconds']))

    return fixations

# correlates detected fixations with known regions of interest (ROI)
def correlateFixationsWithROI(fixations, roiData):
    fixationOutputs = []

    for start, end in fixations:
        # find overlaps with the ROIs
        overlaps = roiData[(roiData['Onset'] <= end) & (roiData['Offset'] >= start)]
        if overlaps.empty:
            # if no overlaps, it's a non-ROI fixation
            fixationOutputs.append({'Onset': start, 'Offset': end})
        else:
            # if there are overlaps, record the fixation
            fixationOutputs.append({'Onset': start, 'Offset': end})

    return fixationOutputs

# read eye tracking data from a text file
filePath = 'child_eye_1.txt'
with open(filePath, 'r') as file:
    childEyeData = file.readlines()

# parse the eye tracking data
parsedData = []
columns = ['recordFrameCount', 'sceneFrameCount', 'avgFps', 'sceneQTtime', 'porQTtime', 
           'porX', 'porY', 'pupilX', 'pupilY', 'cornealRefX', 'cornealRefY', 'diameterW', 'diameterH']
for line in childEyeData[7:]:
    if line.strip():
        parts = line.split()
        dataPoint = {col: parts[i] for i, col in enumerate(columns)}
        dataPoint['timestampSeconds'] = parseTimeToSecondsFixed(dataPoint['sceneQTtime'])
        parsedData.append(dataPoint)

# detect fixations based on the parsed data
detectedFixations = detectFixations(parsedData)

# load ROI data from a CSV file
roiData = pd.read_csv('child_roi_1.csv', names=['Onset', 'Offset'])

# correlate detected fixations with ROI data
correlatedFixations = correlateFixationsWithROI(detectedFixations, roiData)

# output correlated fixations to a CSV file
correlatedFixationsDf = pd.DataFrame(correlatedFixations)
outputFilePath = 'correlatedFixations1.csv'
correlatedFixationsDf.to_csv(outputFilePath, index=False)

print("complete!")
