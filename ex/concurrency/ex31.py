import sys
from pynput import keyboard
import time

def on_activate():
    print('Global hotkey activated!')

def for_canonical(f):
    return lambda k: f(listener.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<ctrl>+<alt>+h'),
    on_activate)
# with keyboard.Listener(
#         on_press=for_canonical(hotkey.press),
#         on_release=for_canonical(hotkey.release)) as l:
#     l.join()
listener = keyboard.Listener(
    on_press=for_canonical(hotkey.press),
    on_release=for_canonical(hotkey.release))
listener.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n")
    sys.exit()
