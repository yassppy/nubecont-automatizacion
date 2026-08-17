"""Extractor de la serie y número correlativo del comprobante SUNAT.

Las series de comprobantes electrónicos peruanos siguen el formato
``XNNN`` (una letra seguida de tres dígitos o alfanuméricos), por ejemplo
``F001``, ``B001``, ``E001``. El correlativo puede tener hasta 8 dígitos.
"""

import re

_PATRONES = [
    re.compile(r"\b([A-Z][A-Z0-9]{3})-(\d{1,8})\b", re.IGNORECASE),
    re.compile(r"\b([FEB][A-Z0-9]{2,4})-(\d{3,12})\b", re.IGNORECASE),
]


def extract_series_number(text: str) -> tuple[str | None, str | None]:
    """Extrae la serie y el número correlativo del comprobante.

    Recorre los patrones en orden de especificidad. El primero cubre el
    formato estándar SUNAT (4 caracteres antes del guion); el segundo
    actúa como fallback para series con longitud variable.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        tuple[str | None, str | None]: Par ``(serie, numero)``.
            - ``serie``: Serie en mayúsculas, ej. ``'F001'``, ``'B002'``.
            - ``numero``: Correlativo como cadena, ej. ``'00000123'``.
            Ambos son ``None`` si no se encuentra ninguna coincidencia.

    Examples:
        >>> extract_series_number("FACTURA ELECTRONICA F001-00000123")
        ('F001', '00000123')
        >>> extract_series_number("Boleta B002-456")
        ('B002', '456')
        >>> extract_series_number("Sin serie")
        (None, None)
    """
    for patron in _PATRONES:
        if m := patron.search(text):
            return m.group(1).upper(), m.group(2)
    return None, None
