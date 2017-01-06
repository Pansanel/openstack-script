#!/usr/bin/python

import MySQLdb

db_list = ['neutron', 'keystone', 'glance', 'cinder', 'nova']
db_hostname = "localhost"
db_username = "root"
db_password = "changeme"

""" Convert MariaDB tables to use utf8
"""


def convert_tables(db_hostname, db_username, db_password, database):
    db = MySQLdb.connect(host=db_hostname, user=db_username,
                         passwd=db_password, db=database)
    cursor = db.cursor()
    query = "ALTER DATABASE %s CHARACTER SET = 'utf8'" % database
    print(i"Executing %s" % query)
    cursor.execute(query)
    query = "ALTER DATABASE %s COLLATE = 'utf8_general_ci'" % database
    print("Executing %s" % query)
    cursor.execute(query)
    cursor.execute("SHOW tables")
    output = cursor.fetchall()
    if output:
        print("Disable foreign keys checks")
        cursor.execute("SET foreign_key_checks = 0")
        for row in output:
            query = "ALTER TABLE %s.%s CONVERT TO " % (database, row[0]) + \
                    "CHARACTER SET 'utf8', COLLATE 'utf8_general_ci'"
            print("Executing %s" % query)
            cursor.execute(query)
        print("Enable foreign keys checks")
        cursor.execute("SET foreign_key_checks = 1")
        db.commit()
    db.close()

if __name__ == "__main__":
    for database in db_list:
        print("Convert all tables in %s to utf8/utf8_general_ci" % database)
        convert_tables(db_hostname, db_username, db_password, database)
