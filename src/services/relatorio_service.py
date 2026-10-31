"""Tabelas, três gráficos e relatório PDF local."""
# Camada de apresentação e exportação; usa os resultados já calculados, sem analisar currículos de novo.
from pathlib import Path
from xml.sax.saxutils import escape
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle
from ..models import AnaliseLote
from ..utils.formatacao import formatar_percentual as percentual
from .ranking_service import gerar_ranking

# Texto obrigatório que explica ao leitor o caráter auxiliar da triagem.
AVISO = ("Os resultados apresentados representam uma análise automatizada baseada nos critérios "
         "e palavras-chave definidos pelo usuário e possuem caráter exclusivamente auxiliar. "
         "A decisão final sobre contratação ou reprovação permanece sob responsabilidade do "
         "profissional responsável pelo processo seletivo.")


def listar(valores):
    # Transforma nomes de requisitos em texto legível nas tabelas e no PDF; trata listas vazias.
    return "; ".join(valores) if valores else "Nenhum"


def gerar_tabelas(lote: AnaliseLote) -> dict[str, pd.DataFrame]:
    # Cria DataFrames de ranking, detalhes, erros e frequências a partir do mesmo resultado de análise.
    # Reutiliza a classificação do serviço de ranking, evitando outra regra de ordenação.
    ranking = gerar_ranking(lote.resultados)
    # Percentuais permanecem numéricos no DataFrame para permitir gráficos e formatação.
    tabela_ranking = pd.DataFrame(
        [{"Posição": r.posicao, "Candidato": r.candidato.nome,
          "Aderência": float(r.aderencia)} for r in ranking],
        columns=["Posição", "Candidato", "Aderência"])
    # Monta uma linha para cada currículo avaliado, inclusive os eliminados.
    linhas = [{"Candidato": r.candidato.nome, "Arquivo": r.candidato.arquivo.name,
               "Situação": r.situacao, "Requisitos atendidos": listar(r.atendidos),
               "Requisitos ausentes": listar(r.ausentes),
               "Obrigatórios não atendidos": listar(r.obrigatorios_ausentes),
               "Aderência": float(r.aderencia) if r.aderencia is not None else None,
               "Posição": r.posicao, "Erro": ""} for r in lote.resultados]
    # Inclui falhas como não avaliadas, sem inventar aderência ou requisitos ausentes.
    linhas.extend({"Candidato": e.arquivo.stem, "Arquivo": e.arquivo.name,
                   "Situação": "ERRO DE PROCESSAMENTO", "Requisitos atendidos": "Não avaliados",
                   "Requisitos ausentes": "Não avaliados", "Obrigatórios não atendidos": "Não avaliados",
                   "Aderência": None, "Posição": None, "Erro": e.mensagem} for e in lote.erros)
    # Declara colunas também quando não houver registros no lote.
    detalhada = pd.DataFrame(linhas, columns=["Candidato", "Arquivo", "Situação",
                           "Requisitos atendidos", "Requisitos ausentes", "Obrigatórios não atendidos",
                           "Aderência", "Posição", "Erro"])
    # Separa as falhas para consulta e apresentação específicas.
    erros = pd.DataFrame([{"Arquivo": e.arquivo.name, "Erro": e.mensagem} for e in lote.erros],
                         columns=["Arquivo", "Erro"])
    # Conta presenças e ausências somente entre currículos analisados com sucesso.
    frequencias = pd.DataFrame(
        [{"Requisito": req.nome,
          "Encontrado": sum(req.nome in r.atendidos for r in lote.resultados),
          "Ausente": sum(req.nome in r.ausentes for r in lote.resultados)}
         for req in lote.vaga.requisitos])
    return {"ranking": tabela_ranking, "detalhada": detalhada,
            "erros": erros, "frequencias": frequencias}


