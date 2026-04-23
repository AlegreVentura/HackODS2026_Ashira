# ASHIRA

**En México no se puede hablar de pobreza sin hablar de dónde naciste.**

HackODS UNAM 2026 · ODS 1 — Fin de la Pobreza · ODS 10 — Reducción de las Desigualdades

Licencia: [CC BY-SA 4.0](LICENSE)

---

## El equipo

| Integrante | Origen | Contribución |
|---|---|---|
| Melisa Asharet Arano Bejarano | Veracruz | Análisis de ingreso y desigualdad territorial (ENIGH 2016–2024) |
| Roberto Jhoshua Alegre Ventura | Guerrero | Análisis de pobreza multidimensional por estado (PM CONEVAL 2024) |
| Israel Martínez Jiménez | Estado de México | Análisis de estructura territorial, etnicidad y competitividad (Censo 2020 e ICE IMCO) |

---

## Declaratoria de uso de inteligencia artificial

Ver: [`ai-log.md`](ai-log.md)

El equipo utilizó herramientas de IA como acelerador técnico para corrección de bugs de sintaxis y generación de código boilerplate. Todas las decisiones analíticas — selección de fuentes, pregunta de investigación, estructura narrativa, interpretación de resultados y verificación de consistencia — son trabajo exclusivo del equipo. El registro completo de interacciones, prompts y decisiones del equipo está en [`ai-log.md`](ai-log.md).

---

## Qué es ASHIRA

México tiene 32 estados con realidades que no caben en un solo número. Cuando el INEGI reporta que la pobreza bajó, tiene razón — pero oculta que en Chiapas sigue en 66% mientras en Baja California es 10%. Oculta que el ingreso del Sur depende cada vez más de remesas y programas gubernamentales, no de trabajo formal. Oculta que los estados más pobres son los que más gente pierden.

### Pregunta central

> **¿En qué medida el estado donde nació una persona en México determina su probabilidad de vivir en pobreza  y por qué esa determinación no ha disminuido en ocho años de datos?**

La perspectiva es territorial, no solo económica: no preguntamos cuánta pobreza hay, sino *por qué el código postal sigue siendo el mejor predictor de si alguien será pobre*. La respuesta involucra estructura étnica, mercado laboral informal, dependencia de transferencias externas y emigración forzada — mecanismos que los promedios nacionales hacen invisibles.

ASHIRA cruza cuatro fuentes de datos oficiales para construir una narrativa en seis actos que responde esa pregunta. El resultado es un dashboard interactivo que pone la pobreza en el mapa, estado por estado, y demuestra que la brecha territorial no se ha cerrado entre 2016 y 2024.

---

## La historia en seis actos

1. **Los dos Méxicos** — Chiapas (66% en pobreza) frente a Baja California (10%). 56 puntos de diferencia bajo la misma bandera.
2. **La brecha que no cierra** — El Norte gana 1.7 veces más que el Sur en 2024. En 2016 era 1.6 veces. Ocho años, la misma estructura.
3. **Las raíces** — Correlación etnicidad-pobreza (r ≈ 0.8). A mayor informalidad laboral, menor ingreso mediano, sin excepción.
4. **El parche** — Los estados del Sur viven cada vez más de transferencias gubernamentales y remesas, no de trabajo formal propio.
5. **Los que se van** — Los estados más pobres son los que más población pierden. La emigración es la única válvula de escape disponible.
6. **¿Está cambiando?** — El ingreso creció en todos los estados entre 2016 y 2024. Pero los estados ricos crecieron más, en pesos absolutos, que los pobres.

---

## Audiencia y potencial de impacto

ASHIRA está dirigido a tres audiencias concretas:

- **Diseñadores de política pública** — el dashboard permite identificar qué estados requieren intervenciones urgentes y qué mecanismos (informalidad laboral, dependencia de transferencias, emigración) son los más activos en cada región. Los seis actos están ordenados como un argumento de política, no solo como visualización.
- **Periodistas y comunicadores** — una narrativa con datos oficiales verificables que traduce la estadística agregada en historias estatales: Chiapas no es un dato, es 66% de personas en pobreza frente al 10% de Baja California, bajo la misma ley y el mismo presupuesto federal.
- **Investigadores y sociedad civil** — código reproducible, fuentes auditadas y notebooks exploratorios disponibles para continuar el análisis o adaptarlo a preguntas derivadas.

