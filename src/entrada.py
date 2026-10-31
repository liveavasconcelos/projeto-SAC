"""Cadastro no terminal e configuração JSON local, sem banco de dados."""
# Camada de apresentação textual: recebe os critérios no terminal e salva o cadastro local.
import json
from dataclasses import replace
from pathlib import Path
from .models import Requisito, Vaga
from .utils.validacoes import converter_peso, texto_obrigatorio
from config.configuracoes import ARQUIVO_VAGA



def perguntar(mensagem, conversor=texto_obrigatorio):
    # Lê a entrada e aplica o conversor recebido. Repete a pergunta se a validação levantar ValueError.
    # Mantém a etapa ativa até que a entrada ou a configuração satisfaça suas validações.
    while True:
        try:
            return conversor(input(mensagem))
        # Exibe a causa da entrada inválida para permitir a correção pelo usuário.
        except ValueError as erro:
            print(erro)


def sim_nao(valor: str) -> bool:
    # Converte s/n em True/False para controlar o cadastro e a obrigatoriedade dos requisitos.
    resposta = valor.strip().casefold()
    # Rejeita respostas diferentes das duas opções previstas no cadastro.
    if resposta not in {"s", "n"}:
        raise ValueError("Responda somente s ou n.")
    return resposta == "s"


def separar_palavras(valor: str) -> tuple[str, ...]:
    # Divide a entrada por vírgulas, limpa as extremidades e remove itens vazios e duplicados.
    # Limpa cada termo sem alterar os espaços internos de expressões como Python 3.
    palavras = [p.strip() for p in valor.split(",") if p.strip()]
    if not palavras:
        raise ValueError("Informe pelo menos uma palavra-chave.")
    # Mantém a ordem de cadastro e remove duplicatas exatas.
    return tuple(dict.fromkeys(palavras))


def cadastrar_vaga() -> Vaga:
    # Constrói a vaga com os requisitos informados no terminal e só conclui quando os pesos somam 100%.
    nome = perguntar("Informe o nome da vaga: ")
    requisitos = []
    continuar = perguntar("Deseja cadastrar um requisito? (s/n): ", sim_nao)
    # Mantém a etapa ativa até que a entrada ou a configuração satisfaça suas validações.
    while True:
        if continuar:
            descricao = perguntar("Nome/descrição do requisito: ")
            # Evita dois critérios com o mesmo nome, inclusive com diferença de caixa.
            if any(r.nome.casefold() == descricao.casefold() for r in requisitos):
                print("Este requisito já foi cadastrado. Use outro nome.")
                continue
            palavras = perguntar("Digite as palavras-chave separadas por vírgula: ", separar_palavras)
            obrigatorio = perguntar("Este requisito é obrigatório? (s/n): ", sim_nao)
            peso = perguntar("Informe o peso deste requisito: ", converter_peso)
            # Converte as respostas em um objeto Requisito validado.
            requisitos.append(Requisito(descricao, palavras, obrigatorio, peso))
            continuar = perguntar("Deseja cadastrar outro requisito? (s/n): ", sim_nao)
        # Impede encerrar o cadastro de uma vaga sem nenhum critério.
        elif not requisitos:
            print("É necessário cadastrar pelo menos um requisito.")
            continuar = perguntar("Deseja cadastrar um requisito? (s/n): ", sim_nao)
        else:
            break
    # Mantém a etapa ativa até que a entrada ou a configuração satisfaça suas validações.
    while True:
        try:
            # O construtor valida a soma dos pesos antes de liberar o processamento.
            vaga = Vaga(nome, requisitos)
            print("Pesos validados: total de 100%.")
            return vaga
        # Exibe a causa da entrada inválida para permitir a correção pelo usuário.
        except ValueError as erro:
            print(erro)
            print("Corrija os pesos dos requisitos cadastrados:")
            # Como Requisito é imutável, replace cria cópias com os pesos corrigidos.
            requisitos = [replace(r, peso=perguntar(f"Peso de {r.nome}: ", converter_peso))
                          for r in requisitos]


def solicitar_pasta() -> Path:
    # Solicita um diretório existente com PDFs e devolve seu caminho absoluto para o notebook.
    from .repositories.curriculo_repository import listar_pdfs
    # Mantém a etapa ativa até que a entrada ou a configuração satisfaça suas validações.
    while True:
        caminho = perguntar("Informe o caminho da pasta contendo os currículos PDF: ")
        # Aceita caminho copiado entre aspas e expande o atalho de pasta pessoal.
        pasta = Path(caminho.strip('"')).expanduser()
        try:
            arquivos = listar_pdfs(pasta)
            print(f"{len(arquivos)} arquivo(s) PDF encontrado(s).")
            # Só conclui a escolha quando há ao menos um PDF no diretório.
            if arquivos:
                return pasta.resolve()
            print("Nenhum PDF encontrado. Informe outra pasta.")
        except (OSError, ValueError) as erro:
            print(f"Pasta inválida: {erro}")


def salvar_configuracao(vaga: Vaga, pasta: Path, destino: Path):
    # Grava os critérios em JSON local para transportar o cadastro do terminal até o notebook.
    vaga.validar()
    # Converte objetos em estruturas JSON; pesos viram texto para preservar os decimais.
    conteudo = {"vaga": vaga.nome, "pasta_curriculos": str(pasta.resolve()),
                "requisitos": [{"nome": r.nome, "palavras_chave": list(r.palavras_chave),
                                "obrigatorio": r.obrigatorio, "peso": str(r.peso)}
                               for r in vaga.requisitos]}
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Salva a configuração com acentos preservados e codificação UTF-8.
    destino.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")


def carregar_configuracao(origem: Path) -> tuple[Vaga, Path]:
    # Reconstrói os objetos a partir do JSON. Os construtores validam novamente os dados carregados.
    try:
        # Lê somente o JSON local produzido no cadastro; não acessa serviços externos.
        dados = json.loads(origem.read_text(encoding="utf-8"))
        # **r distribui os campos de cada dicionário aos parâmetros do modelo.
        requisitos = [Requisito(**r) for r in dados["requisitos"]]
        vaga = Vaga(dados["vaga"], requisitos)
        pasta = Path(texto_obrigatorio(dados["pasta_curriculos"]))
        return vaga, pasta
    # Trata conteúdo corrompido ou incompatível como configuração inválida.
    except (KeyError, TypeError, ValueError) as erro:
        raise ValueError("Configuração inválida. Refaça o cadastro pelo terminal.") from erro


def main():
    # É o ponto de entrada do cadastro: reúne vaga e pasta e salva a configuração após a conclusão.
    try:
        vaga = cadastrar_vaga()
        pasta = solicitar_pasta()
        destino = ARQUIVO_VAGA
        salvar_configuracao(vaga, pasta, destino)
        print(f"Cadastro salvo em: {destino}")
        print("Agora execute as células do notebook SAC_principal.ipynb em ordem.")
    # Permite cancelar a entrada antes de gravar uma nova configuração.
    except (KeyboardInterrupt, EOFError):
        print("\nCadastro cancelado. Nenhuma nova configuração foi salva.")
    except OSError as erro:
        print(f"Não foi possível salvar a configuração: {erro}")


# Executa o cadastro apenas com python -m src.entrada; importar o módulo não inicia perguntas.
if __name__ == "__main__":
    main()
