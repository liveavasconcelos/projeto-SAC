"""Representa a vaga e valida os requisitos antes da análise."""

from dataclasses import dataclass
from decimal import Decimal

from .requisito import Requisito
from ..utils.validacoes import texto_obrigatorio


@dataclass(frozen=True)
class Vaga:
    # Nome da vaga apresentado no cadastro e nos relatórios.
    nome: str

    # Critérios cadastrados manualmente para analisar os currículos.
    requisitos: tuple[Requisito, ...]

    def __post_init__(self):
        # Remove espaços nas extremidades e impede nome vazio.
        object.__setattr__(
            self,
            "nome",
            texto_obrigatorio(self.nome),
        )

        # Guarda os requisitos em uma coleção imutável.
        object.__setattr__(
            self,
            "requisitos",
            tuple(self.requisitos),
        )

        # Impede a criação de uma vaga com configuração inválida.
        self.validar()

    def validar(self) -> None:
        """Exige requisitos distintos e pesos totalizando exatamente 100%."""

        # Uma vaga precisa de pelo menos um requisito para ser analisada.
        if not self.requisitos:
            raise ValueError("Cadastre pelo menos um requisito.")

        # Compara os nomes sem diferenciar maiúsculas de minúsculas.
        nomes = [
            requisito.nome.casefold()
            for requisito in self.requisitos
        ]

        # Impede critérios duplicados no cadastro.
        if len(nomes) != len(set(nomes)):
            raise ValueError(
                "Os requisitos devem ter nomes diferentes."
            )

        # Decimal evita imprecisão na soma de pesos com casas decimais.
        total = sum(
            (requisito.peso for requisito in self.requisitos),
            Decimal("0"),
        )
        total_obrigatorio = Decimal("100")

        # Bloqueia a análise quando a soma estiver abaixo de 100%.
        if total < total_obrigatorio:
            faltante = total_obrigatorio - total
            raise ValueError(
                f"A soma dos pesos deve ser exatamente 100%. "
                f"Total atual: {total:.2f}%. "
                f"Faltam {faltante:.2f} pontos percentuais. "
                "Corrija os pesos para continuar."
            )

        # Bloqueia a análise quando a soma ultrapassar 100%.
        if total > total_obrigatorio:
            excedente = total - total_obrigatorio
            raise ValueError(
                f"A soma dos pesos deve ser exatamente 100%. "
                f"Total atual: {total:.2f}%. "
                f"O total excede o permitido em "
                f"{excedente:.2f} pontos percentuais. "
                "Corrija os pesos para continuar."
            )

        # Quando a soma é exatamente 100%, a validação termina
        # normalmente e permite continuar o fluxo do sistema.