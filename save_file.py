#!/usr/bin/env python
import cgitb; cgitb.enable()
import cgi, os
import formencode
from formencode.validators import *
from formencode.national import *
import ConfigParser, sqlite3 as sql
from datetime import datetime
from hashlib import sha224
import magic
import shutil
from stlparser import StlBinaryParser,StlAsciiParser

print """\
Content-Type: text/html\n"""

config = ConfigParser.SafeConfigParser()
config.readfp(open('resolution.conf'))

filename = config.get('database','filename')
user = config.get('database','user')
database = config.get('database','database')
material_table = config.get('database','material_table')
jobs_table = config.get('database','jobs_table')

db = sql.connect(filename)
cur = db.cursor()

materials = []
for result in cur.execute('select idx from %s'%material_table):
    materials.append(str(result[0])) 


error_format = '<span class="error">%s</span><br>'
message = ''
fail = False

form = cgi.FieldStorage()

#### User details ####
try:
    name = NotEmpty(messages=dict(empty='Please enter your name.')).to_python(form.getfirst('name'))
    email = Email(resolve_domain=True).to_python(form.getfirst('email',''))
    phone = USPhoneNumber().to_python(form.getfirst('phone',''))
    
    if not phone:
        phone = ''

    if not email:
        email = ''

    if not (email or phone):
        raise ValueError,'Please enter either or both of your email address and phone number.'
except formencode.Invalid, e:
    message += error_format%e
    fail = True
except ValueError, e:
    message += error_format%e
    fail = True
else:
    message += 'Name is %s, using %s as email and %s as phone<br>'%(name,email,phone)
#### End user details ####

#### Basic job details ####
try:
    material = OneOf(materials).to_python(form.getfirst('material','1'))
except formencode.Invalid, e:
    message += error_format%e
    fail = True
else:
    (colour,plastic) = cur.execute('select colour, material from %s where idx=?'%material_table,material).fetchone()
    message += 'Job should be done in %s %s<br>'%(colour, plastic)
#### End basic job details ####

#### Slicer settings ####
try:
    zstep = Number(min=0.125,max=0.5).to_python(form.getfirst('zstep','0.25'))
    fillp = Int(min=0,max=100).to_python(form.getfirst('fillp','25'))
    support = StringBool().to_python(form.getfirst('support','false'))
    wallnum = Int(min=0,max=9).to_python(form.getfirst('wallnum','3'))
    wallthick = Number(min=0.125).to_python(form.getfirst('wallthick','0.595'))
except formencode.Invalid, e:
    message += error_format%e
    fail = True
else:
    message += 'Slicer to use %smm z-step, %s%% fill, %s support, %s lines on perimeter, %smm thick walls<br>'%(zstep,fillp,('NO','FULL')[support],wallnum,wallthick)
#### End slicer settings ####

#### Post settings ####
try:
    cleanup = StringBool().to_python(form.getfirst('cleanup','false'))
    acetone = StringBool().to_python(form.getfirst('acetone','false'))
except formencode.Invalid, e:
    message += error_format%e
    fail = True
else:
    message += 'Lab technicians %s clean up parts, %s acetone<br>'%(('SHOULD NOT','SHOULD')[cleanup],('WITHOUT','WITH')[acetone])
#### End post settings ####

comments = cgi.escape(form.getfirst('comments'))

message += '</p><p>Comments as follows:<br>"%s"</p><p>'%comments
time = datetime.today()
Loc = sha224(name+email+phone+material+str(time)).hexdigest()

if not fail:
    #### File upload, if everything else seems sane ####
    
    # Generator to buffer file chunks
    def fbuffer(f, chunk_size=10000):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            yield chunk
      
    # A nested FieldStorage instance holds the file
    fileitem = form['file']

    # Test if the file was uploaded
    if fileitem.filename:

        # strip leading path from file name to avoid directory traversal attacks,
        # fail-fast on file extension.
        fn = 'files/' + os.path.basename(fileitem.filename)
        if not fn.upper().endswith('STL'):
            message += error_format%'The file must have an STL extension.'
            fail = True
        else:

            with open(fn, 'wb', 10000) as f:
                # Read the file in chunks
                for chunk in fbuffer(fileitem.file):
                    f.write(chunk)

        # determine if the file is correct type
        ms = magic.open(magic.MAGIC_NONE)
        ms.load()
        t = ms.file(fn)
        
        try:
            if t == 'data':
                s = StlBinaryParser(fn)
                s.parse()
            elif t == 'ASCII text':
                s = StlAsciiParser(fn)
                s.parse()
            else:
                raise ValueError,'Format bad'
        except Exception,e:
            message += error_format%'The file must be a sane ASCII or binary STL file.<br>%s'%e
            fail = True
        else:
            message += 'The file "' + fn[6:] + '" was uploaded successfully'
            shutil.move(fn,'STL/%s.stl'%Loc)

    else:
        message += error_format%'No file was uploaded'
        fail = True

    #### End file upload ####

if not fail:
    #### database entry and communications ####
    cur.execute('insert into %s (name,email,phone,material,submitDate,comments,stlLoc,gcodeLoc,sliceLoc,labLoc) values (?,?,?,?,?,?,?,?,?,?)'%jobs_table,(name,email,phone,material,time,comments,'STL/%s.stl'%Loc,'GCODE/%s.bfb'%Loc,'slicer/%s.cfg'%Loc,'lab/%s.txt'%Loc))
    db.commit()

    with open('slicer/%s.cfg'%Loc,'wb') as f:
        f.write('[slicer]\n')
        f.write('zstep:%4.3f\n'%zstep)
        f.write('fillp:%d\n'%fillp)
        f.write('support:%s\n'%('off','on')[support])
        f.write('wallnum:%d\n'%wallnum)
        f.write('wallthick:%4.3f\n'%wallthick)
    
    with open('lab/%s.txt'%Loc,'wb') as f:
        f.write('Dear lab technicians:\n')
        f.write('Please %s clean up this job of support material and rafting.\n'%('DO NOT','DO')[cleanup])
        f.write('In addition, please %s polish this job with acetone.\n'%('DO NOT','DO')[acetone])
        if comments:
            f.write('\nComments:\n%s\n'%comments)
        f.write('\nThanks,\n\n%s\n%s\n%s\n'%(name,email,phone))

    #### end database entry and communications ####

#TODO slicer goes here!
   
print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>IEEE 3D Printer Job Results</title>
<link rel="stylesheet" type="text/css" href="default.css">
</head>
<body>
<p>%s</p>
</body></html>
""" % (message,)
