"""Extractor del tipo de moneda desde texto de comprobantes SUNAT.

Soporta detección explícita mediante la etiqueta 'Tipo de Moneda'
y detección implícita por palabras clave en el cuerpo del documento.
"""

import re


def extract_currency(text: str) -> str | None:
    """Extrae el tipo de moneda declarado en el comprobante.

    Primero intenta leer la etiqueta explícita 'Tipo de Moneda'.
    Si no la encuentra, infiere la moneda buscando palabras clave
    como 'SOLES', 'S/', 'DOLAR' o 'USD' en el texto.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        str | None: Nombre de la moneda tal como aparece en el comprobante
            (ej. ``'SOLES'``, ``'USD'``), o ``None`` si no se puede determinar.

    Examples:
        >>> extract_currency("Tipo de Moneda: SOLES")
        'SOLES'
        >>> extract_currency("Importe Total USD 150.00")
        'USD'
        >>> extract_currency("S/ 250.00")
        'SOLES'
    """
    if m := re.search(r"Tipo de Moneda\s*:\s*(.+)", text, re.IGNORECASE):
        return m.group(1).strip()

    text_upper = text.upper()
    if "SOLES" in text_upper or "S/" in text_upper:
        return "SOLES"
    if "DOLAR" in text_upper or "USD" in text_upper:
        return "USD"

    return None
