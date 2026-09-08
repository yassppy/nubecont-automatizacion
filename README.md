# NubeCont Automatización

<div align="center">
  <p>
    <b>Automatización del registro de ventas y validación de comprobantes.</b><br>
    Aplicación de escritorio que extrae información de facturas y boletas,<br>
    valida RUC/DNI directamente con SUNAT y genera reportes Excel listos para NubeCont.
  </p>
  <p>
    <img src="https://img.shields.io/badge/Estado-Completado-success?style=flat-square" alt="Status">
    <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Flet-1C1C1C?style=flat-square&logo=flet&logoColor=white" alt="Flet">
    <img src="https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white" alt="Go">
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="Excel">
    <img src="https://img.shields.io/badge/SUNAT-003B71?style=flat-square" alt="SUNAT">
  </p>
</div>

---

## Capturas de pantalla

|                                                   **Procesamiento de comprobantes**                                                  |                                                        **Validación SUNAT**                                                       |                                                           **Reporte Excel**                                                          |
| :----------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------: |
| ![Procesamiento](https://raw.githubusercontent.com/yassppy/portfolio-website/main/template-portfolio/public/projects/01/parte01.png) | ![Validación](https://raw.githubusercontent.com/yassppy/portfolio-website/main/template-portfolio/public/projects/01/parte02.png) | ![Reporte Excel](https://raw.githubusercontent.com/yassppy/portfolio-website/main/template-portfolio/public/projects/01/parte03.png) |

---

## 📖 Descripción del Proyecto

**NubeCont Automatización** es una aplicación de escritorio desarrollada para automatizar el proceso de **registro de ventas en NubeCont**.

El sistema procesa facturas y boletas electrónicas en formato PDF, extrae automáticamente la información necesaria y realiza la **validación de RUC/DNI en tiempo real directamente contra SUNAT**.

Una vez procesada y validada la información, la aplicación genera un **reporte Excel consolidado** y un segundo archivo con los clientes únicos, preparado para su posterior importación y sincronización con NubeCont.

El proceso permite reducir significativamente el tiempo empleado en el registro manual, pasando de un proceso que podía tomar aproximadamente **30 minutos a alrededor de 10 minutos**, incluyendo las validaciones de los comprobantes.

> [!NOTE]
> Este proyecto se centra exclusivamente en el **Registro de Ventas**. El flujo de Compras se gestiona de forma independiente mediante un sistema basado en OCR.

---

## 🎯 Problema

El registro manual de comprobantes de venta en NubeCont genera diferentes problemas operativos:

* **Procesamiento lento:** la digitación manual de cada comprobante requiere tiempo y atención constante.
* **Errores de digitación:** ingresar manualmente montos, IGV, fechas, series y correlativos aumenta el riesgo de errores.
* **Datos desactualizados:** las consultas internas de NubeCont pueden mostrar información diferente a la registrada actualmente en SUNAT.
* **Validación manual:** verificar individualmente el estado de cada RUC/DNI incrementa el tiempo necesario para completar el proceso.
* **Procesos repetitivos:** gran parte de las tareas pueden ser automatizadas.

---

## 💡 Solución

La solución combina una **aplicación de escritorio en Python**, un **microservicio concurrente desarrollado en Go** y herramientas de automatización para reducir el trabajo manual.

El sistema:

1. Procesa las facturas y boletas electrónicas en PDF.
2. Extrae automáticamente la información de cada comprobante.
3. Genera una estructura de datos preparada para Excel.
4. Valida los RUC/DNI directamente contra SUNAT.
5. Consolida los resultados de las validaciones.
6. Genera un Excel principal con la información procesada.
7. Genera un segundo Excel con los RUC/DNI únicos.
8. Prepara la información para los procesos posteriores de automatización en NubeCont.

El resultado es una reducción del tiempo de procesamiento de aproximadamente **30 a 10 minutos**, manteniendo la validación de los datos durante el flujo.

---

## 🚀 Funcionalidades Principales

* **Procesamiento de comprobantes:** extracción de información desde facturas y boletas electrónicas en PDF.
* **Validación RUC/DNI en tiempo real:** consulta de información directamente contra SUNAT.
* **Consultas concurrentes:** microservicio desarrollado en Go para realizar consultas de forma eficiente.
* **Generación de Excel:** creación automática del reporte consolidado.
* **Excel de clientes únicos:** generación de un archivo secundario con RUC/DNI únicos en la columna A.
* **Limpieza de datos:** eliminación de duplicados y valores no deseados.
* **Interfaz gráfica:** aplicación de escritorio desarrollada con Flet.
* **Ejecutables independientes:** la aplicación y el microservicio pueden distribuirse como ejecutables para Windows.
* **Integración con RPA:** información preparada para automatizaciones posteriores mediante Power Automate u otras herramientas.

---

## 📊 Impacto de la Automatización

Uno de los principales resultados del proyecto es la reducción del tiempo necesario para completar el proceso.

| Proceso                           |   Antes |      Después |
| :-------------------------------- | ------: | -----------: |
| Procesamiento completo            | ~30 min |      ~10 min |
| Validación RUC/DNI                |  Manual | Automatizada |
| Registro de comprobantes          |  Manual | Automatizado |
| Generación de Excel               |  Manual |   Automática |
| Identificación de clientes únicos |  Manual |   Automática |

**Reducción aproximada del tiempo: 67 %.**

---

## 🛠️ Stack Tecnológico

Construido con herramientas orientadas a automatización, procesamiento de documentos y consultas concurrentes.

| Tecnología               |                                                           Insignia                                                           | Uso                                                 |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------- |
| **Python 3.12+**         |             ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square\&logo=python\&logoColor=white)            | Lenguaje principal de la aplicación.                |
| **Flet**                 |                ![Flet](https://img.shields.io/badge/Flet-1C1C1C?style=flat-square\&logo=flet\&logoColor=white)               | Interfaz gráfica de escritorio.                     |
| **uv**                   |                 ![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square\&logo=astral\&logoColor=white)                | Gestión de dependencias y entorno Python.           |
| **PyMuPDF**              |                           ![PyMuPDF](https://img.shields.io/badge/PyMuPDF-3776AB?style=flat-square)                          | Extracción de información desde documentos PDF.     |
| **Pandas**               |             ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square\&logo=pandas\&logoColor=white)            | Procesamiento y estructuración de datos.            |
| **Go**                   |                   ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square\&logo=go\&logoColor=white)                  | Microservicio para consultas concurrentes.          |
| **SUNAT**                |                             ![SUNAT](https://img.shields.io/badge/SUNAT-003B71?style=flat-square)                            | Fuente oficial para validación de RUC/DNI.          |
| **Bruno**                |                             ![Bruno](https://img.shields.io/badge/Bruno-F4AA41?style=flat-square)                            | Pruebas y documentación de la API.                  |
| **Power Automate / RPA** | ![Power Automate](https://img.shields.io/badge/Power_Automate-0066FF?style=flat-square\&logo=powerautomate\&logoColor=white) | Automatización de procesos posteriores en NubeCont. |

---

## 📂 Estructura del Proyecto

El proyecto está dividido en dos componentes principales: la aplicación de escritorio y el microservicio encargado de las consultas a SUNAT.

```bash
NubeContSUNAT/
├── app/
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── excel_cleaner.py         # Limpieza y generación del Excel secundario
│   ├── pyproject.toml           # Dependencias y configuración Python
│   ├── tests/                   # Pruebas unitarias
│   └── dist/                    # Archivos generados para distribución
│       └── NubeContSUNAT/
│           ├── NubeContSUNAT.exe
│           └── api_sunat.exe
│
├── api-app/
│   └── main.go                   # Microservicio de consultas SUNAT
│
├── .env.template                 # Plantilla de variables de entorno
└── README.md
```

---

## 🔄 Flujo de Trabajo

```mermaid
graph LR
    A[Carpeta de PDFs] --> B[Aplicación Flet<br/>Python]
    B --> C[Extracción PyMuPDF]
    C --> D[Datos de comprobantes]
    D --> E[Microservicio Go]
    E --> F[Validación RUC/DNI]
    F --> G[SUNAT]
    G --> H[Resultados de validación]
    H --> I[Excel Consolidado]
    I --> J[Excel Clientes Únicos]
    J --> K[Power Automate / RPA]
    K --> L[NubeCont]
```

### Flujo general

1. **Selección:** el usuario selecciona la carpeta donde se encuentran los comprobantes PDF.
2. **Extracción:** PyMuPDF procesa las facturas y boletas electrónicas.
3. **Estructuración:** los datos extraídos se organizan para generar el reporte.
4. **Validación:** el microservicio desarrollado en Go consulta los RUC/DNI contra SUNAT.
5. **Consolidación:** los resultados de las validaciones se incorporan al reporte.
6. **Exportación:** se genera el Excel principal.
7. **Limpieza:** se procesa la información para obtener los clientes únicos.
8. **Automatización:** el archivo secundario queda preparado para los procesos posteriores de NubeCont.

---

## ⚙️ Instalación y Configuración Local

### Requisitos

* Python 3.12+
* [uv](https://docs.astral.sh/uv/)
* Go
* Windows, para ejecutar los `.exe`

### 1. Aplicación principal

```bash
cd app

uv sync

python -m pytest

uv run .\main.py
```

### 2. Microservicio API

```bash
cd api-app

go run main.go
```

### 3. Compilar el microservicio

```bash
cd api-app

go build -o ../app/api_sunat.exe main.go
```

### 4. Generar el ejecutable de la aplicación

```bash
cd app

.venv/Scripts/activate

pyinstaller --noconsole --onedir \
  --exclude-module pytest \
  --exclude-module setuptools \
  --exclude-module unittest \
  main.py -n "NubeContSUNAT"
```

Después de generar la aplicación, debes copiar manualmente `api_sunat.exe` dentro de:

```text
app/dist/NubeContSUNAT/api_sunat.exe
```

> [!IMPORTANT]
> En la versión compilada, **debes ejecutar tanto `NubeContSUNAT.exe` como `api_sunat.exe`** para que la aplicación pueda realizar las consultas de validación.

---

## ⚠️ Consideraciones

> [!IMPORTANT]
> Configura correctamente las variables de entorno tomando como referencia `.env.template`.

* No compartas las credenciales almacenadas en `.env`.
* El microservicio `api_sunat.exe` debe estar disponible para realizar las validaciones.
* Los RUC/DNI deben estar previamente registrados en NubeCont si serán utilizados posteriormente por los flujos de automatización.
* El repositorio incluye una colección de **Bruno** para probar los endpoints del microservicio.
* Para la distribución mediante PyInstaller, `api_sunat.exe` debe colocarse manualmente dentro de la carpeta generada por `--onedir`.

---

## 👥 Equipo

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/yassppy" target="_blank">
        <img src="https://github.com/yassppy.png" width="80px" alt="Miguel Mallqui" style="border-radius: 50%;"/><br />
        <sub><b>Miguel Mallqui</b></sub>
      </a>
    </td>
  </tr>
</table>
