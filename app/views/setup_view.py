"""Vista de configuración modularizada con selección de Compras / Ventas."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft


class SetupView(ft.Container):
    """Componente visual para la selección de parámetros, carpetas e inicio."""

    def __init__(
        self,
        page: ft.Page,
        on_start_process: Callable[[str, str, str, str, str, str], None],
    ) -> None:
        super().__init__(padding=ft.Padding.all(32), expand=True)
        self.app_page = page
        self.on_start_process = on_start_process
        self.selected_input_folder: str | None = None
        self.selected_output_folder: str | None = None

        # 1. Registros de FilePicker (Origen y Destino)
        self.input_picker = ft.FilePicker()
        self.output_picker = ft.FilePicker()
        self.app_page.services.extend([self.input_picker, self.output_picker])

        # 2. Desplegables de parámetros (Tipo Operación, Empresa, Año, Mes)
        self.dd_tipo_op = ft.Dropdown(
            label="Tipo de Operación",
            value="VENTAS",
            options=[
                ft.dropdown.Option("VENTAS"),
                ft.dropdown.Option("COMPRAS"),
            ],
            expand=True,
            border_radius=ft.BorderRadius.all(10),
        )

        self.dd_empresa = ft.Dropdown(
            label="Empresa",
            value="NRUTA",
            options=[
                ft.dropdown.Option("NRUTA"),
                ft.dropdown.Option("TALLEDO"),
            ],
            expand=True,
            border_radius=ft.BorderRadius.all(10),
        )

        self.dd_anio = ft.Dropdown(
            label="Año",
            value="2026",
            options=[
                ft.dropdown.Option("2024"),
                ft.dropdown.Option("2025"),
                ft.dropdown.Option("2026"),
            ],
            width=120,
            border_radius=ft.BorderRadius.all(10),
        )

        self.dd_mes = ft.Dropdown(
            label="Mes",
            value="01",
            options=[
                ft.dropdown.Option("01", "01 - Enero"),
                ft.dropdown.Option("02", "02 - Febrero"),
                ft.dropdown.Option("03", "03 - Marzo"),
                ft.dropdown.Option("04", "04 - Abril"),
                ft.dropdown.Option("05", "05 - Mayo"),
                ft.dropdown.Option("06", "06 - Junio"),
                ft.dropdown.Option("07", "07 - Julio"),
                ft.dropdown.Option("08", "08 - Agosto"),
                ft.dropdown.Option("09", "09 - Setiembre"),
                ft.dropdown.Option("10", "10 - Octubre"),
                ft.dropdown.Option("11", "11 - Noviembre"),
                ft.dropdown.Option("12", "12 - Diciembre"),
            ],
            expand=True,
            border_radius=ft.BorderRadius.all(10),
        )

        # 3. Elementos de texto para las rutas elegidas
        self.input_folder_path = ft.Text(
            "Sin carpeta de origen (PDFs)",
            color=ft.Colors.BLACK_54,
            selectable=True,
        )
        self.output_folder_path = ft.Text(
            "Sin carpeta de destino (Excel)",
            color=ft.Colors.BLACK_54,
            selectable=True,
        )

        # 4. Botones de acción estilo Cal AI
        btn_input = ft.Button(
            content="Carpeta origen (PDFs)",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
            elevation=0,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius.all(12)),
            ),
            on_click=self._choose_input_folder,  # pyright: ignore[reportArgumentType]
        )

        btn_output = ft.Button(
            content="Carpeta destino (Excel)",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK_87,
            elevation=0,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius.all(12)),
            ),
            on_click=self._choose_output_folder,  # pyright: ignore[reportArgumentType]
        )

        process_button = ft.Button(
            content="Comenzar Procesamiento",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
            elevation=0,
            style=ft.ButtonStyle(
                padding=ft.Padding.symmetric(horizontal=20, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius.all(14)),
            ),
            on_click=self._start,  # pyright: ignore[reportArgumentType]
        )

        # 5. Estructura visual de la vista
        self.content = ft.Column(
            controls=[
                ft.Text("NubeCont AI", size=32, weight=ft.FontWeight.W_700),
                ft.Text(
                    "Configura los parámetros y selecciona las carpetas de trabajo",
                    size=14,
                    color=ft.Colors.BLACK_54,
                ),
                ft.Container(height=8),
                # Fila con Tipo de Operación y Empresa
                ft.Row(controls=[self.dd_tipo_op, self.dd_empresa], spacing=12),
                # Fila con Año y Mes
                ft.Row(controls=[self.dd_anio, self.dd_mes], spacing=12),
                ft.Container(height=8),
                # Selección de carpeta Origen
                ft.Row(
                    controls=[
                        btn_input,
                        ft.Container(
                            content=self.input_folder_path,
                            bgcolor=ft.Colors.BLACK_12,
                            border_radius=ft.BorderRadius.all(12),
                            padding=ft.Padding.all(12),
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
                # Selección de carpeta Destino
                ft.Row(
                    controls=[
                        btn_output,
                        ft.Container(
                            content=self.output_folder_path,
                            bgcolor=ft.Colors.BLACK_12,
                            border_radius=ft.BorderRadius.all(12),
                            padding=ft.Padding.all(12),
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(height=12),
                process_button,
            ],
            spacing=10,
        )

    async def _choose_input_folder(self, e: Any = None) -> None:
        folder = await self.input_picker.get_directory_path(
            dialog_title="Selecciona la carpeta con los comprobantes PDF"
        )
        if folder:
            self.selected_input_folder = folder
            self.input_folder_path.value = folder
            self.input_folder_path.color = ft.Colors.BLACK_87
            if not self.selected_output_folder:
                self.selected_output_folder = folder
                self.output_folder_path.value = folder
                self.output_folder_path.color = ft.Colors.BLACK_87
            self.app_page.update()

    async def _choose_output_folder(self, e: Any = None) -> None:
        folder = await self.output_picker.get_directory_path(
            dialog_title="Selecciona la carpeta para guardar el Excel"
        )
        if folder:
            self.selected_output_folder = folder
            self.output_folder_path.value = folder
            self.output_folder_path.color = ft.Colors.BLACK_87
            self.app_page.update()

    def _start(self, e: Any = None) -> None:
        if not self.selected_input_folder:
            self.app_page.show_dialog(
                ft.SnackBar(content=ft.Text("Selecciona la carpeta origen de los PDF."))
            )
            return

        out_folder = self.selected_output_folder or self.selected_input_folder
        tipo_op = str(self.dd_tipo_op.value or "VENTAS")
        empresa = str(self.dd_empresa.value or "NRUTA")
        anio = str(self.dd_anio.value or "2026")
        mes = str(self.dd_mes.value or "01")

        # Pasa los 6 parámetros requeridos al callback principal
        self.on_start_process(
            self.selected_input_folder, out_folder, tipo_op, empresa, anio, mes
        )
