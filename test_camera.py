import cv2

print("Program Started")

cap = cv2.VideoCapture(0)

print("Camera Opened")

while True:
    success, frame = cap.read()

    if not success:
        print("Could not read frame")
        break

    cv2.imshow("AI Interview Coach", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        print("Closing...")
        break

cap.release()
cv2.destroyAllWindows()