# Guia de instalação e execução do SAC

## 1. Pré-requisitos

Para executar o projeto no Windows, é necessário ter:

- Python 3.13 instalado.
- Visual Studio Code instalado.
- Extensões **Python** e **Jupyter**, ambas da Microsoft, instaladas no VS Code.
- Conexão com a internet para instalar as bibliotecas.

Após a instalação das dependências, o processamento dos currículos é local.

## 2. Abrir o projeto

Descompacte o ZIP e, no VS Code, selecione **Arquivo → Abrir Pasta**.

Abra a pasta `SAC`, que contém diretamente o arquivo `requirements.txt`.

Em seguida, clique em **Terminal → Novo Terminal**. Pode utilizar o **PowerShell**.

## 3. Conferir a pasta do terminal

Execute:

```powershell
dir requirements.txt
```

O arquivo deve aparecer na listagem.

Se não aparecer, abra a pasta correta no VS Code e crie um novo terminal antes de continuar.

## 4. Conferir o Python

Execute:

```powershell
py -3.13 --version
```

O resultado deve indicar:

```text
Python 3.13.x
```

## 5. Criar o ambiente virtual

Execute:

```powershell
py -3.13 -m venv .venv
```

Aguarde o comando terminar. É normal não aparecer uma mensagem de sucesso.

Depois, confira se o executável foi criado:

```powershell
Test-Path .\.venv\Scripts\python.exe
```

O resultado esperado é:

```text
True
```

Se retornar `False`, confira a pasta do terminal e a mensagem apresentada durante a criação do ambiente. Não prossiga até o executável existir.

Os comandos seguintes usam diretamente o Python da `.venv`, sem precisar ativar o ambiente virtual.

## 6. Instalar as bibliotecas

Execute um comando por vez e aguarde cada um terminar:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

O segundo comando instala todas as bibliotecas indicadas no arquivo e suas dependências.

O nome correto do arquivo é **`requirements.txt`**.

Confira a instalação:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

O resultado esperado é:

```text
No broken requirements found.
```

## 7. Inserir os currículos

Coloque os currículos na pasta:

```text
SAC\data\curriculos
```

Os arquivos devem estar em formato **PDF com texto selecionável**, sem senha. Esta versão não realiza OCR para reconhecer texto em imagens digitalizadas.

## 8. Cadastrar a vaga

No terminal, permanecendo na raiz da pasta `SAC`, execute:

```powershell
.\.venv\Scripts\python.exe -m src.entrada
```

Informe:

1. Nome da vaga.
2. Nome ou descrição de cada requisito.
3. Palavras-chave separadas por vírgula.
4. Se o requisito é obrigatório: `s` ou `n`.
5. Peso do requisito.
6. Se deseja cadastrar outro requisito.

### Exemplo de critérios — DADOS FICTÍCIOS PARA TESTE

| Requisito | Palavras-chave | Obrigatório? | Peso |
|---|---|---|---|
| Python | Python, Python 3 | s | 40 |
| SQL | SQL | s | 30 |
| Git | Git | n | 20 |
| Inglês | Inglês, English | n | 10 |

A soma dos pesos deve ser exatamente **100%**. Caso contrário, o sistema solicitará a correção.

Ao terminar o cadastro dos requisitos, responda `n` à pergunta sobre cadastrar outro requisito.

## 9. Informar a pasta dos PDFs

Quando o sistema solicitar o caminho da pasta, digite:

```text
data\curriculos
```

Esse caminho relativo funciona quando o terminal está na raiz da pasta `SAC`.

Também é possível informar o caminho completo de outra pasta contendo os PDFs.

Após concluir, o sistema criará automaticamente:

```text
config\vaga.json
```

Não é necessário criar esse arquivo manualmente.

## 10. Abrir o notebook

No explorador do VS Code, abra:

```text
notebooks\SAC_principal.ipynb
```

No canto superior direito, clique em **Selecionar Kernel**.

Escolha **Ambientes Python**, se essa opção aparecer, e selecione o Python da pasta `.venv` do SAC.

## 11. Executar as células

Execute as seis células de cima para baixo, clicando no botão **▶** de cada uma. Aguarde a conclusão antes de iniciar a seguinte.

| Célula | Finalidade |
|---|---|
| 1 | Importar os módulos e localizar o projeto. |
| 2 | Carregar os critérios cadastrados no terminal. |
| 3 | Processar os currículos. |
| 4 | Apresentar tabelas e ranking. |
| 5 | Apresentar os três gráficos. |
| 6 | Exportar automaticamente o PDF e os gráficos. |

Se alguma célula apresentar erro, interrompa a sequência e verifique a mensagem antes de continuar.

## 12. Localizar os resultados

O relatório PDF será salvo em:

```text
outputs\relatorios
```

Os três gráficos PNG serão salvos em:

```text
outputs\graficos
```

O notebook também apresentará os caminhos completos dos arquivos gerados.

## 13. Próximas utilizações

Não é necessário reinstalar as bibliotecas a cada execução.

Para cadastrar outra vaga ou alterar os critérios, execute novamente:

```powershell
.\.venv\Scripts\python.exe -m src.entrada
```

Depois, abra o notebook, selecione o kernel da `.venv` e execute novamente todas as células em ordem.