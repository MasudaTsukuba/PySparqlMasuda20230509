import os
import pandas as pd


class Uri:
    def __init__(self, path):
        self.uri_dict = {}
        self.inv_dict = {}
        self.uri_dict_all = {}
        self.inv_dict_all = {}
        for file in os.listdir(path):
            if file.endswith(".csv"):
                df = pd.read_csv(path+file, header=None)
                key = file.replace('.csv', '')
                self.uri_dict[key] = dict(zip(df[0], df[1]))
                self.inv_dict[key] = dict(zip(df[1], df[0]))
                self.uri_dict_all.update(dict(zip(df[0], df[1])))
                self.inv_dict_all.update(dict(zip(df[1], df[0])))
        pass

    # def read_dict(self):
    #     path = 'data/data_set2/uri'
    #     pass

    def sql_to_rdf(self, sql_results):
        sparql_results = []
        for result in sql_results:
            result_new = []
            for element in result:
                try:
                    rdf_value = self.uri_dict_all[element]
                    result_new.append(rdf_value)
                except KeyError:
                    result_new.append(element)
            pass
            sparql_results.append(result_new)
        pass
        return sparql_results
