import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

# Keep checking the image/frame the camera captures and show that image
first_frame = None

while True:
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # cv2.imshow("A Video", gray_frame_gau)
    if first_frame is None:
        first_frame = gray_frame_gau

    # Find the difference between the first frame and this frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Only show the parts of the image where there are big differences, ignore small differences. Get an image of only the object
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("A Video", dilated_frame)

    # Find the edges of images
    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small shapes/objects
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a rectangle around this object in the current frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        cv2.imwrite("image.png", frame)
        break

video.release()
