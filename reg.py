from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza' #dopo i due punti andrebbe la password
db = SQLAlchemy(app)

class Utenti(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    facolta_codice = db.Column(db.Integer, db.ForeignKey('facolta.codice'))
    ultimaGiocata = db.Column(db.Date)

    # Definizione della relazione con la tabella facolta
    facolta = db.relationship('Facolta', backref='utenti')

class Facolta(db.Model):
    __tablename__ = 'facolta'
    codice = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    puntiTot = db.Column(db.Integer, nullable=False)

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
        facolta = Facolta.query.all()
        return render_template('reg_page.html', facolta=facolta)
    else:
        return "Errore di connessione al database"
    
@app.route('/registrazione', methods=['POST'])
def registrazione():
    # Accedi ai dati inviati come JSON
    data = request.json

    # Estrai i valori dei campi
    nome = data['nome']
    cognome = data['cognome']
    email = data['email']
    password = data['password']
    facolta_codice = data['facolta']


    # Creazione di un nuovo utente
    nuovo_utente = Utenti(nome=nome, cognome=cognome, email=email, password=password, facolta_codice=facolta_codice)

    # Salvataggio dell'utente nel database
    try:
        db.session.add(nuovo_utente)
        db.session.commit()
        return redirect('/successo')  # Reindirizza alla pagina di registrazione avvenuta con successo
    except Exception as e:
        print(f"Errore durante la registrazione: {e}")
        db.session.rollback()
        return "Errore durante la registrazione"
@app.route('/successo')
def successo():
    return "Registrazione avvenuta con successo!"
if __name__ == '__main__':
    app.run(debug=True)