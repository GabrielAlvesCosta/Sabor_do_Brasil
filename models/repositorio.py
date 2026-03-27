import json
import os
from models.usuario import Usuario
from models.receita import Receita

class RepositorioUsuarios:
    ARQUIVO = "usuarios.json"

    def listar(self) -> list[Usuario]:
        if not os.path.exists(self.ARQUIVO):
            return []
        with open(self.ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return [Usuario.from_dict(d) for d in dados]

    def buscar_por_nickname(self, nickname: str) -> Usuario | None:
        nickname_lower = nickname.lower()
        for usuario in self.listar():
            if usuario.nickname.lower() == nickname_lower:
                return usuario
        return None

    def nickname_existe(self, nickname: str) -> bool:
        return self.buscar_por_nickname(nickname) is not None

    def salvar(self, usuario: Usuario) -> bool:
        try:
            usuarios = self.listar()
            usuarios.append(usuario)
            self._persistir(usuarios)
            return True
        except Exception:
            return False

    def _persistir(self, usuarios: list[Usuario]) -> None:
        with open(self.ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in usuarios], f, indent=4)


class RepositorioReceitas:
    ARQUIVO = "receitas.json"

    def listar(self) -> list[Receita]:
        if not os.path.exists(self.ARQUIVO):
            self._criar_dados_iniciais()
            
        with open(self.ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return [Receita.from_dict(d) for d in dados]

    def buscar_por_id(self, receita_id: int) -> Receita | None:
        for receita in self.listar():
            if receita.id == receita_id:
                return receita
        return None

    def salvar_todas(self, receitas: list[Receita]) -> bool:
        try:
            with open(self.ARQUIVO, "w", encoding="utf-8") as f:
                json.dump([r.to_dict() for r in receitas], f, indent=4)
            return True
        except Exception:
            return False

    def _criar_dados_iniciais(self):
        # Cria algumas receitas base caso o arquivo não exista
        iniciais = [
            Receita(1, "Feijoada", "A clássica feijoada brasileira com carnes selecionadas.", "🍲"),
            Receita(2, "Pão de Queijo", "Tradicional receita mineira, crocante por fora e macio por dentro.", "🧀"),
            Receita(3, "Brigadeiro", "O doce mais amado do Brasil, feito com chocolate e leite condensado.", "🍫")
        ]
        self.salvar_todas(iniciais)