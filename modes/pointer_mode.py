import cv2

class PointerMode:
    def __init__(self):
        self.active = False

    def toggle(self, is_active):
        self.active = is_active

    def draw_pointer(self, frame, landmarks, width, height):
        if not self.active or landmarks is None:
            return frame

        # Get index fingertip (landmark 8)
        try:
            index_finger = landmarks.landmark[8]
            x = int(index_finger.x * width)
            y = int(index_finger.y * height)

            # Draw red circle
            cv2.circle(frame, (x, y), 15, (0, 0, 255), -1)

            # Debug log to confirm it's working
            print(f"Pointer active → Drawing at ({x}, {y})")

        except Exception as e:
            print("Pointer drawing error:", e)

        return frame
