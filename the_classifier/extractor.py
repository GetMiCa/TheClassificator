import csv


class Extractor(object):
    def __init__(self, path):
        self.path = path
        self.config = [("bathrooms", ["<0", "<2", ">1"]),
                       ("surface", ["<0", ">90", "<=90"]),
                       ("floor", [">=2", "<=1"])]
        self.cluster_elements = path + "_clusters_elements.csv"
        self.great_deals = path + "_great_deals.csv"

        with open(self.great_deals, "w", newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Cluster", "Price", "Url"])

        with open(self.cluster_elements, "w", newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Cluster"] + [configName.capitalize() for (configName, values) in self.config] + ["Price"])

    def extract_clusters(self, data):
        with open(self.path + "_clusters.csv", "w", newline='') as output:
            writer = csv.writer(output,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Name", "Average", "Elements"])
            for (zone, subclusters) in data.items():
                self.get_leafs(subclusters, writer, f"{zone}_")

    def get_leafs(self, clusters, writer, root):
        if type(clusters) is tuple:
            (average, elements, num) = clusters
            writer.writerow([root, average, num])
            self.extract_elements(root, elements)
            self.extract_great_deals(root, average, elements)
        else:
            for (index, key) in enumerate(clusters):
                self.get_leafs(clusters[key], writer, root + str(index))

    def extract_elements(self, cluster, elements):
        with open(self.cluster_elements, "a",
                  newline='') as output:
            writer = csv.writer(output)
            for el in elements:
                writer.writerow([cluster] + [
                    str(el[configName])
                    for (configName, configValue) in self.config
                ]+ [el["price"]])

    def extract_great_deals(self, cluster, average, elements):
        with open(self.great_deals, "a", newline='') as output:
            writer = csv.writer(output)
            for el in elements:
                if float(el["price"]) <= average:
                    writer.writerow([cluster, el["price"], el["url"]])
