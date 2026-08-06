from flask import Flask, g, abort, render_template, send_from_directory
import sqlite3
import datetime

app = Flask(__name__)

DATABASE = 'app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def show_home():
    cursor = get_db().cursor()

    data = []

    for row in cursor.execute('SELECT id, name, uploadDateTime FROM uploads'):
        data.append(
            {"noteName": row[1], "noteId": row[0], "uploadDateTime": row[2]}
        )

    return render_template('home_template.html',listItems=data)

@app.route("/note/<noteId>")
def show_note(noteId=None):
    cursor = get_db().cursor()

    cursor.execute('SELECT * FROM uploads WHERE id = ?',(noteId,))
    if (cursor.fetchone() is None):
        return abort(404)

    with open(f'notes/{noteId}.html',mode='r',encoding='utf-8') as f:
        return f.read()

@app.route("/note/<noteId>/download")
def download_note(noteId=None):
    cursor = get_db().cursor()

    cursor.execute('SELECT * FROM uploads WHERE id = ?',(noteId,))
    if (cursor.fetchone() is None):
        return abort(405)

    return send_from_directory('notes',f'{noteId}.html',as_attachment=True)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_template.html')

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405_template.html')