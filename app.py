import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
db = SQLAlchemy(app)

# Modelo de Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Rota principal - Página inicial
@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

# Rota para adicionar produtos
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        novo_produto = Produto(nome=nome, quantidade=int(quantidade), preco=float(preco))
        db.session.add(novo_produto)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('adicionar.html')

# Inicialização do banco de dados e definição da porta do Heroku
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))  # Heroku define a porta como uma variável de ambiente
    app.run(host='0.0.0.0', port=port, debug=True)