El impacto concreto: en un contexto donde el gobierno federal reporta avances usando promedios nacionales, ASHIRA demuestra que ese promedio oculta una brecha territorial de 56 puntos porcentuales que lleva ocho años sin cerrarse. Eso es lo que el ODS 10 — Reducción de las Desigualdades — señala como el problema central, y es lo que los datos muestran.

---

## Los datos

Todas las fuentes son instituciones del Estado mexicano o institutos de investigación independientes con metodologías auditadas. Los archivos de datos no están en el repositorio por restricciones de tamaño de GitHub. Descárgalos con las instrucciones siguientes.

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

### Censo de Población y Vivienda 2020 (INEGI)

Tabulados ampliados por entidad federativa. Usamos tres archivos para etnicidad, educación e inseguridad alimentaria.

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

### Migración origen-destino entre entidades federativas 2015–2020 (INEGI)

Tabulado complementario del Censo 2020 que registra la entidad y municipio de residencia en marzo de 2015 y en marzo de 2020 para la población de 5 años y más. Permite construir la matriz de flujos origen-destino a nivel estatal y municipal. Usamos este archivo para el mapa de flujos interestatales del Acto 5.

| Campo | Valor |
|---|---|
| URL | https://www.inegi.org.mx/programas/ccpv/2020/#Tabulados |
| Cobertura | 32 entidades · todos los municipios · corte censal 2020 |
| Formato | CSV (separado por punto y coma, encoding UTF-8) |
| Peso | 10.6 MB |
| Licencia | Datos Abiertos de México — https://datos.gob.mx/libreusomx |

**Variables usadas:** entidad de residencia en 2015, entidad de residencia en 2020, población de 5 años y más (total de personas por par origen-destino)

**Archivo y ruta:**
```
datos/migracion_od/
  cpv2020_migracion_municipios_2015_2020.csv  ← tabulado complementario de migración OD
```

**Descarga:**
1. Ir a la URL (sección "Tabulados" → "Tabulados complementarios")
2. Descargar "Migración origen-destino 2020" (xlsx → convertir a CSV con delimitador `;`)
3. Colocar en `datos/migracion_od/cpv2020_migracion_municipios_2015_2020.csv`

---

### Índice de Competitividad Estatal 2020 (IMCO)

Permite vincular la pobreza con la calidad del mercado laboral. Usamos la hoja `Ind (18)` que corresponde a datos de 2018, el año más reciente disponible en formato Excel (las ediciones 2022 y 2023 solo existen como PDF).

| Campo | Valor |
|---|---|
| URL | https://imco.org.mx/wp-content/uploads/2020/06/ICE-2020_Base-de-datos.xlsx |
| Cobertura | 32 entidades · datos 2018 |
| Formato | XLSX (hoja `Ind (18)`) |
| Licencia | Público — descarga directa |

**Variables usadas:** columna 59 (informalidad laboral %), columna 40 (migración neta)

**Descarga:**
1. Descargar el archivo desde la URL
2. Colocar en `datos/imco/ICE_2020_Base_datos.xlsx`

---

## Exploración de datos

La carpeta `exploracion_datos/` contiene los notebooks de análisis exploratorio que precedieron al dashboard. Están organizados por fuente y son la evidencia del proceso de investigación: qué preguntamos a cada dataset, qué descartamos y por qué.

| Carpeta | Contenido |
|---|---|
| `ENIGH_Hogares/` | Distribución de ingreso per cápita por estado y año, descomposición por fuente (trabajo, transferencias, remesas) |
| `Pobreza_Multidimensional/` | Tasas de pobreza y carencias sociales por entidad (PM CONEVAL 2024), ranking y comparativos regionales |
| `Censo_Competitividad/` | Correlación etnicidad–pobreza y educación–pobreza (Censo 2020); informalidad laboral y migración neta (ICE IMCO) |

