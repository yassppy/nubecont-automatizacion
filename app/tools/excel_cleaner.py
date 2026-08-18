"""Módulo para limpieza y extracción de listas únicas de clientes."""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def generate_unique_docs_file(
    input_excel: Path, output_folder: Path, tipo_op: str, empresa: str
) -> Path:
    """Extrae los Doc. Cliente únicos de un reporte Excel y genera un nuevo archivo."""
    df = pd.read_excel(input_excel)

    if "Doc. Cliente" not in df.columns:
        return input_excel

    # Limpieza de texto y filtrado
    series_docs = df["Doc. Cliente"].astype(str).str.strip()
    invalid_values = {"00000000", "nan", "NONE", "", "NO ENCONTRADO"}
    filtered = series_docs[~series_docs.isin(invalid_values)].drop_duplicates()

    # Guardar en nuevo Excel
    df_result = pd.DataFrame({"Doc. Cliente": filtered.reset_index(drop=True)})
    output_path = output_folder / f"Doc_Unicos_{tipo_op.upper()}_{empresa}.xlsx"
    df_result.to_excel(output_path, index=False)

    return output_path
