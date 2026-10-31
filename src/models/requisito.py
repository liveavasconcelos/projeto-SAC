"""Requisito cadastrado manualmente."""
# Modelo compartilhado que mantém os dados de cada requisito válidos desde a construção.
from dataclasses import dataclass
from decimal import Decimal
from ..utils.validacoes import texto_obrigatorio, converter_peso

@dataclass(frozen=True)
# Representa um critério manual da vaga: nome, termos alternativos, obrigatoriedade e peso.
class Requisito:
    # Nome exibido para identificar este objeto no cadastro e nos resultados.
    nome: str
    # Termos cadastrados manualmente: encontrar qualquer um deles atende ao requisito.
    palavras_chave: tuple[str, ...]
    # True faz a ausência deste requisito eliminar o candidato da classificação.
    obrigatorio: bool
    # Participação do requisito no percentual, armazenada com precisão decimal.
    peso: Decimal

    def __post_init__(self):
        # Valida e prepara os campos imediatamente após a construção da dataclass.
        # Inicializa o campo validado mesmo com a dataclass marcada como frozen.
        object.__setattr__(self, "nome", texto_obrigatorio(self.nome))
        # Exige um booleano real para impedir classificação ambígua.
        if not isinstance(self.obrigatorio, bool):
            raise ValueError("A classificação deve ser obrigatória ou desejável.")
        # Evita interpretar uma única string como sequência de caracteres.
        if not isinstance(self.palavras_chave, (list, tuple)):
            raise ValueError("Informe uma lista de palavras-chave.")
        # Valida cada termo e guarda uma coleção imutável, sem duplicatas exatas.
        palavras = tuple(dict.fromkeys(texto_obrigatorio(p) for p in self.palavras_chave))
        # Um critério precisa ter ao menos um termo pesquisável.
        if not palavras:
            raise ValueError("Informe pelo menos uma palavra-chave.")
        object.__setattr__(self, "palavras_chave", palavras)
        # Converte o peso para Decimal aplicando a mesma validação usada pelo terminal.
        object.__setattr__(self, "peso", converter_peso(self.peso))