def gerar_graficos(lote: AnaliseLote) -> list:
    # Monta os três gráficos exigidos. Frequências usam todos os currículos processados, inclusive eliminados.
    tabelas = gerar_tabelas(lote)
    ranking, freq = tabelas["ranking"], tabelas["frequencias"]
    # Define apenas as três visualizações exigidas pelo escopo do SAC.
    series = [
        ("Aderência dos aprovados na triagem", ranking["Candidato"].tolist(),
         ranking["Aderência"].tolist(), "Aderência (%)", True),
        ("Requisitos mais encontrados", freq.sort_values("Encontrado", ascending=False, kind="stable")["Requisito"].tolist(),
         freq.sort_values("Encontrado", ascending=False, kind="stable")["Encontrado"].tolist(), "Currículos", False),
        ("Requisitos mais ausentes", freq.sort_values("Ausente", ascending=False, kind="stable")["Requisito"].tolist(),
         freq.sort_values("Ausente", ascending=False, kind="stable")["Ausente"].tolist(), "Currículos", False)]
    figuras = []
    # Produz uma figura para cada conjunto de dados preparado acima.
    for titulo, nomes, valores, eixo, porcentagem in series:
        fig, ax = plt.subplots(figsize=(9, max(3, len(nomes) * 0.4)))
        # Mostra barras apenas quando existe base de dados para a visualização.
        if nomes and (porcentagem or lote.processados):
            # Usa posições numéricas para não sobrepor pessoas com nomes iguais.
            indices = list(range(len(nomes)))
            ax.barh(indices, valores, color="#205493")
            ax.set_yticks(indices, nomes)  # Não sobrepõe candidatos com nomes iguais.
            # Coloca os primeiros itens da ordenação no topo do gráfico.
            ax.invert_yaxis()
            # O gráfico de aderência tem escala fixa de 0 a 100%.
            if porcentagem:
                ax.set_xlim(0, 100)
            else:
                from matplotlib.ticker import MaxNLocator
                # As frequências são contagens de currículos, portanto usam marcas inteiras.
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        else:
            # Apresenta uma mensagem compreensível quando não há dados para desenhar barras.
            ax.text(0.5, 0.5, "Sem dados para este gráfico", ha="center", transform=ax.transAxes)
            ax.set_yticks([])
        ax.set_title(titulo)
        ax.set_xlabel(eixo)
        if not porcentagem:
            fig.text(0.5, 0.01, "Base: currículos processados com sucesso, incluindo eliminados.",
                     ha="center", fontsize=8)
        # Ajusta o espaço para rótulos e rodapé da figura.
        fig.tight_layout(rect=(0, 0.04, 1, 1))
        figuras.append(fig)
    return figuras


