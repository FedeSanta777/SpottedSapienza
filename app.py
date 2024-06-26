from flask import Flask, render_template, jsonify, request, redirect, url_for, session, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'chiave log'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Definisci il modello Facolta
class Facolta(db.Model):
    __tablename__ = 'facolta'
    codice = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    puntiTot = db.Column(db.Integer, nullable=False)

# Definisci il modello Utenti
class Utenti(db.Model, UserMixin):
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
    
# Definizione del modello della tabella "eventi"
class Eventi(db.Model):
    __tablename__ = 'eventi'
    id_evento = db.Column(db.Integer, primary_key=True)
    nome_evento = db.Column(db.String(255))
    latitudine = db.Column(db.Float)
    longitudine = db.Column(db.Float)
    data_evento = db.Column(db.DateTime)
    
# Definizione del modello della tabella "spot"
class Spot(db.Model):
    __tablename__ = 'spot'
    id_spot = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utente = db.Column(db.Integer, db.ForeignKey('utenti.id'))
    id_facolta = db.Column(db.Integer, db.ForeignKey('facolta.codice'))
    contenuto = db.Column(db.Text)
    anonimato = db.Column(db.Boolean)
    utente = db.relationship('Utenti', backref=db.backref('spot', lazy=True))
    facolta = db.relationship('Facolta', backref=db.backref('spot', lazy=True))
    
# Definizione del modello della tabella "risposte"
class Risposte(db.Model):
    __tablename__ = 'risposte'
    id_risposta = db.Column(db.Integer, primary_key=True)
    id_utente_risp = db.Column(db.Integer, db.ForeignKey('utenti.id'))
    id_utente_spot = db.Column(db.Integer, db.ForeignKey('utenti.id'))
    id_spot = db.Column(db.Integer, db.ForeignKey('spot.id_spot'))
    contenuto = db.Column(db.Text)
    utente_risp = db.relationship('Utenti', foreign_keys=[id_utente_risp])
    utente_spot = db.relationship('Utenti', foreign_keys=[id_utente_spot])
    spot = db.relationship('Spot', foreign_keys=[id_spot])

# Funzione per caricare un utente in base all'ID
@login_manager.user_loader
def load_user(user_id):
    return Utenti.query.get(int(user_id))

# Funzione per verificare le credenziali dell'utente nel database

def verify_user(email, password):
    return Utenti.query.filter_by(email=email, password=password).first()

def test_database_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Errore di connessione al database: {e}")
        return False

@app.route('/')
def home():
    if test_database_connection():
        session["id"] = 1
        id_utente = session["id"]
        utente = Utenti.query.filter_by(id=id_utente).first()
        spot = Spot.query.all() # Recupera tutti gli spot dalla tabella "spot"
        return render_template('home.html', spot=spot, utente=utente)
    else:
        return "Errore di connessione al database"
    
@app.route('/inserisci_spot', methods=['POST'])
def inserisci_spot():
    id_utente = session.get('id')  # Accesso all'ID dell'utente dalla sessione Flask
    contenuto = request.form.get('contenuto')
    anonimato = True if request.form.get('anonimato') == 'on' else False
    facolta = request.form.get('facolta')
    
    nuovo_spot = Spot(
        id_utente=id_utente,
        contenuto=contenuto,
        anonimato=anonimato,
        id_facolta=facolta
    )

    try:
        db.session.add(nuovo_spot)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/inserisci_risposta', methods=['POST'])
def inserisci_risposta():
    id_utente_risp = request.form.get('id_utente_risp')
    id_spot = request.form.get('id_spot')
    contenuto = request.form.get('contenuto')
    
    # Ricava id_utente_spot dalla tabella Spot
    spot = Spot.query.get_or_404(id_spot)
    id_utente_spot = spot.id_utente
    
    nuova_risposta = Risposte(
        id_utente_risp=id_utente_risp,
        id_utente_spot=id_utente_spot,
        id_spot=id_spot,
        contenuto=contenuto
    )
    
    try:
        db.session.add(nuova_risposta)
        db.session.commit()
        return Response('success', status=200)
    except Exception as e:
        db.session.rollback()
        return Response('error', status=500)
    
## Codice per la pagina classifica

@app.route('/classifica')
def index():
    if test_database_connection():
        utenti = Utenti.query.all()  # Recupero di tutti i dati dalla tabella "utenti"
        facolta = Facolta.query.order_by(Facolta.puntiTot.desc()).all()  # Recupero di tutti i dati dalla tabella "facolta"
        id = session["id"]
        # Recupero di una domanda a caso dal database
        random_question = Domande.query.order_by(db.func.random()).first()
        
        # Query per ottenere la data dall'ultima giocata per l'utente
        prima_tupla_utenti = Utenti.query.filter(Utenti.id == id).first()
        ultima_giocata = prima_tupla_utenti.ultimaGiocata
        
        ultima_giocata = ultima_giocata.strftime('%Y-%m-%d')

        # Verifica se la data dell'ultima giocata è diversa dalla data attuale
        today = datetime.now().date()
        enable_button = str(ultima_giocata) != str(today)
        return render_template('classifica.html', utenti=utenti, facolta=facolta, domande=random_question, image_path=random_question.srcArg, enable_button=enable_button, oggi=today, data=ultima_giocata, utente_scelto=prima_tupla_utenti)
    else:
        return "Errore di connessione al database"

