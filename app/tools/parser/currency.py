"""Extractor del tipo de moneda desde texto de comprobantes SUNAT.

Soporta detección explícita mediante la etiqueta 'Tipo de Moneda' o 'Moneda'
y detección implícita por palabras clave en el cuerpo del documento.
"""

from __future__ import annotations

import re


def extract_currency(text: str) -> str | None:
    """Extrae el tipo de moneda declarado en el comprobante.

    Primero intenta leer la etiqueta explícita 'Tipo de Moneda' o 'MONEDA'.
    Si no la encuentra, infiere la moneda buscando palabras clave
    como 'USD', 'DOLAR', 'DÓLAR', 'SOLES' o 'S/' en el texto.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        str | None: Nombre de la moneda tal como lo espera el formato del proyecto
            ('SOLES', 'DÓLAR AMERICANO'), o None si no se puede determinar.

    Examples:
        >>> extract_currency("MONEDA: SOLES")
        'SOLES'
        >>> extract_currency("MONEDA: DOLAR AMERICANO")
        'DÓLAR AMERICANO'
        >>> extract_currency("Importe Total USD 150.00")
        'DÓLAR AMERICANO'
        >>> extract_currency("S/ 250.00")
        'SOLES'
    """
    if not text:
        return None

    # 1. Búsqueda explícita con etiquetas: "Tipo de Moneda:", "MONEDA:", etc.
    if m := re.search(
        r"(?:Tipo de Moneda|Moneda)\s*:\s*([^\n\r]+)", text, re.IGNORECASE
    ):
        valor = m.group(1).strip().upper()
        # Normalizar acentos para la evaluación
        valor_clean = valor.replace("Ó", "O").replace("Á", "A")

        if "DOLAR" in valor_clean or "USD" in valor_clean or "$" in valor:
            return "DÓLAR AMERICANO"
        if "SOL" in valor_clean or "PEN" in valor_clean or "S/" in valor:
            return "SOLES"
        return valor

    # 2. Búsqueda implícita en el cuerpo del documento por palabras clave
    text_upper = text.upper().replace("Ó", "O").replace("Á", "A")

    if any(
        patron in text_upper
        for patron in ("USD", "DOLAR AMERICANO", "DOLARES AMERICANOS", "DOLAR", "US$")
    ):
        return "DÓLAR AMERICANO"

    if any(patron in text_upper for patron in ("SOLES", "S/", "PEN", "NUEVOS SOLES")):
        return "SOLES"

    return None
