"""Extractor del tipo de comprobante electrónico SUNAT.

Identifica si el documento es una factura o boleta de venta electrónica
y retorna su nombre normalizado junto con el código SUNAT correspondiente.
"""

# Mapeo de texto encontrado → (tipo normalizado, código SUNAT)
_TIPOS: dict[str, tuple[str, str]] = {
    "FACTURA ELECTRONICA": ("FACTURA ELECTRONICA", "01 - FACTURA"),
    "FACTURA ELECTRÓNICA": ("FACTURA ELECTRONICA", "01 - FACTURA"),
    "BOLETA DE VENTA ELECTRONICA": ("BOLETA DE VENTA", "03 - BOLETA DE VENTA"),
    "BOLETA DE VENTA ELECTRÓNICA": ("BOLETA DE VENTA", "03 - BOLETA DE VENTA"),
    "BOLETA DE VENTA": ("BOLETA DE VENTA", "03 - BOLETA DE VENTA"),
    "FACTURA": ("FACTURA ELECTRONICA", "01 - FACTURA"),
    "BOLETA": ("BOLETA DE VENTA", "03 - BOLETA DE VENTA"),
}


def extract_invoice_type(text: str) -> tuple[str | None, str | None]:
    """Extrae el tipo de comprobante y su código SUNAT desde el texto del PDF.

    Recorre el diccionario de tipos en orden de especificidad (claves más
    largas primero) para evitar que 'FACTURA' coincida antes que
    'FACTURA ELECTRONICA'. La comparación se hace en mayúsculas.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        tuple[str | None, str | None]: Par ``(tipo, id_comprobante)``.
            - ``tipo``: Nombre normalizado, ej. ``'FACTURA ELECTRONICA'``.
            - ``id_comprobante``: Código SUNAT, ej. ``'01 - FACTURA'``.
            Ambos valores son ``None`` si no se identifica ningún tipo.

    Examples:
        >>> extract_invoice_type("FACTURA ELECTRÓNICA F001-00000123")
        ('FACTURA ELECTRONICA', '01 - FACTURA')
        >>> extract_invoice_type("BOLETA DE VENTA B001-00000456")
        ('BOLETA DE VENTA', '03 - BOLETA DE VENTA')
        >>> extract_invoice_type("Documento sin tipo reconocible")
        (None, None)
    """
    text_upper = text.upper()
    for clave, (tipo, id_comp) in _TIPOS.items():
        if clave in text_upper:
            return tipo, id_comp
    return None, None
