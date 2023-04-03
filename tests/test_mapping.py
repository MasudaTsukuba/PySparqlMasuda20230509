import rdflib
from src.MappingClass import Mapping


def test_mapping():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    assert len(mapping.mapping_dict) == 24
    assert mapping.mapping_dict[0]['mappingID'] == 1


def test_graph1():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    results = mapping.mapping_graph.query('select distinct ?p where { ?s ?p ?o .} ')
    assert len(mapping.mapping_graph) == 168
    assert len(results.bindings) == 7
    # assert results.bindings == ''


def test_graph2():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    # results = mapping.mapping_graph.query('select ?s ?o where { ?s <http://example.com/SQL> ?o .} ')
    # results = mapping.mapping_graph.query('select ?s ?o where { ?s <ex:SQL> ?o .} ')
    results = mapping.mapping_graph.query('select ?s ?o where { ?s <http://example.com/predicate> ?o .} ')
    assert len(results.bindings) == 24


def test_graph3():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    results = mapping.mapping_graph.query('select ?p where { ?s ?p <http://example.com/ontology/Museum> .} ')
    assert len(results.bindings) == 1
    assert results.bindings == [{rdflib.term.Variable('p'): rdflib.term.URIRef('http://example.com/object')}]


def test_graph4():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    sparql_query = 'SELECT * WHERE {' + \
                   '?ss <http://example.com/mappingID> ?mapping_id . ' + \
                   '?ss <http://example.com/subject_uri> ?subject_uri . ' + \
                   '?ss <http://example.com/object_uri> ?object_uri . ' + \
                   '?ss <http://example.com/SQL> ?sql . ' + \
                   '?ss <http://example.com/subject> ' + '?s' + '. ' + \
                   '?ss <http://example.com/predicate> ' + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' + '. ' + \
                   '?ss <http://example.com/object> ' + '<http://example.com/ontology/Museum>' + '. }'
    results = mapping.mapping_graph.query(sparql_query)
    assert len(results.bindings) == 1
    assert len(results.bindings[0]) == 6
    sql = results.bindings[0][rdflib.term.Variable('sql')]
    assert sql == rdflib.term.Literal('SELECT museum_id AS Var0 FROM museum;')
    assert str(sql) == 'SELECT museum_id AS Var0 FROM museum;'


def test_graph5():
    mapping = Mapping('data/data_set2/mapping/mapping.json')
    sparql_query = 'SELECT * WHERE {' + \
                   '?ss <http://example.com/mappingID> ?mapping_id . ' + \
                   '?ss <http://example.com/subject_uri> ?subject_uri . ' + \
                   '?ss <http://example.com/object_uri> ?object_uri . ' + \
                   '?ss <http://example.com/subject> ?subject . ' + \
                   '?ss <http://example.com/predicate> ?predicate . ' + \
                   '?ss <http://example.com/object> ?object . ' + \
                   '?ss <http://example.com/SQL> ?sql . ' + \
                   '?ss <http://example.com/subject> ' + '?s' + '. ' + \
                   '?ss <http://example.com/predicate> ' + '<http://www.w3.org/1999/02/22-rdf-syntax-ns#label>' + '. ' + '}'
    results = mapping.mapping_graph.query(sparql_query)
    assert len(results.bindings) == 4
    assert len(results.bindings[0]) == 9
    sql = results.bindings[0][rdflib.term.Variable('sql')]
    assert sql == rdflib.term.Literal('SELECT museum_id AS Var4, name AS Var5 FROM museum;')
    assert str(sql) == 'SELECT museum_id AS Var4, name AS Var5 FROM museum;'
    object_value = results.bindings[0][rdflib.term.Variable('object')]
    assert object_value == rdflib.term.Literal('Var5')
