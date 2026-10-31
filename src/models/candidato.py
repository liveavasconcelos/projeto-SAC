"""Currículo extraído e erro de leitura."""
# Contratos de dados usados pelo serviço de extração e pela análise.
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
# Transporta o nome identificado, o arquivo de origem e o texto extraído entre as camadas.
class Candidato:
    # Nome exibido para identificar este objeto no cadastro e nos resultados.
    nome: str
    # Caminho do PDF de origem, mantido para rastrear o resultado ou a falha.
    arquivo: Path
    # Conteúdo textual extraído, usado somente no processamento local.
    texto: str

@dataclass(frozen=True)
# Registra o arquivo e a causa da falha, sem criar um candidato artificial para um PDF inválido.
class ErroPDF:
    # Caminho do PDF de origem, mantido para rastrear o resultado ou a falha.
    arquivo: Path
    # Descrição da falha apresentada ao usuário e incluída no relatório.
    mensagem: str
