# Reexporta os modelos para permitir importações como from src.models import Vaga.
"""Contratos de dados compartilhados entre os módulos."""
from .requisito import Requisito
from .vaga import Vaga
from .candidato import Candidato, ErroPDF
from .resultado import Resultado, AnaliseLote
