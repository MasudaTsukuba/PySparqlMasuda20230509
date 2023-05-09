import json
import re

import rdflib.term


class Sparql:
    def __init__(self, path, mapping, uri):
        self.sparql_query = None
        self.sql_query = None
        self.variables_list = []
        self.filters_list = []
        self.mapping = mapping
        self.uri = uri
        self.read_query_in_json(path)
        self.get_variables_list()
        self.get_filters_list()
        self.convert_to_sql()
        pass

    def read_query_in_json(self, path):
        with open(path, 'r') as f:
            self.sparql_query = json.load(f)

    def get_variables_list(self):
        temp_list = self.sparql_query['variables']
        for variable in temp_list:
            if variable['termType'] == 'Variable':
                self.variables_list.append(variable['value'])

    def get_filters_list(self):
        where_list = self.sparql_query['where']
        for where_element in where_list:
            if where_element['type'] == 'filter':
                expression = where_element['expression']
                if expression['type'] == 'operation':
                    operator = expression['operator']
                    args = expression['args']
                    temp_args = []
                    for arg in args:
                        arg_value = arg['value']
                        if arg['termType'] == 'Variable':
                            temp_args.append(arg_value)
                        if arg['termType'] == 'NamedNode':  # 2023/5/8
                            temp_args.append(f'"{arg_value}"')  # 2023/5/8
                        if arg['termType'] == 'Literal':
                            temp_args.append(f'"{arg_value}"')
                    self.filters_list.append(
                        [temp_args[0], temp_args[0] + operator + temp_args[1]])  # [var_name, expression]

    def convert_to_sql(self):
        def triple_to_sql(triple_json, filter_list):
            var_list_string_local = ''
            var_list = []
            temp_subject = triple_json['subject']
            value_subject = temp_subject['value']
            var_subject = '?dummy_subject'
            if temp_subject['termType'] == 'Variable':
                var_list.append(value_subject)
                value_subject = '?' + value_subject
                var_subject = value_subject
                var_list_string_local += value_subject
            else:
                value_subject = '<' + value_subject + '>'
            temp_predicate = triple_json['predicate']
            value_predicate = temp_predicate['value']
            var_predicate = '?dummy_predicate'
            if temp_predicate['termType'] == 'Variable':
                var_list.append(value_predicate)
                value_predicate = '?' + value_predicate
                var_predicate = value_predicate
                var_list_string_local += value_predicate
            else:
                value_predicate = '<' + value_predicate + '>'
                var_predicate = value_predicate
            temp_object = triple_json['object']
            value_object = temp_object['value']
            var_object = '?dummy_object'
            if temp_object['termType'] == 'Variable':
                var_list.append(temp_object['value'])
                value_object = '?' + temp_object['value']
                var_object = value_object
                var_list_string_local += value_object
            elif temp_object['termType'] == 'Literal':
                value_object = '"' + value_object + '"'
                var_object = value_object
            else:
                value_object = '<' + value_object + '>'
                var_object = value_object
            # sparql_query = 'SELECT ' + var_list + ' ?mapping_id WHERE {' + \
            sparql_query = 'SELECT * WHERE {' + \
                '?ss <http://example.com/mappingID> ?mapping_id . ' + \
                '?ss <http://example.com/subject_uri> ?subject_uri . ' + \
                '?ss <http://example.com/object_uri> ?object_uri . ' + \
                '?ss <http://example.com/subject> ?subject . ' + \
                '?ss <http://example.com/predicate> ?predicate . ' + \
                '?ss <http://example.com/object> ?object . ' + \
                '?ss <http://example.com/SQL> ?sql . ' + \
                '?ss <http://example.com/subject> ' + var_subject + '. ' + \
                '?ss <http://example.com/predicate> ' + var_predicate + '. ' + \
                '?ss <http://example.com/object> ' + var_object + '. }'
            results = self.mapping.mapping_graph.query(sparql_query)  # find applicable mappings
            sql_string_union = ''  # sql_strings connected by 'UNION'
            if len(results.bindings) > 0:  # if applicable mapping is found
                for binding in results.bindings:  # try for each mapping
                    sql_string = str(binding[rdflib.term.Variable('sql')])  # get sql statement
                    sql_string = re.sub(';$', '', sql_string)  # remove last ';'
                    sql_append = []
                    subject_uri = binding[rdflib.term.Variable('subject_uri')]
                    if value_subject.find('?') < 0 and subject_uri != rdflib.term.Literal('plain') and subject_uri != rdflib.term.Literal('-'):
                        subject_symbol = binding[rdflib.term.Variable('subject')]
                        try:
                            subject_value = self.uri.inv_dict_all[value_subject.replace('<', '').replace('>', '')]
                            sql_append.append(f'{str(subject_symbol)}="{subject_value}"')
                        except KeyError:
                            pass
                        pass
                    object_uri = binding[rdflib.term.Variable('object_uri')]
                    if value_object.find('?') < 0 and object_uri != rdflib.term.Literal('plain') and object_uri != rdflib.term.Literal('-'):
                        object_symbol = binding[rdflib.term.Variable('object')]
                        object_value = self.uri.inv_dict_all[value_object.replace('<', '').replace('>', '')]
                        sql_append.append(f'{str(object_symbol)}="{object_value}"')
                        pass
                    for filter_element in filter_list:
                        filter_var = filter_element[0]
                        found = False
                        for var0 in var_list:
                            if var0 == filter_var:
                                sql_append.append(filter_element[1])
                    if sql_append:
                        sql_string += ' WHERE '
                        for element in sql_append:
                            sql_string += element + ' AND '
                        sql_string = re.sub(' AND $', '', sql_string)
                    for var in var_list:  # var is s, name, cname, etc
                        var_symbol = str(binding[rdflib.term.Variable(var)])  # var_symbol is VAR0, etc
                        sql_string = re.sub(var_symbol, var, sql_string)  # replace variable

                    pass
                    sql_string_union += sql_string + ' UNION '  # connect with 'UNION'
                sql_string_union = re.sub(' UNION $', '', sql_string_union)  # remove last 'UNION'

            return sql_string_union

        var_list_string = ''
        for var in self.sparql_query['variables']:
            var_list_string += var['value'] + ', '
        var_list_string = re.sub(', $', '', var_list_string)
        where_list = self.sparql_query['where']
        sql_natural_join = ''
        for where_element in where_list:
            if where_element['type'] == 'bgp':
                triples = where_element['triples']
                for triple in triples:
                    sql = triple_to_sql(triple, self.filters_list)
                    sql_natural_join += '(' + sql + ') NATURAL JOIN '
        self.sql_query = f'SELECT {var_list_string} FROM ' + re.sub(' NATURAL JOIN $', '', sql_natural_join) + ';'
        aaa = self.sql_query
        pass
