from src.UriClass import Uri


def test_uri():
    uri = Uri('data/data_set2/uri/')
    assert len(uri.uri_dict) == 8
    assert len(uri.inv_dict) == 8
    assert len(uri.uri_dict['PREFIX_hotel']) == 822
    assert len(uri.inv_dict['PREFIX_hotel']) == 822
