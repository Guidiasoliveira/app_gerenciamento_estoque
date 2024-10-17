from flask import Flask, render_template, request, redirect, url_for, send_file
from models import db, Produto
import os
import pandas as pd

app = Flask(__name__)

# Configuração do banco de dados
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estoque.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/')
def index():
    produtos = Produto.query.all()
    categorias = [produto.nome for produto in produtos]
    quantidades = [produto.quantidade for produto in produtos]
    return render_template('index.html', produtos=produtos, categorias=categorias, quantidades=quantidades)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        preco_compra = request.form['preco_compra']
        unidade_medida = request.form['unidade_medida']
        ponto_reposicao = request.form['ponto_reposicao']
        localizacao = request.form['localizacao']
        quantidade = request.form['quantidade']

        novo_produto = Produto(
            nome=nome,
            preco_compra=float(preco_compra),
            unidade_medida=unidade_medida,
            ponto_reposicao=int(ponto_reposicao),
            localizacao=localizacao,
            quantidade=int(quantidade)
        )
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/relatorios')
def relatorios():
    produtos = Produto.query.all()
    data = {
        "Nome": [produto.nome for produto in produtos],
        "Quantidade": [produto.quantidade for produto in produtos],
        "Preço de Compra": [produto.preco_compra for produto in produtos],
        "Unidade de Medida": [produto.unidade_medida for produto in produtos],
        "Ponto de Reposição": [produto.ponto_reposicao for produto in produtos],
        "Localização": [produto.localizacao for produto in produtos]
    }
    df = pd.DataFrame(data)
    excel_path = os.path.join(project_dir, 'estoque.xlsx')
    df.to_excel(excel_path, index=False)
    return send_file(excel_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
