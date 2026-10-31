"""Camada de aplicação: coordena o lote sem regras no notebook."""
# Camada de aplicação que conecta os módulos na sequência do fluxo do SAC.
from datetime import datetime
from pathlib import Path
from ..models import AnaliseLote, Vaga
from ..repositories.curriculo_repository import listar_pdfs
from .vaga_service import validar_vaga
from .pdf_service import processar_curriculos
from .analise_service import analisar_candidato
from .ranking_service import gerar_ranking


def executar_analise(vaga: Vaga, pasta: Path) -> AnaliseLote:
    # Coordena validação, localização, extração, análise e ranking, retornando um resumo único do lote.
    # Valida os critérios antes de abrir qualquer currículo.
    validar_vaga(vaga)  # Impede leitura e processamento com pesos inválidos.
    # Usa o repository para encontrar os documentos na pasta escolhida.
    arquivos = listar_pdfs(pasta)
    print(f"{len(arquivos)} arquivo(s) PDF encontrado(s).")
    if not arquivos:
        print("Nenhum PDF encontrado; não há currículos para analisar.")
    # O serviço de PDF isola falhas e devolve somente os textos lidos com sucesso.
    candidatos, erros = processar_curriculos(arquivos)
    # Aplica as mesmas regras da vaga a todos os candidatos extraídos.
    resultados = [analisar_candidato(c, vaga) for c in candidatos]
    # Atribui posições aos elegíveis; os eliminados permanecem nos detalhes do lote.
    gerar_ranking(resultados)
    # Reúne os dados para que todas as saídas usem a mesma análise.
    return AnaliseLote(vaga, datetime.now().astimezone(), len(arquivos), resultados, erros)
