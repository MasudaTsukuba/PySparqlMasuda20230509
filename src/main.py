from src.DatabaseClass import Database
from src.MappingClass import Mapping
from src.UriClass import Uri
from src.SparqlClass import Sparql
from src.OutputClass import Output


def execute(query):
    db = Database('data/data_set2/db/data2.db')
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    uri = Uri('data/data_set2/uri/')
    sparql = Sparql(query, mapping, uri)
    exe_query = sparql.sql_query
    sql_results, headers = db.execute(exe_query)
    sparql_results = uri.sql_to_rdf(sql_results)
    Output.save_file(query.replace('query/', 'output/').replace('.json', '.csv'), sparql_results, headers)
    pass


if __name__ == "__main__":
    # execute('query/q1.json')
    # execute('query/q2.json')
    execute('query/q3a.json')
    execute('query/q3b.json')
    execute('query/q4.json')
    execute('query/q5.json')
    execute('query/q6.json')
    execute('query/q7.json')
    # execute('query/q7.json')
