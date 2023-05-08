from src.DatabaseClass import Database
from src.MappingClass import Mapping
from src.UriClass import Uri
from src.SparqlClass import Sparql
from src.OutputClass import Output
import subprocess

path = '/home/masuda/PycharmProjects/PySparqlMasuda20230501/'
# path = '/home/masuda/PycharmProjects/PySparqlQuery20230508/'


def query2json(input_file):
    json_file = input_file.replace('.txt', '.json')
    working_dir = '/home/masuda/PycharmProjects/PySparqlMasuda20230501/'
    command = working_dir + 'action_folder/node_modules/sparqljs/bin/sparql-to-json'
    cp = subprocess.run([command, '--strict', path + input_file],
                        capture_output=True, text=True)  # , '>', 'query_parse.json'])  # クエリをjson形式に構造化
    if cp.returncode != 0:
        print('Error: sparql-to-json: ', cp.stderr)
        return -1
    with open(working_dir+json_file, mode='w') as f:
        f.write(cp.stdout)
    return working_dir+json_file


def execute_query(query):
    db = Database('/home/masuda/PycharmProjects/PySparqlMasuda20230501/data/data_set2/db/data2.db')
    mapping = Mapping('/home/masuda/PycharmProjects/PySparqlMasuda20230501/data/data_set2/mapping/mapping.json')
    uri = Uri('/home/masuda/PycharmProjects/PySparqlMasuda20230501/data/data_set2/uri/')
    sparql = Sparql(query2json(query), mapping, uri)
    exe_query = sparql.sql_query
    sql_results, headers = db.execute(exe_query)
    sparql_results = uri.sql_to_rdf(sql_results)
    Output.save_file(path+query.replace('query/', 'output/').replace('.json', '.csv'), sparql_results, headers)
    print(len(sql_results))
    pass
    return sparql_results


if __name__ == "__main__":
    # execute_query('query/q1.json')
    execute_query('query/q1.txt')
    # execute_query('query/q2.json')
    # execute_query('query/q3a.json')
    # execute_query('query/q3b.json')
    # execute_query('query/q4.json')
    # execute_query('query/q5.json')
    # execute_query('query/q6.json')
    # execute_query('../query/q7.json')
    # execute('query/q7.json')
