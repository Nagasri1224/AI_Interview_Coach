import cv2
import mediapipe as mp

def get_eye_contact_score():

    print("Eye Contact Tracker Started")

    mp_face_mesh = mp.solutions.face_mesh

    cap = cv2.VideoCapture(0)

    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    total_frames = 0
    eye_contact_frames = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb)

        status = "NO FACE"

        if results.multi_face_landmarks:

            total_frames += 1

            face = results.multi_face_landmarks[0]

            left_eye = face.landmark[33]
            right_eye = face.landmark[263]
            nose = face.landmark[1]

            eye_center_x = (
                left_eye.x +
                right_eye.x
            ) / 2

            difference = abs(
                eye_center_x -
                nose.x
            )

            if difference < 0.03:

                status = "LOOKING AT CAMERA"

                eye_contact_frames += 1

            else:

                status = "LOOKING AWAY"

            eye_contact_score = (
                eye_contact_frames /
                total_frames
            ) * 100

            cv2.putText(
                frame,
                f"Eye Contact Score: {eye_contact_score:.1f}%",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            status,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Eye Contact Tracker",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if total_frames > 0:

        final_score = (
            eye_contact_frames /
            total_frames
        ) * 100

    else:

        final_score = 0

    return round(final_score, 2)


if __name__ == "__main__":

    score = get_eye_contact_score()

    print(
        "\nFinal Eye Contact Score:",
        score
    )