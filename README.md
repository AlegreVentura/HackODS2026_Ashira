# ASHIRA

[![Licencia CC BY-SA 4.0](https://img.shields.io/badge/Licencia-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Quarto 1.9+](https://img.shields.io/badge/Quarto-1.9%2B-75AADB?logo=quarto&logoColor=white)](https://quarto.org)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![ODS 1](https://img.shields.io/badge/ODS%201-Fin%20de%20la%20Pobreza-E5243B)](https://sdgs.un.org/goals/goal1)
[![ODS 10](https://img.shields.io/badge/ODS%2010-Reducción%20de%20Desigualdades-DD1367)](https://sdgs.un.org/goals/goal10)

---

![Preview del dashboard ASHIRA](dashboard/untitled.GIF)

---

**En México no se puede hablar de pobreza sin hablar de dónde naciste.**

Cuatro bases de datos oficiales. Ocho años de registros. Una sola pregunta:

> **¿Cuánto influye el estado donde naciste en tu probabilidad de vivir en pobreza?**
>
> La respuesta corta: **Muchísimo.**
> La respuesta larga: **esta historia.**

ASHIRA cruza ENIGH, CONEVAL, Censo 2020 e ICE IMCO para demostrar que la brecha territorial de pobreza en México lleva ocho años sin cerrarse — y que los promedios nacionales la hacen invisible.

---

## El equipo

| Integrante | Origen | Contribución |
|---|---|---|
| Melisa Asharet Arano Bejarano | Veracruz | Análisis de ingreso y desigualdad territorial (ENIGH 2016–2024) |
| Roberto Jhoshua Alegre Ventura | Guerrero | Análisis de pobreza multidimensional por estado (PM CONEVAL 2024) |
| Israel Martínez Jiménez | Estado de México | Análisis de estructura territorial, etnicidad y competitividad (Censo 2020 e ICE IMCO) |

---

## La historia en seis actos

| Acto | Título | Hallazgo clave |
|:---:|---|---|
| 1 | **Los dos Méxicos** | Chiapas (66% en pobreza) frente a Baja California (10%). 56 puntos de diferencia bajo la misma bandera. |
| 2 | **La brecha que no cierra** | El Norte gana 1.7 veces más que el Sur en 2024. En 2016 era 1.6 veces. Ocho años, la misma estructura. |
| 3 | **Las raíces** | Correlación etnicidad–pobreza r ≈ 0.8. A mayor informalidad laboral, menor ingreso mediano, sin excepción. |
| 4 | **El parche** | Los estados del Sur viven cada vez más de transferencias gubernamentales y remesas, no de trabajo formal. |
| 5 | **Los que se van** | Los estados más pobres son los que más población pierden. La emigración es la única válvula de escape disponible. |
| 6 | **¿Está cambiando?** | El ingreso creció en todos los estados entre 2016 y 2024. Pero los estados ricos crecieron más en pesos absolutos. |

---

## Cómo reproducir el análisis

### Requisitos

- [Python 3.13+](https://python.org)
- [uv](https://docs.astral.sh/uv/) — gestor de entornos y dependencias
- [Quarto 1.9+](https://quarto.org/docs/get-started/) — para renderizar el dashboard

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Israwss/Ashira.git
cd Ashira

# 2. Instalar dependencias con uv (crea el entorno automáticamente)
uv sync

# 3. Descargar los datos — ver sección "Los datos" más abajo
#    y colocarlos en las rutas indicadas

# 4. Renderizar el dashboard
uv run quarto render dashboard/index.qmd
```

El resultado queda en **`docs/index.html`** — se abre directo en el navegador sin servidor.

> **Alternativa sin Quarto:** el notebook `dashboard/ASHIRA_narrativa.ipynb` contiene las mismas visualizaciones y se puede ejecutar con `uv run jupyter notebook`.

---

## Los datos

Todas las fuentes son instituciones del Estado mexicano o institutos de investigación independientes con metodologías auditadas. **Los archivos de datos no están en el repositorio** por restricciones de tamaño de GitHub — descárgalos con las instrucciones siguientes.

### ENIGH 2016–2024 (INEGI)

La fuente oficial de ingresos de los hogares en México. Usamos el archivo `concentradohogar` de cada edición bienal para calcular el ingreso per cápita mensual ponderado por hogar.

**Variables usadas:** `ubica_geo`, `factor`, `tot_integ`, `ing_cor`, `ingtrab`, `bene_gob`, `remesas`, `transfer`, `tam_loc`

| Campo | Valor |
|---|---|
| URL | https://www.inegi.org.mx/programas/enigh/nc/2024/ |
| Cobertura | 32 entidades · 2016, 2018, 2020, 2022, 2024 |
| Formato | CSV (`concentradohogar`) |
| Licencia | Datos Abiertos de México — https://datos.gob.mx/libreusomx |

**Descarga:**
1. Ir a la URL de cada año (2016, 2018, 2020, 2022, 2024) desde el sitio de ENIGH
2. Descargar "Conjunto de datos" y localizar `concentradohogar.csv` dentro del ZIP
3. Colocar en `datos/enigh/` con los nombres `enigh_2016.csv`, `enigh_2018.csv`, `enigh_2020.csv`, `enigh_2022.csv`, `enigh_2024.csv`

---

### Pobreza Multidimensional 2024 (CONEVAL)

Medición oficial de pobreza por entidad federativa. Un archivo Excel con una hoja por estado y una hoja resumen nacional.

| Campo | Valor |
|---|---|
| URL | https://www.coneval.org.mx/coordinacion/entidades/Paginas/inicioent.aspx |
| Cobertura | 32 entidades · 2024 |
| Formato | XLSX (`pm_ef_2024.xlsx`) |
| Licencia | Datos Abiertos de México — https://datos.gob.mx/libreusomx |

**Descarga:**
1. Ir a la URL e ingresar a cada entidad federativa
2. Descargar el archivo de pobreza por entidad federativa 2024
3. Colocar en `datos/pobreza_multidimensional/pm_ef_2024.xlsx`

---

### Censo de Población y Vivienda 2020 (INEGI)

Tabulados ampliados por entidad federativa para etnicidad, educación e inseguridad alimentaria.

| Campo | Valor |
|---|---|
| URL | https://www.inegi.org.mx/programas/ccpv/2020/ |
| Cobertura | 32 entidades · corte censal marzo 2020 |
| Formato | XLSX (tabulados ampliados) |
| Licencia | Datos Abiertos de México — https://datos.gob.mx/libreusomx |

**Archivos y rutas:**
```
datos/censo2020/
  cpv2020_a_educacion.xlsx    ← hoja 04: población con educación superior
  cpv2020_a_etnicidad.xlsx    ← hoja 02: autoadscripción indígena por estado
  cpv2020_a_alimentacion.xlsx ← hoja 02: inseguridad alimentaria por estado
```

Solo se usan registros con Sexo = Total y Estimador = Valor.

---

### Migración origen-destino 2015–2020 (INEGI / Censo 2020)

Tabulado complementario del Censo que registra la entidad de residencia en 2015 y en 2020 para la población de 5 años y más. Construye la matriz de flujos interestatales del Acto 5.

| Campo | Valor |
|---|---|
| URL | https://www.inegi.org.mx/programas/ccpv/2020/#Tabulados |
| Cobertura | 32 entidades · todos los municipios · corte censal 2020 |
| Formato | CSV (delimitador `;`, encoding UTF-8) |
| Licencia | Datos Abiertos de México — https://datos.gob.mx/libreusomx |

**Descarga:**
1. Ir a la URL → sección "Tabulados" → "Tabulados complementarios"
2. Descargar "Migración origen-destino 2020" (xlsx → convertir a CSV con delimitador `;`)
3. Colocar en `datos/migracion_od/cpv2020_migracion_municipios_2015_2020.csv`

---

### Índice de Competitividad Estatal 2020 (IMCO)

Vincula la pobreza con la calidad del mercado laboral. Usamos la hoja `Ind (18)` (datos 2018, el año más reciente en formato Excel — las ediciones 2022 y 2023 solo existen como PDF).

| Campo | Valor |
|---|---|
| URL | https://imco.org.mx/wp-content/uploads/2020/06/ICE-2020_Base-de-datos.xlsx |
| Cobertura | 32 entidades · datos 2018 |
| Formato | XLSX (hoja `Ind (18)`) |
| Licencia | Público — descarga directa |

**Variables usadas:** columna 59 (informalidad laboral %), columna 40 (migración neta)

**Descarga:** descargar el archivo desde la URL y colocar en `datos/imco/ICE_2020_Base_datos.xlsx`

---

## Por qué estas fuentes son las correctas

El ODS 1 tiene como meta 1.2 reducir la pobreza en todas sus dimensiones. La medición de pobreza multidimensional de CONEVAL es el indicador oficial de México para este ODS. La ENIGH es la fuente oficial de ingresos que México usa para reportar ante la ONU. El Censo 2020 conecta la pobreza con sus determinantes estructurales (etnicidad, educación, alimentación). El ICE IMCO la conecta con la calidad del mercado laboral, el mecanismo por el que la pobreza se perpetúa o se supera.

Decidimos no usar datos del Banco Mundial ni de la ONU porque la pregunta es específicamente regional: Norte, Centro, Sur y CDMX dentro de México, y esas fuentes no tienen ese nivel de desagregación.

La combinación de las cuatro fuentes permite triangular: si la pobreza sube (CONEVAL), el ingreso no crece (ENIGH), la informalidad es alta (IMCO) y la población indígena es mayoritaria (Censo), eso no es coincidencia. Es estructura. Ninguna fuente sola puede decir eso.

---

## Audiencia y potencial de impacto

| Audiencia | Uso del dashboard |
|---|---|
| **Diseñadores de política pública** | Identificar qué regiones requieren intervenciones urgentes y qué mecanismos son los más activos. Los seis actos están ordenados como un argumento de política, no solo como visualización. |
| **Periodistas y comunicadores** | Narrativa con datos verificables que traduce la estadística agregada en historias concretas: Chiapas no es un dato, es 66% de personas frente al 10% de Baja California bajo el mismo presupuesto federal. |
| **Investigadores y sociedad civil** | Código reproducible, fuentes auditadas y notebooks exploratorios disponibles para continuar el análisis o adaptarlo a preguntas derivadas. |

En un contexto donde el gobierno federal reporta avances usando promedios nacionales, ASHIRA demuestra que ese promedio oculta una brecha territorial de 56 puntos porcentuales que lleva ocho años sin cerrarse. Eso es exactamente lo que el ODS 10 señala como el problema central.

---

## Estructura del repositorio

```
Ashira/
├── README.md                          ← Este archivo
├── ai-log.md                          ← Registro de uso de IA
├── LICENSE                            ← CC BY-SA 4.0
├── pyproject.toml                     ← Dependencias del proyecto (uv)
├── .gitignore
├── datos/
│   ├── shapefiles/                    ← GeoJSON de estados de México (incluido)
│   ├── migracion_od/                  ← Migración OD Censo 2020 (no incluido)
│   └── [demás datos]                  ← No incluidos — ver instrucciones arriba
├── scripts/
│   ├── parse_censo.py                 ← Parser de tabulados del Censo 2020
│   └── build_ashira.py                ← Construye el dataset maestro
├── exploracion_datos/
│   ├── ENIGH_Hogares/                 ← Análisis exploratorio de ingresos (ENIGH 2016–2024)
│   ├── Pobreza_Multidimensional/      ← Análisis exploratorio de PM CONEVAL 2024
│   └── Censo_Competitividad/          ← Análisis exploratorio de Censo 2020 e ICE IMCO
├── dashboard/
│   ├── index.qmd                      ← Fuente del dashboard (Quarto + Python) ← PRINCIPAL
│   ├── _quarto.yml                    ← Configuración de Quarto (output → docs/)
│   ├── ashira_custom.css              ← Estilos del dashboard
│   ├── ASHIRA_narrativa.ipynb         ← Notebook equivalente (Jupyter)
│   └── ASHIRA_narrativa.qmd          ← Versión narrativa alternativa
└── docs/
    └── index.html                     ← Dashboard generado (resultado final)
```

---

## Exploración de datos

La carpeta `exploracion_datos/` contiene los notebooks de análisis exploratorio que precedieron al dashboard. Son la evidencia del proceso de investigación: qué preguntamos a cada dataset, qué descartamos y por qué.

| Carpeta | Contenido |
|---|---|
| `ENIGH_Hogares/` | Distribución de ingreso per cápita por estado y año, descomposición por fuente (trabajo, transferencias, remesas) |
| `Pobreza_Multidimensional/` | Tasas de pobreza y carencias sociales por entidad (PM CONEVAL 2024), ranking y comparativos regionales |
| `Censo_Competitividad/` | Correlación etnicidad–pobreza y educación–pobreza (Censo 2020); informalidad laboral y migración neta (ICE IMCO) |

Estos notebooks no son el producto final — son el trabajo de campo. El dashboard en `dashboard/index.qmd` sintetiza y narra los hallazgos.

---

## Declaratoria de uso de inteligencia artificial

Ver: [`ai-log.md`](ai-log.md)

El equipo utilizó herramientas de IA como acelerador técnico para corrección de bugs de sintaxis y generación de código boilerplate. Todas las decisiones analíticas — selección de fuentes, pregunta de investigación, estructura narrativa, interpretación de resultados y verificación de consistencia — son trabajo exclusivo del equipo. El registro completo de interacciones, prompts y decisiones está en [`ai-log.md`](ai-log.md).

---

*ASHIRA · HackODS UNAM 2026 · ODS 1 y ODS 10*
*Fuentes: INEGI · CONEVAL · IMCO · Censo 2020 · Migración OD — todas oficiales y de acceso público*
