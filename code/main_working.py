import cv2
import numpy as np
import time
import sys
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500,2500)
kit.servo[1].set_pulse_width_range(500,2500)
kit.servo[2].set_pulse_width_range(500,2500)
kit.servo[3].set_pulse_width_range(500,2500)


def nothing(x):
    pass

def prompt_for_pid_values():
    global Kp, Ki, Kd
    try:
        new_kp = float(input("Enter new Kp value for all motors: "))
        new_ki = float(input("Enter new Ki value for all motors: "))
        new_kd = float(input("Enter new Kd value for all motors: "))
        Kp = np.array([new_kp, new_kp, new_kp, new_kp])
        Ki = np.array([new_ki, new_ki, new_ki, new_ki])
        Kd = np.array([new_kd, new_kd, new_kd*1.5, new_kd])
    except ValueError:
        print("Invalid input, using previous values.")


initial_angle = [135, 131, 131, 135]  # Initial angles for the motors
def adjust_motor_angles():
    window_name = "Motor Angle Adjuster"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 500, 200)

    # Create trackbars for each motor
    min_angle = 105
    max_angle = 155
    angles = [135, 135, 135, 135]  # Initial angles for the motors
    
    def update_angle(index, value):
        angle = min_angle + value  # Adjusting the value to the correct range
        angles[index] = angle
        kit.servo[index].angle = angle
        print(f"Motor {index+1} angle set to: {angle}")

    for i in range(4):
        cv2.createTrackbar(f"Motor {i+1}", window_name, 0, max_angle-min_angle, lambda x, i=i: update_angle(i, x))
        cv2.setTrackbarPos(f"Motor {i+1}", window_name, angles[i] - min_angle)  # Adjust trackbar position to the correct range


    # Wait until 'q' is pressed to close the adjustment window
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Camera is not opened")
    exit()

# Variables to store the ROI coordinates
roi = [0, 0, 0, 0]
drawing = False  # True if mouse is pressed

# Function to send control signal to the servos
# Placeholder function, replace with your implementation
min_motor = np.array([120,120,120,120])
max_motor = np.array([150,150,150,150])

# kit.servo[0].angle = initial_angle[0]
# kit.servo[1].angle = initial_angle[1] 
# kit.servo[2].angle = initial_angle[2] 
# kit.servo[3].angle = initial_angle[3]

kit.servo[0].angle = 155
kit.servo[1].angle = 111
kit.servo[2].angle = 136
kit.servo[3].angle = 155
def move_motors(pid):
    for i in range(0,4,1):
        print("pid " + str(i) + " " + str(pid[i])) 
        angle = initial_angle[i] + (pid[i]/40)
        angle = np.floor(angle)
        print("angle " + str(angle))
        if angle > max_motor[i]:
            print("angle limit high")
            angle = max_motor[i]
        if angle < min_motor[i]:
            print("angle limit low")
            angle = min_motor[i]
        kit.servo[i].angle = angle 


# Placeholder for your servo control logic
# This function needs to be implemented based on your servo setup
lastderivative = 0
lastlastderivative = 0
derivative = 0
integral = 0
pid = 0
def control_servos():
    global start_time
    global computation_time
    global errors, pasterrors
    global lastderivative, lastlastderivative, derivative
    global Ki
    global integral
    comp_time = time.time() - start_time
    computation_time.append(comp_time)
    if np.all(errors > 10):
        integral += errors * 0.5 
    else:
        integral = 0
    Kd_normalized = np.copy(Kd)
    Ka_normalized = np.copy(Ka)
    Kp_normalized = np.copy(Kp)
#     Kp_normalized[np.abs(errors) < 50] = Kp_normalized[np.abs(errors) < 50] * 0.5

    
    print("kd: " + str(Kd_normalized) + " kp: " + str(Kp_normalized) + " ki: " + str(Ki) + " ka: " + str(Ka_normalized))
    
    lastlastderivative = np.copy(lastderivative)
    lastderivative = np.copy(derivative)
    derivative = (errors - pasterrors)
    
    if np.sum(abs(derivative)) < 30:
        Kd_normalized = Kd_normalized *  0.1
    # elif np.sum(abs(derivative)) > 20:
    #     Kd_normalized = Kd_normalized * 1.1
    if np.all(np.abs(derivative) < 0.5):
        Kd_normalized = 0
    
    pid = Kp_normalized * errors + Ki * integral + Kd_normalized * derivative + Ka_normalized * (((derivative - lastderivative) + (lastderivative - lastlastderivative))/2.0)
    print("Pid: ", pid)
    
    move_motors(pid)
    
    pass


# Mouse callback function
def draw_roi(event, x, y, flags, param):
    global roi, drawing

    # If left mouse button clicked, record the starting ROI coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi = [x, y, x, y]

    # If mouse is moved, record the ending ROI coordinates
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            roi[2], roi[3] = x, y

    # If left mouse button is released, complete the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi[2], roi[3] = x, y

# Create a window and attach the mouse callback function
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_roi)

print("Draw ROI rectangle with the mouse and press 'c' to confirm")

# Loop for drawing the ROI
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture the image")
        break

    # Draw the ROI rectangle on the frame
    if drawing or roi[2]:
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif key == ord('c'):  # Press 'c' to confirm the ROI and continue
        if roi[2] and roi[3]:
            break

