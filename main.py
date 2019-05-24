from time import sleep
from sys import platform
import signal
import threading
import queue
from client.comm import Comm
from module.mod import NavigationModule

SHOULD_STOP = False


def read_kbd_input(input_queue):
    """
    This function reads keyboard input from a queue.
    https://stackoverflow.com/questions/5404068/how-to-read-keyboard-input/53344690#53344690

    :param input_queue: python queue that holds the characters put in
    """
    while True:
        input_str = input()
        input_queue.put(input_str)


def main():
    """
    This function acts as a symbolic main since Python doesn't actually utilize it
    in the same way C does. 
    """
    global SHOULD_STOP
    input_queue = queue.Queue()
    input_thread = threading.Thread(
        target=read_kbd_input, args=(input_queue,), daemon=True)
    input_thread.start()

    print("Starting application...\n")
    nav = NavigationModule(Comm())
    print("Module created...")

    while not SHOULD_STOP:
        # did this so i can exit cleanly,
        # for some reason i can't ctrl c out of this python application.
        if (input_queue.qsize() > 0):
            input_str = input_queue.get()
            if input_str == "exit":
                SHOULD_STOP = True

        nav.process()
        if nav.requested:
            nav.process_request()
        sleep(0.05)

    nav.stop()


def stop(signal, frame):
    """ This function stops processing CAN bus data
    :param signal: not used
    :param frame: not used """
    global SHOULD_STOP
    SHOULD_STOP = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()
