from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spottedsapienza' #dopo i due punti andrebbe la password
db = SQLAlchemy(app)

class Utenti(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    facolta = db.Column(db.String(100))

def test_database_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Errore di connessione al database: {e}")
        return False

@app.route('/')
def index():
    if test_database_connection():
        utenti = Utenti.query.all()
        return render_template('reg_page.html', utenti=utenti)
    else:
        return "Errore di connessione al database"

@app.route('/registrazione', methods=['POST'])
def registrazione():
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    password = request.form['password']
    facolta = request.form['facolta']

    nuovo_utente = Utenti(nome=nome, cognome=cognome, email=email, password=password, facolta=facolta)

    try:
        db.session.add(nuovo_utente)
        db.session.commit()
        return redirect(url_for('index'))  # Reindirizza alla pagina principale dopo la registrazione
    except Exception as e:
        print(f"Errore durante la registrazione: {e}")
        db.session.rollback()
        return "Errore durante la registrazione"


if __name__ == '__main__':
    app.run(debug=True)


