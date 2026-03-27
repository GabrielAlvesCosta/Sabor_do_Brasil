import uuid

class Comentario:
    def __init__(self, autor_id: str, autor_nickname: str, texto: str, id=None):
        self.id = id if id else str(uuid.uuid4())
        self.autor_id = autor_id
        self.autor_nickname = autor_nickname
        self.texto = texto

    def to_dict(self):
        return {
            "id": self.id,
            "autor_id": self.autor_id,
            "autor_nickname": self.autor_nickname,
            "texto": self.texto
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Comentario":
        return cls(
            id=dados.get("id"),
            autor_id=dados.get("autor_id", ""),
            autor_nickname=dados.get("autor_nickname", ""),
            texto=dados.get("texto", "")
        )