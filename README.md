# Projeto SchoolTracker

Projeto SchoolTracker é uma aplicação desenvolvida no Senai Taguatinga utilizando Python e Flask. O objetivo do projeto é permitir a adição de estudantes a um banco de dados, possibilitar a criação de diários de bordo para registrar as aulas, e permitir que os dados dos alunos sejam alterados ou removidos conforme necessário.

## Funcionalidades

- Adicionar estudantes ao banco de dados.
- Criar e armazenar diários de bordo para as aulas.
- Listar todos os alunos cadastrados.
- Editar informações de estudantes (RA, nome, tempo de estudo, renda familiar).
- Remover estudantes do banco de dados.
- Interface simples para entrada e manipulação de dados.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework utilizado para o desenvolvimento da aplicação web.
- **MySQL**: Banco de dados para armazenamento dos estudantes e diários de bordo.
- **SQLAlchemy**: Toolkit SQL para interagir com o banco de dados MySQL.
- **HTML/CSS**: Interface básica para interação com o usuário.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/henriqueserafin/projeto-schooltracker.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd projeto-schooltracker
    ```

3. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    source venv/bin/activate  # No Linux/MacOS
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Configure o banco de dados MySQL com as credenciais adequadas no arquivo principal do projeto (`app.py`).

6. Execute a aplicação:
    ```bash
    python app.py
    ```

## Uso

1. Acesse a aplicação via navegador em `http://127.0.0.1:5001/`.
2. Na página principal, você pode visualizar a lista de alunos cadastrados, adicionar novos alunos, editar informações existentes ou remover alunos do banco de dados.
3. Para adicionar ou editar um aluno, utilize os formulários disponíveis nas respectivas páginas de cadastro e edição.
4. As alterações são salvas automaticamente no banco de dados.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask.
- `templates/`: Diretório que contém os arquivos HTML.
- `static/`: Diretório para arquivos estáticos como CSS.

## Diagrama de Sequência

```mermaid
sequenceDiagram
    participant User as Usuário
    participant Browser as Navegador
    participant Flask as Servidor Flask
    participant DB as Banco de Dados

    User->>Browser: Acessa "/"
    Browser->>Flask: GET "/"
    Flask->>Browser: render_template("index.html")

    User->>Browser: Acessa "/cadastro"
    Browser->>Flask: GET "/cadastro"
    Flask->>Browser: render_template("cadastro.html")

    User->>Browser: Submete formulário de novo aluno
    Browser->>Flask: POST "/novoaluno"
    Flask->>Flask: session.add(aluno)
    Flask->>DB: session.commit()
    DB-->>Flask: Confirmação de inserção
    Flask->>Browser: redirect(url_for('listar_alunos'))

    User->>Browser: Acessa "/alunos"
    Browser->>Flask: GET "/alunos"
    Flask->>DB: Buscar todos os alunos
    DB-->>Flask: Retorna lista de alunos
    Flask->>Browser: render_template('listaalunos.html', alunos=alunos)

    User->>Browser: Clica em "Remover"
    Browser->>Flask: GET "/remover_aluno/<id>"
    Flask->>DB: Buscar aluno por ID
    Flask->>Flask: session.delete(aluno)
    Flask->>DB: session.commit()
    DB-->>Flask: Confirmação de deleção
    Flask->>Browser: redirect(url_for('listar_alunos'))

    User->>Browser: Clica em "Alterar"
    Browser->>Flask: GET "/editar/<id>"
    Flask->>DB: Buscar aluno por ID
    DB-->>Flask: Retorna dados do aluno
    Flask->>Browser: render_template('editar_aluno.html', aluno=aluno)

    User->>Browser: Submete formulário de edição
    Browser->>Flask: POST "/editar/<id>"
    Flask->>Flask: Atualizar dados do aluno
    Flask->>DB: session.commit()
    DB-->>Flask: Confirmação de atualização
    Flask->>Browser: redirect(url_for('listar_alunos'))
