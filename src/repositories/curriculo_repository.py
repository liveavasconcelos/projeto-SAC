"""Acesso ao diretório de currículos; não extrai nem analisa texto."""
# Camada de dados: conhece arquivos e diretórios, sem extrair texto nem pontuar candidatos.
from pathlib import Path
from config.configuracoes import EXTENSAO_PDF
from ..utils.validacoes import validar_pasta


def listar_pdfs(pasta: Path) -> list[Path]:
    # Localiza somente PDFs diretamente na pasta escolhida e ordena os caminhos de forma estável.
    # Valida o diretório antes de acessar seus arquivos.
    pasta = validar_pasta(pasta)
    # Filtra por extensão sem distinguir caixa e ordena para manter a sequência previsível.
    return sorted((p for p in pasta.iterdir()
                   if p.is_file() and p.suffix.casefold() == EXTENSAO_PDF),
                  key=lambda p: (p.name.casefold(), p.name))
