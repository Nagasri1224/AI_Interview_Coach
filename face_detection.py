import cv2

print("Program Started")

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Open webcam
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("Camera Opened")
else:
    print("Failed to Open Camera")

face_detected_once = False

while True:
    success, frame = cap.read()

    if not success:
        print("Could not access camera")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Improve low-light detection
    gray = cv2.equalizeHist(gray)

    # Detect faces
    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=8,
    minSize=(100, 100)
)

    # Print only first time face is detected
    if len(faces) > 0 and not face_detected_once:
        print("Face Detected")
        face_detected_once = True

    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

    # Display face count
    cv2.putText(
        frame,
        f"Faces: {len(faces)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Face Detection", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Closing...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

print("Camera Closed")
print("Program Ended")