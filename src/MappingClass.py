import json
from rdflib import Graph


class Mapping:
    def __init__(self, path):
        # mapping_uri = path  # 'data/data_set2/mapping/mapping.json'
        # マッピングデータの取り込み
        # with open(path, 'r') as json_open_file:
        #     self.mapping_dict = json.load(json_open_file)
        # json_open_file.close()
        self.mapping_graph = Graph()
        self.mapping_graph.parse(path)  # ('data/data_set2/mapping/mapping_ld2.json')
        # self.mapping_graph.serialize('xxx.ttl', format='turtle')  # debug
