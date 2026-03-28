from flask import Blueprint, render_template, request, jsonify, session
from models.repositorio import ler_dados, salvar_dados, usuario_pode_editar

receita_bp = Blueprint("receita", __name__)


@receita_bp.route("/")
def home():
    dados = ler_dados()
    usuario_logado = session.get("usuario")
    return render_template("index.html", receitas=dados["receitas"], usuario=usuario_logado)

@receita_bp.route("/curtir/<int:receita_id>", methods=["POST"])
def curtir(receita_id: int):
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"erro": "Você precisa estar logado para curtir"}), 401

    dados = ler_dados()

    for receita in dados["receitas"]:
        if receita["id"] == receita_id:
            nickname = usuario["nickname"]
            if nickname in receita["curtidas"]:
                receita["curtidas"].remove(nickname)
                acao = "removida"
            else:
                receita["curtidas"].append(nickname)
                acao = "adicionada"
            
            salvar_dados(dados)
            return jsonify({
                "mensagem": f"Curtida {acao}!",
                "total_curtidas": len(receita["curtidas"]),
                "curtiu": nickname in receita["curtidas"]
            }), 200

    return jsonify({"erro": "Receita não encontrada"}), 404

@receita_bp.route("/comentar/<int:receita_id>", methods=["POST"])
def comentar(receita_id: int):
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"erro": "Você precisa estar logado para comentar"}), 401

    corpo = request.get_json()
    texto = corpo.get("texto", "").strip()

    if not texto:
        return jsonify({"erro": "O comentário não pode estar vazio"}), 400

    dados = ler_dados()

    for receita in dados["receitas"]:
        if receita["id"] == receita_id:
            novo_comentario = {
                "id": dados["proximo_comentario_id"],
                "autor_id": usuario["id"],
                "autor_nickname": usuario["nickname"],
                "texto": texto
            }
            receita["comentarios"].append(novo_comentario)
            dados["proximo_comentario_id"] += 1
            salvar_dados(dados)
            return jsonify({
                "mensagem": "Comentário adicionado!",
                "comentario": novo_comentario,
                "total_comentarios": len(receita["comentarios"])
            }), 201

    return jsonify({"erro": "Receita não encontrada"}), 404

@receita_bp.route("/comentario/<int:comentario_id>", methods=["DELETE"])
def excluir_comentario(comentario_id: int):
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"erro": "Você precisa estar logado"}), 401

    dados = ler_dados()

    for receita in dados["receitas"]:
        for comentario in receita["comentarios"]:
            if comentario["id"] == comentario_id:
                if not usuario_pode_editar(usuario["id"], comentario["autor_id"]):
                    return jsonify({"erro": "Sem permissão para excluir este comentário"}), 403
                
                receita["comentarios"].remove(comentario)
                salvar_dados(dados)
                return jsonify({
                    "mensagem": "Comentário excluído com sucesso!",
                    "total_comentarios": len(receita["comentarios"])
                }), 200

    return jsonify({"erro": "Comentário não encontrado"}), 404

@receita_bp.route("/comentario/<int:comentario_id>", methods=["PUT"])
def editar_comentario_rota(comentario_id: int):
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"erro": "Você precisa estar logado"}), 401

    corpo = request.get_json()
    novo_texto = corpo.get("texto", "").strip()

    if not novo_texto:
        return jsonify({"erro": "O comentário não pode ficar vazio"}), 400

    dados = ler_dados()

    for receita in dados["receitas"]:
        for comentario in receita["comentarios"]:
            if comentario["id"] == comentario_id:
                if not usuario_pode_editar(usuario["id"], comentario["autor_id"]):
                    return jsonify({"erro": "Sem permissão para editar este comentário"}), 403
                
                comentario["texto"] = novo_texto
                salvar_dados(dados)
                return jsonify({"mensagem": "Comentário editado com sucesso!"})

    return jsonify({"erro": "Comentário não encontrado"}), 404