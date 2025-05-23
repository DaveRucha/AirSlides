import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands

class GestureDetector:
    def __init__(self, detection_confidence=0.7):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.hand_connections = mp_hands.HAND_CONNECTIONS

    def detect_hand_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None

    def get_finger_states(self, landmarks, frame_width, frame_height):
        # Convert normalized landmarks to pixel positions
        points = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in landmarks.landmark]
        
        fingers = []

        # Thumb (horizontal check)
        fingers.append(1 if points[4][0] > points[3][0] else 0)

        # Index to Pinky (vertical check)
        for tip_id in [8, 12, 16, 20]:
            fingers.append(1 if points[tip_id][1] < points[tip_id - 2][1] else 0)

        return fingers  # [Thumb, Index, Middle, Ring, Pinky]

    def classify_gesture(self, finger_states, landmarks):
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        ok_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

        if ok_distance < 0.05 and sum(finger_states[2:]) >= 2:
            return "OK Sign"

        if finger_states == [0, 0, 0, 0, 0]:
            return "Fist"
        elif sum(finger_states) >= 4:
            return "Palm"
        elif finger_states == [0, 1, 0, 0, 0]:
            return "Point"
        elif finger_states == [0, 1, 1, 0, 0]:
            return "V Sign"
        elif finger_states == [1, 0, 0, 0, 0]:
            return "Thumbs Up"
        elif finger_states == [1, 1, 0, 0, 0]:
            return "L Sign"
        elif finger_states[0] == 1 and finger_states[4] == 1 and sum(finger_states[1:4]) <= 1:
            return "Rock"

        return "Unknown"
