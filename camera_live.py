import cv2
import mediapipe as mp


def get_live_camera_scores():

    mp_face_mesh = mp.solutions.face_mesh

    cap = cv2.VideoCapture(0)

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True
    )

    total_frames = 0

    eye_contact_frames = 0

    attentive_frames = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb)

        eye_status = "NO FACE"

        head_status = "NO FACE"

        if results.multi_face_landmarks:

            total_frames += 1

            face = results.multi_face_landmarks[0]

            # ------------------
            # Eye Contact
            # ------------------

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

            if difference < 0.08:

                eye_contact_frames += 1

                eye_status = "LOOKING AT CAMERA"

            else:

                eye_status = "LOOKING AWAY"

            # ------------------
            # Attention
            # ------------------

            left_cheek = face.landmark[234]
            right_cheek = face.landmark[454]

            center_x = (
                left_cheek.x +
                right_cheek.x
            ) / 2

            diff = nose.x - center_x

            if abs(diff) < 0.03:

                attentive_frames += 1

                head_status = "LOOKING STRAIGHT"

            elif diff > 0:

                head_status = "LOOKING LEFT"

            else:

                head_status = "LOOKING RIGHT"

            eye_score = (
                eye_contact_frames /
                total_frames
            ) * 100

            attention_score = (
                attentive_frames /
                total_frames
            ) * 100

            cv2.putText(
                frame,
                f"Eye: {eye_score:.1f}%",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Attention: {attention_score:.1f}%",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Live Camera Analysis",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()

    if total_frames == 0:

        return 0, 0

    eye_score = round(
        (
            eye_contact_frames /
            total_frames
        ) * 100,
        2
    )

    attention_score = round(
        (
            attentive_frames /
            total_frames
        ) * 100,
        2
    )

    return eye_score, attention_score


if __name__ == "__main__":

    eye, attention = get_live_camera_scores()

    print("\nEye Contact:", eye)

    print("Attention:", attention)