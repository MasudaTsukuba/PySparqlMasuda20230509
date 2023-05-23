from src.DatabaseClass import Database


def test_hotel():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT * FROM Hotel;')
    assert len(results) == 822
    assert len(headers) == 3
    results, headers = db.execute('SELECT * FROM H_country;')
    assert len(results) == 187
    assert len(headers) == 3
    results, headers = db.execute('SELECT * FROM Hotel_place_in;')
    assert len(results) == 835
    assert len(headers) == 2


def test_museum():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT * FROM Museum;')
    assert len(results) == 19958
    assert len(headers) == 3


def test_building():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT * FROM Build;')
    assert len(results) == 18556
    assert len(headers) == 3


def test_heritage():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT * FROM heritage;')
    assert len(results) == 5154
    assert len(headers) == 3


def test_join():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT Hotel_place_in.h_id, Hotel_place_in.cn_id FROM Hotel_place_in JOIN H_country ON Hotel_place_in.cn_id = H_country.cn_id JOIN Hotel ON Hotel_place_in.h_id = Hotel.h_id;')
    assert len(results) == 801


def test_natural_join():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT h_id, name, cn_id, country_name FROM Hotel NATURAL JOIN (SELECT h_id, cn_id FROM Hotel_place_in) NATURAL JOIN (SELECT cn_id, name AS country_name FROM H_country);')
    assert len(results) == 801
    assert results[0][0] == '1585008h'
    assert results[0][2] == '30h'
    assert results[0][3] == 'United States of America'


def test_union():
    db = Database('data/data_set2/db/landmark.db')
    results, headers = db.execute('SELECT h_id FROM Hotel UNION SELECT h_id FROM Hotel_place_in;')
    assert len(results) == 822
