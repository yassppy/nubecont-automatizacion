"""Extractor del documento de identidad del cliente/receptor del comprobante.

Distingue entre facturas (receptor con RUC) y boletas (receptor con DNI
o venta a consumidor final sin identificación).
"""

import re


def extract_customer(text: str, es_factura: bool) -> tuple[str, str]:
    """Extrae el tipo y número de documento del cliente receptor.

    Para facturas se asume que el receptor tiene RUC (11 dígitos) y se
    toma el segundo RUC encontrado en el texto (el primero corresponde
    al emisor). Para boletas se busca DNI primero; si no hay, se intenta
    el segundo RUC; si tampoco existe, se registra como venta menor.

    Args:
        text (str): Texto plano extraído del PDF del comprobante.
        es_factura (bool): ``True`` si el comprobante es una factura
            electrónica, ``False`` si es boleta u otro tipo.

    Returns:
        tuple[str, str]: Par ``(tipo_documento, numero_documento)``.
            Valores posibles para tipo: ``'RUC'``, ``'DNI'``, ``'VENTA MENOR'``.
            El número es la cadena extraída o ``'00000000'`` cuando no aplica.

    Examples:
        >>> extract_customer("RUC: 20601234567 ... RUC cliente 20509876543", True)
        ('RUC', '20509876543')
        >>> extract_customer("DNI: 45678912", False)
        ('DNI', '45678912')
        >>> extract_customer("Consumidor Final", False)
        ('VENTA MENOR', '00000000')
    """
    if es_factura:
        rucs = re.findall(r"\d{11}", text)
        id_cliente = rucs[1] if len(rucs) > 1 else "NO ENCONTRADO"
        return "RUC", id_cliente

    if m := re.search(r"DNI\s*[:\s]+(\d{8})", text, re.IGNORECASE):
        return "DNI", m.group(1)

    rucs = re.findall(r"\d{11}", text)
    if len(rucs) > 1:
        return "VENTA MENOR", rucs[1]

    return "VENTA MENOR", "00000000"
