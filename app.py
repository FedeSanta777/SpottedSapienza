from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza'
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
    ultimaGiocata = db.Column(db.Date)
    
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
        # Recupera una domanda a caso dal database
        random_question = Domande.query.order_by(db.func.random()).first()
        
        # Query per ottenere la data dall'ultima giocata per l'utente, sostituisci con la tua logica di query
        prima_tupla_utenti = Utenti.query.order_by(db.func.random()).first()
        ultima_giocata = prima_tupla_utenti.ultimaGiocata
        
        
        ultima_giocata = ultima_giocata.strftime('%Y-%m-%d')

        # Verifica se la data dell'ultima giocata è diversa dalla data attuale
        today = datetime.now().date()
        enable_button = str(ultima_giocata) != str(today)
        
        
    
        return render_template('classifica.html', utenti=utenti, facolta=facolta, domande=random_question, image_path=random_question.srcArg, enable_button=enable_button, oggi=today, data=ultima_giocata, utente_scelto=prima_tupla_utenti)
    else:
        return "Errore di connessione al database"
    
@app.route('/incrementa/<int:codice_facolta>', methods=['POST'])
def incrementa_punti(codice_facolta):
    facolta = Facolta.query.get_or_404(codice_facolta)
    facolta.puntiTot += 10
    db.session.commit()
    return jsonify({'success': True, 'nuovi_punti': facolta.puntiTot})


if __name__ == '__main__':
    app.run(debug=True)
