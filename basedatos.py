# bbdd.py
import psycopg2
from datetime import datetime
import bcrypt  # Para cifrar las contraseñas

def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname="proyectoRafa",
            user="postgres",
            password="1234",
            host="192.160.51.164",  # Cambiar a la IP de tu servidor si es necesario
            port="5432",
            client_encoding="UTF8"
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Error de conexión a PostgreSQL:", e)
        return None

def verificar_usuario(usuario, password):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        # Comprobar si el valor ingresado es un email o un nombre de usuario
        query = "SELECT * FROM users WHERE (email = %s OR username = %s)"
        cur.execute(query, (usuario, usuario))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):  # Comparar contraseñas cifradas
            # Actualizamos el último login
            cur.execute("UPDATE users SET ultimo_login = %s WHERE email = %s", (datetime.now(), user[3]))  # Usamos el email para actualizar el último login
            conn.commit()
            return user
        return None
    finally:
        cur.close()
        conn.close()

def registrar_usuario(nombre_usuario, apellidos_usuario, email, password, fecha_nacimiento):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        # Verificar si el nombre de usuario o el email ya están registrados
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return "Error: Email ya registrado"

        cur.execute("SELECT username FROM users WHERE username = %s", (nombre_usuario,))
        if cur.fetchone():
            return "Error: Nombre de usuario ya registrado"

        # Cifrar la contraseña antes de almacenarla
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insertar el nuevo usuario con nombre, apellidos, nombre de usuario, email, password, fecha de nacimiento y rol
        cur.execute("""
            INSERT INTO users (nombre, apellidos, username, email, password, fechaNacimiento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_usuario, apellidos_usuario, nombre_usuario, email, hashed_password.decode('utf-8'), fecha_nacimiento))
        conn.commit()
        return "Usuario registrado con éxito!"
    finally:
        cur.close()
        conn.close()

def eliminar_usuario(user_id):
    conn = conectar_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))  # Usar el ID en lugar del email
        conn.commit()
        return "Usuario eliminado"
    finally:
        cur.close()
        conn.close()