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

try:
    data = cur.execute('select * from %s'%jobs_table).fetchall()
    print 'Jobs table found, %d rows!'%len(data)
except sql.OperationalError,e:
    print e
    cur.execute('create table %s (idx INTEGER PRIMARY KEY ASC, name TEXT, email TEXT, phone TEXT, material INTEGER, submitDate TEXT, completeDate TEXT, kgUsed REAL, timeUsed TEXT, comments TEXT, stlLoc TEXT, gcodeLoc TEXT, sliceLoc TEXT, labLoc TEXT)'%jobs_table)
    print 'Jobs table %s created'%jobs_table

try:
    data = cur.execute('select * from %s'%material_table).fetchall()
    print 'Materials table found, %d rows!'%len(data)
except sql.OperationalError,e:
    print e
    cur.execute('create table %s (idx INTEGER PRIMARY KEY ASC, colour TEXT, material TEXT, present TEXT, remaining REAL, imageLoc TEXT)'%material_table)
    print 'Materials table %s created'%material_table

for d in ('files','GCODE','lab','STL','slicer'):
    if not os.path.exists(d):
	print '%s not found, creating.'%d
        os.makedirs(d)
    else:
        print '%s found!'%d
