"""Extractor de documento de identidad (RUC/DNI) para comprobantes SUNAT."""

from __future__ import annotations

import re


def extract_ruc(text: str, es_venta: bool = False) -> str:
    """Extrae el RUC o DNI del comprobante según el tipo de operación.

    Args:
        text (str): Texto extraído del PDF.
        es_venta (bool): True para Registro de Ventas (extrae 2do doc: RUC o DNI).
                         False para Registro de Compras (extrae 1er RUC: Emisor).

    Returns:
        str: RUC (11 dígitos), DNI (8 dígitos) o "00000000" si no se encuentra.
    """
    if not text:
        return "00000000"

    if es_venta:
        # Busca RUCs (11 dígitos con 10/20) o DNIs (8 dígitos) aislados
        docs = re.findall(r"(?<![\d.,])((?:10|20)\d{9}|\d{8})(?![\d.,])", text)
        docs_validos = [d for d in docs if d != "00000000"]
        return docs_validos[1] if len(docs_validos) > 1 else "00000000"

    # En compras buscamos únicamente el RUC del emisor/proveedor
    rucs = re.findall(r"(?<![\d.,])((?:10|20)\d{9})(?![\d.,])", text)
    return rucs[0] if rucs else "00000000"
