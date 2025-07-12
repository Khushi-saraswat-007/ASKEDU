import math

import cv2
import mediapipe as mp
def calculate_ear(landmarks, eye_indices, w, h):
    A = math.dist(
        (landmarks[eye_indices[1]].x * w, landmarks[eye_indices[1]].y * h),
        (landmarks[eye_indices[5]].x * w, landmarks[eye_indices[5]].y * h)
    )
    B = math.dist(
        (landmarks[eye_indices[2]].x * w, landmarks[eye_indices[2]].y * h),
        (landmarks[eye_indices[4]].x * w, landmarks[eye_indices[4]].y * h)
    )
    C = math.dist(
        (landmarks[eye_indices[0]].x * w, landmarks[eye_indices[0]].y * h),
        (landmarks[eye_indices[3]].x * w, landmarks[eye_indices[3]].y * h)
    )
    return (A + B) / (2.0 * C)

def get_ear(landmarks, left_eye_indices, right_eye_indices, w, h):
    left_ear = calculate_ear(landmarks, left_eye_indices, w, h)
    right_ear = calculate_ear(landmarks, right_eye_indices, w, h)
    return (left_ear + right_ear) / 2.0



# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_avg_ear(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape
        ear = get_ear(landmarks, LEFT_EYE, RIGHT_EYE, w, h)
        return ear
    return 1.0  # Return default EAR if face not detected
