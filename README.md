**Overview**:
This script processes eye-tracking data to detect fixation. Fixations help us understand visual information.

**Approach**:
The code reads eye-tracking data from a file that includes timestamps and pupil coordinates. It then calculates the distance between consecutive gaze points using the Euclidean distance formula. Fixations are identified based on whether the eye movement between successive points falls below a specified distance threshold for a minimum duration, indicating stability in gaze.

**Correlation with Regions of Interest (ROI)**:
After detecting fixations, the code correlates these with predefined ROIs provided in a separate file. Each fixation is checked against these ROIs to determine if it occurred within or outside these areas. This correlation helps in classifying the attention focus of the viewer.

**Output**:
The results are saved to a CSV file.
