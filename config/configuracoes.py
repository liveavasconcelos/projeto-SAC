"""Caminhos padrão; a pasta de entrada continua sendo informada pelo usuário."""
# Centraliza os caminhos da aplicação; a pasta de currículos usada na análise é escolhida no cadastro.
from pathlib import Path

# Obtém a raiz pela posição deste arquivo, sem depender do diretório do terminal.
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
# Sugere o local de entrada; o usuário ainda pode informar outra pasta no cadastro.
PASTA_CURRICULOS = RAIZ_PROJETO / "data" / "curriculos"
# Destino padrão dos relatórios PDF produzidos ao final do notebook.
PASTA_RELATORIOS = RAIZ_PROJETO / "outputs" / "relatorios"
# Destino padrão dos três gráficos salvos como imagens PNG.
PASTA_GRAFICOS = RAIZ_PROJETO / "outputs" / "graficos"
# Arquivo gerado pelo cadastro para ser carregado depois pelo notebook.
ARQUIVO_VAGA = RAIZ_PROJETO / "config" / "vaga.json"
# Limita a entrada ao formato PDF previsto no escopo.
EXTENSAO_PDF = ".pdf"
# Documenta a referência percentual da regra de soma igual a 100%.
PESO_TOTAL = 100
