"""
Tema visual de la app
"""

import flet as ft

PRIMARY = "#000000"  # Negro sólido para botones principales
PRIMARY_CONTAINER = "#F3F4F6"  # Gris claro para contenedores interactivos
SECONDARY = "#22C55E"  # Verde para estados de éxito/validación
ACCENT_BLUE = "#2563EB"  # Azul sutil para enlaces o notas
BG_DARK = "#F8FAFC"  # Fondo de la aplicación (Gris limpio)
BG_CARD = "#FFFFFF"  # Tarjetas y paneles en blanco puro
BG_CARD_LIGHT = "#F1F5F9"  # Fondo para campos de texto / inputs
BG_TERMINAL = "#0F172A"  # Consola profunda contrastada

BORDER_COLOR = "#E2E8F0"  # Bordes gris claro ultra finos
BORDER_FOCUS = "#000000"  # Borde activo negro

TEXT_PRIMARY = "#0F172A"  # Texto principal (Casi negro)
TEXT_SECONDARY = "#64748B"  # Texto secundario (Gris neutro)
TEXT_MUTED = "#94A3B8"  # Texto atenuado

# Colores de estado
LOG_GREEN = "#16A34A"
LOG_YELLOW = "#D97706"
LOG_RED = "#DC2626"
LOG_CYAN = "#0284C7"
LOG_DIM = "#94A3B8"
LOG_WHITE = "#F8FAFC"
LOG_PURPLE = "#9333EA"

# Tipografías
FONT_NORMAL = "Roboto"
FONT_MONO = "Roboto Mono"


def color_scheme() -> ft.ColorScheme:
    """Establecemos la configuración de colores
    https://flet.dev/docs/types/colorscheme/
    """
    return ft.ColorScheme(
        primary=PRIMARY,  # Colorea elementos de alta prioridad
        secondary=SECONDARY,
        surface=BG_CARD,  # Defenir el fondo de las tarjetas
        on_primary="#FFFFFF",  # Garantizan el constraste
        on_surface=TEXT_PRIMARY,  # Garantizan el constraste
    )


def mobile_card(content: ft.Control, padding: int = 16, **kwargs) -> ft.Container:
    """Crear una tarjeta con esquinas redondeadas"""
    return ft.Container(
        content=content,  # Recibe cualquier elemento column, Text ..
        bgcolor=BG_CARD,  # Fondo
        border_radius=20,  # La curva del border
        border=ft.Border.all(1, BORDER_COLOR),  # Dibuja una linea de borde muy delgada
        padding=padding,  # Margen interno
        **kwargs,  # Acepta cualquier propiedad extra y se guarda aquí lo que se te envie
    )
