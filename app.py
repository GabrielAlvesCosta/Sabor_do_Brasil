from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.receita_controller import receita_bp

app = Flask(__name__)

# SEM ISSO, A SESSÃO NÃO FUNCIONA E O LOGIN É IGNORADO!
app.secret_key = "sabor_do_brasil_chave_secreta_2024" 

# Aqui embaixo devem estar os registros dos seus controllers/blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(receita_bp)

if __name__ == "__main__":
    app.run(debug=True)