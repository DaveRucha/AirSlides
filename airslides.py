import sys
import os
sys.stderr = open(os.devnull, 'w')  # Suppress native stderr logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pywinauto")

import logging
import absl.logging
absl.logging.set_verbosity('error')
logging.getLogger('absl').setLevel(logging.ERROR)

import cv2
import time
import ctypes
from pywinauto import Application

from gestures.gesture_detector import GestureDetector
from utils.stabilizer import GestureStabilizer
from modes.pointer_mode import PointerMode
from modes.draw_mode import DrawMode
from utils.pdf_to_slides import convert_pdf_to_images
from utils.narration import narrate_slide, stop_narration

# Load slide images from the slides/ folder
def load_slides(folder_path="slides"):
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    slide_images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            img = cv2.imread(path)
            if img is not None:
                h, w = img.shape[:2]
                scale = min(screen_width / w, screen_height / h)
                new_size = (int(w * scale), int(h * scale))
                slide_images.append(cv2.resize(img, new_size))
    return slide_images

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        return

    detector = GestureDetector()
    stabilizer = GestureStabilizer(cooldown=1.5)
    pointer = PointerMode()
    draw = DrawMode()

    pdf_path = input("Enter the path to your slide PDF (or press Enter to skip): ").strip()
    if pdf_path:
        convert_pdf_to_images(pdf_path)

    slides = load_slides("slides")
    current_slide_index = 0
    total_slides = len(slides)

    print("AirSlides started. Show gestures to control slides.")
    window_title = "AirSlides - Presentation View"
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
    window_focused = False

    while True:
        frame = slides[current_slide_index].copy()
        h, w, _ = frame.shape

        ret, webcam_frame = cap.read()
        if not ret:
            break
        webcam_frame = cv2.flip(webcam_frame, 1)

        landmarks = detector.detect_hand_landmarks(webcam_frame)
        if landmarks:
            detector.mp_draw.draw_landmarks(webcam_frame, landmarks, detector.hand_connections)
            finger_states = detector.get_finger_states(landmarks, w, h)
            gesture = detector.classify_gesture(finger_states, landmarks)

            cv2.putText(frame, f'Gesture: {gesture}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print("Detected:", gesture)

            if gesture == "Palm" and stabilizer.can_trigger("Palm"):
                stop_narration()
                current_slide_index = min(current_slide_index + 1, total_slides - 1)
                draw.clear()
            elif gesture == "V Sign" and stabilizer.can_trigger("V Sign"):
                current_slide_index = max(current_slide_index - 1, 0)
                draw.clear()
            elif gesture == "Point":
                pointer.toggle(True)
            else:
                pointer.toggle(False)

            if gesture == "OK Sign" and stabilizer.can_trigger("OK Sign"):
                draw.active = not draw.active
                print("Draw Mode:", "ON" if draw.active else "OFF")

            elif gesture == "Rock" and stabilizer.can_trigger("Rock"):
                draw.clear()
                print("Drawing cleared.")

            elif gesture == "L Sign" and stabilizer.can_trigger("L Sign"):
                print("Narrating current slide...")
                narrate_slide(slides[current_slide_index])

            if draw.active:
                cv2.putText(frame, "Draw Mode: ON", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 50, 50), 2)

            frame = pointer.draw_pointer(frame, landmarks, w, h)
            draw.update(landmarks, w, h)
            frame = draw.draw(frame)

        cv2.imshow(window_title, frame)

        if not window_focused:
            time.sleep(0.5)
            try:
                app = Application(backend="uia").connect(title=window_title)
                window = app.window(title=window_title)
                window.set_focus()
                window_focused = True
            except Exception as e:
                print("⚠️ Could not focus window:", e)
        time.sleep(0.01)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
