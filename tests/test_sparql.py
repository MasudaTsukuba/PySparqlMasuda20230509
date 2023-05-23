from src.SparqlClass import Sparql
from src.MappingClass import Mapping
from src.UriClass import Uri


# def test_q1():
#     mapping = Mapping('data/data_set2/mapping/mapping.json')
#     uri = Uri('data/data_set2/uri/')
#     sparql = Sparql('query/q1.json', mapping, uri)
#     assert sparql.sparql_query['queryType'] == 'SELECT'
#     assert sparql.sparql_query['type'] == 'query'
#
#
# def test_q2():
#     mapping = Mapping('data/data_set2/mapping/mapping.json')
#     uri = Uri('data/data_set2/uri/')
#     sparql = Sparql('query/q2.json', mapping, uri)
#     assert sparql.sparql_query['queryType'] == 'SELECT'
#     assert sparql.sparql_query['type'] == 'query'
#     assert len(sparql.sparql_query['variables']) == 3
#     assert len(sparql.variables_list) == 3
#     assert len(sparql.sparql_query['where'][0]['triples']) == 4
#     assert sparql.filters_list == [['cname', 'cname="United Kingdom"']]
