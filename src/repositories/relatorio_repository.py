"""Organização dos arquivos gerados; sem renderização ou regra de negócio."""
# Organiza os destinos das saídas; a renderização é responsabilidade do serviço de relatório.
from datetime import datetime
from pathlib import Path
from config.configuracoes import PASTA_RELATORIOS, PASTA_GRAFICOS
from ..utils.formatacao import nome_seguro_arquivo


def garantir_pastas_saida():
    # Cria as pastas de relatório e gráficos quando necessário, incluindo diretórios intermediários.
    PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)


def novo_caminho_relatorio(vaga: str) -> Path:
    # Combina nome seguro da vaga e horário com microssegundos para distinguir as exportações.
    garantir_pastas_saida()
    # Inclui microssegundos no identificador para distinguir execuções próximas.
    instante = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # Usa o diretório centralizado e um nome adequado a arquivos no Windows.
    return PASTA_RELATORIOS / f"relatorio_{nome_seguro_arquivo(vaga)}_{instante}.pdf"
