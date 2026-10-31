# SAC — Sistema de Automação de Currículos

Projeto acadêmico da disciplina de Gerência e Projetos, desenvolvido em Python para apoiar a triagem inicial de currículos por profissionais de Recursos Humanos.

**Ambiente de utilização:** Windows, Python 3.13 de 64 bits e Jupyter Notebook, aberto no VS Code ou no navegador local.

**O SAC não utiliza inteligência artificial, APIs externas, OCR, análise semântica ou banco de dados.** Os critérios, palavras-chave e pesos são definidos manualmente pelo usuário. O uso de IA como auxílio ao desenvolvimento não integra a aplicação.

## 1. Objetivo e problemática

### Objetivo

Automatizar a comparação inicial de currículos em PDF com requisitos de uma vaga, identificando requisitos atendidos e ausentes, excluindo do ranking quem não atende aos obrigatórios e apresentando a aderência dos candidatos elegíveis.

### Problemática

Como automatizar a análise inicial de currículos de forma a auxiliar o recrutador na identificação de candidatos que atendam aos requisitos previamente definidos para uma determinada vaga?

### Apoio à decisão

O sistema não contrata nem reprova definitivamente candidatos. “Aprovado na triagem” significa atendimento dos requisitos obrigatórios cadastrados. “Eliminado da classificação” significa exclusão do ranking desta análise. A decisão final permanece com o profissional responsável pelo processo seletivo.

## 2. Funcionalidades

- Cadastro manual da vaga e dos requisitos pelo terminal.
- Uma ou mais palavras-chave por requisito, separadas por vírgula.
- Classificação de cada requisito como obrigatório ou desejável.
- Definição dos pesos e validação da soma exata de 100%.
- Escolha manual do caminho da pasta de PDFs.
- Localização e processamento de múltiplos PDFs textuais.
- Identificação simples do nome, com alternativa pelo nome do arquivo.
- Correspondência literal sem diferenciar maiúsculas de minúsculas.
- Identificação dos requisitos atendidos, ausentes e obrigatórios ausentes.
- Eliminação da classificação por ausência de qualquer obrigatório.
- Aderência e ranking dos elegíveis, com desempate determinístico.
- Tabelas de ranking, análise detalhada, erros e frequências.
- Três gráficos: aderência, requisitos encontrados e requisitos ausentes.
- Exportação automática do relatório PDF e dos gráficos PNG pela última célula do notebook.
- Registro de erros por arquivo, com continuidade do processamento dos demais.

## 3. Estrutura completa

```text
SAC/
├── config/
│   ├── __init__.py
│   └── configuracoes.py
├── data/
│   └── curriculos/
├── notebooks/
│   └── SAC_principal.ipynb
├── outputs/
│   ├── relatorios/
│   └── graficos/
├── src/
│   ├── __init__.py
│   ├── entrada.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requisito.py
│   │   ├── vaga.py
│   │   ├── candidato.py
│   │   └── resultado.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── curriculo_repository.py
│   │   └── relatorio_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vaga_service.py
│   │   ├── pdf_service.py
│   │   ├── analise_service.py
│   │   ├── ranking_service.py
│   │   ├── fluxo_service.py
│   │   └── relatorio_service.py
│   └── utils/
│       ├── __init__.py
│       ├── validacoes.py
│       └── formatacao.py
├── requirements.txt
├── GUIA_INSTALACAO.md
└── README.md
```

O arquivo `config/vaga.json` é criado automaticamente ao concluir o cadastro e não acompanha o ZIP. As pastas de entrada e saída começam vazias. Os relatórios e gráficos também são gerados durante a execução.

