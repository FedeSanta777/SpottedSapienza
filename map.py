from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

if __name__ == '__main__':
    app.run(debug=True)
