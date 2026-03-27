from models.comentario import Comentario

class Receita:
    def __init__(self, id: int, titulo: str, descricao: str, imagem: str, curtidas=None, comentarios=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem
        self.curtidas = curtidas if curtidas is not None else []
        self.comentarios = comentarios if comentarios is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "curtidas": self.curtidas,
            "comentarios": [c.to_dict() for c in self.comentarios]
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Receita":
        comentarios_obj = [Comentario.from_dict(c) for c in dados.get("comentarios", [])]
        return cls(
            id=dados.get("id"),
            titulo=dados.get("titulo", ""),
            descricao=dados.get("descricao", ""),
            imagem=dados.get("imagem", ""),
            curtidas=dados.get("curtidas", []),
            comentarios=comentarios_obj
        )