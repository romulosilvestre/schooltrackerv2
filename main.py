from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
import urllib.parse

app = Flask(__name__)

# Configuração do Banco de Dados
user = 'root'
password = urllib.parse.quote_plus('1234')
host = 'localhost'
database = 'schooltracker'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

base = automap_base(metadata=metadata)
base.prepare()

Aluno = base.classes.aluno

session = sessionmaker(bind=engine)
session = session()

@app.route("/")
def index():
    mensagem = request.args.get("mensagem", "")
    return render_template("index.html", mensagem=mensagem)

@app.route("/login", methods=["POST"])
def login():
    ra = request.form["ra"]
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        return redirect(url_for("listar_alunos"))
    else:
        mensagem = "RA não encontrado. Por favor, tente novamente."
        return redirect(url_for("index", mensagem=mensagem))

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route('/novoaluno', methods=['POST'])
def inserir_aluno():
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = request.form['tempoestudo']
    rendafamiliar = request.form['rendafamiliar']
    
    aluno = Aluno(ra=ra, nome=nome, tempoestudo=tempoestudo, rendafamiliar=rendafamiliar)

    try:
        session.add(aluno)
        session.commit()
        mensagem = "Aluno cadastrado com sucesso."
    except:
        session.rollback()
        mensagem = "Erro ao cadastrar o aluno."
    finally:
        session.close()
    
    return redirect(url_for('listar_alunos', mensagem=mensagem))

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    mensagem = request.args.get("mensagem", "")
    try:
        alunos = session.query(Aluno).all()
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos"
        return render_template('index.html', mensagem=mensagem)
    finally:
        session.close()

    return render_template('listaalunos.html', alunos=alunos, mensagem=mensagem)

@app.route("/remover_aluno/<int:id>", methods=["POST", "GET"])
def remover_aluno(id):
    aluno = session.query(Aluno).filter_by(id=id).first()
    
    try:
        session.delete(aluno)
        session.commit()
        mensagem = "Aluno removido com sucesso."
    except:
        session.rollback()
        mensagem = "Erro ao remover o aluno."
    
    return redirect(url_for('listar_alunos', mensagem=mensagem))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = session.query(Aluno).get(id)
    if request.method == 'POST':
        aluno.ra = request.form['ra']
        aluno.nome = request.form['nome']
        aluno.tempoestudo = request.form['tempoestudo']
        aluno.rendafamiliar = request.form['rendafamiliar']

        try:
            session.commit()
            mensagem = "Dados atualizados com sucesso."
        except:
            session.rollback()
            mensagem = "Erro ao atualizar dados."
        finally:
            session.close()

        return redirect(url_for('listar_alunos', mensagem=mensagem))

    return render_template('editar_aluno.html', aluno=aluno)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
