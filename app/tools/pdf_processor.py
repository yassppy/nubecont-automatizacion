"""Procesador de comprobantes PDF e integración de extractores y validación SUNAT."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import pymupdf  # PyMuPDF

# Extractores modularizados desde el paquete parser
from tools.parser.amounts import extract_igv, extract_subtotal, extract_total
from tools.parser.currency import extract_currency
from tools.parser.customer import extract_customer
from tools.parser.description import extract_description
from tools.parser.invoice_type import extract_invoice_type
from tools.parser.issue_date import extract_issue_date
from tools.parser.ruc import extract_ruc
from tools.parser.series_number import extract_series_number

# Integración con herramientas de validación externa
from tools.ruc_validator import validate_documents_batch

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Procesador Principal PDF → Excel
# ---------------------------------------------------------------------------


def generate_unique_docs_file(
    input_excel: Path,
    output_dir: Path,
    tipo_op: str,
    empresa: str,
    anio: str,
    mes: str,
) -> Path | None:
    """Extrae los RUCs/DNIs únicos de la columna 'Doc. Cliente' o 'RUC Emisor',

    elimina '00000000' y valores nulos/inválidos, y genera un Excel con los
    datos en la Columna A.
    """
    try:
        df = pd.read_excel(input_excel)

        col_target = "Doc. Cliente" if tipo_op.upper() == "VENTAS" else "RUC Emisor"

        if col_target not in df.columns:
            logger.warning(
                "No se encontró la columna '%s' para extraer los documentos únicos.",
                col_target,
            )
            return None

        # Clean y normalizar valores a texto
        series_docs = df[col_target].astype(str).str.strip()

        # Filtrar ceros, nulos, 'NO ENCONTRADO', etc.
        invalid_values = {
            "00000000",
            "nan",
            "NONE",
            "",
            "NO ENCONTRADO",
            "None",
            "0",
        }
        filtered = series_docs[~series_docs.isin(invalid_values)]

        # Eliminar duplicados manteniendo solo únicos
        unique_docs = filtered.drop_duplicates().reset_index(drop=True)

        # Crear nuevo DataFrame con una sola columna (queda en Columna A)
        col_name = "Doc. Cliente" if tipo_op.upper() == "VENTAS" else "RUC Emisor"
        df_result = pd.DataFrame({col_name: unique_docs})

        output_path = (
            output_dir / f"Doc_Unicos_{tipo_op.upper()}_{empresa}_{anio}_{mes}.xlsx"
        )
        df_result.to_excel(output_path, index=False)

        logger.info("Archivo de documentos únicos generado en: %s", output_path)
        return output_path

    except Exception as err:
        logger.error("Error al generar el archivo de documentos únicos: %s", err)
        return None


def process_single_pdf(pdf_path: Path) -> dict[str, str]:
    """Lee el texto completo del PDF con PyMuPDF y extrae todos los campos."""
    text = ""
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            if isinstance(page_text, str):
                text += page_text + "\n"

    tipo, id_comprobante = extract_invoice_type(text)
    es_factura = bool(tipo and "FACTURA" in tipo)

    ruc_emisor = extract_ruc(text) or "NO ENCONTRADO"
    serie, numero = extract_series_number(text)
    fecha_emision, dia = extract_issue_date(text)
    moneda = extract_currency(text) or "SOLES"

    subtotal = extract_subtotal(text) or "0.00"
    igv = extract_igv(text) or "0.00"
    total = extract_total(text) or "0.00"

    tipo_doc_cliente, num_doc_cliente = extract_customer(text, es_factura)
    descripcion = extract_description(text) or "COMPRA DIVERSA"

    return {
        "Archivo": pdf_path.name,
        "RUC Emisor": ruc_emisor,
        "Tipo Comprobante": id_comprobante or "00 - OTROS",
        "Serie": serie or "NO ENCONTRADO",
        "Número": numero or "NO ENCONTRADO",
        "Fecha Emisión": fecha_emision or "NO ENCONTRADO",
        "Día": dia or "0",
        "Moneda": moneda,
        "Op. Gravada (Subtotal)": subtotal,
        "IGV": igv,
        "Importe Total": total,
        "Tipo Doc. Cliente": tipo_doc_cliente,
        "Doc. Cliente": num_doc_cliente,
        "Nombre / Razón Social Cliente": "NO CONSULTADO",
        "Estado Cliente": "-",
        "Condición Cliente": "-",
        "Descripción / Glosa": descripcion,
    }


def process_directory(
    input_folder_path: str,
    output_folder_path: str,
    tipo_op: str,
    empresa: str,
    anio: str,
    mes: str,
) -> Path:
    """Escanea los PDF, genera el Excel primero y luego intenta enriquecerlo con la API Go."""
    input_dir = Path(input_folder_path)
    output_dir = Path(output_folder_path)

    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No se encontraron archivos PDF en la carpeta de origen seleccionada."
        )

    es_venta = tipo_op.upper() == "VENTAS"

    # 1. Extracción de datos base desde los PDF
    records = [process_single_pdf(pdf) for pdf in pdf_files]

    # Asignar nombres de columna dinámicos
    label_nombre = (
        "Nombre / Razón Social Cliente" if es_venta else "Nombre / Razón Social Emisor"
    )
    label_estado = "Estado Cliente" if es_venta else "Estado Emisor"
    label_condicion = "Condición Cliente" if es_venta else "Condición Emisor"

    # Inicializar columnas de validación por defecto en los registros
    for rec in records:
        if not es_venta:
            rec.pop("Nombre / Razón Social Cliente", None)
            rec.pop("Estado Cliente", None)
            rec.pop("Condición Cliente", None)

        rec[label_nombre] = "PENDIENTE / NO CONSULTADO"
        rec[label_estado] = "-"
        rec[label_condicion] = "-"

    filename = f"Reporte_{tipo_op.upper()}_{empresa}_{anio}_{mes}.xlsx"
    output_excel = output_dir / filename

    # =========================================================================
    # PASO CRÍTICO: Guardar el Excel Inmediatamente ANTES de llamar a la API
    # =========================================================================
    df = pd.DataFrame(records)
    df.to_excel(output_excel, index=False)
    logger.info(f"Excel inicial creado exitosamente en: {output_excel}")

    # 2. Construcción de lote ÚNICO según tipo de operación para consultar a la API
    docs_to_query: list[dict[str, str]] = []
    seen_docs: set[str] = set()

    for rec in records:
        if es_venta:
            doc_num = rec.get("Doc. Cliente")
            doc_tipo = rec.get("Tipo Doc. Cliente")
        else:
            doc_num = rec.get("RUC Emisor")
            doc_tipo = "RUC"

        if (
            doc_num
            and doc_num not in ("00000000", "NO ENCONTRADO")
            and doc_num not in seen_docs
            and doc_tipo in ("RUC", "DNI")
        ):
            docs_to_query.append({"num_doc": doc_num, "tipo_doc": doc_tipo})
            seen_docs.add(doc_num)

    # 3. Intentar consultar a la API de Go sin bloquear la creación del archivo
    if docs_to_query:
        try:
            sunat_results = validate_documents_batch(docs_to_query)
        except Exception as err:
            logger.error(f"La API de Go falló o demoró demasiado: {err}")
            sunat_results = {}

        if sunat_results:
            # 4. Si la API devolvió resultados, actualizar los datos y re-guardar el Excel
            for rec in records:
                doc_key = rec.get("Doc. Cliente") if es_venta else rec.get("RUC Emisor")

                if doc_key in ("00000000", "NO ENCONTRADO"):
                    rec[label_nombre] = (
                        "VENTA MENOR / PÚBLICO GENERAL" if es_venta else "NO ENCONTRADO"
                    )
                elif doc_key in sunat_results and sunat_results[doc_key].get("success"):
                    info = sunat_results[doc_key]
                    rec[label_nombre] = info.get("nombre", "SIN NOMBRE")
                    rec[label_estado] = info.get("estado", "-")
                    rec[label_condicion] = info.get("condicion", "-")
                else:
                    rec[label_nombre] = "NO VALIDADO"

            # Sobrescribir el Excel con las validaciones obtenidas
            df_updated = pd.DataFrame(records)
            df_updated.to_excel(output_excel, index=False)
            logger.info("Excel actualizado con los datos de la API SUNAT.")

    return output_excel
