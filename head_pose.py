import cv2
import mediapipe as mp

def get_attention_score():

    mp_face_mesh = mp.solutions.face_mesh

    cap = cv2.VideoCapture(0)

    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True
    )

    total_frames = 0
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

        status = "NO FACE"

        if results.multi_face_landmarks:

            total_frames += 1

            face = results.multi_face_landmarks[0]

            nose = face.landmark[1]
            left_cheek = face.landmark[234]
            right_cheek = face.landmark[454]

            center_x = (
                left_cheek.x +
                right_cheek.x
            ) / 2

            diff = nose.x - center_x

            if diff > 0.03:

                status = "LOOKING LEFT"

            elif diff < -0.03:

                status = "LOOKING RIGHT"

            else:

                status = "LOOKING STRAIGHT"

                attentive_frames += 1

            attention_score = (
                attentive_frames /
                total_frames
            ) * 100

            cv2.putText(
                frame,
                f"Attention Score: {attention_score:.1f}%",
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
            "Attention Tracker",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if total_frames > 0:

        final_score = (
            attentive_frames /
            total_frames
        ) * 100

    else:

        final_score = 0

    print(
        "\nFinal Attention Score:",
        round(final_score, 2)
    )

    return round(final_score, 2)


if __name__ == "__main__":

    get_attention_score()