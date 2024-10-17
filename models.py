from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    unidade_medida = db.Column(db.String(20), nullable=False)
    ponto_reposicao = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
