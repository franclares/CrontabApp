import flet as ft
from basedatos import *
from datetime import datetime


def main(page: ft.Page):
    page.title = "LOGIN PAGE"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Campos de entrada
    nombre_usuario = ft.TextField(label="Nombre de Usuario", autofocus=True)
    apellidos = ft.TextField(label="Apellidos de Usuario")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña", password=True)
    fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)")
    mensaje = ft.Text()


    def set_mensaje(texto, color="green"):
        mensaje.value = texto
        mensaje.color = color
        page.update()

    def limpiar_campos():
        nombre_usuario.value = ""
        apellidos.value = ""
        email.value = ""
        password.value = ""
        fecha_nacimiento.value = ""
        mensaje.value = ""
        page.update()

    def register(e):
        try:
            # Verificar si el formato de la fecha es correcto
            datetime.strptime(fecha_nacimiento.value, "%Y-%m-%d")
        except ValueError:
            set_mensaje("Error: Formato de fecha incorrecto. Usa YYYY-MM-DD.", "red")
            return

        # Verificar que el nombre de usuario no esté vacío
        if not nombre_usuario.value:
            set_mensaje("Error: El nombre de usuario no puede estar vacío.", "red")
            return

        # Verificar que el campo de apellidos no esté vacío
        if not apellidos.value:
            set_mensaje("Error: Los apellidos no pueden estar vacíos.", "red")
            return

        # Verificar que el campo de email no esté vacío
        if not email.value:
            set_mensaje("Error: El email no puede estar vacío.", "red")
            return

        # Verificar que el campo de contraseña no esté vacío
        if not password.value:
            set_mensaje("Error: La contraseña no puede estar vacía.", "red")
            return


        # Registrar usuario con nombre de usuario, apellidos, email, password, fecha de nacimiento
        msg = registrar_usuario(nombre_usuario.value, apellidos.value, email.value, password.value,
                                fecha_nacimiento.value)
        set_mensaje(msg, "green" if "éxito" in msg else "red")
        if "éxito" in msg:
            limpiar_campos()

    def mostrar_registro(e=None):
        limpiar_campos()
        page.clean()
        page.add(
            ft.Column([
                nombre_usuario, apellidos, email, password, fecha_nacimiento, mensaje,
                ft.ElevatedButton("Registrar", on_click=register, bgcolor="green", color="white"),
                ft.ElevatedButton("Volver", on_click=mostrar_login, bgcolor="gray", color="white")
            ], alignment="center")
        )
        page.update()

    def mostrar_login(e=None):
        limpiar_campos()
        page.clean()
        email.label = "Email/Usuario"  # Cambiar la etiqueta a "Email/Usuario"
        page.add(
            ft.Column([
                email, password, mensaje,
                ft.ElevatedButton("Iniciar sesión", on_click=login, bgcolor="blue", color="white"),
                ft.ElevatedButton("Registrarse", on_click=mostrar_registro, bgcolor="green", color="white")
            ], alignment="center")
        )
        page.update()

    def login(e):
        user = verificar_usuario(email.value, password.value)
        if user:
            ultimo_login = user[9] if user[9] else "Nunca"
            set_mensaje("Login exitoso!", "green")
            page.clean()

            # Agregar un botón para iniciar la aplicación
            page.add(
                ft.ElevatedButton("Iniciar Aplicación", on_click=iniciar_aplicacion, bgcolor="blue", color="white")
            )

            page.update()
        else:
            set_mensaje("Email/Usuario o contraseña incorrectos. Por favor, intenta nuevamente.", "red")

    def iniciar_aplicacion(e):
        import tareasSistemas  # Aquí se importa el archivo ActionSelector.py
        tareasSistemas.main(page)  # Llamar a la función principal del archivo ActionSelector

    def mostrar_home(nombre_usuario, ultimo_login):
        page.clean()
        column_elements = [
            ft.Text(f"Bienvenido, {nombre_usuario}!", size=20, weight="bold", color="blue"),
            ft.Text(f"Último login: {ultimo_login}", size=14, italic=True, color="gray"),
            ft.ElevatedButton("Cerrar sesión", on_click=logout, bgcolor="blue", color="white"),
            # Botón para eliminar la cuenta
            ft.ElevatedButton("Eliminar cuenta", on_click=eliminar, bgcolor="red", color="white")
        ]

        page.add(ft.Column(column_elements, alignment="center"))
        page.update()

    def eliminar(e):
        user = verificar_usuario(email.value, password.value)
        print(f"Datos del usuario: {user}")  # Verificar que estás obteniendo toda la tupla
        if user:
            user_id = user[0]  # Obtener el ID del usuario
            print(f"El ID del usuario a eliminar es: {user_id}")  # Ver el ID
            mensaje = eliminar_usuario(user_id)  # Pasar el ID a la función de eliminación
            set_mensaje(mensaje, "green" if "eliminado" in mensaje else "red")
            limpiar_campos()
            mostrar_login()
        else:
            set_mensaje("No se pudo eliminar la cuenta.", "red")

    def logout(e):
        limpiar_campos()
        mostrar_login()

    mostrar_login()


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=30012)