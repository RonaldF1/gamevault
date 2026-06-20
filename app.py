from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_db():
    conn = sqlite3.connect('juegos.db')
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_db():
    conn = conectar_db()
    # Añadimos la columna imagen_url a la tabla
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videojuegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            estado TEXT NOT NULL,
            imagen_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = conectar_db()
    juegos = conn.execute('SELECT * FROM videojuegos').fetchall()
    
    # Calculamos estadísticas rápidas para el panel superior
    total = len(juegos)
    jugando = len([j for j in juegos if j['estado'] == 'Jugando'])
    pendientes = len([j for j in juegos if j['estado'] == 'Pendiente'])
    terminados = len([j for j in juegos if j['estado'] == 'Terminado'])
    
    conn.close()
    return render_template('index.html', juegos=juegos, total=total, jugando=jugando, pendientes=pendientes, terminados=terminados)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form.get('titulo')
    plataforma = request.form.get('plataforma', '').strip().lower()
    estado = request.form.get('estado')
    imagen_url = request.form.get('imagen_url')
    
    # Si el usuario no puso una imagen, Python elige una según la plataforma
    if not imagen_url:
        if 'pc' in plataforma:
            imagen_url = 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500' # Foto de Setup PC
        elif 'switch' in plataforma or 'nintendo' in plataforma:
            imagen_url = 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500' # Consola portátil
        elif 'playstation' in plataforma or 'ps' in plataforma:
            imagen_url = 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500' # Control PS
        elif 'xbox' in plataforma:
            imagen_url = 'https://images.unsplash.com/photo-1621259182978-f09e5e2ae090?w=500' # Xbox
        else:
            imagen_url = 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500' # Fondo retro general

    if titulo and plataforma:
        conn = conectar_db()
        conn.execute('INSERT INTO videojuegos (titulo, plataforma, estado, imagen_url) VALUES (?, ?, ?, ?)',
                     (titulo, request.form.get('plataforma'), estado, imagen_url)) # Guardamos el texto original de la plataforma
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar_db()
    conn.execute('DELETE FROM videojuegos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/cambiar_estado/<int:id>/<string:nuevo_estado>')
def cambiar_estado(id, nuevo_estado):
    conn = conectar_db()
    conn.execute('UPDATE videojuegos SET estado = ? WHERE id = ?', (nuevo_estado, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    inicializar_db()
    app.run(debug=True)
