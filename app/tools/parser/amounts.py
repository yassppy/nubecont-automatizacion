"""Extractor de valores monetarios desde texto de comprobantes SUNAT.

Soporta los formatos más comunes de facturas y boletas electrónicas peruanas:
valor de venta (subtotal), IGV e importe total.
"""

import re


def _limpiar_monto(valor: str | None) -> str | None:
    """Normaliza una cadena de monto eliminando separadores de miles.

    Elimina comas usadas como separador de miles, dejando únicamente
    el punto decimal y los dígitos. No convierte a float para preservar
    la precisión original del comprobante y facilitar la escritura en Excel.

    Args:
        valor (str | None): Cadena cruda capturada por el patrón regex,
            por ejemplo ``'1,250.00'`` o ``'350.00'``.

    Returns:
        str | None: Cadena limpia como ``'1250.00'``, o ``None`` si la
            entrada es vacía o ``None``.

    Examples:
        >>> _limpiar_monto('1,250.00')
        '1250.00'
        >>> _limpiar_monto(None)
        None
    """
    if not valor:
        return None
    return valor.replace(",", "")


def extract_subtotal(text: str) -> str | None:
    """Extrae el valor de venta (subtotal antes de IGV) del comprobante.

    Busca etiquetas comunes en facturas y boletas SUNAT como
    'Valor Venta', 'Op. Gravada' y 'Base Imponible'.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        str | None: Monto como cadena sin separadores de miles,
            por ejemplo ``'847.46'``. Retorna ``None`` si no se encuentra.

    Examples:
        >>> extract_subtotal("Valor Venta S/ 847.46")
        '847.46'
        >>> extract_subtotal("Base Imponible: 1,200.00")
        '1200.00'
    """
    patrones = [
        r"(?:Valor Venta|Op\.? Gravada|Base Imponible)[^\d]*([\d,]+\.\d{2})",
        r"SUB\s*TOTAL.*?([\d,]+\.\d{2})",
    ]
    for patron in patrones:
        if m := re.search(patron, text, re.IGNORECASE):
            return _limpiar_monto(m.group(1))
    return None


def extract_igv(text: str) -> str | None:
    """Extrae el monto de IGV del comprobante.

    Reconoce las variantes 'IGV' e 'I.G.V' presentes en distintos
    formatos de comprobantes electrónicos peruanos.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        str | None: Monto del IGV como cadena, por ejemplo ``'152.54'``.
            Retorna ``None`` si no se encuentra la etiqueta.

    Examples:
        >>> extract_igv("IGV 18% 152.54")
        '152.54'
        >>> extract_igv("I.G.V: 90.00")
        '90.00'
    """
    patrones = [
        r"(?:IGV|I\.G\.V)[^\d]*([\d,]+\.\d{2})",
    ]
    for patron in patrones:
        if m := re.search(patron, text, re.IGNORECASE):
            return _limpiar_monto(m.group(1))
    return None


def extract_total(text: str) -> str | None:
    """Extrae el importe total a pagar del comprobante.

    Prueba múltiples patrones en orden de especificidad para cubrir
    los distintos formatos de facturas, boletas y tickets SUNAT.
    El último patrón es más genérico y actúa como fallback.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.

    Returns:
        str | None: Importe total como cadena, por ejemplo ``'1000.00'``.
            Retorna ``None`` si ningún patrón encuentra coincidencia.

    Examples:
        >>> extract_total("Importe Total S/ 1,000.00")
        '1000.00'
        >>> extract_total("Total a Pagar: 250.00")
        '250.00'
        >>> extract_total("TOTAL S/. 99.90")
        '99.90'
    """
    patrones = [
        r"Importe\s+Total[^\d]*([\d,]+\.\d{2})",
        r"Total\s+a\s+Pagar[^\d]*([\d,]+\.\d{2})",
        r"TOTAL\s+S/\.?\s*([\d,]+\.\d{2})",
        r"(?<!\w)Total[^\d]*([\d,]+\.\d{2})(?!\d)",
    ]
    for patron in patrones:
        if m := re.search(patron, text, re.IGNORECASE):
            return _limpiar_monto(m.group(1))
    return None
