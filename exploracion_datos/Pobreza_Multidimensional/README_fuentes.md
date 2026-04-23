# Fuentes de Datos — HackODS: Pobreza Territorial en México

Narrative central: **"En México no se puede hablar de pobreza sin hablar de dónde naciste."**

---

## Estructura de carpetas

```
Posibles Datos/
├── README_fuentes.md
├── analisis_pobreza_mexico.ipynb
│
├── scripts/
│   ├── build_notebook.py      ← genera el notebook desde cero
│   ├── patch_mgn.py           ← inyecta celdas del Marco Geoestadístico
│   ├── patch_enoe.py          ← inyecta celdas de informalidad laboral (ENOE)
│   └── viz_utils.py           ← paleta y helpers de visualización
│
├── datos/
│   ├── lineas_pobreza/        ← LP: valor mensual de canastas
│   ├── pobreza_laboral/       ← PL: % sin ingreso para canasta, trimestral
│   ├── pobreza_multidimensional/ ← PM: indicadores por entidad 2016–2024
│   ├── derechos_sociales/     ← SIDS: acceso efectivo a derechos
│   ├── marco_geoestadistico/  ← MGN: polígonos de entidades (caché GeoJSON)
│   └── ocupacion_y_empleo/    ← ENOE: informalidad por estado 2024 (CSV agregado)
│
└── imagenes/
    └── fig_*.png              ← 17 gráficas generadas
```

---

## Fuente 1 — Líneas de Pobreza (LP)

**URL portal:** https://www.inegi.org.mx/desarrollosocial/lp/#tabulados  
**Publicación reciente:** 11 de marzo de 2026  
**Próxima publicación:** 13 de abril de 2026

**Archivos descargados:**

| Archivo | URL directa | Descripción |
|---------|-------------|-------------|
| `datos/lineas_pobreza/lp_2026.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_2026.xlsx | Valor mensual de las líneas de pobreza (rural y urbano) enero 1992 – febrero 2026 |
| `datos/lineas_pobreza/lp_cvm_1992_2026.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_cvm_1992_2026.xlsx | Composición y valor de la canasta básica (agosto 2026) |

**Contenido clave:**
- Línea de Pobreza por Ingresos (canasta alimentaria + no alimentaria) — Rural y Urbano
- Línea de Pobreza Extrema por Ingresos (solo canasta alimentaria) — Rural y Urbano
- Serie mensual desde enero de 1992

---

## Fuente 2 — Pobreza Laboral (PL)

**URL portal:** https://www.inegi.org.mx/desarrollosocial/pl/#tabulados  
**Publicación reciente:** 25 de febrero de 2026  
**Próxima publicación:** 27 de mayo de 2026

**Archivos descargados:**