@app.route('/incrementa/<int:codice_facolta>/<int:codice_utente>', methods=['POST'])
def incrementa_punti(codice_facolta, codice_utente):
    # Ottenimento della facoltà dal database
    facolta = Facolta.query.get_or_404(codice_facolta)
    # Incremento dei punti della facoltà
    facolta.puntiTot += 10

    # Ottenimento dell'utente dal database
    utente = Utenti.query.get_or_404(codice_utente)
    # Aggiornamento dell campo ultima_giocata con la data attuale
    utente.ultimaGiocata = datetime.now().strftime('%Y-%m-%d')

    # Salvataggio delle modifiche nel database
    db.session.commit()

    # Restituzione di una risposta JSON
    return jsonify({'success': True, 'nuovi_punti': facolta.puntiTot, 'ultima_giocata': utente.ultimaGiocata})

## Codice per la pagina Spotted Eventi
# Pagina principale
@app.route('/mappa')
def mappa():
    # Recupero di tutti gli eventi dal database
    eventi = Eventi.query.all()
    return render_template('mappa.html', eventi=eventi)

# Gestione della richiesta POST per l'inserimento di un nuovo evento
@app.route('/submit_event', methods=['POST'])
def submit_event():
    if request.method == 'POST':
        nome_evento = request.form['nome_evento']
        latitudine = request.form['latitudine']
        longitudine = request.form['longitudine']
        data_evento = datetime.strptime(request.form['datetimepicker'], '%Y-%m-%d %H:%M')

        nuovo_evento = Eventi(nome_evento=nome_evento, latitudine=latitudine, longitudine=longitudine, data_evento=data_evento)
        db.session.add(nuovo_evento)
        db.session.commit()

        return redirect(url_for('mappa'))
    
@app.route('/profilo')
def profilo():
    # Recupero dell'ID dell'utente loggato
    user_id = session["id"]
    u = Utenti.query.filter(Utenti.id == user_id).first()
    
    # Query per ottenere gli spot dell'utente loggato
    spots = Spot.query.filter(Spot.id_utente == user_id).all()
    
    # Query per ottenere le risposte relative agli spot dell'utente loggato
    spot_ids = [spot.id_spot for spot in spots]
    risposte = Risposte.query.filter(Risposte.id_spot.in_(spot_ids)).all()
    
    # Organizzazione delle risposte per spot
    risposte_per_spot = {}
    for risposta in risposte:
        if risposta.id_spot not in risposte_per_spot:
            risposte_per_spot[risposta.id_spot] = []
        risposte_per_spot[risposta.id_spot].append(risposta)
    
    # Passaggio dei dati al template
    return render_template('profilo.html', spots=spots, risposte_per_spot=risposte_per_spot, utente=u, id=session["id"])

# Registrazione
@app.route('/reg_page')
def reg():
    if test_database_connection():
        facolta = Facolta.query.all()
        return render_template('reg_page.html', facolta=facolta)
    else:
        return "Errore di connessione al database"
    
@app.route('/registrazione', methods=['POST'])
def registrazione():
     # Ricezione dei dati inviati come JSON
    data = request.get_json()

    # Estrazione dei valori dei campi
    nome = data['nome']
    cognome = data['cognome']
    email = data['email']
    password = data['password']
    facolta_codice = data['facolta']
    
    # Controllo se l'email esiste già nel database
    existing_user = Utenti.query.filter_by(email=email).first()
    if existing_user:
        return "L'email inserita è già registrata. Si prega di utilizzare un'email diversa."

    # Creazione di un nuovo utente
    nuovo_utente = Utenti(nome=nome, cognome=cognome, email=email, password=password, facolta_codice=facolta_codice)

    # Salvataggio dell'utente nel database
    try:
        db.session.add(nuovo_utente)
        db.session.commit()
        return redirect('/successo')  # Reindirizzamento alla pagina di registrazione avvenuta con successo
    except Exception as e:
        print(f"Errore durante la registrazione: {e}")
        db.session.rollback()
        return "Errore durante la registrazione"
    

#Controllo email già presente nel server:
@app.route('/check_email')
def check_email():
    email = request.args.get('email')
    existing_user = Utenti.query.filter_by(email=email).first()
    if existing_user:
        session["id"] = existing_user.id
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

#login
@app.route('/loginpage')
def log():
    if test_database_connection():
        return render_template('loginpage.html')
    else:
        return "Errore di connessione al database"

@app.route('/login', methods=['POST'])
def login():
    # Ottenimento i dati inviati dal client come JSON
    data = request.json
    # Estrazione della email e della password dall'oggetto dei dati
    email = data.get('email')
    password = data.get('password')
    
    print(f'Trying to login with email: {email}')
    
    # Verifica delle credenziali dell'utente nel database
    user = verify_user(email, password)
    print(user)
    if user is not None:
        print('User authenticated successfully')
        # Login riuscito, effettua il login dell'utente
        login_user(user)
        session["id"] = Utenti.query.filter_by(email=email).first().id
        return jsonify({'loginStatus': 'success'})  # Invia una risposta JSON indicando il successo del login
    else:
        print('Authentication failed')
        # Login fallito, restituisce un messaggio di errore con codice di stato 401
        return jsonify({'loginStatus': 'failure'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # Effettua il logout dell'utente corrente
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
