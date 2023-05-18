from src.DatabaseClass import Database
from src.MappingClass import Mapping
from src.UriClass import Uri
from src.main import execute_query


def test_main():
    # execute_query('query/q2.json')
    execute_query('query/q2.txt')
