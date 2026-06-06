try:
    print("Step 1: Importing OpenCV")
    import cv2

    print("Step 2: Importing MediaPipe")
    import mediapipe as mp

    print("Step 3: Creating Face Detection")
    mp_face_detection = mp.solutions.face_detection

    print("Step 4: Opening Camera")
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        print("Camera Opened")
    else:
        print("Camera Failed")

except Exception as e:
    print("\nERROR OCCURRED:")
    print(type(e).__name__)
    print(e)

input("\nPress Enter to exit...")
