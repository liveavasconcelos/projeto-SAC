"""Correspondência literal e requisitos obrigatórios."""
# Regras de correspondência literal e obrigatórios; não utiliza IA nem interpretação semântica.
from ..models import Candidato, Resultado, Vaga, Requisito
from .ranking_service import calcular_aderencia


def normalizar_texto(texto: str) -> str:
    # Não altera acentos, espaços internos ou pontuação.
    # Uniformiza a caixa com casefold; preserva acentos, pontuação e espaços internos da busca literal.
    return texto.casefold()


def verificar_requisito(texto: str, requisito: Requisito) -> bool:
    # Retorna True se qualquer palavra-chave cadastrada ocorrer como trecho literal no texto.
    return any(normalizar_texto(p) in normalizar_texto(texto)
               for p in requisito.palavras_chave)


def analisar_candidato(candidato: Candidato, vaga: Vaga) -> Resultado:
    # Compara cada requisito e separa atendidos/ausentes. Só atribui aderência após verificar os obrigatórios.
    # Reconfere as condições necessárias antes de analisar o currículo.
    vaga.validar()
    texto = normalizar_texto(candidato.texto)
    resultado = Resultado(candidato, "APROVADO NA TRIAGEM")
    encontrados = []
    for requisito in vaga.requisitos:
        # Basta uma das palavras-chave do critério aparecer para marcá-lo como atendido.
        if verificar_requisito(texto, requisito):
            resultado.atendidos.append(requisito.nome)
            encontrados.append(requisito)
        else:
            resultado.ausentes.append(requisito.nome)
            # Separa ausências eliminatórias das ausências apenas desejáveis.
            if requisito.obrigatorio:
                resultado.obrigatorios_ausentes.append(requisito.nome)
    # A falta de qualquer obrigatório encerra a elegibilidade para o ranking.
    if resultado.obrigatorios_ausentes:
        resultado.situacao = "ELIMINADO DA CLASSIFICAÇÃO"
        # Aderência não se aplica: RF14 prevê cálculo para aprovados na triagem.
    else:
        # Calcula a soma somente para quem cumpriu todos os obrigatórios.
        resultado.aderencia = calcular_aderencia(encontrados)
    return resultado
