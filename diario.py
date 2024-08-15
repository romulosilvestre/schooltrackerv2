from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine, text
import pymysql
import urllib.parse
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados
user = 'root'
password = urllib.parse.quote_plus('senai@123')
host = 'localhost'
database = 'schooltracker'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

@app.route('/')
def diario():
    return render_template('diario.html')

@app.route('/add_diario', methods=['POST'])
def add_diario():
    texto = request.form.get("texto")
    datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Monta a consulta SQL
    add_diario = text("INSERT INTO diariobordo (texto, datahora) VALUES (:texto, :datahora)")
    
    try:
        # Executa a consulta no banco de dados
        with engine.connect() as connection:
            connection.execute(add_diario, {'texto': texto, 'datahora': datahora})
            connection.commit()
        print(f"Entrada adicionada: {texto} em {datahora}")
        return "Entrada adicionada ao diário de bordo com sucesso!"
    except Exception as e:
        print(f"Erro ao adicionar entrada: {e}")
        return "Ocorreu um erro ao adicionar a entrada ao diário de bordo."

if __name__ == '__main__':
    app.run(debug=True)
