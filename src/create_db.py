import os
import sqlite3
import csv

working_path = os.getcwd()
if working_path.endswith('src'):
    working_path = os.path.dirname(working_path)
dataset_path = working_path+'/data/data_set2/csv/'
database_path = working_path+'/data/data_set2/db/'


def create_database():
    conn = sqlite3.connect(database_path+'landmark.db')
    conn.commit()
    conn.close()


def create_table():
    conn = sqlite3.connect(database_path+'landmark.db')
    cursor = conn.cursor()
    tables = [
        "build", "b_country", "buildinc",
        "hotel", "h_country", "hotel_place_in",
        "museum", "m_country", "museumincountry",
        "heritage", "w_country", "heritage_placein"]
    for table in tables:
        sql = "DROP TABLE " + table + ";"
        try:
            cursor.execute(sql)
        except:
            print('DROP FAILED: ' + table)
            pass
        # finally:
        #     if cnx:
        #         cnx.close()

    sqls = [
        "CREATE TABLE build (b_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE b_country (bc_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE buildinc (b_id VARCHAR(255), bc_id VARCHAR(255), FOREIGN KEY (b_id) REFERENCES build(b_id), FOREIGN KEY (bc_id) REFERENCES b_country(bc_id));",
        "CREATE TABLE hotel (h_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE h_country (cn_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE hotel_place_in (h_id VARCHAR(255), cn_id VARCHAR(255), FOREIGN KEY (h_id) REFERENCES hotel(h_id), FOREIGN KEY (cn_id) REFERENCES h_country(cn_id));",
        "CREATE TABLE museum (museum_iD VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE m_country (co_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE museumincountry (museum_iD VARCHAR(255), co_id VARCHAR(255), FOREIGN KEY (museum_iD) REFERENCES museum(museum_iD), FOREIGN KEY (co_id) REFERENCES m_country(co_id));",
        "CREATE TABLE heritage (p_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE w_country (c_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), comment VARCHAR(255));",
        "CREATE TABLE heritage_placein (p_id VARCHAR(255), c_id VARCHAR(255), FOREIGN KEY (p_id) REFERENCES heritage(p_id), FOREIGN KEY (c_id) REFERENCES w_country(c_id));"]

    for sql in sqls:
        try:
            cursor.execute(sql)
            print('CREATE TABLE SUCCEEDED: ' + sql)
            pass
        except:
            print('CREATE TABLE FAILED: ' + sql)
            pass
        # finally:
        #     if cnx:
        #         cnx.close()

    cursor.close()
    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect(database_path+'landmark.db')
    cursor = conn.cursor()
    tables = [
        "build", "b_country", "buildinc",
        "hotel", "h_country", "hotel_place_in",
        "museum", "m_country", "museumincountry",
        "heritage", "w_country", "heritage_placein"]

    path_tables = [
        "building/Build", "building/B_country", "building/buildinC",
        "hotel/Hotel", "hotel/H_country", "hotel/Hotel_place_in",
        "museum/museum", "museum/M_country", "museum/museumIncountry",
        "heritage/heritage", "heritage/W_country", "heritage/Heritage_placein"]
    sqls = [
        "INSERT INTO build (b_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO b_country (bc_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO buildinc (b_id, bc_id) VALUES (?, ?)",
        "INSERT INTO hotel (h_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO h_country (cn_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO hotel_place_in (h_id, cn_id) VALUES (?, ?)",
        "INSERT INTO museum (museum_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO m_country (co_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO museumincountry (museum_id, co_id) VALUES (?, ?)",
        "INSERT INTO heritage (p_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO w_country (c_id, name, comment) VALUES (?, ?, ?)",
        "INSERT INTO heritage_placein (p_id, c_id) VALUES (?, ?)"]

    for table, path_table, sql in zip(tables, path_tables, sqls):
        file = dataset_path + path_table + ".csv"
        print(path_table)
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            first = True
            for row in reader:
                if first:
                    first = False
                else:
                    try:
                        # print(row)
                        cursor.execute(sql, row)
                    except:
                        pass
            conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    create_database()
    create_table()
    insert_data()
