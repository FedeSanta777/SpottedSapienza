from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza' #dopo i due punti andrebbe la password
db = SQLAlchemy(app)

# Definisci il modello Utenti
class Utenti(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    facolta = db.Column(db.String(100))
#funzione di test collegamento al database
def test_database_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Errore di connessione al database: {e}")
        return False
def verify_user(email, password):
    conn = sqlite3.connect('spottedsapienza.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM utenti WHERE email = ? AND password = ?''', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = verify_user(email, password)
        if user:
            # Login riuscito, reindirizza alla home page
            return redirect('home.html')
        else:
            # Login fallito, mostra un messaggio di errore
            error = "Credenziali non valide. Riprova."
            return render_template('login.html', error=error)
    else:
        # Metodo GET, mostra la schermata di login
        return render_template('login.html')

#equivalente del main
@app.route('/')
def index():
    if test_database_connection():
        utenti = Utenti.query.all()
        return render_template('loginpage.html', utenti=utenti) #funzione che richiama il file di interesse
    else:
        return "Errore di connessione al database"

if __name__ == '__main__':
    app.run(debug=True)
