"""Extractor de la descripción principal del bien o servicio del comprobante.

PyMuPDF extrae las tablas SUNAT con cada celda en una línea separada.
El bloque de ítems sigue siempre este orden de líneas:

    1.00          ← cantidad
    UNIDAD        ← unidad de medida
    <codigo>      ← código numérico (puede ser corto o largo)
    <DESCRIPCIÓN> ← una o más líneas con el nombre del producto
    <valor>       ← valor unitario con muchos decimales (ej. 84.7457627)
    <descuento>   ← descuento (ej. 0.00)
    <importe>     ← importe de venta (ej. 99.999999986)

La estrategia es localizar la línea 'UNIDAD' dentro del bloque de detalle
y tomar la(s) línea(s) que vienen después del código, antes del valor
unitario (flotante con más de 2 decimales).
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Unidades de medida SUNAT reconocidas
# ---------------------------------------------------------------------------

_UNIDADES = frozenset({
    "UNIDAD", "UND", "NIU", "ZZ", "GLO",
    "PCS", "UNI", "KG", "LT", "MT", "M2",
    "CAJA", "PACK", "JGO", "PAR",
})

# Patrón de valor unitario: número con más de 2 decimales (precio sin redondear)
_RE_VALOR_UNITARIO = re.compile(r"^\d+\.\d{3,}$")

# Patrón de código de ítem: solo dígitos, o alfanumérico sin vocales (ej. "76", "545454", "CR7")
# Una palabra con solo mayúsculas y vocales es probablemente descripción (ej. "ACEITE", "CASCO")
_RE_CODIGO = re.compile(r"^[0-9]+$|^[A-Z0-9]{1,8}$", re.IGNORECASE)
_RE_SOLO_LETRAS = re.compile(r"^[A-ZÁÉÍÓÚÑ\s]+$", re.IGNORECASE)

# Palabras que nunca son una descripción válida
_EXCLUIR = frozenset({
    "DESCRIPCION", "DESCRIPCIÓN", "CANTIDAD", "CANT",
    "UNIDAD", "MEDIDA", "CODIGO", "CÓDIGO",
    "VALOR UNITARIO", "DESCUENTO", "IMPORTE DE VENTA",
    "OTROS CARGOS", "OTROS TRIBUTOS", "IMPORTE TOTAL",
    "OP. GRAVADA", "BASE IMPONIBLE", "IGV", "ISC",
    "SUB TOTAL VENTAS", "ANTICIPOS",
})


# ---------------------------------------------------------------------------
# Función pública
# ---------------------------------------------------------------------------


def extract_description(text: str) -> str | None:
    """Extrae la descripción del bien o servicio desde el texto del comprobante.

    Localiza el bloque de detalle buscando la secuencia característica que
    PyMuPDF genera al extraer tablas SUNAT:
    ``cantidad → UNIDAD → código → DESCRIPCIÓN → valor_unitario``.

    Tras encontrar la línea ``UNIDAD``, salta el código numérico y recolecta
    las líneas de descripción hasta topar con el valor unitario (número con
    más de 2 decimales). Si hay múltiples ítems distintos retorna
    ``'ACCESORIOS VARIOS'``.

    Args:
        text (str): Texto plano extraído del PDF mediante PyMuPDF.

    Returns:
        str | None: Descripción limpia del producto o servicio,
            ``'ACCESORIOS VARIOS'`` si hay múltiples ítems distintos,
            o ``None`` si no se puede determinar ninguna descripción.

    Examples:
        >>> t = "1.00\\nUNIDAD\\n455454\\nSISTEMA DE ARRASTRE\\n84.7457627\\n0.00\\n99.99"
        >>> extract_description(t)
        'SISTEMA DE ARRASTRE'
        >>> t2 = "1.00\\nUNIDAD\\n76\\nMASCARA + PROTECTOR\\nZAPATO\\n40.67796\\n0.00\\n47.99"
        >>> extract_description(t2)
        'MASCARA + PROTECTOR ZAPATO'
    """
    lineas = [l.strip() for l in text.splitlines()]

    items: list[str] = []

    i = 0
    while i < len(lineas):
        linea = lineas[i]

        # Detectar línea de unidad de medida
        if linea.upper() not in _UNIDADES:
            i += 1
            continue

        # Siguiente línea tras UNIDAD: debe ser el código (alfanumérico, sin espacios)
        j = i + 1
        if j >= len(lineas):
            break

        # Saltar el código de ítem solo si es puramente numérico o alfanumérico sin espacios
        # y NO parece una descripción real (palabras con vocales)
        if _RE_CODIGO.match(lineas[j]) and not _RE_SOLO_LETRAS.match(lineas[j]):
            j += 1

        # Recolectar líneas de descripción hasta el valor unitario
        partes: list[str] = []
        while j < len(lineas):
            candidato = lineas[j]

            # Fin de descripción: valor unitario con muchos decimales
            if _RE_VALOR_UNITARIO.match(candidato):
                break

            # Fin de descripción: línea vacía o cabecera conocida
            if not candidato or candidato.upper() in _EXCLUIR:
                break

            # Fin de descripción: línea que empieza con "Otros" o "Importe"
            if re.match(r"^(Otros|Importe|SON:|Op\.)", candidato, re.IGNORECASE):
                break

            partes.append(candidato)
            j += 1

        if partes:
            descripcion = " ".join(partes).strip()
            # Limpiar prefijo numérico inicial pegado a la descripción:
            # - Cantidades sueltas (1-2 dígitos): "2 ARO" → "ARO"
            # - Códigos de ítem largos (≥5 dígitos): "8868886 CANDADO U" → "CANDADO U"
            # Números de 3-4 dígitos se conservan: pueden ser modelos del producto.
            descripcion = re.sub(r"^(\d{1,2}|\d{5,})\s+", "", descripcion).strip()
            if descripcion and descripcion not in items:
                items.append(descripcion)

        i = j  # continuar desde donde terminó este ítem

    if not items:
        return None
    if len(items) == 1:
        return items[0]
    return "ACCESORIOS VARIOS"
