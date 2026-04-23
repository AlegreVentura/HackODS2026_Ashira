# Fuentes de Datos — Israel Martínez Jiménez
## HackODS: Pobreza Territorial en México

Narrativa central: **"En México no se puede hablar de pobreza sin hablar de dónde naciste."**

---

## Estructura de carpetas

```
Posibles Datos Israel/
├── fuentes investigadas.md
├── analisis_censo_pobreza.ipynb     ← notebook Censo 2020
├── analisis_competitividad.ipynb    ← notebook IMCO ICE
│
├── scripts/
│   ├── parse_censo.py               ← parser de tabulados INEGI
│   ├── build_notebook.py            ← generador notebook Censo 2020
│   └── build_notebook_imco.py       ← generador notebook IMCO
│
├── datos/
│   ├── censo2020/                   ← tabulados ampliados Censo 2020
│   │   ├── cpv2020_a_poblacion.xlsx
│   │   ├── cpv2020_a_educacion.xlsx
│   │   ├── cpv2020_a_economia.xlsx
│   │   ├── cpv2020_a_etnicidad.xlsx
│   │   ├── cpv2020_a_salud.xlsx
│   │   ├── cpv2020_a_vivienda.xlsx
│   │   ├── cpv2020_a_alimentacion.xlsx
│   │   ├── cpv2020_a_ingresos.xlsx
│   │   ├── cpv2020_a_migracion.xlsx
│   │   └── cpv2020_a_discapacidad.xlsx
│   │
│   └── imco/                        ← Índice de Competitividad Estatal
│       ├── ICE_2016_Base_datos.xlsx
│       ├── ICE_2018_Base_datos.xlsx
│       ├── ICE_2020_Base_datos.xlsx
│       ├── Reporte-Competitividad-Estatal-2022.pdf
│       └── Boletas-por-estado-ICE2022.pdf
│
└── imagenes/
    ├── isr_*.png                    ← gráficas Censo 2020
    └── ice_*.png                    ← gráficas IMCO
```

---

## Fuente — Censo de Población y Vivienda 2020 (INEGI)

### Información General

| Campo | Valor |
|---|---|
| **Fuente** | INEGI — Instituto Nacional de Estadística y Geografía |
| **Nombre del dataset** | Censo de Población y Vivienda 2020 — Tabulados Ampliados |
| **URL del programa** | https://www.inegi.org.mx/programas/ccpv/2020/ |
| **Fecha de descarga** | 12 de abril de 2026 |
| **Método de descarga** | DescargaMasiva INEGI (ZIP `DescargaMasiva_1242026_1700.zip`) |
| **Cobertura temporal** | 2020 (corte censal, marzo 2020) |
| **Cobertura geográfica** | 32 entidades federativas de México |
| **Formato** | XLSX (tabulados con estimadores ampliados) |
| **Licencia** | Datos Abiertos de México |

**Descripción:** Tabulados ampliados del cuestionario ampliado del Censo 2020. Incluyen
estimadores (valor, error estándar, intervalo de confianza, coeficiente de variación)
desglosados por tamaño de localidad y por entidad federativa.

### Archivos utilizados en el análisis

| Archivo | Tema | Hojas usadas | Indicadores clave |
|---------|------|-------------|-------------------|
| `cpv2020_a_educacion.xlsx` | Educación | 04 (por estado) | Población con educación superior |
| `cpv2020_a_etnicidad.xlsx` | Etnicidad | 02 (por estado) | % autoadscripción indígena |
| `cpv2020_a_salud.xlsx` | Salud | 02 (por estado) | % uso de servicios de salud, % IMSS |
| `cpv2020_a_alimentacion.xlsx` | Alimentación | 02 (por estado) | % inseguridad alimentaria |
| `cpv2020_a_vivienda.xlsx` | Vivienda | (disponible) | Materiales, servicios, TIC |
| `cpv2020_a_economia.xlsx` | Economía | (disponible) | Ocupación, posición en el trabajo |
| `cpv2020_a_poblacion.xlsx` | Población | (disponible) | Pirámide, distribución etaria |
| `cpv2020_a_migracion.xlsx` | Migración | (disponible) | Migración interna e internacional |
| `cpv2020_a_discapacidad.xlsx` | Discapacidad | (disponible) | Prevalencia por estado |
| `cpv2020_a_ingresos.xlsx` | Ingresos | (disponible) | Ingresos no laborales |

### Estructura de los tabulados

Cada archivo Excel contiene:
- **Hoja `Índice`**: Listado de tabulados con desglose (tamaño de localidad o entidad federativa)
- **Hojas impares (01, 03, ...)**: Desglose por tamaño de localidad (nivel nacional)
- **Hojas pares (02, 04, ...)**: Desglose por entidad federativa (32 estados + EUM)

Cada bloque de datos por entidad contiene:
- Sexo: Total / Hombres / Mujeres
- Estimador: Valor / Error estándar / Límites de confianza / Coef. de variación

**Solo se extraen:** `Sexo == "Total"` y `Estimador == "Valor"`.

---

## Rol en la narrativa del proyecto

Los datos del Censo 2020 aportan la capa **estructural** al análisis de pobreza territorial:

