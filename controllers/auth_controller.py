import json
import bcrypt
from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint("auth", __name__)

# Caminho do arquivo de persistência JSON
ARQUIVO_DADOS = "usuarios.json"

# --- FUNÇÕES DE ARQUIVO (Mantidas do original para não quebrar o JSON) ---
def ler_dados():
     """
    Lê e retorna o conteúdo do arquivo usuarios.json como dicionário Python.

    Returns:
        dict: Dados completos do sistema (usuários, receitas, etc.)

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        json.JSONDecodeError: Se o arquivo estiver corrompido.
    """
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_dados(dados):
    """
    Salva o dicionário Python de volta no arquivo usuarios.json.

    O parâmetro `indent=2` garante formatação legível.
    O parâmetro `ensure_ascii=False` preserva caracteres especiais (ç, ã, etc.).

    Args:
        dados (dict): Dicionário completo a ser persistido.
    """
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)

# --- ROTAS DE AUTENTICAÇÃO ---

@auth_bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    """
    Rota de cadastro de novo usuário.

    Recebe via JSON: { "nickname": "...", "senha": "..." }
    Retorna JSON com sucesso ou mensagem de erro.

    IMPORTANTE: A senha NUNCA deve ser salva em texto puro!
    Use a função hash_senha() que você implementou.
    """
    corpo = request.get_json()
    nickname = corpo.get("nickname", "").strip()
    senha = corpo.get("senha", "").strip()
    perfil = corpo.get("perfil", "comum").strip()

    # Validação básica dos campos
    if not nickname or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    if perfil not in ["comum", "admin"]:
        return jsonify({"erro": "Perfil inválido"}), 400

    dados = ler_dados()

    # Verifica se o nickname já existe
    for usuario in dados["usuarios"]:
        if usuario["nickname"].lower() == nickname.lower():
            return jsonify({"erro": "Nickname já está em uso"}), 409

    # Criptografia correta usando bcrypt
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    senha_hash_str = hash_bytes.decode("utf-8")

    novo_usuario = {
        "id": dados["proximo_usuario_id"],
        "nickname": nickname,
        "senha": senha_hash_str,
        "perfil": perfil
    }

    dados["usuarios"].append(novo_usuario)
    dados["proximo_usuario_id"] += 1
    
    salvar_dados(dados)

    return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    corpo = request.get_json()
    nickname = corpo.get("nickname", "").strip()
    senha = corpo.get("senha", "").strip()

    if not nickname or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    dados = ler_dados()
    usuario_encontrado = None

    # Busca o usuário
    for usuario in dados["usuarios"]:
        if usuario["nickname"].lower() == nickname.lower():
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        return jsonify({"erro": "Usuário ou senha incorreto"}), 401

    # Verificação correta usando bcrypt
    senha_bytes = senha.encode("utf-8")
    hash_bytes = usuario_encontrado["senha"].encode("utf-8")
    if not bcrypt.checkpw(senha_bytes, hash_bytes):
        return jsonify({"erro": "Usuário ou senha incorreto"}), 401

    # ==========================================================
    # CORREÇÃO DA SESSÃO: Limpa sessões velhas e força a gravação
    # ==========================================================
    session.clear() 
    session["usuario"] = {
        "id": usuario_encontrado["id"],
        "nickname": usuario_encontrado["nickname"],
        "perfil": usuario_encontrado["perfil"]
    }
    session.modified = True # ISSO FORÇA O FLASK A MANDAR O COOKIE PRO NAVEGADOR!

    return jsonify({
        "mensagem": "Login realizado!", 
        "usuario": session["usuario"]
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("usuario", None)
    return jsonify({"mensagem": "Logout realizado com sucesso!"}), 200
