import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

# Configuration
FRAME_WIDTH = 800
FRAME_HEIGHT = 600
OUTPUT_CSV = "calibration_results.csv" 

# Select the folder of analysis
root = tk.Tk()
root.withdraw()  # Hide main tkinter window

video_folder = filedialog.askdirectory(
    title="Select folder containing videos"
)

if not video_folder:
    print("No folder selected. Exiting.")
    exit()

folder_name = os.path.basename(os.path.normpath(video_folder))

# Setup paths
RATIO_FILE = "calibration_results.csv"
GAIT_FILE = f"{folder_name} gait parameters.csv"
OUTPUT_CSV = "gait_results_converted.csv"

# Load the data
ratios_df = pd.read_csv(os.path.join(video_folder, RATIO_FILE))
gait_df = pd.read_csv(os.path.join(video_folder, GAIT_FILE))

# Extract Conversion Ratio from RATIO_FILE
ratio_cm = ratios_df["cm_per_pixel"].item()
ratio_fps = ratios_df["fps"].item()

# Spatial Parameterer (pixel to cm)
# Pixel * ratio_cm = cm
cols_to_convert_spatial = [
    'Base of Support', 
    'Stride Length', 
    'Right Stride Length', 
    'Left Stride Length', 
    'Step Length', 
    'Mean Absolute Interlimb Distance', 
    'SD of Absolute Interlimb Distance'
]


# Temporal Parameterer (frame to second)
# Frame / ratio_fps = second
cols_to_convert_temporal = [
    'Stance Duration'
]

# Velocity Parameterer (Pixels/Frame} to cm/second)
# (Pixels/Frame) * ratio_cm * ratio_fps
cols_to_convert_velocity = [
    'Stride Speed First Stride',
    'Stride Speed Second Stride',
    'Stride Speed Third Stride'
]

# Area Parameterer (pixel^2) to cm^2)
# pixel^2 * ratio_cm * ratio_cm
cols_to_convert_area = [
    'Average of Maximum Areas'
]

# 5. Apply the conversion
for col in gait_df.columns:
    if col in cols_to_convert_spatial:
        gait_df[col] = gait_df[col] * ratio_cm
    elif col in cols_to_convert_temporal:
        gait_df[col] = gait_df[col] / ratio_fps
    elif col in cols_to_convert_velocity:
        gait_df[col] = gait_df[col] * ratio_cm * ratio_fps
    elif col in cols_to_convert_area:
        gait_df[col] = gait_df[col] * ratio_cm * ratio_cm


# 6. Save to CSV
output_path = os.path.join(video_folder, OUTPUT_CSV)
gait_df.to_csv(output_path, index=False)

print(f"Successfully converted units to cm using ratio: {ratio_cm}")