| Parte | Responsabilidade |
|---|---|
| `config/configuracoes.py` | Centraliza caminhos e referências do projeto. |
| `src/entrada.py` | Faz o cadastro no terminal e grava/carrega a configuração JSON local. |
| `models/requisito.py` | Representa e valida os dados de cada requisito. |
| `models/vaga.py` | Agrupa os requisitos e mantém a configuração da vaga consistente. |
| `models/candidato.py` | Representa o currículo extraído e as falhas de leitura. |
| `models/resultado.py` | Representa a avaliação individual e o resumo do lote. |
| `repositories/curriculo_repository.py` | Localiza os PDFs sem extrair ou analisar texto. |
| `repositories/relatorio_repository.py` | Prepara os diretórios e o caminho do relatório. |
| `services/vaga_service.py` | Expõe a validação da vaga para o fluxo. |
| `services/pdf_service.py` | Extrai texto, tenta identificar nomes e isola falhas por PDF. |
| `services/analise_service.py` | Verifica palavras-chave e obrigatórios. |
| `services/ranking_service.py` | Soma os pesos encontrados e ordena os elegíveis. |
| `services/fluxo_service.py` | Coordena as etapas da análise em lote. |
| `services/relatorio_service.py` | Gera tabelas, gráficos e relatório PDF. |
| `utils/validacoes.py` | Reúne validações reutilizáveis de entrada, peso, pasta e texto. |
| `utils/formatacao.py` | Padroniza percentuais e nomes dos arquivos de saída. |
| `notebooks/SAC_principal.ipynb` | Organiza a execução e a apresentação dos resultados. |
| `requirements.txt` | Lista todas as dependências diretas da execução. |
| `GUIA_INSTALACAO.md` | Contém o roteiro prático de instalação. |
| `README.md` | Documenta o projeto, sua organização, suas regras e sua utilização. |

Os arquivos `__init__.py` identificam os pacotes Python. O de `models` também reexporta os modelos para facilitar as importações. Todos os módulos e células possuem comentários explicativos em português.

## 4. Arquitetura em N Camadas

A separação é lógica e adequada a uma aplicação acadêmica local; não exige servidores nem um arquivo para cada camada.

| Camada | Implementação |
|---|---|
| Apresentação | Terminal, notebook e apresentação de tabelas/gráficos. |
| Aplicação | `fluxo_service.py` e coordenação das chamadas no notebook. |
| Negócio | Validações dos modelos e serviços de vaga, análise e ranking. |
| Processamento | Extração textual e renderização das saídas. |
| Dados | Objetos em memória, arquivos locais e repositories. |

Os modelos não importam serviços. Os serviços utilizam modelos, repositories e utilitários. O notebook chama os módulos e não concentra as regras de negócio. O JSON é somente a configuração local de uma vaga; não é um banco de dados.

## 5. Tecnologias e dependências

| Biblioteca | Finalidade |
|---|---|
| `notebook` | Ambiente Jupyter no navegador local. |
| `ipykernel` | Kernel Python para executar as células no Jupyter e no VS Code. |
| `pandas` | Tabelas e organização dos resultados. |
| `PyMuPDF` | Leitura do conteúdo textual dos PDFs. |
| `matplotlib` | Gráficos de barras. |
| `reportlab` | Construção do relatório PDF. |

`pathlib`, `decimal`, `dataclasses`, `json`, `datetime` e outros recursos usados pelo código pertencem à biblioteca padrão do Python e não precisam de instalação separada.

As faixas do `requirements.txt` permitem atualizações nas famílias indicadas, portanto não constituem um ambiente congelado. Para reproduzir exatamente um ambiente Windows validado pela equipe, registre suas versões com `python -m pip freeze` usando o Python da `.venv` e compartilhe esse registro entre as máquinas.

## 6. Instalação no Windows com Python 3.13

### 6.1 Downloads

1. Python 3.13 de 64 bits: https://www.python.org/downloads/windows/
2. VS Code: https://code.visualstudio.com/
3. No VS Code, instale as extensões **Python** e **Jupyter**, ambas da Microsoft.

Se o Python 3.13 já estiver instalado, não é necessário reinstalá-lo. Ao instalar, habilite a adição ao PATH e o launcher quando essas opções forem oferecidas. Reabra os terminais e o VS Code após a instalação.

