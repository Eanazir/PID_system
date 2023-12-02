import cv2
import numpy as np
 
# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
# Predefined HSV color ranges
color_ranges = {
    'blue': ([100, 150, 0], [140, 255, 255]),
    'green': ([40, 70, 70], [80, 255, 255]),
    'orange': ([5, 50, 50], [15, 255, 255]),
    'yellow': ([25, 100, 100], [35, 255, 255])
}
 
# Ask the user for the color
print("Enter the color of the ball: (blue, green, orange, yellow)")
selected_color = input().lower()
 
# Get the selected color range
lower_hsv, upper_hsv = color_ranges.get(selected_color, ([0, 0, 0], [179, 255, 255]))
 
lower_hsv = np.array(lower_hsv)
upper_hsv = np.array(upper_hsv)
 
# Start tracking the selected color
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
 
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # Create a mask using the selected HSV range
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
 
    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    if contours:
        # Find the largest contour and compute the minimum enclosing circle
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
 
        # Check if the found contour is of a sufficient size
        if radius > 10:
            # Draw the circle and center on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
 
    # Display the resulting frame and mask
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
 
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
 