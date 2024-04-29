from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spottedsapienza'
db = SQLAlchemy(app)

# Definisci il modello Facolta
class Facolta(db.Model):
    __tablename__ = 'facolta'
    codice = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    puntiTot = db.Column(db.Integer, nullable=False)

# Definisci il modello Utenti
class Utenti(db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cognome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    facolta_codice = db.Column(db.Integer, db.ForeignKey('facolta.codice'))
    facolta = db.relationship('Facolta', backref=db.backref('utenti', lazy=True))
    
# Definisci il modello Domanda
class Domande(db.Model):
    __tablename__ = 'domande'
    codice = db.Column(db.Integer, primary_key=True)
    argomento = db.Column(db.String(255))
    testo = db.Column(db.String(255))
    risposta_1 = db.Column(db.String(255))
    risposta_2 = db.Column(db.String(255))
    risposta_3 = db.Column(db.String(255))
    risposta_4 = db.Column(db.String(255))
    risposta_corretta = db.Column(db.Enum('risposta_1', 'risposta_2', 'risposta_3', 'risposta_4'))
    srcArg = db.Column(db.String(255))

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
        utenti = Utenti.query.all()  # Recupera tutti i dati dalla tabella "utenti"
        facolta = Facolta.query.order_by(Facolta.puntiTot.desc()).all()  # Recupera tutti i dati dalla tabella "facolta"
        domande =  Domande.query.order_by(db.func.rand()).first()
        return render_template('classifica.html', utenti=utenti, facolta=facolta, domande=domande)
    else:
        return "Errore di connessione al database"


if __name__ == '__main__':
    app.run(debug=True)
