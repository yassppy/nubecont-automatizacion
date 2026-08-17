"""Cliente HTTP para validar documentos RUC/DNI consumiendo la API de Go."""

from __future__ import annotations

import logging

import httpx

API_URL = "http://localhost:7860/api/v1/validar-lote"

logger = logging.getLogger(__name__)


def validate_documents_batch(documents: list[dict[str, str]]) -> dict[str, dict]:
    """Envía un lote de RUCs/DNIs a la API de Go y retorna un diccionario mapeado por documento.

    Ejemplo de entrada:
        [
            {"num_doc": "20100070970", "tipo_doc": "RUC"},
            {"num_doc": "48992773", "tipo_doc": "DNI"}
        ]

    Ejemplo de salida:
        {
            "20100070970": {"nombre": "...", "estado": "ACTIVO", "condicion": "HABIDO", "success": True},
            ...
        }
    """
    if not documents:
        return {}

    payload = {"documents": documents}

    # Calculamos un timeout amplio según la cantidad de documentos (12s por consulta, mínimo 60s)
    # Esto evita que httpx aborte la petición antes de que la API Go termine de consultar en SUNAT.
    total_timeout = max(60.0, float(len(documents) * 12.0))

    try:
        # Usamos httpx.Timeout especificando un read_timeout alto o None
        timeout_config = httpx.Timeout(
            connect=10.0, read=total_timeout, write=10.0, pool=10.0
        )

        with httpx.Client(timeout=timeout_config) as client:
            response = client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("results", {})
    except Exception as err:
        logger.error("Error al conectar con la API Go de SUNAT: %s", err)
        return {}
