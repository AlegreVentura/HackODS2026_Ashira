# Declaratoria de uso de inteligencia artificial — ASHIRA
**HackODS UNAM 2026 · ODS 1 — Fin de la Pobreza · ODS 10 — Reducción de las Desigualdades**

---

## 1. Filosofía de uso de IA

Usamos herramientas de IA como **acelerador técnico**, no como sustituto del pensamiento del equipo. Nuestra regla fue simple: la IA puede escribir código repetitivo y corregir errores de sintaxis; la IA no puede decidir qué pregunta hacerle a los datos ni qué significa la respuesta.

**Delegamos a la IA:**
- Corrección de errores de sintaxis y bugs de librería (pandas, openpyxl)
- Generación de código boilerplate para visualizaciones con parámetros que nosotros definimos
- Lectura de estructuras de archivos desconocidos (formatos XLSX con multi-header)

**No delegamos a la IA (ver sección 3):**
- La selección de fuentes de datos y la justificación de su pertinencia
- La pregunta central de investigación y la estructura narrativa de seis actos
- La interpretación de todos los resultados y hallazgos
- Las decisiones de exclusión (qué variables, qué años, qué fuentes descartar)
- La identificación de inconsistencias entre los datos y el código generado

---

## 2. Registro de interacciones

### Interacción 1

| Campo | Detalle |
|---|---|
| Fecha | 2026-04-12 |
| Herramienta | Claude Code (Anthropic) |
| Tarea delegada | Corrección de error de sintaxis en pandas |

**Prompt utilizado:**
> "Tengo este error en pandas: `TypeError: DataFrame.pivot_table() got an unexpected keyword argument 'include_groups'`. ¿Cómo lo corrijo?"

**Resultado obtenido:**
La IA explicó que `include_groups` es un argumento de `groupby.apply()`, no de `pivot_table()`. Generó el fragmento corregido eliminando el argumento incorrecto.

**Modificaciones del equipo:**
Aplicamos la corrección en los notebooks correspondientes y ejecutamos las celdas para verificar que los resultados fueran consistentes con el análisis previo. La lógica del análisis no cambió.

**Decisión del equipo:**
Aceptamos la corrección sin modificaciones adicionales porque el error era de sintaxis pura, sin implicaciones analíticas. La verificación de consistencia de resultados fue responsabilidad exclusiva del equipo.

---

### Interacción 2

| Campo | Detalle |
|---|---|
| Fecha | 2026-04-12 |
| Herramienta | Claude Code (Anthropic) |
| Tarea delegada | Lectura de la estructura del archivo `pm_ef_2024.xlsx` de CONEVAL |

**Prompt utilizado:**
> "El archivo de CONEVAL tiene hojas con nombres abreviados por estado. ¿Cómo leo el nombre completo del estado desde dentro de la hoja en lugar de usar el nombre de la pestaña?"

**Resultado obtenido:**
La IA sugirió leer la celda R4 (fila 4, columna 0) de cada hoja, que contiene el nombre oficial de la entidad. Generó el código de lectura con `openpyxl`.

**Modificaciones del equipo:**
El equipo identificó manualmente los 5 estados cuyos nombres difieren entre fuentes (Ciudad de México, México, Veracruz, Coahuila, Michoacán) y construyó el diccionario de equivalencias. La IA no tuvo participación en esa decisión: requería conocimiento del contexto geográfico-político de México que el equipo aportó.

**Decisión del equipo:**
Aceptamos el código de lectura, rechazamos la normalización automática de nombres porque la IA no podía saber cuáles eran los nombres canónicos correctos para cruzar con las demás fuentes. Esa decisión fue nuestra.

---

### Interacción 3

| Campo | Detalle |
|---|---|
| Fecha | 2026-04-12 |
| Herramienta | Claude Code (Anthropic) |
| Tarea delegada | Generación de código base para visualizaciones con formato oscuro |

**Prompt utilizado:**
> "Genera el código matplotlib para una gráfica de barras horizontales con fondo oscuro, paleta por región Norte/Centro/Sur/CDMX, texto grande y sin superposición de etiquetas."

**Resultado obtenido:**
La IA generó el código base con `rcParams` globales y la estructura de la función de graficación, usando la paleta de colores que el equipo había definido previamente.

**Modificaciones del equipo:**
El equipo revisó y modificó todas las gráficas individualmente: cambió los estados destacados en cada visualización, ajustó los rangos de ejes, y corrigió cinco inconsistencias entre valores hardcodeados y los datos reales. Por ejemplo, la IA incluyó el valor "2074" sin respaldo en los datos; el equipo lo eliminó y lo reemplazó por "8 años sin convergencia Norte–Sur", que sí está soportado por la serie ENIGH 2016–2024.

**Decisión del equipo:**
Aceptamos la estructura de código como punto de partida (boilerplate), pero rechazamos todos los valores de datos hardcodeados. El diseño narrativo de los seis actos —qué muestra cada gráfica, en qué orden y con qué énfasis— fue definido íntegramente por el equipo antes de escribir una sola línea de código.

---

## 3. Decisiones tomadas sin IA

Las siguientes decisiones son trabajo exclusivo del equipo y no fueron delegadas a herramientas de IA en ningún momento:

- **Selección de fuentes:** La decisión de usar ENIGH, PM CONEVAL, Censo 2020 e ICE IMCO —y de excluir datos del Banco Mundial y la ONU— fue del equipo, basada en el nivel de desagregación subnacional que requería la pregunta.
- **Pregunta central de investigación:** "¿En qué medida el estado donde nació una persona en México determina su probabilidad de vivir en pobreza?" fue formulada por el equipo antes de abrir ninguna herramienta de IA.
- **Estructura narrativa en seis actos:** El orden lógico (distribución → tendencia → raíces → mecanismo de supervivencia → consecuencias → balance final) fue diseñado por el equipo como argumento.
- **Interpretación de resultados:** La correlación etnicidad–pobreza (r ≈ 0.8), la dependencia del sur en transferencias gubernamentales, la ausencia de convergencia Norte–Sur en ocho años de datos — todas estas lecturas son del equipo.
- **Reconocimiento de limitaciones:** La advertencia sobre los datos IMCO 2018 (las ediciones 2022–2023 solo existen como PDF) fue identificada por el equipo al revisar la fuente, no sugerida por la IA.
- **Diccionario de equivalencias de nombres de estados:** Construido manualmente por el equipo a partir del conocimiento del contexto geográfico-político mexicano.
- **Verificación de consistencia:** Cada resultado fue verificado por el equipo contra las fuentes originales antes de incluirlo en el análisis.

---

*ASHIRA · HackODS UNAM 2026*
*Herramientas de IA utilizadas: Claude Code (Anthropic)*
