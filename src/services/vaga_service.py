"""Operações de validação da configuração da vaga."""
# Serviço de validação chamado antes do processamento em lote.
from decimal import Decimal
from ..models import Vaga, Requisito


def somar_pesos(requisitos: tuple[Requisito, ...]) -> Decimal:
    # Soma os pesos com Decimal para manter a precisão dos percentuais cadastrados.
    return sum((r.peso for r in requisitos), Decimal("0"))


def validar_vaga(vaga: Vaga) -> None:
    # A própria Vaga mantém suas invariantes; não duplicamos a regra.
    # Reutiliza a validação do modelo, mantendo a regra de consistência em um único lugar.
    vaga.validar()
