from src.DatabaseClass import Database
from src.MappingClass import Mapping
from src.UriClass import Uri
from src.SparqlClass import Sparql
from src.OutputClass import Output
import subprocess

common_query_path = '/home/masuda/PycharmProjects/PySparqlQuery20230508/'
working_dir = '/home/masuda/PycharmProjects/PySparqlMasuda20230509/'


def query2json(input_file):
    json_file = input_file.replace('.txt', '.json')
    command = working_dir + 'action_folder/node_modules/sparqljs/bin/sparql-to-json'
    cp = subprocess.run([command, '--strict', common_query_path + input_file],
                        capture_output=True, text=True)  # , '>', 'query_parse.json'])  # クエリをjson形式に構造化
    if cp.returncode != 0:
        print('Error: sparql-to-json: ', cp.stderr)
        return -1
    with open(working_dir+json_file, mode='w') as f:
        f.write(cp.stdout)
    return working_dir+json_file


def execute_query(query):
    db = Database(working_dir+'data/data_set2/db/data2.db')
    mapping = Mapping(working_dir+'data/data_set2/mapping/mapping2.json')
    uri = Uri(working_dir+'data/data_set2/uri/')
    sparql = Sparql(query2json(query), mapping, uri)
    exe_query = sparql.sql_query
    print(exe_query)
    sql_results, headers = db.execute(exe_query)
    sparql_results = uri.sql_to_rdf(sql_results)
    Output.save_file(working_dir+query.replace('query/', 'output/').replace('.json', '.csv'), sparql_results, headers)
    print(len(sql_results))
    pass
    return sparql_results


if __name__ == "__main__":
    # execute_query('query/q1.json')
    # execute_query('query/q1.txt')
    # execute_query('query/q2.json')
    # execute_query('query/q3a.json')
    # execute_query('query/q3b.json')
    # execute_query('query/q4.json')
    # execute_query('query/q5.txt')
    # execute_query('query/q6.json')
    # execute_query('../query/q7.json')
    # execute('query/q7.json')
    # query = 'query/q1pred_hotel.txt'
    query = 'query/query_type_object_hotel20230518.txt'
    execute_query(query)