| Archivo | URL directa | Descripción |
|---------|-------------|-------------|
| `datos/pobreza_laboral/pl_2005t_2025t.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pl/tabulados/pl_2005t_2025t.xlsx | Serie trimestral Q1-2005 a Q4-2025; % pobreza laboral por estado |

**Contenido clave (hojas principales):**
- `Cuadro 1` — ITLP nacional por ámbito rural/urbano (2005–2025)
- `Cuadro 2` — % población con ingreso < canasta alimentaria, nacional
- `Cuadro 9` — % pobreza laboral por entidad federativa, trimestral (2005–2025)
- `Cuadro 18.*` — Ingreso laboral promedio por estado y sector

---

## Fuente 3 — Pobreza Multidimensional (PM)

**URL portal:** https://www.inegi.org.mx/desarrollosocial/pm/#tabulados  
**Publicación reciente:** 13 de agosto de 2025

**Archivos descargados:**

| Archivo | URL directa | Descripción |
|---------|-------------|-------------|
| `datos/pobreza_multidimensional/pm_ar_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ar_2024.xlsx | Indicadores de pobreza por ámbito rural y urbano (2016–2024) |
| `datos/pobreza_multidimensional/pm_cc_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_cc_2024.xlsx | Componentes de las carencias sociales (2016–2024) |
| `datos/pobreza_multidimensional/pm_ct_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ct_2024.xlsx | Condición territorial |
| `datos/pobreza_multidimensional/pm_ef_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ef_2024.xlsx | **Indicadores por entidad federativa** (2016–2024) — hoja por estado |
| `datos/pobreza_multidimensional/pm_gp_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_gp_2024.xlsx | Indicadores por grupo de población (sexo) |
| `datos/pobreza_multidimensional/pm_ic_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ic_2024.xlsx | **Ingreso corriente per cápita** por entidad (2016–2024) |
| `datos/pobreza_multidimensional/pm_ip_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ip_2024.xlsx | Indicadores de precisión nacional |
| `datos/pobreza_multidimensional/pm_ut_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ut_2024.xlsx | Unidades territoriales |

**Archivo estrella:** `pm_ef_2024.xlsx` — una hoja por estado (32) + EUM, con % pobreza, extrema, carencias y carencias promedio para 2016, 2018, 2020, 2022 y 2024.

---

## Fuente 4 — Sistema de Información de Derechos Sociales (SIDS)

**URL portal:** https://www.inegi.org.mx/desarrollosocial/sids/#tabulados  
**Publicación reciente:** 13 de agosto de 2025

**Archivos descargados:**

| Archivo | URL directa | Descripción |
|---------|-------------|-------------|
| `datos/derechos_sociales/sids_ia_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_ia_2024.xlsx | Acceso efectivo a la alimentación por estado (2016–2024) |
| `datos/derechos_sociales/sids_ie_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_ie_2024.xlsx | Acceso efectivo a la educación por estado (2016–2024) |
| `datos/derechos_sociales/sids_is_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_is_2024.xlsx | Acceso efectivo a la salud por estado (2016–2024) |
| `datos/derechos_sociales/sids_iss_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_iss_2024.xlsx | Acceso efectivo a la seguridad social por estado (2016–2024) |
| `datos/derechos_sociales/sids_iv_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_iv_2024.xlsx | Acceso efectivo a la vivienda por estado (2016–2024) |
| `datos/derechos_sociales/bg_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bg_2024.xlsx | Brecha de género en inseguridad alimentaria (2016–2024) |
| `datos/derechos_sociales/bmi_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bmi_2024.xlsx | Brecha étnica (indígena vs no indígena) en inseguridad alimentaria |
| `datos/derechos_sociales/bnna_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bnna_2024.xlsx | Brecha en niñas y niños (0–17 años) |
| `datos/derechos_sociales/bpam_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpam_2024.xlsx | Brecha en adultos mayores (60+ años) |
| `datos/derechos_sociales/bpd_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpd_2024.xlsx | Brecha en personas con discapacidad |
| `datos/derechos_sociales/bpj_2024.xlsx` | https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpj_2024.xlsx | Brecha en jóvenes (12–29 años) |

---

## Pasos de descarga y extracción (replicabilidad)

### Método 1 — Script Python (recomendado)

```python
import urllib.request, os

BASE_URLS = {
    "datos/lineas_pobreza/lp_2026.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_2026.xlsx",
    "datos/lineas_pobreza/lp_cvm_1992_2026.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_cvm_1992_2026.xlsx",
    "datos/pobreza_laboral/pl_2005t_2025t.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pl/tabulados/pl_2005t_2025t.xlsx",
    "datos/pobreza_multidimensional/pm_ar_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ar_2024.xlsx",
    "datos/pobreza_multidimensional/pm_cc_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_cc_2024.xlsx",
    "datos/pobreza_multidimensional/pm_ct_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ct_2024.xlsx",
    "datos/pobreza_multidimensional/pm_ef_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ef_2024.xlsx",
    "datos/pobreza_multidimensional/pm_gp_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_gp_2024.xlsx",
    "datos/pobreza_multidimensional/pm_ic_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ic_2024.xlsx",
    "datos/pobreza_multidimensional/pm_ip_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ip_2024.xlsx",
    "datos/pobreza_multidimensional/pm_ut_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/pm_ut_2024.xlsx",
    "datos/derechos_sociales/bg_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bg_2024.xlsx",
    "datos/derechos_sociales/bmi_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bmi_2024.xlsx",
    "datos/derechos_sociales/bnna_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bnna_2024.xlsx",
    "datos/derechos_sociales/bpam_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpam_2024.xlsx",
    "datos/derechos_sociales/bpd_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpd_2024.xlsx",
    "datos/derechos_sociales/bpj_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/bpj_2024.xlsx",
    "datos/derechos_sociales/sids_ia_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_ia_2024.xlsx",
    "datos/derechos_sociales/sids_ie_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_ie_2024.xlsx",
    "datos/derechos_sociales/sids_is_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_is_2024.xlsx",
    "datos/derechos_sociales/sids_iss_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_iss_2024.xlsx",
    "datos/derechos_sociales/sids_iv_2024.xlsx":
        "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/sids_iv_2024.xlsx",
}

