from flask import Blueprint, render_template

estoque_blueprint = Blueprint('estoque', __name__)

@estoque_blueprint.route('/')
def estoque_home():
    return render_template('estoque/home.html')
