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
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"[ERRO] Arquivo '{ARQUIVO_DADOS}' não encontrado!")
        print("Certifique-se de que o arquivo usuarios.json está na mesma pasta que app.py.")
    else:
        print("=" * 50)
        print("  Sabor do Brasil — Servidor iniciado!")
        print("  Acesse: http://127.0.0.1:5000")
        print("=" * 50)
        app.run(debug=True)