from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

def db_execute(query, params=()):
    with sqlite3.connect('pedido.db') as con:
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        return cur.fetchall()



# Cria a tabela se não existir
db_execute('''
    CREATE TABLE IF NOT EXISTS compradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        idade INTEGER,
        sexo TEXT,
        unidade TEXT,
        camiseta TEXT
    )
''')


@app.route('/')
def index():
    pedido_confirmado = request.args.get('pedido_confirmado')  # Recebe a confirmação do pedido, se houver
    return render_template('index.html', pedido_confirmado=pedido_confirmado)


@app.route('/Fazer Pedido', methods=['POST'])
def fazer_pedido():
    nome = request.form['nome']
    idade = request.form['idade']
    sexo = request.form['sexo']
    unidade = request.form['unidade']
    camiseta = request.form['camiseta']

    if nome and idade and sexo and unidade and camiseta:
        db_execute(
            'INSERT INTO compradores (nome, idade, sexo, unidade, camiseta) VALUES (?, ?, ?, ?, ?)',
            (nome, int(idade), sexo, unidade, camiseta)
        )
    # Redireciona para a página inicial com uma mensagem de confirmação
    return redirect(url_for('index', pedido_confirmado='true'))



@app.route('/compradores')
def listar_usuarios():
    compradores = db_execute('SELECT * FROM compradores')
    return render_template('compradores.html', usuarios=compradores)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    db_execute('DELETE FROM compradores WHERE id = ?', (id,))
    return redirect(url_for('listar_usuarios'))



if __name__ == '__main__':
    app.run(debug=True)
