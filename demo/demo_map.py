print("load")


class Demo_map():
    #demo load map function
    def load_map(self,block_size,map_size):

        block_w = block_size[0]
        block_h = block_size[1]

        width   = map_size[0]
        height  = map_size[1]

        # fill blocks (2D list of lists)
        blocks = list()
        for x in range(0, width+1, int(block_w)):
            blocks.append(list())
            for y in range(0, height+1, int(block_h)):
                b = Rectangle((x, y), (block_w, block_h))
                blocks[-1].append(b)

        # create a numpy array based on the (slow) python list of lists
        npblocks = np.array(blocks)
        del blocks
        tmp = False
        for row in npblocks:
                        for block in row:
                            if tmp is True:
                                tmp = False
                                block.mark_obstacle()
                            else:
                                tmp = True


        return npblocks
