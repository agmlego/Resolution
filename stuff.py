#!/usr/bin/env python
import ConfigParser, sqlite3 as sql, os, os.path

config = ConfigParser.SafeConfigParser()
config.readfp(open('resolution.conf'))

filename = config.get('database','filename')
user = config.get('database','user')
database = config.get('database','database')
material_table = config.get('database','material_table')
jobs_table = config.get('database','jobs_table')

db = sql.connect(filename)
cur = db.cursor()

data = [
        ['red','ABS','y',2.2],
        ['white','ABS','a',2.1],
        ['blue','ABS','y',2.0],
        ['black','ABS','y',2.2]
        ]
for i in xrange(len(data)):
    cur.execute('insert into %s (colour, material, present, remaining, imageLoc) values ("%s","%s","%s",%s,"%s")'%(material_table,data[i][0],data[i][1],data[i][2],data[i][3],data[i][0]+data[i][1]))

db.commit()
