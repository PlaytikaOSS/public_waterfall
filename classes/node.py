class Node:
    """Node is in fact an ad_unit in the Viterbi algorithm"""

    def __init__(self, adnetwork_name, layer_id, serial_id, price = 0, best_revenue = 0):

        self.adnetwork_name = adnetwork_name
        self.layer_id = layer_id
        self.node_id = serial_id
        self.price = price
        self.best_revenue = best_revenue
        self.impressions = 0
        self.best_parent_id = None
        self.parents = dict()

    def add_parent(self, node_id, best_revenue):
        self.parents[node_id] = best_revenue

    def set_best_revenue(self, best_revenue):
        self.best_revenue = best_revenue

    def set_best_parent_id(self, best_parent_id):
        self.best_parent_id = best_parent_id

    def calculate_revenue(self, data, above_price = None, parent_node = None):
        """This function calculate the best revenue of the best path until the current node"""

        index = data.query('price == @self.price').index.tolist()[0] # there is a sinlt index for each price in data
        if above_price is None and parent_node is None:
            # if this is the first layer then there are no parents
            return sum(data.loc[:index, self.adnetwork_name]) * self.price / 1000
        else:
            # the revenue is a combination of the curr_revenue and the parent revenue
            if above_price is not None: # above price is the price of the ad_unit that is above the current node and belong to the same adNetwork
                above_index = data.query('price == @above_price').index.tolist()[0] + 1 # this function assumes that data is order by price N:1 without gaps!!
            else:
                above_index = 0
            parent_revenue = parent_node.best_revenue # revenue of the best path so far
            node_revenue = sum(data.loc[above_index:index, self.adnetwork_name]) * self.price / 1000
            return parent_revenue + node_revenue

    def count_impressions(self, data, above_price = None):
        """This function counts the number of impressions that would be bought by the node according to data"""

        # this function assumes that data is order by price N:1 without gaps!!
        index = data.query('price == @self.price').index.tolist()[0] # there is a sinlt index for each price in data
        if above_price is not None: # above price is the price of the ad_unit that is above the current node and belong to the same adNetwork
            above_index = data.query('price == @above_price').index.tolist()[0] + 1
        else:
            above_index = 0
        return sum(data.loc[above_index:index, self.adnetwork_name])