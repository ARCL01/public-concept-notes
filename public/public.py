import os
from pathlib import Path
import sqlite3
from flask import Flask, g, abort, render_template, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATABASE = 'app.db'
NOTES_DIR = Path('notes').resolve()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_safe_note_path(note_id):
    if not note_id:
        return None
    
    target_path = (NOTES_DIR / f"{note_id}.html").resolve()
    
    if not target_path.is_relative_to(NOTES_DIR):
        return None
        
    return target_path

@app.route("/")
def show_home():
    cursor = get_db().cursor()
    data = []

    for row in cursor.execute('SELECT id, name, uploadDateTime FROM uploads'):
        data.append({
            "noteName": row[1], 
            "noteId": row[0], 
            "uploadDateTime": row[2]
        })

    return render_template('home_template.html', listItems=data)

@app.route("/note/<noteId>")
def show_note(noteId=None):
    cursor = get_db().cursor()

    cursor.execute('SELECT id FROM uploads WHERE id = ?', (noteId,))
    if cursor.fetchone() is None:
        return abort(404)

    file_path = get_safe_note_path(noteId)
    if file_path is None:
        return abort(400)

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return abort(404)

@app.route("/note/<noteId>/download")
def download_note(noteId=None):
    cursor = get_db().cursor()
    result = cursor.execute('SELECT name FROM uploads WHERE id = ?', (noteId,)).fetchone()
    if result is None:
        return abort(404)

    file_path = get_safe_note_path(noteId)
    if file_path is None or not os.path.exists(file_path):
        return abort(404)

    download_name = secure_filename(f"{result[0]}.html")
    if not download_name:
        download_name = "note.html"

    return send_from_directory('notes',f'{noteId}.html',download_name=download_name,as_attachment=True)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_template.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405_template.html'), 405

@app.errorhandler(400)
def bad_request(error):
    return render_template('400_template.html'), 400