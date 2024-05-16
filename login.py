from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'chiave log'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza' #dopo i due punti andrebbe la password
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Definisci il modello Utenti
class Utenti(db.Model, UserMixin):
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

# Funzione per caricare un utente in base all'ID
@login_manager.user_loader
def load_user(user_id):
    return Utenti.query.get(int(user_id))

# Funzione di test collegamento al database
def test_database_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Errore di connessione al database: {e}")
        return False
    
# Funzione per verificare le credenziali dell'utente nel database
def verify_user(email, password):
    return Utenti.query.filter_by(email=email, password=password).first()

@app.route('/login', methods=['POST'])
def login():
    # Ottieni i dati inviati dal client come JSON
    data = request.json
    
    # Estrai email e password dall'oggetto dei dati
    email = data.get('email')
    password = data.get('password')

    # Verifica le credenziali dell'utente nel database
    user = verify_user(email, password)
    
    if user:
        # Login riuscito, effettua il login dell'utente
        login_user(user)
        return jsonify({'loginStatus': 'success'})
    else:
        # Login fallito, restituisce un messaggio di errore
        return jsonify({'loginStatus': 'failure'})

@app.route('/logout')
@login_required
def logout():
    # Effettua il logout dell'utente corrente
    logout_user()
    return redirect('/')

@app.route('/')
def index():
    if test_database_connection():
        # Verifica se l'utente è autenticato
        if current_user.is_authenticated:
            # Utente autenticato, reindirizza alla home page
            return render_template('home.html')
        else:
            # Utente non autenticato, reindirizza alla pagina di login
            return render_template('loginpage.html')
    else:
        return "Errore di connessione al database"

if __name__ == '__main__':
    app.run(debug=True)