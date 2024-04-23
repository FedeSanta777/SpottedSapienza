from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/spottedsapienza'
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

from sqlalchemy import text

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
        return render_template('index.html', utenti=utenti)
    else:
        return "Errore di connessione al database"

if __name__ == '__main__':
    app.run(debug=True)