Estos notebooks no son el producto final — son el trabajo de campo. El dashboard en `dashboard/ASHIRA_narrativa.qmd` sintetiza y narra los hallazgos.

---

## Cómo reproducir el análisis

### Requisitos

```bash
pip install pandas numpy openpyxl geopandas plotly
```

Python 3.10 o mayor. Para generar el dashboard también necesitas [Quarto 1.9+](https://quarto.org) y el kernel de Jupyter configurado.

### Pasos

```bash
# 1. Descarga los datos según las instrucciones de arriba

# 2. Genera el dataset maestro
python scripts/build_ashira.py

# 3. Renderiza el dashboard
cd dashboard
quarto render ASHIRA_narrativa.qmd
```

El resultado es `dashboard/ASHIRA_narrativa.html`, un archivo que se abre directo en el navegador sin necesidad de servidor.

> **Alternativa sin Quarto:** el dashboard también está disponible como `dashboard/ASHIRA_narrativa.ipynb`, un notebook Jupyter con los mismos datos y visualizaciones. Se puede ejecutar con `jupyter notebook` o revisar directamente en GitHub sin instalar Quarto.

---

## Estructura del repositorio

```
Ashira/
├── README.md                          ← Este archivo
├── ai-log.md                          ← Registro de uso de IA (módulo requerido)
├── LICENSE                            ← CC BY-SA 4.0
├── .gitignore
├── datos/
│   ├── shapefiles/                    ← GeoJSON de estados de México (incluido, 180 KB)
│   ├── migracion_od/                  ← Migración origen-destino Censo 2020 (no incluido)
│   └── [datos descargados]            ← No incluidos — ver instrucciones arriba
├── scripts/
│   ├── parse_censo.py                 ← Parser de tabulados del Censo 2020
│   └── build_ashira.py                ← Construye el dataset maestro y el notebook
├── exploracion_datos/
│   ├── ENIGH_Hogares/                 ← Análisis exploratorio de ingresos (ENIGH 2016–2024)
│   │   └── exploracion_pobreza_mexico.ipynb
│   ├── Pobreza_Multidimensional/      ← Análisis exploratorio de PM CONEVAL 2024
│   │   └── analisis_pobreza_mexico.ipynb
│   └── Censo_Competitividad/          ← Análisis exploratorio de Censo 2020 e ICE IMCO
│       ├── analisis_censo_pobreza.ipynb
│       └── analisis_competitividad.ipynb
└── dashboard/
    ├── ASHIRA_narrativa.qmd           ← Fuente del dashboard (Quarto + Python)
    ├── ASHIRA_narrativa.ipynb         ← Notebook equivalente (Jupyter)
    ├── ASHIRA_narrativa.html          ← Dashboard generado (resultado final)
    ├── ashira_custom.css              ← Estilos del dashboard
    └── imagenes/                      ← Visualizaciones exportadas como PNG
```

---

## Por qué estas fuentes son las correctas

El ODS 1 tiene como meta 1.2 reducir la pobreza en todas sus dimensiones. La medición de pobreza multidimensional de CONEVAL es el indicador oficial de México para este ODS. La ENIGH es la fuente oficial de ingresos que México usa para reportar ante la ONU. El Censo 2020 conecta la pobreza con sus determinantes estructurales (etnicidad, educación, alimentación). El ICE IMCO la conecta con la calidad del mercado laboral, el mecanismo por el que la pobreza se perpetúa o se supera.

Decidimos no usar datos del Banco Mundial ni de la ONU porque la pregunta es específicamente subnacional: estado por estado dentro de México, y esas fuentes no tienen ese nivel de desagregación.

La combinación de las cuatro fuentes permite triangular: si la pobreza sube (CONEVAL), el ingreso no crece (ENIGH), la informalidad es alta (IMCO) y la población indígena es mayoritaria (Censo), eso no es coincidencia. Es estructura. Ninguna fuente sola puede decir eso.

---

*ASHIRA · HackODS UNAM 2026 · ODS 1 y ODS 10*
*Fuentes: INEGI · CONEVAL · IMCO · Censo 2020 · Migración OD Censo 2020 — todas oficiales y de acceso público*
