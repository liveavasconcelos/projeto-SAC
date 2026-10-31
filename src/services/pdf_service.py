"""Extração textual com PyMuPDF, sem OCR e com falhas isoladas por arquivo."""
# Processamento de PDFs com PyMuPDF, sem envio externo e sem OCR.
from pathlib import Path
import re
import pymupdf
from ..models import Candidato, ErroPDF
from ..utils.validacoes import validar_texto_extraido

def identificar_nome(texto: str, arquivo: Path) -> str:
    # Política conservadora: só aceita um nome explicitamente rotulado no início.
    # Procura um nome plausível rotulado nas cinco primeiras linhas; usa o arquivo como alternativa.
    # Limita a heurística de nome ao início do currículo.
    for linha in texto.splitlines()[:5]:
        # Aceita rótulos explícitos Nome: e Nome completo:, sem interpretar o conteúdo por IA.
        busca = re.fullmatch(r"\s*(?:nome|nome completo)\s*:\s*(.+?)\s*", linha, re.IGNORECASE)
        if busca:
            nome = busca.group(1)
            palavras = nome.split()
            # Desconsidera partículas do nome ao exigir ao menos dois componentes principais.
            principais = [p for p in palavras if p.casefold() not in {"de", "da", "do", "dos", "das", "e"}]
            if (2 <= len(palavras) <= 6 and len(principais) >= 2 and len(nome) <= 80
                    and all(p[0].isupper() and all(c.isalpha() or c in "'-’" for c in p)
                            for p in palavras if p.casefold() not in {"de", "da", "do", "dos", "das", "e"})
                    and all(any(c.isalpha() for c in p) for p in palavras)):
                return nome
    # Fallback: mantém a identificação pelo arquivo sem a extensão .pdf.
    return Path(arquivo).stem


def extrair_texto_pdf(arquivo: Path) -> str:
    # Abre o PDF local, reúne o texto das páginas e rejeita senha ou ausência de texto; não executa OCR.
    # O gerenciador de contexto fecha o documento mesmo se ocorrer falha.
    with pymupdf.open(str(arquivo)) as documento:
        # Arquivos protegidos por senha são registrados como não suportados nesta versão.
        if documento.is_encrypted:
            raise ValueError("PDF protegido por senha; não suportado nesta versão.")
        # Reúne o texto extraível das páginas e preserva uma separação entre elas.
        texto = "\n".join(pagina.get_text("text") for pagina in documento)
    # Rejeita documentos sem texto aproveitável; não tenta reconhecer letras em imagens.
    return validar_texto_extraido(texto)


def processar_curriculos(arquivos: list[Path]) -> tuple[list[Candidato], list[ErroPDF]]:
    # Processa cada arquivo isoladamente e devolve duas listas: candidatos extraídos e erros registrados.
    candidatos, erros = [], []
    # Cada tentativa tem seu próprio tratamento de erro para não interromper o lote.
    for arquivo in arquivos:
        try:
            texto = extrair_texto_pdf(arquivo)
            candidatos.append(Candidato(identificar_nome(texto, arquivo), arquivo, texto))
        # Captura falhas na fronteira de leitura de um arquivo e registra a causa.
        except Exception as erro:
            # Fronteira por arquivo: uma falha de extração não interrompe o lote.
            mensagem = f"{type(erro).__name__}: {erro}"
            erros.append(ErroPDF(arquivo, mensagem))
            print(f"Erro em {arquivo.name}: {mensagem}")
    return candidatos, erros
