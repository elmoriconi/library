from flask import Flask, request, render_template, g
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)

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

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.executescript('''
            DROP TABLE IF EXISTS books;
            DROP TABLE IF EXISTS members;
            DROP TABLE IF EXISTS borrowed_books;

            CREATE TABLE books (
                book_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                is_borrowed BOOLEAN NOT NULL DEFAULT FALSE
            );

            CREATE TABLE members (
                member_id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE borrowed_books (
                member_id TEXT,
                book_id TEXT,
                PRIMARY KEY (member_id, book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            );
        ''')
        db.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/inserimento', methods=['POST'])
def inserimento():
    id_book = request.form['book-id']
    titolo = request.form['book-title']
    autore = request.form['book-author']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO books (book_id, title, author) VALUES (?, ?, ?)", (id_book, titolo, autore))
    db.commit()

    db.close()
    
    return "Dati inseriti correttamente!"

@app.route('/visualizza')
def visualizza():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT book_id, title, author FROM books")
    libri = cursor.fetchall()
    return render_template('visualizza.html', libri=libri)
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)