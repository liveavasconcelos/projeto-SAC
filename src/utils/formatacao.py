"""Formatação de saída; não transforma o texto usado na análise."""
# Funções de apresentação; não modificam o conteúdo textual usado na correspondência literal.
import re


def formatar_percentual(valor):
    # Padroniza a apresentação com duas casas decimais; None significa aderência não aplicável.
    return "Não se aplica" if valor is None else f"{valor:.2f}%"


def nome_seguro_arquivo(texto: str) -> str:
    # Retira caracteres impróprios do nome de saída, preservando um identificador curto para a vaga.
    nome = re.sub(r"[^a-zA-Z0-9_-]+", "_", texto).strip("_")
    return (nome or "SAC")[:60]
