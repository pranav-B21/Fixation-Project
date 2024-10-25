Overview:

This script processes eye-tracking data to detect fixation periods, where the eye gaze remains relatively stable. Fixations are crucial for understanding how viewers process visual information, making this script valuable for research in visual perception and cognitive sciences.

Approach:

The script begins by reading eye-tracking data from a file that includes timestamps and pupil coordinates. It then calculates the distance between consecutive gaze points using the Euclidean distance formula. Fixations are identified based on whether the eye movement between successive points falls below a specified spatial threshold for a minimum duration, indicating stability in gaze.

Correlation with Regions of Interest (ROI):

After detecting fixations, the script correlates these with predefined regions of interest (ROIs) provided in a separate file. Each fixation is checked against these ROIs to determine if it occurred within or outside these areas. This correlation helps in classifying the attention focus of the viewer.

Output:

The results are saved to a CSV file, detailing the onset and offset times of each detected fixation. This output can be used for further analysis to draw conclusions about the viewer's attention and gaze behavior during the eye-tracking session.
