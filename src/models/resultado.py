"""Resultado individual e resumo do lote."""
# Contratos de saída que abastecem o ranking, as tabelas, os gráficos e o PDF.
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from .candidato import Candidato, ErroPDF
from .vaga import Vaga

@dataclass
# Guarda a avaliação de um currículo e as informações que serão apresentadas ao recrutador.
class Resultado:
    # Documento/candidato ao qual esta avaliação pertence.
    candidato: Candidato
    # Identifica aprovação na triagem ou eliminação da classificação, sem decisão definitiva de contratação.
    situacao: str
    # Nomes dos requisitos encontrados. default_factory cria uma lista independente por resultado.
    atendidos: list[str] = field(default_factory=list)
    # Nomes dos requisitos não encontrados; cada candidato possui sua própria lista.
    ausentes: list[str] = field(default_factory=list)
    # Subconjunto eliminatório dos ausentes, usado para justificar a exclusão do ranking.
    obrigatorios_ausentes: list[str] = field(default_factory=list)
    # Percentual dos elegíveis; None indica que o cálculo não se aplica ao eliminado.
    aderencia: Decimal | None = None
    # Posição sequencial no ranking; None indica que o candidato ficou fora dele.
    posicao: int | None = None

    @property
    def elegivel(self) -> bool:
        # Indica atendimento aos obrigatórios na triagem; não representa decisão de contratação.
        return self.situacao == "APROVADO NA TRIAGEM" and not self.obrigatorios_ausentes

    @property
    def motivo_eliminacao(self) -> str:
        # Produz a justificativa textual com os nomes dos obrigatórios ausentes para o relatório.
        if not self.obrigatorios_ausentes:
            return ""
        return "Não atendimento de requisito(s) obrigatório(s): " + "; ".join(self.obrigatorios_ausentes)

@dataclass
# Reúne os resultados e erros de uma execução para manter tabelas, gráficos e PDF consistentes.
class AnaliseLote:
    # Critérios e pesos usados nesta análise, também registrados no PDF.
    vaga: Vaga
    # Data/hora local da análise, incluindo o fuso configurado no computador.
    data: datetime
    # Quantidade de PDFs localizados, contando também os que falharem na leitura.
    encontrados: int
    # Avaliações dos currículos processados com sucesso, inclusive eliminados.
    resultados: list[Resultado]
    # Falhas por arquivo, separadas dos resultados avaliados.
    erros: list[ErroPDF]

    @property
    def processados(self) -> int:
        # Conta apenas currículos analisados com sucesso; arquivos com erro estão em outra lista.
        return len(self.resultados)
