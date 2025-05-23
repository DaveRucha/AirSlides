import cv2

class DrawMode:
    def __init__(self):
        self.active = False
        self.points = []

    def toggle(self, is_active):
        self.active = is_active
        if not is_active:
            self.points.clear()

    def clear(self):
        self.points.clear()

    def update(self, landmarks, width, height):
        if not self.active or landmarks is None:
            return

        # Index finger tip = landmark 8
        x = int(landmarks.landmark[8].x * width)
        y = int(landmarks.landmark[8].y * height)
        self.points.append((x, y))

    def draw(self, frame):
        for i in range(1, len(self.points)):
            cv2.line(frame, self.points[i - 1], self.points[i], (255, 0, 0), 5)
        return frame
