import streamlit as st
import cv2
import numpy as np

def detect_color(image, color):
    # Convert BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of color in HSV
    if color == 'red':
        lower_color = np.array([0, 100, 100])
        upper_color = np.array([10, 255, 255])
    elif color == 'green':
        lower_color = np.array([40, 100, 100])
        upper_color = np.array([80, 255, 255])
    elif color == 'blue':
        lower_color = np.array([100, 100, 100])
        upper_color = np.array([140, 255, 255])

    # Threshold the HSV image to get only specified color
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    return res

def main():
    st.title('Color Detection App')

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if not cap.isOpened():
        st.error("Error: Could not open camera.")
        return

    color_options = ('red', 'green', 'blue')

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Display the frame
            st.image(frame, caption='Live Video', channels="BGR")

            # Detect color
            selected_color = st.radio('Select color to detect:', options=color_options)
            color_detected = detect_color(frame, selected_color)

            # Display color-detected result
            st.image(color_detected, caption='Color Detected', channels="BGR")

        else:
            st.error("Error: Could not read frame from camera.")
            break

    # Release the VideoCapture object and close the streamlit app
    cap.release()

if __name__ == "__main__":
    main()
