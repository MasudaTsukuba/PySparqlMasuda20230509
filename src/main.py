from src.DatabaseClass import Database
from src.MappingClass import Mapping
from src.UriClass import Uri
from src.SparqlClass import Sparql
from src.OutputClass import Output
import subprocess
import os

working_dir = os.getcwd()
if working_dir.endswith('src'):
    working_dir = os.path.dirname(working_dir)
# '/home/masuda/PycharmProjects/PySparqlMasuda20230509/'
common_query_path = os.path.dirname(working_dir)+'/PySparqlQuery20230508/query/'


def query2json(input_file):
    json_file = input_file.replace('.txt', '.json')
    command = working_dir + '/action_folder/node_modules/sparqljs/bin/sparql-to-json'
    cp = subprocess.run([command, '--strict', common_query_path + input_file],
                        capture_output=True, text=True)  # , '>', 'query_parse.json'])  # クエリをjson形式に構造化
    if cp.returncode != 0:
        print('Error: sparql-to-json: ', cp.stderr)
        return -1
    json_file_path = working_dir+'/query/'+json_file
    with open(json_file_path, mode='w') as f:
        f.write(cp.stdout)
    return json_file_path


def execute_query(sparql_query):
    db = Database(working_dir+'/data/data_set2/db/landmark.db')
    mapping = Mapping(working_dir+'/data/data_set2/mapping/mapping_ld2.json')  # working_dir+'/data/data_set2/mapping/mapping2.json')
    uri = Uri(working_dir+'/data/data_set2/uri/')
    sparql_query_json_path = query2json(sparql_query)
    sparql = Sparql(sparql_query_json_path, mapping, uri)
    exe_query = sparql.sql_query
    print(exe_query)
    sql_results, headers = db.execute(exe_query)
    sparql_results = uri.sql_to_rdf(sql_results)
    Output.save_file(working_dir+'/output/'+sparql_query.replace('.json', '.csv'), sparql_results, headers)
    print(len(sql_results))
    pass
    return sparql_results


if __name__ == "__main__":
    query = 'q1.txt'
    # query = 'q2.txt'
    # execute_query('q3a.json')
    # execute_query('q3b.json')
    # execute_query('q4.json')
    query = 'q5.txt'
    # execute_query('q6.json')
    # query = 'q7.txt'
    query = 'q1pred_hotel.txt'
    # query = 'q1pred_build.txt'
    query = 'q1pred_get_hotel.txt'
    # query = 'query_type_object_hotel20230518.txt'
    execute_query(query)
