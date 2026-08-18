from tools.parser.currency import extract_currency

TEXTO_FACTURA_VENTA = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): MEJIAS LUIS DAVID
RUC: 20601234567

MONEDA: SOLES

Valor Unitario: 201.694915254
"""

TEXTO_BOLETA = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): -

MONEDA: DOLAR AMERICANO

Valor Unitario: 201.694915254
"""

TEXTO_CONTIENE_DOLAR = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): -

MONEDA: USD

Valor Unitario: 201.694915254
"""

TEXTO_CONTIENE_SOLES = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): -

MONEDA: SOLES

S/ 1200

Valor Unitario: 201.694915254
"""


def test_extract_soles():
    """Extraer la moneda en soles"""
    assert extract_currency(TEXTO_FACTURA_VENTA) == "SOLES"


def test_extract_dolar():
    """Extraer cuando la moneda es dolar"""
    assert extract_currency(TEXTO_BOLETA) == "DÓLAR AMERICANO"


def test_extract_contiene_usd():
    """Extraer cuando la moneda es dolar"""
    assert extract_currency(TEXTO_CONTIENE_DOLAR) == "DÓLAR AMERICANO"


def test_extract_contiene_soles():
    """Extraer cuando la moneda contiene soles"""
    assert extract_currency(TEXTO_CONTIENE_SOLES) == "SOLES"
