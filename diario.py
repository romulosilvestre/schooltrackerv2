from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
import pymysql
import urllib.parse
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sai_da_venv_vei-Professor_Romulo-2024'  # Necessário para usar flash messages

# Configurações do banco de dados
user = 'root'
password = urllib.parse.quote_plus('1234')  # Atualize com a senha do seu banco de dados
host = 'localhost'
database = 'schooltracker'  # Atualize com o nome do seu banco de dados
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

# rota pra home (index)
@app.route('/')
def index():
    return render_template('index.html')

# rota pro diario de bordo
@app.route('/diario')
def diario():
    return render_template('diario.html')

@app.route('/add_diario', methods=['POST'])
def add_diario():
    texto = request.form.get("texto")
    # Passei cerca de 2 horas por causa de datahora por não lembrar que ele era notnull 💀💀💀💀💀💀💀 
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # pega as variaveis e joga no bd
    add_diario = text("INSERT INTO diariobordo (texto, datahora) VALUES (:texto, :datahora)")
    
    # with engine.connect() as connection:
    # connection.execute(some_table.insert(), {"x": 7, "y": "this is some data"})
    # connection.execute(
    #     some_other_table.insert(), {"q": 8, "p": "this is some more data"}
    # )

    # connection.commit()  # commit the transaction
    try:
        # ve se deu certo
        with engine.connect() as connection:
            connection.execute(add_diario, {'texto': texto, 'datahora': datahora})
            connection.commit()
        print(f"Entrada adicionada: {texto} em {datahora}")
        return "Entrada adicionada ao diário de bordo com sucesso!"
    except Exception as e:
        print(f"Erro ao adicionar entrada: {e}")
        return "Ocorreu um erro ao adicionar a entrada ao diário de bordo."

# Rota para verificar o RA e permitir acesso ao diário de bordo
@app.route('/login', methods=['POST'])
def login():
    ra = request.form.get("ra")
    
    # Consulta SQL para verificar se o RA existe
    verifica_ra = text("SELECT COUNT(*) FROM aluno WHERE ra = :ra")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(verifica_ra, {'ra': ra}).scalar()
        
        if result > 0:
            # RA encontrado, redireciona para a página do diário
            return redirect(url_for('diario'))
        else:
            # RA não encontrado, mostra mensagem de erro
            flash("RA não encontrado. Por favor, cadastre-se primeiro.")
            return redirect(url_for('index'))
    except Exception as e:
        flash(f"Ocorreu um erro ao verificar o RA: {e}")
        return redirect(url_for('index'))

# Rota para adicionar uma nova entrada ao diário de bordo


# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota para processar o cadastro do aluno
@app.route('/novoaluno', methods=['POST'])
def novoaluno():
    nome = request.form.get("nome")
    ra = request.form.get("ra")
    tempoestudo = request.form.get("tempoestudo")
    rendafamiliar = request.form.get("rendafamiliar")
    
    # Monta a consulta SQL
    add_aluno = text("INSERT INTO aluno (ra, nome, tempoestudo, rendafamiliar) VALUES (:ra, :nome, :tempoestudo, :rendafamiliar)")
    
    try:
        # Executa a consulta no banco de dados
        with engine.connect() as connection:
            connection.execute(add_aluno, {'ra': ra, 'nome': nome, 'tempoestudo': tempoestudo, 'rendafamiliar': rendafamiliar})
            connection.commit()
        flash("Aluno cadastrado com sucesso!")
        return redirect(url_for('cadastro'))
    except Exception as e:
        flash(f"Ocorreu um erro ao cadastrar o aluno: {e}")
        return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
