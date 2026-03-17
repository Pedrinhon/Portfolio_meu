from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do banco
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), nullable=False)
    text = db.Column(db.String(500), nullable=False)

# Página inicial
@app.route('/')
def index():
    return render_template(
        'index.html',
        button_python=False,
        button_discord=False,
        button_html=False,
        button_db=False
    )

# Botões de habilidades
@app.route('/skills', methods=['POST'])
def skills():
    button_python = False
    button_discord = False
    button_html = False
    button_db = False

    if "button_python" in request.form:
        button_python = True
    if "button_discord" in request.form:
        button_discord = True
    if "button_html" in request.form:
        button_html = True
    if "button_db" in request.form:
        button_db = True

    return render_template('index.html', button_python=button_python, button_discord=button_discord, button_html=button_html, button_db=button_db)

@app.route('/feedback', methods=['POST'])
def feedback():
    email = request.form.get("email")
    text = request.form.get("text")

    if not email or not text:
        return "Preencha todos os campos!"

    novo_feedback = Feedback(email=email, text=text)

    db.session.add(novo_feedback)
    db.session.commit()

    return render_template(
        'index.html', button_python=False, button_discord=False, button_html=False, button_db=False , certo="Obrigado! Seu feedback foi enviado com sucesso e logo será lido!!!")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)