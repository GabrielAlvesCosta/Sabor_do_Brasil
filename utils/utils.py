import json
import bcrypt
from bcrypt import checkpw

ARQUIVO_DADOS = "usuarios.json"

def ler_dados():
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)

def usuario_pode_editar(id_usuario_acao: int, id_autor_comentario: int) -> bool:
    dados = ler_dados()
    for usuario in dados.get("usuarios", []):
        if usuario["id"] == id_usuario_acao:
            if usuario["perfil"] == "admin" or id_usuario_acao == id_autor_comentario:
                return True
    return False

def hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")

def verificar_senha(senha_texto_puro: str, senha_hash: str) -> bool:
    senha_bytes = senha_texto_puro.encode("utf-8")
    hash_bytes = senha_hash.encode("utf-8")
    return checkpw(senha_bytes, hash_bytes)