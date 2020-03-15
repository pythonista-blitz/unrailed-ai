import cv2
import numpy as np
import pyautogui
from threading import Thread
import time
import win32gui

class WindowCapture:
    def __init__(self, window_name, capture_rate):
        self.window_name = window_name
        self._thread_name = window_name + " Capture"

        self.wait_time = 1/capture_rate

        self.frame = self.screenshot()
        self.should_stop = False

    def start(self):
        self._thread = Thread(target=self.update, name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()
        return self

    def update(self):
        while True:
            start = time.time()

            self.frame = self.screenshot()

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    def read(self):
        return self.frame

    def stop(self):
        self.should_stop = True
        self._thread().join()

    def screenshot(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise Exception("Window not found!")

        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        return cv2.cvtColor(
            np.asarray(pyautogui.screenshot(region=(
                *win32gui.ClientToScreen(hwnd, (x, y)),
                *win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            ))),
            cv2.COLOR_RGB2BGR
        )