### 6.2 Abrir a pasta correta

Extraia o ZIP em uma pasta nova. No VS Code, use **Arquivo → Abrir Pasta** e selecione `SAC`, a pasta que contém diretamente o arquivo `requirements.txt`.

Abra **Terminal → Novo Terminal** e confira:

```bat
dir requirements.txt
```

O arquivo deve ser listado. Se não aparecer, abra a pasta correta antes de continuar. Uma alternativa é abrir `SAC` no Explorador de Arquivos do Windows, digitar `cmd` na barra de endereço e pressionar Enter: o Prompt abrirá nessa pasta.

### 6.3 Criar o ambiente virtual

Execute um comando de cada vez:

```bat
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe --version
```

O resultado deve indicar Python 3.13.x. Se o launcher `py` não estiver disponível, confira `python --version`; se ele apontar para Python 3.13, use `python -m venv .venv`.

Os comandos seguintes usam diretamente o executável da `.venv`, funcionando no Prompt e no PowerShell sem ativação do ambiente.

### 6.4 Instalar as bibliotecas

```bat
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

A instalação inicial exige internet. O `pip` instala as bibliotecas e suas dependências automaticamente. O último comando deve informar `No broken requirements found.`

Confira também as importações:

```bat
.\.venv\Scripts\python.exe -c "import notebook, ipykernel, pandas, pymupdf, matplotlib, reportlab; print('Instalacao concluida!')"
```

### 6.5 Selecionar o interpretador

No VS Code, pressione `Ctrl+Shift+P`, escolha **Python: Select Interpreter** e selecione o executável `SAC/.venv/Scripts/python.exe`. Se necessário, use a opção de inserir o caminho manualmente.

## 7. Utilização do sistema

### 7.1 Preparar os currículos

Coloque PDFs textuais em `data/curriculos/` ou em outra pasta local de sua escolha. O pacote enxuto não inclui currículos de exemplo.

### 7.2 Cadastrar a vaga pelo terminal

Na pasta `SAC`, execute:

```bat
.\.venv\Scripts\python.exe -m src.entrada
```

O cadastro é feito no terminal, um requisito por vez. O sistema solicita nome da vaga, nome/descrição de cada requisito, palavras-chave separadas por vírgula, obrigatoriedade e peso. Ao terminar, valida os pesos e solicita o caminho da pasta de PDFs.

O caminho é informado pelo usuário, não fixado no código. Copie o caminho completo da pasta pelo Explorador de Arquivos. A pasta deve existir, ser um diretório e conter ao menos um PDF para concluir o cadastro.

Ao concluir, o SAC salva `config/vaga.json`. Um novo cadastro concluído substitui a configuração anterior. Não edite o JSON durante a execução.

### 7.3 Executar o notebook no VS Code

Abra `notebooks/SAC_principal.ipynb`, clique em **Selecionar Kernel** e escolha o Python da `.venv` do SAC. Execute as seis células em ordem:

| Célula | Ação |
|---|---|
| 1 | Localiza a raiz, importa os módulos e apresenta o aviso de apoio à decisão. |
| 2 | Carrega e exibe os critérios cadastrados no terminal. |
| 3 | Processa o lote e apresenta as contagens. |
| 4 | Exibe ranking, detalhes, erros e frequências. |
| 5 | Exibe os três gráficos. |
| 6 | Exporta automaticamente o PDF e os gráficos PNG. |

### 7.4 Alternativa: Jupyter no navegador

```bat
.\.venv\Scripts\python.exe -m notebook
```

Abra o notebook principal na página local e execute as células na ordem. Para encerrar o Jupyter, use `Ctrl+C` no terminal. O servidor utilizado pelo Jupyter é local, não um servidor externo de análise de currículos.

### 7.5 Encontrar as saídas

- Relatórios PDF: `outputs/relatorios/`.
- Três gráficos PNG: `outputs/graficos/`.

O notebook mostra os caminhos completos. Os nomes incluem data, hora e microssegundos para distinguir exportações. A última célula precisa ser executada para gravar as saídas.

### 7.6 Outra análise

Refaça o cadastro com `python -m src.entrada` usando o executável da `.venv`, depois reexecute todas as células. Não é necessário reinstalar as bibliotecas em cada utilização. Não misture resultados de um lote antigo com uma vaga recém-carregada.

## 8. Regras de negócio e decisões adotadas

### Cadastro e pesos

- A vaga deve ter nome não vazio e pelo menos um requisito.
- Os requisitos devem ter nomes distintos, sem diferenciar caixa na comparação dos nomes.
- Cada requisito possui pelo menos uma palavra-chave e classificação obrigatória ou desejável.
- Pesos aceitam ponto ou vírgula decimal, até duas casas, na faixa de 0 a 100.
- Valores vazios, negativos, não numéricos, infinitos ou em formatos não aceitos são rejeitados.
- A soma deve ser exatamente 100%. O cadastro solicita correção se o total for diferente.
- `Decimal` evita a imprecisão de ponto flutuante nessa validação.
- Peso zero é permitido. Um obrigatório com peso zero continua eliminatório.

### Correspondência literal

A entrada `Python, Python 3, programação Python` forma uma lista de termos. Espaços nas extremidades, itens vazios e duplicatas exatas são removidos. A expressão interna de cada termo é preservada.

Um requisito é atendido se pelo menos uma das palavras-chave ocorrer como trecho literal do texto. A comparação usa `casefold()`, sem distinguir caixa. Não remove acentos nem normaliza espaços internos ou pontuação.

Consequências do método:

- `PYTHON` corresponde a `Python`.
- `ingles` não corresponde automaticamente a `Inglês`.
- `Git` pode corresponder a um trecho de `GitHub`.
- `Não conheço Python` contém a palavra-chave e atende ao critério literal.
- Expressões equivalentes precisam ser cadastradas explicitamente; não há inferência semântica.

### Obrigatórios e aderência

Se faltar qualquer obrigatório, o candidato é eliminado da classificação. Aderência e posição ficam não aplicáveis. Ele continua visível na análise detalhada, com os obrigatórios ausentes e o motivo.

Para quem atende a todos os obrigatórios:

```text
Aderência (%) = soma dos pesos dos requisitos atendidos
```

Obrigatórios e desejáveis entram na soma. Como o total da vaga é 100%, a aderência máxima é 100%.

É permitida uma vaga sem obrigatórios: nesse caso, todos os currículos processados corretamente são elegíveis, inclusive com 0% de aderência.

### Ranking e empates

Só participam os candidatos processados corretamente e elegíveis. A ordenação considera:

1. Aderência decrescente.
2. Nome sem distinguir caixa.
3. Nome do arquivo.
4. Caminho do arquivo.

As posições são sequenciais, inclusive quando há empate de aderência. A ordem alfabética utiliza Unicode, sem regras regionais de colação.

## 9. PDFs e tratamento de erros

- São localizados apenas os PDFs diretamente na pasta informada, sem busca em subpastas.
- Extensões `.pdf` e `.PDF` são aceitas.
- A identificação de nome procura `Nome:` ou `Nome completo:` nas primeiras cinco linhas, com validação simples. Se não houver um nome plausível, usa o nome do arquivo sem extensão, por exemplo `Joao_Silva.pdf` → `Joao_Silva`.
- PDFs inválidos, protegidos por senha ou sem texto extraível são registrados como erro; os demais continuam sendo processados.
- Arquivos com erro não recebem aderência, posição ou análise fictícia de requisitos.
- Não há OCR. Em documentos mistos, somente a parte com texto extraível é avaliada.
- Se a pasta ficar vazia depois do cadastro, o processamento informa a ausência e permite apresentar um lote vazio.

## 10. Tabelas, gráficos e relatório

As tabelas são produzidas com pandas. Percentuais permanecem numéricos nos dados; a exibição os formata como porcentagem. Ausência de aderência é representada por `None`/`NaN` internamente e por “Não se aplica” na apresentação.

As frequências incluem todos os currículos processados com sucesso, inclusive eliminados. PDFs com erro não entram na base de frequências. Os três gráficos apresentam aderência dos elegíveis, requisitos mais encontrados e requisitos mais ausentes. Quando não há dados aplicáveis, aparece uma mensagem explicativa.

O relatório PDF contém vaga, data/hora local, contagens, critérios e palavras-chave, pesos, ranking, aderência, requisitos atendidos/ausentes, obrigatórios ausentes, motivos de eliminação, erros por arquivo e a mensagem de apoio à decisão. Os gráficos são exibidos no notebook e salvos separadamente em PNG; não são incorporados ao PDF.

## 11. Exemplo — DADOS FICTÍCIOS PARA TESTE

O pacote não inclui PDFs fictícios. Para demonstrar, crie os três documentos abaixo no Word e exporte como PDFs textuais para `data/curriculos/`. Os nomes e conteúdos são inteiramente fictícios.

**Ana_Teste.pdf**

```text
Nome: Ana Teste
DADOS FICTÍCIOS PARA TESTE
Conhecimentos: Python, SQL e Git.
```

**Bruno_Teste.pdf**

```text
Nome: Bruno Teste
DADOS FICTÍCIOS PARA TESTE
Conhecimentos: Python 3, SQL, Git e Inglês.
```

**Carla_Teste.pdf**

```text
Nome: Carla Teste
DADOS FICTÍCIOS PARA TESTE
Conhecimentos: Python e Git.
```

Cadastre a vaga fictícia **Desenvolvedor Python Júnior — DADOS FICTÍCIOS PARA TESTE** com estes critérios:

| Requisito | Palavras-chave | Obrigatório? | Peso |
|---|---|---|---|
| Python | Python, Python 3, programação Python | s | 40 |
| SQL | SQL | s | 30 |
| Git | Git | n | 20 |
| Inglês | Inglês, English | n | 10 |

Informe o caminho completo da pasta, conclua o cadastro e execute o notebook. Resultados esperados somente para os textos fictícios acima:

| Candidato | Atendidos | Ausentes | Situação | Aderência | Posição |
|---|---|---|---|---|---|
| Bruno Teste | Python, SQL, Git, Inglês | Nenhum | Aprovado na triagem | 100% | 1 |
| Ana Teste | Python, SQL, Git | Inglês | Aprovado na triagem | 90% | 2 |
| Carla Teste | Python, Git | SQL, Inglês | Eliminado da classificação | Não se aplica | Não se aplica |

Carla não atende SQL obrigatório. Ana soma 40 + 30 + 20 = 90%; Bruno soma 100%. O lote possui 3 encontrados, 3 processados, 1 eliminado, 2 no ranking e 0 erros.

## 12. Validação e testes

O pacote enxuto não contém a suíte de testes nem depende de pytest para executar. A suíte foi mantida fora do pacote de distribuição e executada sobre o código extraído da versão comentada: **37 testes passaram, mais 9 subcasos, em Python 3.13 no Linux**.

Os casos cobrem pesos, entradas inválidas, obrigatórios/desejáveis, aderência, eliminação, ranking/empates, múltiplos PDFs, erros, PDFs sem texto/senha, pastas, nome/fallback, configuração, tabelas, gráficos e PDF. Não se deve executar um comando de pytest esperando encontrar testes nesta distribuição enxuta.

Também foi conferido que os comentários não modificaram a árvore sintática dos módulos nem as instruções executáveis das seis células. A execução direta das células no Python 3.13 gerou o PDF e os três gráficos com um lote fictício.

**Limite da validação:** não foi realizada execução direta no Windows nem na interface do VS Code/Jupyter. O kernel Jupyter foi bloqueado pelas restrições de sockets do ambiente de validação; por isso a execução direta das células não é apresentada como teste da interface. A equipe deve conferir a instalação e o fluxo no Windows antes da apresentação.

## 13. Solução de problemas

| Problema | Verificação ou solução |
|---|---|
| `Could not open requirements file` | Execute `dir requirements.txt`. Entre na pasta `SAC` que contém esse arquivo e use exatamente `requirements.txt`, não `requerimento.txt`. |
| `py` não é reconhecido | Confira `python --version`; se for 3.13, use `python -m venv .venv`. Se nenhum existir, revise a instalação do Python/PATH. |
| Executável da `.venv` não encontrado | Confira a pasta do terminal e conclua a criação com `py -3.13 -m venv .venv`. |
| `ModuleNotFoundError` no notebook | Selecione o kernel da mesma `.venv` em que instalou as dependências. |
| Configuração não encontrada | Conclua primeiro o cadastro pelo terminal com `-m src.entrada`. |
| Nenhum PDF localizado | Confira o caminho, a extensão e se os arquivos estão diretamente na pasta, não em subpastas. |
| PDF sem texto | Utilize uma versão com texto extraível; esta versão não executa OCR. |
| Arquivo PDF protegido por senha | Forneça uma cópia textual acessível que você tenha autorização para utilizar. |
| Falha ao gravar relatório | Confira permissão de escrita na pasta de saída e a mensagem apresentada no notebook. |
| Resultados parecem ser de outra vaga | Refaça o cadastro quando necessário e execute novamente todas as células em ordem. |

## 14. Limitações e privacidade

O método literal pode contar termos fora de contexto e deixar de identificar competências descritas de outra forma. Não interpreta nível de experiência, negação, intenção, veracidade ou sinônimos. PDFs com colunas, palavras quebradas ou espaços diferentes podem produzir falhas de correspondência. A heurística de nomes não garante identificação correta.

Não há OCR, IA, análise semântica, banco de dados, autenticação, histórico de vagas ou serviços externos. A versão processa uma vaga por vez e não verifica se um documento misto contém informações adicionais apenas em imagens.

Currículos, configuração e saídas permanecem no computador. A aplicação não os envia automaticamente para a internet. Se o usuário escolher uma pasta sincronizada com nuvem por outro programa, essa sincronização está fora do controle do SAC.

Use somente dados fictícios para demonstrações e compartilhamentos. Não envie currículos reais, `config/vaga.json`, relatórios pessoais ou a pasta `.venv` a repositórios da equipe. Esta distribuição enxuta não inclui `.gitignore`; revise os arquivos que pretende versionar.

## 15. Relação com os requisitos acadêmicos

| Requisitos | Componentes principais |
|---|---|
| RF01–RF05: vaga, requisitos, classificação, pesos e validação | Entrada, modelos e vaga_service. |
| RF06–RF08 e RF19: entrada/leitura em lote e erros | Curriculo_repository, pdf_service e fluxo_service. |
| RF09–RF14: correspondência, atendidos/ausentes, obrigatórios, eliminação e aderência | Analise_service e ranking_service. |
| RF15: ranking | Ranking_service. |
| RF16–RF18: tabelas, gráficos e exportação | Relatorio_service e notebook. |
| RN01–RN04 | Cadastro prévio, classificação e validação de pesos. |
| RN05–RN08 | Obrigatórios eliminatórios, aderência e seleção dos elegíveis. |
| RN09 | Correspondência literal. |
| RN10 | Situações de triagem e aviso de apoio à decisão. |

A organização modular, o processamento em lote, a execução local e as instruções de instalação dão suporte aos requisitos não funcionais do projeto. A compatibilidade efetiva na máquina Windows deve ser confirmada pela equipe, conforme a seção de validação.

## 16. Aviso presente no relatório

> Os resultados apresentados representam uma análise automatizada baseada nos critérios e palavras-chave definidos pelo usuário e possuem caráter exclusivamente auxiliar. A decisão final sobre contratação ou reprovação permanece sob responsabilidade do profissional responsável pelo processo seletivo.