headers = {"User-Agent": "Mozilla/5.0"}

for path, url in BASE_URLS.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    print(f"OK  {path}  ({len(data)//1024} KB)")
```

### Método 2 — curl (terminal)

```bash
# Crear carpetas
mkdir -p datos/lp datos/pl datos/pm datos/sids imagenes

# LP
curl -A "Mozilla/5.0" -o datos/lineas_pobreza/lp_2026.xlsx \
  "https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_2026.xlsx"
curl -A "Mozilla/5.0" -o datos/lineas_pobreza/lp_cvm_1992_2026.xlsx \
  "https://www.inegi.org.mx/contenidos/desarrollosocial/lp/tabulados/lp_cvm_1992_2026.xlsx"

# PL
curl -A "Mozilla/5.0" -o datos/pobreza_laboral/pl_2005t_2025t.xlsx \
  "https://www.inegi.org.mx/contenidos/desarrollosocial/pl/tabulados/pl_2005t_2025t.xlsx"

# PM
for f in pm_ar pm_cc pm_ct pm_ef pm_gp pm_ic pm_ip pm_ut; do
  curl -A "Mozilla/5.0" -o datos/pobreza_multidimensional/${f}_2024.xlsx \
    "https://www.inegi.org.mx/contenidos/desarrollosocial/pm/tabulados/${f}_2024.xlsx"
done

# SIDS
for f in bg bmi bnna bpam bpd bpj; do
  curl -A "Mozilla/5.0" -o datos/derechos_sociales/${f}_2024.xlsx \
    "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/${f}_2024.xlsx"
done
for f in sids_ia sids_ie sids_is sids_iss sids_iv; do
  curl -A "Mozilla/5.0" -o datos/derechos_sociales/${f}_2024.xlsx \
    "https://www.inegi.org.mx/contenidos/desarrollosocial/sids/tabulados/${f}_2024.xlsx"
done
```

### Regenerar el notebook desde cero

```bash
# 1. Descargar datos (ver Método 1 o 2 arriba)
# 2. Regenerar y ejecutar el notebook
python scripts/build_notebook.py
python -m nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=300 \
  analisis_pobreza_mexico.ipynb
```

---

## Notas sobre los ZIPs originales

Los ZIPs de INEGI (`DescargaMasiva_*.zip`) NO contienen los datos directamente.
Contienen un `DescargaMasivaApp.exe` y un `DescargaMasivaOD.xml` con las URLs reales.
Los archivos Excel se deben descargar manualmente desde esas URLs (ver tabla arriba).

```
DescargaMasiva_842026_14152.zip   → LP  (lp_2026.xlsx + lp_cvm_1992_2026.xlsx)
DescargaMasiva_842026_141758.zip  → PL  (pl_2005t_2025t.xlsx)
DescargaMasiva_842026_141945.zip  → PM  (8 archivos pm_*.xlsx)
DescargaMasiva_842026_142048.zip  → SIDS (11 archivos)
```

---

## Estado de integración de fuentes

| # | Fuente | Tipo | Estado |
|---|--------|------|--------|
| 1–4 | INEGI LP, PL, PM, SIDS | INEGI oficial (Excel) | Integrada |
| 5 | Marco Geoestadístico Nacional (MGN) | INEGI REST API / caché GeoJSON | Integrada |
| 6 | ENOE — Ocupación y Empleo 2024 T4 | INEGI microdata CSV (ZIP en línea) | Integrada |
| 7+ | Por definir | — | Pendiente |

---

## Fuente 5 — Marco Geoestadístico Nacional (MGN)

**API REST oficial:** `https://geoservicios.inegi.org.mx/arcgis/rest/services/marcogeoestadistico/MapServer/1/query`

