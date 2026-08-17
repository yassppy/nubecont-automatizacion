"""Vista de procesamiento minimalista"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft


class ProcessView(ft.Container):
    """Pantalla de carga limpia con spinner e indicador de finalización."""

    def __init__(
        self,
        page: ft.Page,
        folder_path: str,
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(padding=ft.Padding.all(32), expand=True)
        self.app_page = page
        self.folder_path = folder_path
        self.on_back = on_back

        # 1. Indicador circular de carga
        self.spinner = ft.ProgressRing(
            width=48,
            height=48,
            stroke_width=4,
            color=ft.Colors.BLACK,
        )

        # 2. Ícono de estado final (oculto inicialmente)
        self.status_icon = ft.Icon(
            ft.Icons.CHECK_CIRCLE_ROUNDED,
            size=64,
            color=ft.Colors.GREEN_600,
            visible=False,
        )

        # 3. Textos descriptivos
        self.title_text = ft.Text(
            "Procesando comprobantes",
            size=24,
            weight=ft.FontWeight.W_700,
        )
        self.subtitle_text = ft.Text(
            "Extrayendo datos de los PDF y generando el reporte Excel...",
            size=14,
            color=ft.Colors.BLACK_54,
            text_align=ft.TextAlign.CENTER,
        )

        # 4. Botón para regresar al terminar
        self.back_button = ft.Button(
            content="Volver al Inicio",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
            elevation=0,
            visible=False,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius.all(14)),
            ),
            on_click=self._handle_back,  # pyright: ignore[reportArgumentType]
        )

        # Layout centrado
        self.content = ft.Column(
            controls=[
                self.spinner,
                self.status_icon,
                ft.Container(height=16),
                self.title_text,
                self.subtitle_text,
                ft.Container(height=24),
                self.back_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

    def set_completed(
        self,
        success: bool = True,
        message: str = "El reporte Excel ha sido generado con éxito en la carpeta seleccionada.",
    ) -> None:
        """Actualiza la UI sustituyendo el spinner por el resultado final."""
        self.spinner.visible = False

        if success:
            self.status_icon.icon = ft.Icons.CHECK_CIRCLE_ROUNDED
            self.status_icon.color = ft.Colors.GREEN_600
            self.title_text.value = "¡Proceso Completado!"
        else:
            self.status_icon.icon = ft.Icons.ERROR_ROUNDED
            self.status_icon.color = ft.Colors.RED_600
            self.title_text.value = "Ocurrió un problema"

        self.status_icon.visible = True
        self.subtitle_text.value = message
        self.back_button.visible = True
        self.app_page.update()

    def _handle_back(self, e: Any = None) -> None:
        self.on_back()
