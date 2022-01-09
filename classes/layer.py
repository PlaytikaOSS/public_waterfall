from classes.node import Node
from classes.consts import GAP, MIN_FRACTION_VITERBI

class Layer:

    def __init__(self, layer_id = None, serial_start = 0, ADNETWORKS_viterbi = None, max_price = 100):

        self.nodes = []
        self.layer_id = layer_id

        for adnetwork in ADNETWORKS_viterbi:
            for price in range(int(max_price) + MIN_FRACTION_VITERBI * (GAP - 1)):
                cur_price = price/GAP if price < MIN_FRACTION_VITERBI * GAP else price - MIN_FRACTION_VITERBI * (GAP - 1)
                node = Node(adnetwork, layer_id, serial_start, cur_price) # init new node
                self.nodes.append(node)
                serial_start += 1 # id of the node

    def get_node_by_id(self, id):
        """return the found node according to id"""

        found_node = None
        for node in self.nodes:
            if node.node_id == id:
                found_node = node
                break
        return found_node