"""Validações reutilizáveis sem dependências de serviços."""
# Validações reutilizáveis para entradas, pesos, diretórios e texto extraído.
from pathlib import Path
from decimal import Decimal, InvalidOperation
import re

def texto_obrigatorio(valor: str) -> str:
    # Rejeita entradas vazias e remove somente espaços no início e no fim do texto.
    # Não aceita nome ou descrição vazios no cadastro.
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("Informe um texto não vazio.")
    return valor.strip()

def converter_peso(valor) -> Decimal:
    # Até duas casas decimais; Decimal evita imprecisão de ponto flutuante.
    # Aceita ponto ou vírgula, até duas casas decimais e valores de 0 a 100; rejeita negativos e entradas inválidas.
    texto = str(valor).strip().replace(",", ".")
    # Restringe o formato antes da conversão, rejeitando letras, sinais e notação científica.
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", texto):
        raise ValueError("Peso inválido: use número de 0 a 100, com até duas casas decimais.")
    try:
        peso = Decimal(texto)
    except InvalidOperation as erro:
        raise ValueError("Peso inválido.") from erro
    # Impõe a faixa percentual e permite zero quando o usuário assim definir.
    if not Decimal("0") <= peso <= Decimal("100"):
        raise ValueError("O peso deve estar entre 0 e 100.")
    return peso


def validar_pasta(pasta: Path) -> Path:
    # Distingue caminho inexistente de caminho que é arquivo, antes de tentar localizar os PDFs.
    pasta = Path(pasta)
    # Distingue pasta ausente de outros problemas de entrada.
    if not pasta.exists():
        raise FileNotFoundError(f"A pasta não existe: {pasta}")
    # Evita tentar listar um arquivo como se fosse diretório.
    if not pasta.is_dir():
        raise NotADirectoryError(f"O caminho não é uma pasta: {pasta}")
    return pasta


def validar_texto_extraido(texto: str) -> str:
    # Rejeita conteúdo vazio ou só com espaços, pois esta versão trabalha exclusivamente com PDFs textuais.
    # Um PDF sem texto útil não recebe pontuação nem participa do ranking.
    if not texto.strip():
        raise ValueError("PDF sem texto extraível. Esta versão não executa OCR.")
    return texto