| Indicador censal | Qué revela | Conexión con la narrativa |
|------------------|-----------|--------------------------|
| Educación superior | Capital humano por estado | Menos universidades → menos oportunidades → más pobreza |
| Autoadscripción indígena | Componente étnico de la desigualdad | La exclusión histórica se mide en datos |
| Uso de servicios de salud | Protección social efectiva | Sin salud no hay movilidad social |
| Inseguridad alimentaria | Privación material básica | El hambre tiene código postal |

**Insight principal:** La correlación entre % población indígena y % pobreza por estado
demuestra que la desigualdad territorial en México tiene raíces históricas y étnicas,
no solo económicas.

---

---

## Fuente — Índice de Competitividad Estatal (IMCO)

### Información General

| Campo | Valor |
|---|---|
| **Fuente** | IMCO — Instituto Mexicano para la Competitividad |
| **Nombre del dataset** | Índice de Competitividad Estatal (ICE) — Base de datos |
| **URL de descarga 2016** | https://imco.org.mx/wp-content/uploads/2016/11/2016-ICE_2016-Base_datos.xlsx |
| **URL de descarga 2018** | https://imco.org.mx/wp-content/uploads/2019/11/ICE_2018_El_estado_los_estados_la_gente.xlsx |
| **URL de descarga 2020** | https://imco.org.mx/wp-content/uploads/2020/06/ICE-2020_Base-de-datos.xlsx |
| **Fecha de descarga** | 12 de abril de 2026 |
| **Cobertura temporal** | ICE 2020 contiene series anuales 2001–2018 (última edición con Excel público) |
| **Cobertura geográfica** | 32 entidades federativas de México |
| **Formato** | XLSX (series por indicador y año) |
| **Licencia** | Público — descarga directa en imco.org.mx |

**Descripción:** El ICE mide qué tan atractivos son los estados para el talento y la
inversión. Incluye ~100 indicadores agrupados en 10 subíndices: Derecho, Medio Ambiente,
Sociedad, Político, Gobiernos, Mercado de Factores, Economía, Precursores, Relaciones
Internacionales e Innovación. La edición 2020 es la más reciente con base de datos pública
descargable; las ediciones 2022 y 2023 solo publicaron PDFs.

### Archivos y cobertura de datos

| Archivo | Edición | Años de datos disponibles |
|---------|---------|--------------------------|
| `ICE_2016_Base_datos.xlsx` | ICE 2016 | 2003–2016 (14 años) |
| `ICE_2018_Base_datos.xlsx` | ICE 2018 | 2003–2018 (16 años) |
| `ICE_2020_Base_datos.xlsx` | ICE 2020 | 2001–2018 (18 años) ← **fuente principal** |
| `Reporte-Competitividad-Estatal-2022.pdf` | ICE 2022 | Solo PDF, sin datos descargables |
| `Boletas-por-estado-ICE2022.pdf` | ICE 2022 | Solo PDF, sin datos descargables |

### Estructura de los archivos Excel

Cada Excel contiene hojas `Ind (01)` a `Ind (N)` donde `Ind (N)` = año `2000+N`:
- `Ind (16)` → datos de 2016
- `Ind (18)` → datos de 2018 (última disponible en ICE 2020)

Cada hoja tiene: columna 0 = clave INEGI, columna 1 = nombre estado, columnas 2+ = indicadores.

### Indicadores utilizados en el análisis

| Col | Subíndice | Indicador | Conexión narrativa |
|-----|-----------|-----------|-------------------|
| 21 | Sociedad | Pobreza (%) | Validación cruzada con PM/ENIGH |
| 27 | Sociedad | Analfabetismo | Capital humano por estado |
| 28 | Sociedad | Escolaridad | Capital humano por estado |
| 40 | Sociedad | Migración neta | El sur pierde a sus jóvenes |
| 59 | Gobiernos | Informalidad laboral (%) | Calidad del empleo |
| 60 | Mercado | Ingreso promedio de trabajadores | Cruce directo con ENIGH |
| 61 | Mercado | Desigualdad salarial | ODS 10 |
| 62 | Mercado | Personas bajo línea de bienestar | ODS 1 |
| 68 | Economía | PIB per cápita | Brecha económica territorial |

### Coherencia temporal con las demás fuentes

| Año ENIGH (Melisa) | Dato ICE disponible |
|--------------------|---------------------|
| 2016 | ✅ `Ind (16)` en ICE 2020 |
| 2018 | ✅ `Ind (18)` en ICE 2020 |
| 2020 | ❌ ICE 2020 solo llega hasta datos de 2018 |
| 2022 | ❌ Solo PDF |
| 2024 | ❌ Solo PDF |

### Rol en la narrativa del proyecto

| Indicador ICE | Qué revela | Conexión con la narrativa |
|---------------|-----------|--------------------------|
| Informalidad laboral | Calidad del mercado de trabajo | El empleo informal no genera movilidad social |
| Ingreso promedio (ICE) vs Ingreso mediano (ENIGH) | Consistencia entre fuentes | Dos metodologías distintas, misma brecha |
| Migración neta | Quién pierde capital humano | Los estados menos competitivos exportan talento |
| Desigualdad salarial | Concentración del ingreso | La brecha no es solo entre estados, es dentro |

**Insight adicional:** La correlación entre competitividad IMCO y pobreza CONEVAL confirma
que la pobreza territorial no es aleatoria — tiene raíces en la calidad de las instituciones,
el mercado laboral y el acceso a servicios que el ICE mide sistemáticamente.

---

*ASHIRA · HackODS UNAM 2026 · ODS 1 + ODS 10*
