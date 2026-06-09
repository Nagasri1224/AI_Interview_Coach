from eye_contact import get_eye_contact_score
from head_pose import get_attention_score


def get_camera_scores():

    print("\n" + "=" * 50)
    print("CAMERA ANALYSIS")
    print("=" * 50)

    print("\nStep 1: Eye Contact Analysis")
    print("Look at the camera and press 'q' when finished.")

    eye_contact_score = get_eye_contact_score()

    print("\nEye Contact Score:", eye_contact_score)

    print("\nStep 2: Attention Analysis")
    print("Look straight at the screen and press 'q' when finished.")

    attention_score = get_attention_score()

    print("\nAttention Score:", attention_score)

    print("\nCamera Analysis Completed")

    return eye_contact_score, attention_score


if __name__ == "__main__":

    eye_score, attention_score = get_camera_scores()

    print("\n" + "=" * 50)
    print("FINAL CAMERA REPORT")
    print("=" * 50)

    print("Eye Contact Score :", eye_score)
    print("Attention Score   :", attention_score)