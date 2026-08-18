"""Punto de entrada principal de la aplicación NubeCont SUNAT."""

from __future__ import annotations

import asyncio
import atexit
import subprocess
import sys
from pathlib import Path

import flet as ft

from tools.pdf_processor import process_directory
from views.process_view import ProcessView
from views.setup_view import SetupView

# ---------------------------------------------------------------------------
# Gestión del Subproceso de la API en Go
# ---------------------------------------------------------------------------

_GO_PROCESS: subprocess.Popen | None = None


def _get_api_binary_path() -> Path:
    """Determina la ruta del ejecutable de la API Go según el entorno."""
    binary_name = "api_sunat.exe" if sys.platform == "win32" else "api_sunat"

    # En ejecutable (frozen), busca en el directorio donde reside el .exe
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).resolve().parent

    path = base_dir / binary_name
    return path if path.exists() else Path.cwd() / binary_name


def start_go_api() -> None:
    """Inicia el servidor de la API de Go en segundo plano sin ventana de consola."""
    global _GO_PROCESS
    binary_path = _get_api_binary_path()

    if not binary_path.exists():
        print(f"[WARN] No se encontró el ejecutable de la API Go en: {binary_path}")
        return

    creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    try:
        _GO_PROCESS = subprocess.Popen(
            [str(binary_path)],
            creationflags=creation_flags,
        )
        print(f"[INFO] API Go iniciada correctamente PID: {_GO_PROCESS.pid}")
    except Exception as err:  # noqa: BLE001
        print(f"[ERROR] Error al iniciar la API en Go: {err}")


def stop_go_api() -> None:
    """Detiene limpiamente el proceso de la API en Go al cerrar la aplicación."""
    if _GO_PROCESS and _GO_PROCESS.poll() is None:
        print("[INFO] Cerrando servicio API Go...")
        _GO_PROCESS.terminate()
        try:
            _GO_PROCESS.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _GO_PROCESS.kill()


# Registrar el cierre del proceso Go al apagar Python
atexit.register(stop_go_api)


# ---------------------------------------------------------------------------
# Aplicación Principal Flet
# ---------------------------------------------------------------------------


async def main(page: ft.Page) -> None:
    page.title = "NubeCont SUNAT"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 560
    page.window.height = 680
    page.window.resizable = False

    def show_setup_view() -> None:
        """Carga la vista inicial de selección de carpetas y parámetros."""
        setup_view = SetupView(page=page, on_start_process=start_processing)
        page.controls.clear()
        page.add(setup_view)
        page.update()

    def start_processing(
        input_folder: str,
        output_folder: str,
        tipo_op: str,
        empresa: str,
        anio: str,
        mes: str,
    ) -> None:
        """Cambia a la vista de proceso e inicia la extracción en segundo plano."""
        process_view = ProcessView(
            page=page,
            folder_path=input_folder,
            on_back=show_setup_view,
        )
        page.controls.clear()
        page.add(process_view)
        page.update()

        # Ejecutamos la extracción pasando todos los parámetros incluyendo tipo_op
        asyncio.create_task(
            run_pdf_extraction(
                input_folder,
                output_folder,
                tipo_op,
                empresa,
                anio,
                mes,
                process_view,
            )
        )

    async def run_pdf_extraction(
        input_folder: str,
        output_folder: str,
        tipo_op: str,
        empresa: str,
        anio: str,
        mes: str,
        view: ProcessView,
    ) -> None:
        """Ejecuta la lógica de extracción de comprobantes en un hilo secundario."""
        try:
            excel_path: Path = await asyncio.to_thread(
                process_directory,
                input_folder,
                output_folder,
                tipo_op,
                empresa,
                anio,
                mes,
            )

            view.set_completed(
                success=True,
                message=f"Reporte generado con éxito en:\n{excel_path}",
            )
        except (FileNotFoundError, PermissionError, ValueError) as err:
            view.set_completed(
                success=False,
                message=f"Error de archivo o formato: {err}",
            )
        except Exception as err:  # noqa: BLE001
            view.set_completed(
                success=False,
                message=f"Error inesperado del sistema: {err}",
            )

    # Iniciar en la pantalla de selección
    show_setup_view()


if __name__ == "__main__":
    start_go_api()
    ft.run(main)
