Key Components and Workflow

Object Detection:

Uses the YOLO (You Only Look Once) model, specifically YOLOv8 and YOLOv5, for object detection (players, referees, ball).
Fine-tunes YOLO with a specialized football player detection dataset from Roboflow to improve detection accuracy, especially for referees, goalkeepers, and ball detection.
Bounding boxes are represented in xyxy format (top-left and bottom-right corners).
Differentiates referees from players and excludes non-players outside the court.

Data Preparation and Model Training:

Downloads football match videos from the DFL Bundesliga dataset.
Prepares the dataset with labeled bounding boxes and classes (player, referee, ball, goalkeeper).
Trains YOLOv5 model on 612 annotated images to improve detection performance over the out-of-the-box models.
Uses Google Colab for GPU-accelerated training, saving best and last model weights.
Tracking:

Implements tracking using the ByteTrack algorithm via the supervision library.
Assigns consistent IDs to detected objects across video frames to track player movement over time.
Handles issues like goalkeepers switching class labels by merging goalkeeper detections into the player class to simplify analysis.

Annotations Visualization:

Replaces bounding boxes with clearer, minimalistic visual cues:
Players and referees have ellipses (semi-circles) beneath them, colored differently (e.g., red for players, yellow for referees).
The ball is marked with a green triangle pointer above it.
Draws player track IDs below their ellipses for easy identification.

Team Assignment via Color Clustering:

Extracts player jersey colors for team assignment using K-means clustering on the cropped player bounding box images.
Segments the top half of the cropped player image to focus on the jersey and uses clustering to separate background from the jersey color.
Uses a second K-means clustering step to group players into two teams based on dominant jersey colors.
Assigns team colors (e.g., white and green) and annotates players accordingly in the visualization.

Ball Position Interpolation:

Addresses missing ball detections by interpolating ball positions frame-by-frame using pandas, producing smoother ball trajectories and more complete data.

Ball Possession Assignment:

Assigns ball possession by calculating the closest player foot position to the ball within a maximum pixel distance threshold.
Flags players as “has ball” when near the ball, enabling analysis of ball control per player and per team.
Team Ball Control Statistics:

Calculates the percentage of time each team has possession of the ball throughout the match.
Displays this data as a semi-transparent overlay on the video frame.

Camera Motion Estimation and Compensation:

Uses optical flow on corner features extracted from the top and bottom of frames to estimate camera movement between frames.
Camera movement is quantified as the maximum displacement of corner features in x and y directions.
Player positions are adjusted by subtracting camera motion to isolate true player movement on the field.

Perspective Transformation (View Transformer):

Converts distorted camera view coordinates into real-world court coordinates (meters).
Maps a trapezoidal region in pixel coordinates (representing the football field in camera view) to a rectangular real-world coordinate system based on actual football field dimensions (105m length, 68m width).
This transformation enables measurement of player movement distances in meters rather than pixels.

Speed and Distance Estimation:

Calculates player speed (km/h) and distance covered (meters) using transformed, camera-motion-compensated positions.
Speed is computed over sliding windows of frames (e.g., every 5 frames) by measuring distance covered divided by elapsed time.
Annotates player bounding boxes with current speed and total distance covered beneath the player markers.