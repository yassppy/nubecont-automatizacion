from tools.parser.ruc import extract_ruc

TEXTO_FACTURA_VENTA = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): MEJIAS LUIS DAVID
RUC: 20601234567

Valor Unitario: 201.694915254
"""

TEXTO_FACTURA_BOLETA = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): -

Valor Unitario: 201.694915254
"""

TEXTO_CON_DNI = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): JULIAN
RUC: 50653365

Valor Unitario: 201.694915254
"""

TEXTO_PRECIO_DECIMAL_OCHO_DIGITOS = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): JULIAN
RUC: 50653365

Valor Unitario: 201.40653365
"""


# Pruebas de Validación para VENTAS
def test_extract_ruc_ventas():
    """En ventas se extrae el segundo RUC/DNI/OPCIONAL si no trae datos"""
    assert extract_ruc(TEXTO_FACTURA_VENTA, es_venta=True) == "20601234567"


def test_extract_ruc_compras():
    """En compras es el primer ruc que se debe extraer"""
    assert extract_ruc(TEXTO_FACTURA_VENTA, es_venta=True) == "20601234567"
    assert extract_ruc(TEXTO_FACTURA_VENTA, es_venta=False) == "10752788787"


def test_extract_sin_cliente():
    assert extract_ruc(TEXTO_FACTURA_BOLETA, es_venta=True) == "00000000"


def test_extract_con_dni():
    assert extract_ruc(TEXTO_CON_DNI, es_venta=True) == "50653365"


def test_extract_solo_dni():
    assert extract_ruc(TEXTO_PRECIO_DECIMAL_OCHO_DIGITOS, es_venta=True) == "50653365"