# Close the initial window
cv2.destroyAllWindows()

# Define ROI coordinates
x_start, y_start, x_end, y_end = roi
x_start, x_end = sorted([x_start, x_end])
y_start, y_end = sorted([y_start, y_end])


# Predefined HSV color ranges for ball tracking
color_ranges = {
    'blue': ([100, 150, 0], [140, 255, 255]),
    'green': ([40, 70, 70], [80, 255, 255]),
    'orange': ([5, 50, 50], [15, 255, 255]),
    'yellow': ([25, 100, 100], [35, 255, 255])
}

# Prompt for ball color input
print("Enter the color of the ball: (blue, green, orange, yellow)")
selected_color = input().lower()
lower_hsv, upper_hsv = color_ranges.get(selected_color, ([0, 0, 0], [179, 255, 255]))
lower_hsv = np.array(lower_hsv)
upper_hsv = np.array(upper_hsv)

# Create a window for the slider
cv2.namedWindow("Threshold Adjuster", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Threshold Adjuster", 300, 50)  # Width, Height
cv2.createTrackbar("Threshold", "Threshold Adjuster", 0, 255, nothing)
cv2.setTrackbarPos("Threshold", "Threshold Adjuster", 200) # Default value
# Flag to indicate if the threshold is being manually adjusted
manual_threshold = False



# PID constants

Kp = np.array([1, 1, 1, 1])
Ki = np.array([5, 5, 5, 5])
Kd = np.array([30, 30, 30, 30])
Ka = np.array([0, 0, 0, 0])  # Acceleration factor

# PID variables
previous_error_x = 0
previous_error_y = 0
integral_x = 0
integral_y = 0

# Desired position (setpoint) is the center of the platform
# These will be updated once we have the ROI
desired_position_x = 0  # Placeholder, will be set later
desired_position_y = 0  # Placeholder, will be set later



# Main control loop
start_time = time.time()
errors = np.zeros(4)
pasterrors = np.zeros(4)
computation_time = []
paused = False
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture the image")
        break
    frame = frame[y_start:y_end, x_start:x_end]
    # Convert frame to HSV and create a mask
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)  
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assume no ball found yet
    ball_position_x, ball_position_y = None, None

    if contours:
        # Find the largest contour and use it as the ball
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        
        # Consider the ball found if the radius meets a minimum size
        if radius > 10:
            ball_position_x, ball_position_y = int(x), int(y)
            # Draw the circle on the ball
            cv2.circle(frame, (ball_position_x, ball_position_y), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (ball_position_x, ball_position_y), 5, (0, 0, 255), -1)
    
    # Check if manual threshold adjustment is enabled
    if manual_threshold:
        threshold_value = cv2.getTrackbarPos("Threshold", "Threshold Adjuster")
    else:
        # Implement dynamic thresholding based on lighting condition
        # Example: Calculate average brightness of the image and set threshold
        avg_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        threshold_value = int(avg_brightness * 2)  # Example calculation

    # Platform center tracking with adjusted threshold
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 100:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            desired_position_x = int(M["m10"] / M["m00"])
            desired_position_y = int(M["m01"] / M["m00"])
            cv2.circle(frame, (desired_position_x, desired_position_y), 5, (255, 0, 0), -1)
            cv2.drawContours(frame, [largest_contour], -1, (255, 0, 0), 2)

    # Display the resulting frame
    
    
    # Only proceed with PID control if we have a ball position
    if ball_position_x is not None and ball_position_y is not None:
        # Calculate error between desired position and current ball position
        error_x = desired_position_x - ball_position_x
        error_y = desired_position_y - ball_position_y

        # Calculate integral for Ki term
        integral_x += error_x
        integral_y += error_y

        # Calculate derivative for Kd term
        derivative_x = error_x - previous_error_x
        derivative_y = error_y - previous_error_y

        # Calculate control signals
        control_signal_x = Kp*error_x + Ki*integral_x + Kd*derivative_x
        control_signal_y = Kp*error_y + Ki*integral_y + Kd*derivative_y

        # Update previous error
        previous_error_x = error_x
        previous_error_y = error_y
        
        pasterrors = np.copy(errors)

        # Error calculation:
        # Positive error indicates the ball is below the motor position for Y-axis motors
        # and to the left of the motor position for X-axis motors
        errors[0] = y - desired_position_y  # Error for Motor 0 (Top edge)
        errors[1] = desired_position_x - x  # Error for Motor 1 (Right edge)
        errors[2] = desired_position_y - y  # Error for Motor 2 (Bottom edge)
        errors[3] = x - desired_position_x  # Error for Motor 3 (Left edge)

        control_servos()
        print("current ball: ( " + str(ball_position_x) + ", " + str(ball_position_y) + " ) platform center: (" + str(desired_position_x) + ", " + str(desired_position_y) + " ) error: (" + str(error_x) + ", " + str(error_y) + ")")


    cv2.imshow('Combined Tracking', frame)
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t'):
        manual_threshold = not manual_threshold
    elif key == ord('a'):  # If 'a' is pressed, show motor angle adjuster
        adjust_motor_angles()
    elif key == ord('y'):
        cap.release()
        cv2.destroyAllWindows()
        prompt_for_pid_values()
        cap = cv2.VideoCapture(0)  # Reinitialize the camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        continue
            
# Cleanup
cap.release()
cv2.destroyAllWindows()


