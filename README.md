# Projeto Diario

Projeto Diario é uma aplicação desenvolvida no Senai Taguatinga utilizando Python e Flask. O objetivo do projeto é permitir a adição de estudantes a um banco de dados e possibilitar que cada estudante crie diários de bordo para registrar suas aulas, que também são armazenados no banco de dados.

## Funcionalidades

- Adicionar estudantes ao banco de dados.
- Criar e armazenar diários de bordo para as aulas.
- Interface simples para entrada de dados.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Flask**: Framework utilizado para o desenvolvimento da aplicação web.
- **MySQL**: Banco de dados para armazenamento dos estudantes e diários de bordo.
- **SQLAlchemy**: Toolkit SQL para interagir com o banco de dados MySQL.
- **HTML/CSS**: Interface básica para interação com o usuário.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/henriqueserafin/projeto-diario.git
    ```

2. Navegue até o diretório do projeto:
    ```bash
    cd projeto-diario
    ```

3. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Configure o banco de dados MySQL com as credenciais adequadas no arquivo principal do projeto.

6. Execute a aplicação:
    ```bash
    python app.py
    ```

## Uso

1. Acesse a aplicação via navegador em `http://127.0.0.1:5001/`.
2. Na página principal, você pode entrar como um aluno já cadastrado ou se cadastrar no banco de dados.
3. Na página de adicionar um novo diário de bordo você prenche a caixa de texto utilizando o formulário disponível e seleciona enviar.
4. As entradas são salvas automaticamente no banco de dados.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask.
- `templates/`: Diretório que contém os arquivos HTML.
- `static/`: Diretório para arquivos estáticos como CSS.

# Diagrama de Sequência

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
```


## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para discussão.

## Licença

Este projeto está licenciado sob a [Apache License](LICENSE).
