from flask import Flask, render_template, jsonify, request, redirect, url_for, session
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
        # utente = Utenti.query.filter(Utenti.email == email).first()
        session["id"] = 4
        spot = Spot.query.all() # Recupera tutti gli spot dalla tabella "spot"
        return render_template('home.html', spot=spot)
    else:
        return "Errore di connessione al database"
    
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
    
    db.session.add(nuova_risposta)
    db.session.commit()
    
    return jsonify(success=True)

## Codice per la pagina classifica

@app.route('/classifica')
def index():
    if test_database_connection():
        utenti = Utenti.query.all()  # Recupera tutti i dati dalla tabella "utenti"
        facolta = Facolta.query.order_by(Facolta.puntiTot.desc()).all()  # Recupera tutti i dati dalla tabella "facolta"
        id = session["id"]
        # Recupera una domanda a caso dal database
        random_question = Domande.query.order_by(db.func.random()).first()
        
        # Query per ottenere la data dall'ultima giocata per l'utente, sostituisci con la tua logica di query
        # prima_tupla_utenti = Utenti.query.order_by(db.func.random()).first()
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
    # Ottieni la facoltà dal database
    facolta = Facolta.query.get_or_404(codice_facolta)
    # Incrementa i punti della facoltà
    facolta.puntiTot += 10

    # Ottieni l'utente dal database
    utente = Utenti.query.get_or_404(codice_utente)
    # Aggiorna il campo ultima_giocata con la data attuale
    utente.ultimaGiocata = datetime.now().strftime('%Y-%m-%d')

    # Salva le modifiche nel database
    db.session.commit()

    # Restituisci una risposta JSON
    return jsonify({'success': True, 'nuovi_punti': facolta.puntiTot, 'ultima_giocata': utente.ultimaGiocata})

## Codice per la pagina Spotted Eventi
# Pagina principale
@app.route('/mappa')
def mappa():
    # Recupera tutti gli eventi dal database
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

        return redirect(url_for('index'))
    
@app.route('/profilo')
def profilo():
    # Recupera l'ID dell'utente loggato
    user_id = session["id"]
    u = Utenti.query.filter(Utenti.id == user_id).first()
    
    # Query per ottenere gli spot dell'utente loggato
    spots = Spot.query.filter(Spot.id_utente == user_id).all()
    
    # Query per ottenere le risposte relative agli spot dell'utente loggato
    spot_ids = [spot.id_spot for spot in spots]
    risposte = Risposte.query.filter(Risposte.id_spot.in_(spot_ids)).all()
    
    # Organizza le risposte per spot
    risposte_per_spot = {}
    for risposta in risposte:
        if risposta.id_spot not in risposte_per_spot:
            risposte_per_spot[risposta.id_spot] = []
        risposte_per_spot[risposta.id_spot].append(risposta)
    
    # Passa i dati al template
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
     # Ricevi i dati inviati come JSON
    data = request.get_json()

    # Estrai i valori dei campi
    nome = data['nome']
    cognome = data['cognome']
    email = data['email']
    password = data['password']
    facolta_codice = data['facolta']
    
    # Controlla se l'email esiste già nel database
    existing_user = Utenti.query.filter_by(email=email).first()
    if existing_user:
        return "L'email inserita è già registrata. Si prega di utilizzare un'email diversa."

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
        # Verifica se l'utente è autenticato
        if current_user.is_authenticated:
            # Utente autenticato, reindirizza alla home page
            return "Login avvenuto con successo!"
        else:
            #Utente non autenticato, reindirizza alla pagina di login
            return render_template('loginpage.html')
    else:
        return "Errore di connessione al database"

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
    
@app.route('/profile', methods=['GET'])
@login_required  # Assicura che solo gli utenti loggati possano accedere a questa rotta
def profile():
    nome_user=current_user.nome
    cognome_user=current_user.cognome
    return render_template('profilo.html', nome_user=nome_user, cognome_user=cognome_user)


@app.route('/logout')
@login_required
def logout():
    # Effettua il logout dell'utente corrente
    logout_user()
    return redirect('/')

@app.route('/successo')
def successo():
    return "Registrazione avvenuta con successo!"

@app.route('/successo_accesso')
def successo_log():
    return "Login avvenuto con successo!"
if __name__ == '__main__':
    app.run(debug=True)
