import flet as ft
import os
import signal
from crontab import CronTab


def main(page: ft.Page):
    # Configuración de la página con fondo negro y textos claros
    page.title = "SELECCIONAR OPCIÓN"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#000000"  # Fondo negro

    def ir_a_vista(e):
        page.clean()

        if opcion_drop.value == "Control Usuarios":
            user_control()
        elif opcion_drop.value == "Copia Seguridad":
            copia_seguridad()

    # Dropdown con estilo
    opcion_drop = ft.Dropdown(
        label="Selecciona opción",
        width=400,
        options=[ft.DropdownOption("Control Usuarios"), ft.DropdownOption("Copia Seguridad")],
        on_change=ir_a_vista,
        border_color="#4a6fa5",
        focused_border_color="#166084",
        filled=True,
        bgcolor="#333333",  # Fondo gris oscuro
        color="#ffffff"  # Texto blanco
    )

    # Vista principal con más color
    def vista_principal():
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Selecciona una opción:", size=20, weight="bold", color="#ffffff"),
                    opcion_drop
                ],
                alignment="center",
                horizontal_alignment="center"
            )
        )

    def user_control():
        page.clean()

        pid_input = ft.TextField(
            label="Introduce el PID",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color="#4a6fa5",
            focused_border_color="#166084",
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )
        result_text = ft.Text(color="#ffffff")  # Texto blanco

        def kill_process(e):
            try:
                pid = int(pid_input.value)
                os.kill(pid, signal.SIGKILL)
                result_text.value = f"Proceso {pid} finalizado con éxito."
                result_text.color = "green"
            except ValueError:
                result_text.value = "Introduce un número válido."
                result_text.color = "red"
            except ProcessLookupError:
                result_text.value = f"No se encontró el proceso con PID {pid}."
                result_text.color = "red"
            except PermissionError:
                result_text.value = "No tienes permisos para finalizar este proceso."
                result_text.color = "red"

            page.update()

        btn_kill = ft.ElevatedButton(
            "Finalizar Proceso",
            on_click=kill_process,
            color="white",
            bgcolor="#e74c3c",  # Rojo
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            )
        )

        btn_volver = ft.ElevatedButton(
            "Volver",
            on_click=lambda e: vista_principal(),
            color="white",
            bgcolor="#3498db",  # Azul
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            )
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Control de Usuarios", size=20, weight="bold", color="#ffffff"),
                    pid_input,
                    btn_kill,
                    result_text,
                    btn_volver
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20
            )
        )

    def copia_seguridad():
        page.clean()

        src_input = ft.TextField(
            label="Directorio de Origen",
            width=400,
            border_color="#4a6fa5",
            focused_border_color="#166084",
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )

        dest_input = ft.TextField(
            label="Directorio de Destino",
            width=400,
            border_color="#4a6fa5",
            focused_border_color="#166084",
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )

        days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        day_dropdown = ft.Dropdown(
            label="Día de la Semana",
            width=400,
            options=[ft.DropdownOption(i) for i in days_of_week],
            border_color="#4a6fa5",
            focused_border_color="#166084",
            filled=True,
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )

        minutes = [str(i).zfill(2) for i in range(60)]
        hours = [str(i).zfill(2) for i in range(24)]

        minute_dropdown = ft.Dropdown(
            label="Minuto",
            width=400,
            options=[ft.DropdownOption(i) for i in minutes],
            border_color="#4a6fa5",
            focused_border_color="#166084",
            filled=True,
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )

        hour_dropdown = ft.Dropdown(
            label="Hora",
            width=400,
            options=[ft.DropdownOption(i) for i in hours],
            border_color="#4a6fa5",
            focused_border_color="#166084",
            filled=True,
            bgcolor="#333333",  # Fondo gris oscuro
            color="#ffffff"  # Texto blanco
        )

        result_text = ft.Text(color="#ffffff")  # Texto blanco

        def show_alert(title, message):
            result_text.value = f"{title}: {message}"
            result_text.color = "red" if title == "Error" else "green"
            page.update()

        def schedule_backup(e):
            src = src_input.value.strip()
            dest = dest_input.value.strip()
            minute = minute_dropdown.value
            hour = hour_dropdown.value
            day = day_dropdown.value

            if not src or not dest:
                show_alert("Error", "Debes introducir ambos directorios.")
                return

            cron = CronTab(user=True)
            job = cron.new(command=f"cp -r {src} {dest}")

            days_mapping = {
                "Lunes": 1, "Martes": 2, "Miércoles": 3,
                "Jueves": 4, "Viernes": 5, "Sábado": 6, "Domingo": 7
            }

            cron_day = days_mapping.get(day, "*")

            job.setall(f"{minute} {hour} * * {cron_day}")
            cron.write()

            show_alert("Copia Programada", f"Copia de seguridad programada para {minute}:{hour} del {day}.")

        btn_schedule = ft.ElevatedButton(
            "Programar Copia",
            on_click=schedule_backup,
            color="white",
            bgcolor="#2ecc71",  # Verde
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            )
        )

        btn_volver = ft.ElevatedButton(
            "Volver",
            on_click=lambda e: vista_principal(),
            color="white",
            bgcolor="#3498db",  # Azul
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            )
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Copia de Seguridad", size=20, weight="bold", color="#ffffff"),
                    src_input,
                    dest_input,
                    minute_dropdown,
                    hour_dropdown,
                    day_dropdown,
                    btn_schedule,
                    result_text,
                    btn_volver
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=15
            )
        )

    vista_principal()


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=30013)
