from client.comm import BaseComm
from common.frame_enum import FrameType
from .Algorithms import AStar
from .Grid import Grid

# TODO: make a pull request for this frame type

class move_instruction_c:
    def __init__(self, path_id=0, id=0, x=0, y=0):
        self.path_id = path_id
        self.instruction_id = id
        self.x = x
        self.y = y

#TODO: documentation
#TODO: Unit tests

class Module:
    def __init__(self, comm: BaseComm):
        self.path_id = 0
        self.comm = comm
        # we'll need to figure out what frames to listen for
        # self.comm.listen_for([FrameType.ACTIVITY_LED_STATE])

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            values = frame.get_data()

            if values[0]:
                print("The LED is ON")
            else:
                print("The LED is OFF")

    def stop(self):
        self.comm.stop()

    def get_instruction_path(self, path, path_id):
        instruction_path = list()
        self.path_id += 1
        instruction_id = 0

        for coord in path:
            instruction = move_instruction_c(
                path_id, instruction_id, coord[0], coord[1])
            instruction_id += 1
            instruction_path.append(instruction)
        return instruction_path