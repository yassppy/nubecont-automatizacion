"""Extractor de la razón social del proveedor/emisor del comprobante.

Identifica el nombre de la empresa buscando sufijos legales peruanos
comunes en las primeras líneas del documento, donde habitualmente
aparece el encabezado del emisor.
"""

_SUFIJOS_LEGALES = ("S.A.C", "S.A.", "E.I.R.L", "S.R.L", "SAC", "SRL", "S.A.C.")


def extract_supplier_name(text: str, ruc: str | None) -> str | None:
    """Extrae la razón social del emisor desde las primeras líneas del texto.

    Revisa únicamente las primeras 10 líneas del documento, que es donde
    los comprobantes electrónicos peruanos ubican el encabezado del emisor.
    Filtra líneas que empiecen con 'SEÑOR' para evitar confundir datos del
    receptor con los del emisor.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.
        ruc (str | None): RUC del emisor (reservado para uso futuro,
            actualmente no se usa en la búsqueda).

    Returns:
        str | None: Razón social del emisor tal como aparece en el documento,
            ej. ``'IMPORTACIONES XYZ S.A.C'``. Retorna ``None`` si no se
            encuentra ninguna línea con sufijo legal conocido.

    Examples:
        >>> extract_supplier_name("DISTRIBUIDORA PERU S.A.C\\nRUC: 20601234567", "20601234567")
        'DISTRIBUIDORA PERU S.A.C'
        >>> extract_supplier_name("Señores: EMPRESA SAC\\nOtras líneas", None)
        None
    """
    lineas = [l.strip() for l in text.splitlines() if l.strip()]
    for linea in lineas[:10]:
        linea_upper = linea.upper()
        tiene_sufijo = any(sufijo in linea_upper for sufijo in _SUFIJOS_LEGALES)
        es_receptor = linea_upper.startswith("SEÑOR")
        if tiene_sufijo and not es_receptor:
            return linea
    return None
