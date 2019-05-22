## @package main

from time import sleep
from sys import platform
import signal
import threading
import queue
from client.comm import Comm
from module.module import NavigationModule

SHOULD_STOP = False

# This function reads keyboard input from a queue.
# https://stackoverflow.com/questions/5404068/how-to-read-keyboard-input/53344690#53344690
def read_kbd_input(input_queue):
    while True:
        input_str = input()
        input_queue.put(input_str)

# This function acts as a symbolic main since Python doesn't actually utilize it
#  in the same way C does.
def main():
    input_queue = queue.Queue()
    input_thread = threading.Thread(
        target=read_kbd_input, args=(input_queue,), daemon=True)
    input_thread.start()

    print("Starting application...\n")
    nav = NavigationModule(Comm())
    print("Module created...")

    while not should_stop:
        if (input_queue.qsize() > 0):
            input_str = input_queue.get()
            print("input was: {} ".format(input_str))
            if input_str == "send":
                nav.send_test_frames()

        nav.process()
        sleep(0.05)

    nav.stop()

# This function stops processing CAN bus data
# @param signal not sure why this is here
# @param frame also not sure why this is here, might be added to the Python build later
# to exit when it receives a certain frame.
def stop(signal, frame):
    global should_stop
    should_stop = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
