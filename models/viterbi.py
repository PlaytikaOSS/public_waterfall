import pandas as pd
import copy as cp
import math
import logging

from classes.layer import Layer
from classes.waterfall import Waterfall


def get_next_price(layers, i, node, parent_node):
    """Returning the price of the instance before the given node from the same ad-network"""

    price = None
    while i >= 0:
        if node.adnetwork_name == parent_node.adnetwork_name:
            price = parent_node.price
            break
        else:
            parent_node = layers[i-1].get_node_by_id(parent_node.best_parent_id) if layers[i-1].get_node_by_id(parent_node.best_parent_id) is not None else parent_node
            i -= 1
    return price

def find_max_capacity(ad_units, val):
    """calculate the MAX_CAPACITY_VITERBI"""

    MAX_CAPACITY_VITERBI = {"AdNetwork1": val,
                     "AdNetwork2": val,
                     "AdNetwork3": val,
                     "AdNetwork4": val,
                     "AdNetwork5": val,
                     "AdNetwork6": val,
                     "AdNetwork7": val,
                     "AdNetwork8": val,
                     "AdNetwork9": val,
                     "AdNetwork10": val}
    for i in ad_units:
        MAX_CAPACITY_VITERBI[i.adnetwork_name] += 1

    return MAX_CAPACITY_VITERBI

def check_capacity(layers, i, node, parent_node, MAX_CAPACITY_VITERBI):
    """check that adding node will not violate the MAX_CAPACITY_VITERBI property"""

    if i > 3:
        CURR_CAPACITY = {"AdNetwork1": 0,
                      "AdNetwork2": 0,
                      "AdNetwork3": 0,
                      "AdNetwork4": 0,
                      "AdNetwork5": 0,
                      "AdNetwork6": 0,
                      "AdNetwork7": 0,
                      "AdNetwork8": 0,
                      "AdNetwork9": 0,
                      "AdNetwork10": 0}
        CURR_CAPACITY[node.adnetwork_name] += 1
        while parent_node:
            CURR_CAPACITY[parent_node.adnetwork_name] += 1
            parent_node = layers[i-1].get_node_by_id(parent_node.best_parent_id)
            i -= 1
        for adnetwork_name in CURR_CAPACITY:
            if CURR_CAPACITY[adnetwork_name] > MAX_CAPACITY_VITERBI[adnetwork_name]:
                return False
    return True

def recover_path(layers, node):
    """convert the network to waterfall"""

    order = node.layer_id + 1
    waterfall_list = ['High,' + str(order) + ',' + node.adnetwork_name + ' Oct $' + str(node.price) + ',0,' + str(node.impressions) + ',0,' + str(node.impressions * node.price / 1000) + ',0,' + str(node.layer_id) + '_' + str(node.node_id)]
    node = cp.deepcopy(layers[node.layer_id - 1].get_node_by_id(node.best_parent_id))
    while node:
        order -= 1
        waterfall_list.append('High,' + str(order) + ',' + node.adnetwork_name + ' Oct $' + str(node.price) + ',0,' + str(node.impressions) + ',0,' + str(node.impressions * node.price / 1000) + ',0,' + str(node.layer_id) + '_' + str(node.node_id))
        node = cp.deepcopy(layers[node.layer_id - 1].get_node_by_id(node.best_parent_id))
    return pd.DataFrame(data=[sub.split(",") for sub in waterfall_list[::-1]] ,columns=['Section', 'Order', 'Ad unit', 'RPM', 'Impressions', 'Network fill rate', 'Revenue', 'Network RFM', 'Ad unit id'])

def viterbi_opt(csv_path_data, path_log, csv_path_waterfall, min_imp, capacity):

    logging.basicConfig(filename=path_log, filemode = 'a', level=logging.INFO)
    logging.info("running Viterbi optimization")

    data = pd.read_csv(csv_path_data)
    MAX_CAPACITY_VITERBI = find_max_capacity(Waterfall(csv_path=csv_path_waterfall).ad_units, capacity)
    layers = []
    serial_start = 0
    cnt = 0
    for i in list(data.columns):
        if i in MAX_CAPACITY_VITERBI: cnt += MAX_CAPACITY_VITERBI[i]
    for i in range(cnt):    # for each layer
        layers.append(Layer(layer_id=i, serial_start=serial_start, ADNETWORKS_viterbi=list(data.columns)[1:], max_price=data.loc[0,'price']))
        if i == 0: # first layer
            for node in layers[i].nodes:
                revenue = node.calculate_revenue(data)
                node.set_best_revenue(revenue)
                node.set_best_parent_id(None)
                node.impressions = node.count_impressions(data)
        else: # other layers
            sm = 0
            for node in layers[i].nodes: # for each node (ad_unit instance)
                revenue = 0
                for parent_node in layers[i-1].nodes:
                    # add all potential parent paths (nodes from previous layer)
                    above_price = get_next_price(layers, i, node, parent_node)
                    above_price_copy = math.inf if above_price is None else above_price
                    if parent_node.adnetwork_name != node.adnetwork_name and parent_node.price >= node.price and above_price_copy > node.price and check_capacity(layers, i-1, node, parent_node, MAX_CAPACITY_VITERBI) and node.count_impressions(data, above_price) > min_imp:
                        node.add_parent(parent_node.node_id, parent_node.best_revenue)
                        curr_revenue = node.calculate_revenue(data, above_price, parent_node)
                        if curr_revenue > revenue:
                            revenue = curr_revenue
                            best_parent_id = parent_node.node_id
                            node.impressions = node.count_impressions(data, above_price)
                        sm += 1
                node.set_best_revenue(revenue)
                if 'best_parent_id' in locals(): node.set_best_parent_id(best_parent_id)
            logging.info(f"layer: {i} sum_parents: {sm}")
        serial_start += len(layers[i].nodes)

    # print the optimal waterfall
    best_revenue = 0
    for layer in layers:
        for node in layer.nodes:
            if node.best_revenue >= best_revenue:
                best_revenue = node.best_revenue
                best_node = cp.deepcopy(node)
    finalwaterfall = recover_path(layers, best_node)
    return finalwaterfall, layers