from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Produto no Banco de Dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    produtos = Produto.query.all()
    
    # Verificar produtos com estoque baixo (menos de 5 unidades)
    estoque_baixo = [produto for produto in produtos if produto.quantidade < 5]
    
    # Dados para os gráficos
    categorias = [produto.nome for produto in produtos]
    quantidades = [produto.quantidade for produto in produtos]

    return render_template('index.html', produtos=produtos, categorias=categorias, quantidades=quantidades, estoque_baixo=estoque_baixo)

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

if __name__ == '__main__':
    app.run(debug=True)
