"""Ordenação determinística dos candidatos aprovados na triagem."""
# Regras de pontuação e classificação para os candidatos que passaram pelos obrigatórios.
from decimal import Decimal
from ..models import Resultado, Requisito


def gerar_ranking(resultados: list[Resultado]) -> list[Resultado]:
    # Seleciona elegíveis com aderência, ordena do maior percentual para o menor e atribui posições.
    # Limpa posições anteriores caso o ranking seja gerado novamente.
    for resultado in resultados:
        resultado.posicao = None
    # Não inclui eliminados nem resultados sem percentual calculado.
    aprovados = [r for r in resultados
                 if r.situacao == "APROVADO NA TRIAGEM"
                 and not r.obrigatorios_ausentes and r.aderencia is not None]
    # O sinal negativo ordena percentuais de forma decrescente; nome e arquivo resolvem empates.
    aprovados.sort(key=lambda r: (-r.aderencia, r.candidato.nome.casefold(),
                                 r.candidato.arquivo.name.casefold(),
                                 str(r.candidato.arquivo)))
    # enumeração iniciada em 1 gera posições sequenciais, sem empates de posição.
    for posicao, resultado in enumerate(aprovados, start=1):
        resultado.posicao = posicao
    return aprovados


def verificar_elegibilidade(resultado: Resultado) -> bool:
    # Expõe a regra de elegibilidade do resultado para os demais componentes do projeto.
    return resultado.elegivel


def calcular_aderencia(requisitos_encontrados: list[Requisito]) -> Decimal:
    # Soma os pesos dos requisitos atendidos, incluindo obrigatórios e desejáveis. O total da vaga já foi validado.
    return sum((r.peso for r in requisitos_encontrados), Decimal("0"))
