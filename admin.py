from flask import Flask, request, g, abort, render_template
import sqlite3
import uuid
import re
import datetime
import os

app = Flask(__name__)

with open('static/style.css',mode='r') as f:
    stylesheet = f.read() 

with open('static/svg-pan-min.js',mode='r') as f:
    js = f.read()

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def clean_files():
    with app.app_context():
        cursor = get_db().cursor()

        for row in cursor.execute('SELECT id FROM uploads'):
            if not os.path.isfile(f'notes/{row[0]}.html'):
                cursor.execute('DELETE FROM uploads WHERE id = ?',(row[0],))
                get_db().commit()

        for file in os.listdir('notes'):
            result = cursor.execute('SELECT id FROM uploads WHERE id = ?',(file.replace('.html',''),)).fetchall()
            if not len(result) > 0:
                os.remove(f'notes/{file}')

def create_site(svg:str,fileName:str,id:uuid.UUID):

    svg = re.sub(r'width=".*\sheight=".*pt"','id="notes" width="100%" height="100%"',svg)

    with open('templates/note_template.html',mode='r') as f:
        templateContent = f.read()
    
    templateContent = templateContent.replace('{{note-name}}',fileName)
    templateContent = templateContent.replace('{{stylesheet}}',stylesheet)
    templateContent = templateContent.replace('{{js-svg}}',js)
    templateContent = templateContent.replace('{{svg}}',svg)

    with open(f'notes/{id}.html', mode='w',encoding='utf-8') as finalF:
        finalF.write(templateContent)

init_db()
clean_files()

@app.route("/admin")
def show_home():
    return 'home'   

@app.route("/admin/upload", methods=['GET','POST'])
def show_note():
    if request.method == 'POST':
        clean_files()

        f = request.files['upload']
        name = request.form['name']
        id = uuid.uuid4()

        cursor = get_db().cursor()
        result = cursor.execute('SELECT id FROM uploads WHERE name = ?',(name,)).fetchone()

        if len(result) == 1:
            create_site(svg=f.stream.read().decode('utf-8'),fileName=name,id=result[0])

            uploadDateTime = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

            data = ({"datetime":uploadDateTime,"id":result[0]})

            cursor.execute('UPDATE uploads SET uploadDateTime = :datetime WHERE id = :id',data)
            get_db().commit()

        else:
            create_site(svg=f.stream.read().decode('utf-8'),fileName=name,id=id)

            data = (
                {"id": str(id), "name": name, "size": None, "uploadDateTime": datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}
            )

            cursor.execute("INSERT INTO uploads VALUES(:id, :name, :size, :uploadDateTime)", data)
            get_db().commit()

        return data
    else:
        return render_template('upload.html')

@app.route("/admin/danger/drop")
def drop_tables():
    cursor = get_db().cursor()
    cursor.execute('DROP TABLE IF EXISTS files;')
    cursor.execute('DROP TABLE IF EXISTS uploads;')
    init_db()
    return 'dropped and recreated empty'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_template.html')