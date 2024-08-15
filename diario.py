from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
import pymysql
import urllib.parse

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar flash messages

# Configurações do banco de dados
user = 'root'
password = urllib.parse.quote_plus('1234')
host = 'localhost'
database = 'schooltracker'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

# Rota para a tela de login (index)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página do diário de bordo
@app.route('/diario')
def diario():
    return render_template('diario.html')

@app.route('/add_diario', methods=['POST'])
def add_diario():
    texto = request.form.get("texto")
    
    add_diario = text("INSERT INTO diariobordo (texto) VALUES (:texto)")
    
    try:
        with engine.connect() as connection:
            connection.execute(add_diario, {'texto': texto})
            connection.commit()
        flash("Entrada adicionada ao diário de bordo com sucesso!")
        return redirect(url_for('diario'))
    except Exception as e:
        flash(f"Ocorreu um erro ao adicionar a entrada ao diário de bordo: {e}")
        return redirect(url_for('diario'))

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