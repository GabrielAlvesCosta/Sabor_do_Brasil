import bcrypt
from flask import Blueprint, request, jsonify, session
from utils.utils import ler_dados, salvar_dados, hash_senha, verificar_senha


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    corpo = request.get_json()
    nickname = corpo.get("nickname", "").strip()
    senha = corpo.get("senha", "").strip()
    perfil = corpo.get("perfil", "comum").strip()

    if not nickname or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    if perfil not in ["comum", "admin"]:
        return jsonify({"erro": "Perfil inválido"}), 400

    dados = ler_dados()

    for usuario in dados["usuarios"]:
        if usuario["nickname"].lower() == nickname.lower():
            return jsonify({"erro": "Nickname já está em uso"}), 409

    senha_hash_str = hash_senha(senha)

    novo_usuario = {
        "id": dados["proximo_usuario_id"],
        "nickname": nickname,
        "senha": senha_hash_str,
        "perfil": perfil
    }

    dados["usuarios"].append(novo_usuario)
    dados["proximo_usuario_id"] += 1
    
    salvar_dados(dados)

    return jsonify({"mensagem": "Cadastro realizado com sucesso!"})


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

    if not verificar_senha(senha, usuario_encontrado["senha"]):
        return jsonify({"erro": "Usuário ou senha incorreto"}), 401


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
    return jsonify({"mensagem": "Logout realizado com sucesso!"})