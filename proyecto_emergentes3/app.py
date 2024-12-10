from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret_key"

# Configuración de la base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "unidad_educativa"

# Conexión global
db = MySQLdb.connect(
    host=app.config["MYSQL_HOST"],
    user=app.config["MYSQL_USER"],
    passwd=app.config["MYSQL_PASSWORD"],
    db=app.config["MYSQL_DB"]
)

# Rutas
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin":
        return redirect(url_for('dashboard'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Rutas para estudiantes
@app.route('/estudiantes')
def estudiantes():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    data = cursor.fetchall()
    return render_template('estudiantes.html', estudiantes=data)

@app.route('/registrar_estudiante', methods=['GET', 'POST'])
def registrar_estudiante():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ci = request.form['ci']
        rude = request.form['rude']
        fecha_nacimiento = request.form['fecha_nacimiento']
        direccion = request.form['direccion']

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO estudiantes (codigo, nombre, apellido, ci, rude, fecha_nacimiento, direccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, apellido, ci, rude, fecha_nacimiento, direccion))
        db.commit()
        flash('Estudiante registrado con éxito')
        return redirect(url_for('estudiantes'))
    return render_template('registrar_estudiante.html')

@app.route('/modificar_estudiante/<id>', methods=['GET', 'POST'])
def modificar_estudiante(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ci = request.form['ci']
        rude = request.form['rude']
        fecha_nacimiento = request.form['fecha_nacimiento']
        direccion = request.form['direccion']
        
        cursor.execute("""
            UPDATE estudiantes 
            SET nombre=%s, apellido=%s, ci=%s, rude=%s, fecha_nacimiento=%s, direccion=%s 
            WHERE id=%s
        """, (nombre, apellido, ci, rude, fecha_nacimiento, direccion, id))
        db.commit()
        flash('Estudiante actualizado con éxito')
        return redirect(url_for('estudiantes'))
    cursor.execute("SELECT * FROM estudiantes WHERE id = %s", [id])
    estudiante = cursor.fetchone()
    return render_template('modificar_estudiante.html', estudiante=estudiante)

# Rutas para profesores y cursos
@app.route('/profesores')
def profesores():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM profesores")
    data = cursor.fetchall()
    return render_template('profesores.html', profesores=data)

@app.route('/cursos')
def cursos():
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.nombre, c.horario, p.nombre as profesor 
        FROM cursos c
        INNER JOIN profesores p ON c.profesor_id = p.id
    """)
    data = cursor.fetchall()
    return render_template('cursos.html', cursos=data)

if __name__ == '__main__':
    app.run(debug=True)

