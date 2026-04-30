# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    important = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'important': self.important
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    a = [note.to_dict() for note in notes]
    print (type(a))
    return jsonify([note.to_dict() for note in notes])

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    text = data.get('text', '').strip()
    important = data.get('important', False)
    if not text:
        return jsonify({'error': 'Текст не может быть пустым'}), 400
    note = Note(text=text, important=important)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/clear', methods=['DELETE'])
def clear_notes():
    db.session.query(Note).delete()
    db.session.commit()
    return jsonify({'message': 'Все заметки удалены'}), 200

if __name__ == '__main__':
    app.run(debug=True)