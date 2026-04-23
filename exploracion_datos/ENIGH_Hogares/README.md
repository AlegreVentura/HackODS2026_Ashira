# ASHIRA — HackODS UNAM 2026

**Equipo:** Melisa Asharet Arano Bejarano, Roberto Jhoshua Alegre Ventura, Israel Martínez Jiménez

**Pregunta guía:** ¿México está reduciendo la pobreza de forma equitativa, o hay regiones que se están quedando atrás?

**ODS vinculados:** ODS 1 — Fin de la Pobreza · ODS 10 — Reducción de las Desigualdades

---

## Datos utilizados

**Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH)**
Módulo `concentradohogar` · INEGI · Años: 2016, 2018, 2020, 2022, 2024

```
conjunto_de_datos_enigh2016_nueva_serie_csv/conjunto_de_datos_concentradohogar_enigh_2016_ns/
conjunto_de_datos_enigh_2018_ns_csv/conjunto_de_datos_concentradohogar_enigh_2018_ns/
conjunto_de_datos_enigh_ns_2020_csv/conjunto_de_datos_concentradohogar_enigh_2020_ns/
conjunto_de_datos_enigh_ns_2022_csv/conjunto_de_datos_concentradohogar_enigh2022_ns/
conjunto_de_datos_enigh2024_ns_csv/conjunto_de_datos_concentradohogar_enigh2024_ns/
```

---

## 1. Pertinencia

Los datos de la ENIGH son coherentes con ambos ODS de forma directa:

**ODS 1 — Fin de la Pobreza**
La ENIGH mide el ingreso corriente y el gasto monetario de los hogares mexicanos, que son las variables base para calcular líneas de bienestar y tasas de pobreza. El módulo `concentradohogar` contiene variables como `ing_cor`, `gasto_mon`, `bene_gob` y `transfer`, que permiten construir un proxy de pobreza por hogar, desagregado por año y entidad federativa. Esto habilita el seguimiento temporal (2016–2024) de cuántos hogares están por debajo del umbral de bienestar, que es precisamente el indicador central del ODS 1.

**ODS 10 — Reducción de las Desigualdades**
La misma encuesta permite calcular el coeficiente de Gini ponderado por región, analizar la brecha urbano-rural y comparar la evolución del ingreso per cápita entre estados. La divergencia documentada —66 % de pobreza en Chiapas frente a ~10 % en Baja California, o 15.7 puntos de brecha en cumplimiento ODS entre el Norte y el Sureste— solo puede cuantificarse con una fuente que tenga representatividad estatal y series comparables en el tiempo, exactamente lo que ofrece la ENIGH.

---

## 2. Verificabilidad de la fuente

| Fuente | Institución | Acceso | Periodicidad |
|--------|-------------|--------|--------------|
| ENIGH — concentradohogar | INEGI (Instituto Nacional de Estadística y Geografía) | Público, descarga directa en [inegi.org.mx](https://www.inegi.org.mx/programas/enigh/) | Bienal |
| Pobreza Multidimensional 2024 | CONEVAL / INEGI | Público, [coneval.org.mx](https://www.coneval.org.mx) | Bienal |
| Banco de Indicadores | INEGI | Público, API abierta | Continua |
| SDG Index 2025 | SDSN (Sustainable Development Solutions Network) | Público, [sdgindex.org](https://www.sdgindex.org) | Anual |
| Índice de Estados Sostenibles 2023 | Citibanamex / IMCO | Público | Anual |
| SIODS | Gobierno de México — agenda2030.mx | Público | Variable |
| SIE | Banxico | Público, API abierta | Continua |
| CONAPO | Consejo Nacional de Población | Público, [gob.mx](https://www.gob.mx/conapo) | Anual |

La ENIGH, fuente principal del análisis exploratorio, cumple todos los criterios de verificabilidad:

- **Institución responsable:** INEGI, organismo constitucional autónomo con mandato legal de producir estadística oficial.
- **Metodología publicada:** El INEGI publica los marcos muestrales, factores de expansión (`factor`), diseño muestral y notas técnicas junto con cada edición de la encuesta.
- **Reproducibilidad:** Los microdatos están disponibles en formato CSV de libre descarga, sin registro ni costo.
- **Trazabilidad:** Cada hogar tiene identificadores únicos (`folioviv`, `foliohog`) y un factor de expansión que permite replicar los agregados nacionales y estatales publicados por el propio INEGI.

---

## 3. Justificación de la selección

Se eligió la ENIGH — módulo `concentradohogar` — por tres razones específicas:

**Cobertura temporal comparable.** Disponer de seis cortes bienales (2016–2024) bajo la misma metodología de "nueva serie" permite medir si la reducción de pobreza se aceleró, estancó o revirtió en el periodo, y en qué regiones. Sin series largas no hay tendencia; sin tendencia no hay respuesta a la pregunta guía.

**Desagregación geográfica suficiente.** El módulo incluye `ubica_geo` (clave estado-municipio), lo que permite agrupar los 32 estados en regiones (Norte, Centro, Sur-Sureste) y calcular Gini, mediana de ingreso per cápita y brecha urbano-rural por entidad y año. Otras fuentes agregadas (como el SDG Index nacional) no tienen esta granularidad.

**Variables de ingreso y composición del hogar en un solo archivo.** `concentradohogar` consolida ingreso laboral (`ingtrab`), transferencias (`transfer`), apoyos gubernamentales (`bene_gob`) y remesas (`remesas`) junto con características del hogar (tamaño, zona, escolaridad del jefe). Esto permite no solo medir el nivel de pobreza sino diagnosticar de dónde proviene la mejora o el rezago, que es la dimensión narrativa central del proyecto: *en México no se puede hablar de pobreza sin hablar de dónde naciste*.

---

*ASHIRA · HackODS UNAM 2026 · ODS 1 + ODS 10*
