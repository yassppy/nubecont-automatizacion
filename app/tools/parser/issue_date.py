"""Extractor de la fecha de emisión desde texto de comprobantes SUNAT.

Soporta los formatos de fecha más comunes en comprobantes electrónicos
peruanos: formato largo DD/MM/YYYY y formato corto de ticket DD.MM.YY.
"""

import re


def extract_issue_date(text: str) -> tuple[str | None, str | None]:
    """Extrae la fecha de emisión del comprobante y el día numérico.

    Intenta primero el formato estándar ``DD/MM/YYYY``. Si no lo encuentra,
    intenta el formato de ticket ``DD.MM.YY`` y lo convierte al estándar.
    El día se retorna sin cero inicial para cumplir con el formato NubeCont.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        tuple[str | None, str | None]: Par ``(fecha, dia)``.
            - ``fecha``: Cadena en formato ``'DD/MM/YYYY'``,
              ej. ``'05/12/2024'``. ``None`` si no se encuentra.
            - ``dia``: Número de día sin cero inicial, ej. ``'5'`` para el 5.
              ``None`` si no se identifica la fecha.

    Examples:
        >>> extract_issue_date("Fecha de emisión: 05/12/2024")
        ('05/12/2024', '5')
        >>> extract_issue_date("F. Emisión: 12.08.25")
        ('12/08/2025', '12')
        >>> extract_issue_date("Sin fecha")
        (None, None)
    """
    # Formato estándar: DD/MM/YYYY
    if m := re.search(r"(\d{1,2})/(\d{2})/(\d{4})", text):
        fecha = m.group(0)
        dia = m.group(1).lstrip("0") or "0"
        return fecha, dia

    # Formato ticket: DD.MM.YY → DD/MM/20YY
    if m := re.search(r"\b(\d{2})\.(\d{2})\.(\d{2})\b", text):
        day, month, year = m.group(1), m.group(2), m.group(3)
        dia = day.lstrip("0") or "0"
        return f"{day}/{month}/20{year}", dia

    return None, None
