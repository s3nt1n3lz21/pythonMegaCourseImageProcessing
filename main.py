import cv2
import time
from datetime import datetime
import glob
import os
from threading import Thread

from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

# Keep checking the image/frame the camera captures and show that image
first_frame = None
is_object = False
is_object_before = False
count = 1

def clear_images():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    is_object = False
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame is None:
        first_frame = gray_frame_gau

    # Find the difference between the first frame and this frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Only show the parts of the image where there are big differences, ignore small differences. Get an image of only the object
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find the edges of images
    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small shapes/objects
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a rectangle around this object in the current frame
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            is_object = True
            # Save the image if there is an object
            cv2.imwrite(f"images/{count}.png", frame)

    # Send the email if the object has just disappeared
    if not is_object and is_object_before:
        all_images = glob.glob("images/*.png")
        middle_image = all_images[int(len(all_images)/2)]

        # Send the email on another thread
        email_thread = Thread(target=send_email, args=(middle_image,))
        email_thread.daemon = True

        # Clear images in image folder on another thread
        clear_image_thread = Thread(target=clear_images)
        clear_image_thread.daemon = True

        email_thread.start()
        clear_image_thread.start()

    currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Show the current time on the current frame
    cv2.putText(
        img=frame,
        text=currentTime,
        org=(30, 30),
        fontFace=cv2.FONT_HERSHEY_PLAIN,
        fontScale=2,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA
    )

    # Show the current frame
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        cv2.imwrite("image.png", frame)
        break

    is_object_before = is_object
    count = count + 1

video.release()
