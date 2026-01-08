# -*- coding: utf-8 -*-
"""
Calibration tool for pixel-to-cm conversion using video frames.

Created on Wed Jan 07, 2026
Author: ktt920
"""

import cv2
import os
import math
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.messagebox as tkMessageBox

# Configuration
FRAME_WIDTH = 800
FRAME_HEIGHT = 600
OUTPUT_EXCEL = "calibration_results.xlsx"

# Select folder dialog
root = tk.Tk()
root.withdraw()  # Hide main tkinter window

video_folder = filedialog.askdirectory(
    title="Select folder containing videos"
)

if not video_folder:
    print("No folder selected. Exiting.")
    exit()

# Mouse callback
clicked_points = []


# Define a function that click point is defined as when left button is clicked down and can only have max of 2 points.
def mouse_callback(event, x, y, flags, param):
    # Call the global clicked_points so do not create a local list.
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 2:
        clicked_points.append((x, y))


# Main processing
# This store the results for different videos being analyzed.
results = []

# Look for all video files within the selected folder.
video_files = [
    f for f in os.listdir(video_folder)
    if f.lower().endswith(('.mp4', '.avi', '.mov'))
]

if not video_files:
    print("No video files found in selected folder.")
    exit()

# Create a video path for each video
for video_name in video_files:
    video_path = os.path.join(video_folder, video_name)
    cap = cv2.VideoCapture(video_path)

    # Get FPS from the video metadata
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Capture the first frame of the video.
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Failed to read first frame: {video_name}")
        continue

    # Resize frame to 800x600 (no cropping)
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    # Reset clicks
    clicked_points = []

    # Create window
    cv2.namedWindow(video_name)
    cv2.moveWindow(video_name, 100, 100)
    cv2.setMouseCallback(video_name, mouse_callback)

    print(f"\nProcessing: {video_name}")
    tkMessageBox.showinfo("",
                          "Click TWO points to define a known distance.\n Press ENTER to confirm, ESC to skip this video.")

    while True:
        display = frame.copy()

        # Draw points
        for pt in clicked_points:
            cv2.circle(display, pt, 5, (0, 0, 255), -1)

        # Draw line
        if len(clicked_points) == 2:
            cv2.line(display, clicked_points[0], clicked_points[1], (0, 255, 0), 2)

        cv2.imshow(video_name, display)
        key = cv2.waitKey(20) & 0xFF

        # ENTER confirms
        if key == 13 and len(clicked_points) == 2:
            break

        # ESC skips
        if key == 27:
            clicked_points = []
            break

    cv2.destroyWindow(video_name)

    if len(clicked_points) != 2:
        print(f"Skipped: {video_name}")
        continue

    # Compute pixel distance
    (x1, y1), (x2, y2) = clicked_points
    pixel_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Get real-world distance in cm
    while True:
        real_distance_cm = simpledialog.askfloat(
            "",
            f"Enter real-world distance in cm for:\n\n{video_name}",
            minvalue=0.0001
        )

        if real_distance_cm is None:
            # User pressed Cancel
            print(f"Skipped: {video_name}")
            clicked_points = []
            break

        if real_distance_cm > 0:
            break

    if not clicked_points:
        continue

    cm_per_pixel = real_distance_cm / pixel_distance

    results.append({
        "video_name": video_name,
        "pixel_distance_px": pixel_distance,
        "real_distance_cm": real_distance_cm,
        "cm_per_pixel": cm_per_pixel,
        "fps": fps
    })

# Save results to Excel
df = pd.DataFrame(results)

output_path = os.path.join(video_folder, OUTPUT_EXCEL)
df.to_excel(output_path, index=False)

print("\nCalibration complete.")
print(f"Results saved to: {output_path}")
