from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configurazione del database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spotted_sapienza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializzazione del database
db = SQLAlchemy(app)

# Definizione del modello della tabella "eventi"
class Eventi(db.Model):
    __tablename__ = 'eventi'
    id_evento = db.Column(db.Integer, primary_key=True)
    nome_evento = db.Column(db.String(255))
    latitudine = db.Column(db.Float)
    longitudine = db.Column(db.Float)
    data_evento = db.Column(db.DateTime)

# Pagina principale
@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