def exportar_pdf(lote: AnaliseLote, destino: Path) -> Path:
    # Monta o relatório paginado com critérios, contagens, ranking, detalhes, erros e aviso de apoio à decisão.
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Carrega estilos de parágrafos, títulos e subtítulos do ReportLab.
    estilos = getSampleStyleSheet()
    estilos["BodyText"].splitLongWords = True
    # Lista ordenada dos elementos que serão distribuídos nas páginas do relatório.
    historia = []

    def adicionar(texto, estilo="BodyText"):
        # Acrescenta um parágrafo e seu espaçamento ao documento, escapando caracteres de marcação.
        # escape protege nomes e critérios com caracteres como <, > e & na marcação do PDF.
        historia.append(Paragraph(escape(str(texto)), estilos[estilo]))
        historia.append(Spacer(1, 6))

    # Reutiliza a classificação do serviço de ranking, evitando outra regra de ordenação.
    ranking = gerar_ranking(lote.resultados)
    # Conta apenas eliminações por obrigatório; falhas de leitura são contadas separadamente.
    eliminados = sum(bool(r.obrigatorios_ausentes) for r in lote.resultados)
    adicionar("SAC — Relatório de triagem", "Title")
    adicionar(f"Vaga: {lote.vaga.nome}")
    adicionar(f"Data da análise: {lote.data.strftime('%d/%m/%Y %H:%M:%S %z')}")
    adicionar(f"Encontrados: {lote.encontrados} | Processados com sucesso: {lote.processados} | "
              f"Erros: {len(lote.erros)} | Eliminados da classificação: {eliminados} | "
              f"Presentes no ranking: {len(ranking)}")
    adicionar(AVISO)
    adicionar("Critérios cadastrados", "Heading2")
    # Documenta os critérios usados para que o relatório possa ser conferido pelo RH.
    for requisito in lote.vaga.requisitos:
        tipo = "Obrigatório" if requisito.obrigatorio else "Desejável"
        adicionar(f"{requisito.nome} — {tipo} — {percentual(requisito.peso)}")
        adicionar(f"Palavras-chave: {listar(requisito.palavras_chave)}")
    adicionar("Ranking dos aprovados na triagem", "Heading2")
    # Só desenha a tabela de classificação quando houver candidatos elegíveis.
    if ranking:
        # Transforma o conteúdo em parágrafo para permitir quebra de linha dentro das células.
        celula = lambda valor: Paragraph(escape(str(valor)), estilos["BodyText"])
        linhas = [[celula(v) for v in ["Posição", "Candidato", "Aderência"]]]
        linhas.extend([[celula(r.posicao), celula(r.candidato.nome), celula(percentual(r.aderencia))]
                       for r in ranking])
        # repeatRows repete o cabeçalho quando a tabela ocupar mais de uma página.
        tabela = LongTable(linhas, colWidths=[55, 330, 110], repeatRows=1)
        tabela.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                                   ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        historia.append(tabela)
    else:
        adicionar("Nenhum candidato presente no ranking.")
    adicionar("Análise detalhada", "Heading2")
    # Apresenta a avaliação individual de todos os processados, mesmo os eliminados.
    for resultado in lote.resultados:
        adicionar(resultado.candidato.nome, "Heading3")
        adicionar(f"Arquivo: {resultado.candidato.arquivo.name}")
        adicionar(f"Situação: {resultado.situacao}")
        adicionar(f"Aderência: {percentual(resultado.aderencia)} | "
                  f"Posição: {resultado.posicao if resultado.posicao is not None else 'Não se aplica'}")
        # Cada requisito fica em um parágrafo para permitir paginação de listas extensas.
        for titulo, nomes in [("Atendidos", resultado.atendidos), ("Ausentes", resultado.ausentes),
                             ("Obrigatórios não atendidos", resultado.obrigatorios_ausentes)]:
            adicionar(titulo + ":")
            for nome in nomes or ["Nenhum"]:
                adicionar(nome)
        # Explica a exclusão do ranking listando os obrigatórios que não foram encontrados.
        if resultado.obrigatorios_ausentes:
            adicionar("Motivo: " + resultado.motivo_eliminacao)
    adicionar("Erros de processamento", "Heading2")
    # Registra arquivo e mensagem para que o usuário localize os documentos problemáticos.
    for erro in lote.erros:
        adicionar(f"Arquivo: {erro.arquivo.name}")
        adicionar(erro.mensagem)
    if not lote.erros:
        adicionar("Nenhum erro registrado.")
    # Define formato A4 e margens do arquivo de saída.
    documento = SimpleDocTemplate(str(destino), pagesize=A4, rightMargin=50,
                                 leftMargin=50, topMargin=45, bottomMargin=45)
    # Renderiza os elementos preparados em um PDF salvo localmente.
    documento.build(historia)
    return destino.resolve()


def salvar_graficos(lote: AnaliseLote, pasta: Path) -> list[Path]:
    # Exporta os três gráficos em PNG e fecha as figuras para liberar recursos gráficos.
    from datetime import datetime
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    instante = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    caminhos = []
    # Gera nomes individuais para os três PNGs desta exportação.
    for numero, figura in enumerate(gerar_graficos(lote), start=1):
        caminho = pasta / f"grafico_{instante}_{numero}.png"
        try:
            # Exporta a imagem com resolução e enquadramento adequados para leitura.
            figura.savefig(caminho, dpi=140, bbox_inches="tight")
            caminhos.append(caminho.resolve())
        # Libera a figura mesmo se a gravação de seu PNG falhar.
        finally:
            plt.close(figura)
    return caminhos
