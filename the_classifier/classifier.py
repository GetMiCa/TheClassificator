from treelib import Node, Tree
import hashlib
import datetime


class Classifier(object):
    def __init__(self):
        self.config = [("bathrooms", ["<0", "<2", ">1"]),
                       ("surface", ["<0", ">90", "<=90"]),
                       ("floor", [">=2", "<=1"])]
        self.house_features_tree = Tree()
        self.house_features_tree.create_node("Milan", "milan")

    def process(self, data):
        added = {}
        for appartment in data:
            if appartment["zone"] not in added:
                self.house_features_tree.create_node(appartment["zone"],
                                                     appartment["zone"],
                                                     parent="milan")
                added[appartment["zone"]] = {}
            added[appartment["zone"]] = self.initial_structure(
                appartment, appartment["zone"], 0, added[appartment["zone"]])
        #print(self.house_features_tree.show())
        return added

    def initial_structure(self, data, parent, config_index, added):
        if config_index >= len(self.config):
            if added == {}:
                self.house_features_tree.create_node(f"{parent}_number_1",
                                                     f"{parent}_number_1",
                                                     parent=parent)
                return (int(data["price"]),[data], 1)
            else:
                (average, apps, new) = added
                self.house_features_tree.remove_node(f"{parent}_number_{new}")
                self.house_features_tree.create_node(
                    f"{parent}_number_{new+1}",
                    f"{parent}_number_{new+1}",
                    parent=parent)
                apps.append(data)
                return (self.calculate_average(apps), apps, new + 1)
        else:
            (name, values) = self.config[config_index]
            for index, possibilities in enumerate(values):
                #print(data[name], name)
                if eval(data[name].strip() + possibilities):
                    node_name = f"{parent}_{name}_{index}"
                    if node_name not in added:
                        self.house_features_tree.create_node(node_name,
                                                             node_name,
                                                             parent=parent)
                        added[node_name] = {}
                    added[node_name] = self.initial_structure(
                        data, node_name, config_index + 1, added[node_name])
                    return added
            print("Error")

    def calculate_average(self, data):
        prices = [int(app["price"]) for app in data]
        return sum(prices)/len(data)