**Parámetros de la consulta:**
```
?where=1=1
&outFields=CVE_ENT,NOMGEO
&returnGeometry=true
&f=geojson
&outSR=4326
```

**Caché local:** `datos/marco_geoestadistico/entidades.geojson`

El notebook descarga automáticamente desde la API de INEGI al ejecutarse por primera vez.
Si el servicio no está disponible, usa una fuente de respaldo y guarda el resultado en caché.
Ejecuciones posteriores leen desde la caché local sin necesidad de conexión.

**Proyección usada en el análisis:** EPSG:6372 (ITRF2008 / LCC — proyección oficial del INEGI para México)

**Habilita:**
- `fig_mapa_pobreza.png` — coroplético de % pobreza 2024 + panel comparativo
- `fig_mapa_cambio.png` — coroplético de cambio 2016→2024 (mapa divergente)

---

## Fuente 6 — ENOE: Encuesta Nacional de Ocupación y Empleo

**Descripción:** Encuesta trimestral de hogares que mide ocupación, empleo e informalidad laboral.  
**Período integrado:** 2024 T4 (trimestre más reciente con datos completos)  
**Indicador usado:** Tasa de Informalidad Laboral = % de ocupados sin acceso a seguridad social

**URL del ZIP de descarga masiva (2024 T4):**
```
https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/datosabiertos/2024/conjunto_de_datos_enoe_2024_4t_csv.zip
```
Tamaño aproximado: 52 MB (contiene tablas coe1, coe2, sdem, hog, viv en formato CSV).

**Tabla usada:** `sdem` (sociodemográfica) — variables clave:
- `ent` — clave de entidad federativa (01–32)
- `clase2 == 1` — población ocupada
- `seg_soc == 2` — sin acceso a seguridad social (proxy de informalidad)
- `fac_tri` — factor de expansión trimestral (para cifras representativas)
- `ingocup` — ingreso mensual del ocupado principal

**Caché local:** `datos/ocupacion_y_empleo/informalidad_por_estado_2024.csv`  
(CSV con informalidad, ingresos promedio formal/informal y escolaridad por estado)

**Replicabilidad:**
```python
# El notebook descarga y procesa automáticamente si el CSV no existe.
# Para regenerar manualmente:
python scripts/patch_enoe.py   # inyecta celdas (idempotente)
python -m jupyter nbconvert --to notebook --execute analisis_pobreza_mexico.ipynb \
  --ExecutePreprocessor.timeout=600 --output analisis_pobreza_mexico.ipynb
```

```bash
# O descargar el ZIP directamente:
curl -A "Mozilla/5.0" -o enoe_2024_4t.zip \
  "https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/datosabiertos/2024/conjunto_de_datos_enoe_2024_4t_csv.zip"
```

**Habilita:**
- `fig_informalidad_ranking.png` — ranking de informalidad por estado (barras, coloreado por región)
- `fig_informalidad_scatter.png` — scatter informalidad vs pobreza + brecha salarial formal/informal

**Hallazgos clave (2024 T4):**
| Estado | Informalidad | Ingreso informal/mes | Ingreso formal/mes |
|--------|-------------|---------------------|-------------------|
| Chiapas | 85.2% | $5,607 | $12,065 |
| Guerrero | 82.2% | $6,563 | $11,263 |
| Oaxaca | 81.4% | $5,974 | $12,448 |
| **Nuevo León** | **37.6%** | $10,927 | $14,518 |
| **CDMX** | **52.0%** | $10,009 | $18,086 |

Nacional: **60% de informalidad** — 6 de cada 10 trabajadores no tienen seguridad social.
