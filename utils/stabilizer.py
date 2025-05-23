import time

class GestureStabilizer:
    def __init__(self, cooldown=1.5):
        self.last_triggered = {}
        self.cooldown = cooldown  # in seconds

    def can_trigger(self, gesture):
        current_time = time.time()
        last_time = self.last_triggered.get(gesture, 0)

        if current_time - last_time > self.cooldown:
            self.last_triggered[gesture] = current_time
            return True
        return False
