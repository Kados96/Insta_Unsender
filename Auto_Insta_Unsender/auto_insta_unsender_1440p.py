import cv2
import numpy as np
import pyautogui
import time
import os

## For some reason sometimes the emoji.jpg wasn't found. Enter your folder here if that happens
#os.chdir("d:/Programozás/klikk/")

# Load the template image
template_image = cv2.imread('emoji.jpg', cv2.IMREAD_COLOR)

# Define the click offset relative to the blue bubble message
click_offset = (-63, 15)  # Adjust as needed

def detect_blue_bubble(screen_image):
    # Perform template matching
    result = cv2.matchTemplate(screen_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.9  # Adjust the threshold as needed
    if max_val >= threshold:
        # Return the location of the blue bubble message
        return (max_loc[0] + template_image.shape[1] + click_offset[0], max_loc[1] + click_offset[1])
    else:
        return None


non = 0
time.sleep(5)
while True:
    non += 1 # increases by one when no message found
    pyautogui.moveTo((2491, 1300)) # This is where the mouse stays. instead of moving the mouse, the we simply scroll

    screen_image = pyautogui.screenshot().convert('RGB')  # Convert to RGB format
    screen_np = np.array(screen_image)
    screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

    # Detect the blue bubble message
    click_location = detect_blue_bubble(screen_cv) # The "More" button when howering on your message
    if click_location:
        click_location2 = (click_location[0] + -30, click_location[1] + -30) # The "Unsend" button

    if click_location:
        # Click at the calculated location
        pyautogui.click(click_location)
        pyautogui.click(click_location2)

        # Depending on connection or browser speed, delays are necessary between button clicks, adjust them here
        time.sleep(0.5)
        pyautogui.click(1275,789) # The confirmation for "Unsend" in the middle of the screen
        time.sleep(1)
        non = 0 # non counter resets to 0, because message was found

    
    pyautogui.scroll(20)


    # If no message is found for this many iterations, the program will quit
    if non == 10000: 
        print("No messages found")
        break
