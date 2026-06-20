from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_db():
    conn = sqlite3.connect('juegos.db')
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    conn = conectar_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videojuegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = conectar_db()
    juegos = conn.execute('SELECT * FROM videojuegos').fetchall()
    conn.close()
    return render_template('index.html', juegos=juegos)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('titulo')
    plataforma = request.form.get('plataforma')
    estado = request.form.get('estado')

    if titulo and plataforma:
        conn = conectar_db()
        conn.execute('INSERT INTO videojuegos (titulo, plataforma, estado) VALUES (?, ?, ?)',
                     (titulo, plataforma, estado))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)