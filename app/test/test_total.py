from tools.parser.amounts import extract_total

TEXTO_FACTURA_VENTA = """
TALLEDO CALDAS MARCOS ALEJANDRO
RUC: 10752788787
FACTURA ELECTRONICA E001-645
Señor(es): MEJIAS LUIS DAVID
RUC: 20601234567

importe total: S/. 1,000.00
"""

TEXTO_MONTO_CON_VARIOS_DECIMALES = """
Señor(es): MEJIAS LUIS DAVID
RUC: 20601234567
importe total: S/. 1,000.999999999999999999
"""

TEXTO_MONTO_BAJO = """
total: S/ 250.00
"""


def test_extract_monto():
    """En ventas se extrae el segundo RUC/DNI/OPCIONAL si no trae datos"""
    assert extract_total(TEXTO_FACTURA_VENTA) == "1000.00"


def test_extract_monto_con_decimales():
    """Extraer monto con decimales que vienen 2 por defecto,
    pero si hay un error en la aplicación para estar preparado"""
    assert extract_total(TEXTO_MONTO_CON_VARIOS_DECIMALES) == "1000.99"


def test_extract_monto_bajo():
    """Extraer monto bajo"""
    assert extract_total(TEXTO_MONTO_BAJO) == "250.00"
