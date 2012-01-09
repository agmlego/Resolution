#!/usr/bin/env python
import ConfigParser, sqlite3 as sql
#import cgitb; cgitb.enable()
import cgi, os
from datetime import datetime

config = ConfigParser.SafeConfigParser()
config.readfp(open('resolution.conf'))

filename = config.get('database','filename')
user = config.get('database','user')
database = config.get('database','database')
material_table = config.get('database','material_table')

db = sql.connect(filename)
cur = db.cursor()

data = cur.execute('select * from %s'%material_table).fetchall()

def material_template(idx, colour, material, present, remaining, imageLoc):
    return '''<div class="material%s">
    <a target="_blank" href="images/%s.png">
        <img src="images/thumbs/%s_thumb.png" alt="%s %s" width="110" height="90" />
    </a>
    <div class="option"><input type="radio" name="material" value="%s" id="%s" %s><label for="%s">%s %s<br>(%2.1fkg left)</label></div>
</div>'''%( ('','_hide')[present=='n'],
            imageLoc,
            imageLoc, colour, material,
            idx, idx, ('','checked')[present=='a'], idx, colour, material, remaining)

material_list = []

for i in xrange(len(data)):
    (idx,colour,material,present,remaining,imageLoc) = data[i]
    material_list.append(material_template(idx,colour,material,present,remaining,imageLoc))

print '''\
Content-Type: text/html\n'''

print open('index.tpl').read()%('\n'.join(material_list))
