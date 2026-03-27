import uuid

class Usuario:
    def __init__(self, nickname: str, senha: str, perfil="comum", id=None):
        self.id = id if id else str(uuid.uuid4())
        self.nickname = nickname
        self.senha = senha
        self.perfil = perfil

    def eh_admin(self):
        return self.perfil == "admin"
        
    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "senha": self.senha,
            "perfil": self.perfil
        }
    
    @classmethod
    def from_dict(cls, dados: dict) -> "Usuario":
        return cls(
            id=dados.get("id"),
            nickname=dados.get("nickname", ""),
            senha=dados.get("senha", ""),
            perfil=dados.get("perfil", "comum")
        )