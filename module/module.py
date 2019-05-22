## @package mod

from client.comm import BaseComm
from common.frame_enum import FrameType
from common.frames import FramePathStep

from .Algorithms import AStar
from .Structure import Grid
from .Structure import grid_factory

#TODO: documentation
# TODO: Unit tests


## this class is based on the module template and implements the 3 template functions
#  and additional functions that are needed.
class NavigationModule:
    ## The constructor
    # @param comm variable that serves as an interface to the CAN bus
    def __init__(self, comm: BaseComm):
        self.comm = comm
        self.comm.listen_for([FrameType.PATH_STEP])
        self.path_id = 0

    ## This function is what gets and puts data from/on the CAN bus
    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            values = frame.get_data()
            print("received: x is {} y is {} step_id is {} path id is {}".format(
                values[0], values[1], values[2], values[3]))

    ## This function is called when we stop the application
    def stop(self):
        self.comm.stop()

    ## This function converts a path (list of coordinates) to a list of "frames".
    # @return returns a list of frames that acts as a path.
    def generate_frame_path(self, path):
        frame_path = list()
        step_id = 0

        for coord in path:
            frame = FramePathStep()
            frame.set_data(coord[0], coord[1], step_id, self.path_id)
            step_id += 1
            frame_path.append(frame)

        self.path_id += 1
        return frame_path

    ## This function sends a bunch of path step frames over the CAN bus
    # mainly used to test for now, this will cleaned up once we have all the endpoints connected
    # TODO: clean up
    def send_test_frames(self):
        g = grid_factory(10, 10)
        start = g[(0, 0)]
        end = g[(5, 2)]
        a_star = AStar(g, start, end)
        print(a_star.solve())
        frame_path = self.generate_frame_path(a_star.solve())
        for frame in frame_path:
            self.comm.send(frame)
            data = frame.get_data()
            print("sending: x is {} y is {} step_id is {} path_id is {}".format(data[0], data[1], data[2], data[3]))