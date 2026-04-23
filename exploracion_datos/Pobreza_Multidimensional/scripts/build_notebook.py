"""
Script que genera el notebook analisis_pobreza_mexico.ipynb
"""
import json, uuid

def uid():
    return uuid.uuid4().hex[:8]

def md(source):
    return {"cell_type": "markdown", "id": uid(), "metadata": {}, "source": source}

def code(source):
    return {
        "cell_type": "code", "id": uid(), "metadata": {},
        "source": source, "outputs": [], "execution_count": None
    }

cells = []

# PORTADA
cells.append(md(
"""# En México no se puede hablar de pobreza sin hablar de dónde naciste

**Análisis territorial de la pobreza multidimensional en México**

Fuentes: INEGI — Líneas de Pobreza (LP 2026) · Pobreza Multidimensional (PM 2024) · Pobreza Laboral (PL 2025) · Sistema de Información de Derechos Sociales (SIDS 2024)

> La pobreza en México no es homogénea. Tiene dirección, tiene geografía, tiene nombre propio.
> Nacer en Chiapas o nacer en Baja California no es simplemente un accidente geográfico:
> es, en la mayoría de los casos, un condicionante estructural de vida.

Este análisis sostiene esa tesis con datos oficiales del INEGI, cifras cuantificables
y una narrativa que conecta los números con la realidad humana que representan.

**Contenido:**
1. Configuración del entorno
2. Descripción de las fuentes
3. Preparación y limpieza de datos
4. Exploración inicial
5. Análisis territorial de pobreza y desigualdad
6. KPIs clave para el dashboard
7. Los hallazgos más potentes
8. Brechas estructurales: rural-urbano, indigeneidad
9. Hipótesis e interpretación contextual
10. Ideas para visualizaciones del dashboard
11. Conclusión narrativa final
"""))

# SECCIÓN 1 — CONFIGURACIÓN
cells.append(md("## 1. Configuración del entorno"))

cells.append(code(
"""import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from viz_utils import (
    set_global_style, DARK_BG, CARD_BG, ACCENT, ACCENT2, ACCENT3,
    WARM, GREEN, TEXT_MAIN, TEXT_DIM, DIVIDER, SEQ_RED, SEQ_BLUE,
    fig_title, add_source, REGION_COLORS
)

set_global_style()
pd.set_option("display.float_format", "{:,.2f}".format)
print("Entorno configurado correctamente.")
"""))

# SECCIÓN 2 — FUENTES
cells.append(md(
"""## 2. Descripción de las fuentes de datos

Cuatro conjuntos de datos oficiales del INEGI conforman el corpus analítico:

| Fuente | Sigla | Periodicidad | Cobertura | Aporte principal |
|--------|-------|-------------|-----------|-----------------|
| Líneas de Pobreza | LP | Mensual (1992–2026) | Nacional | Valor monetario de las canastas; evolución del poder adquisitivo |
| Pobreza Multidimensional | PM | Bienal (2016–2024) | Nacional y estatal | % pobreza, carencias sociales e ingreso per cápita por entidad |
| Pobreza Laboral | PL | Trimestral (2005–2025) | Nacional y estatal | % población sin ingreso suficiente para cubrir la canasta alimentaria |
| Derechos Sociales | SIDS | Bienal (2016–2024) | Nacional y estatal | Acceso efectivo a alimentación, educación, salud, vivienda y seguridad social |

**Unidad de análisis principal:** entidad federativa (32 estados).
**Variable eje:** porcentaje de población en situación de pobreza multidimensional.
**Dimensión narrativa:** el territorio como condicionante estructural de oportunidades.
"""))

# SECCIÓN 3 — CARGA DE DATOS
cells.append(md("## 3. Preparación y limpieza de datos"))

cells.append(code(
"""# ── Mapa estado → región ────────────────────────────────────────────────────
REGIONES = {
    "Aguascalientes": "Centro", "Baja California": "Norte",
    "Baja California Sur": "Norte", "Campeche": "Sur",
    "Coahuila": "Norte", "Colima": "Centro", "Chiapas": "Sur",
    "Chihuahua": "Norte", "Ciudad de México": "CDMX",
    "Durango": "Norte", "Guanajuato": "Centro", "Guerrero": "Sur",
    "Hidalgo": "Centro", "Jalisco": "Centro",
    "Estado de México": "Centro", "Michoacán": "Centro",
    "Morelos": "Centro", "Nayarit": "Centro",
    "Nuevo León": "Norte", "Oaxaca": "Sur", "Puebla": "Sur",
    "Querétaro": "Centro", "Quintana Roo": "Sur",
    "San Luis Potosí": "Centro", "Sinaloa": "Norte",
    "Sonora": "Norte", "Tabasco": "Sur", "Tamaulipas": "Norte",
    "Tlaxcala": "Sur", "Veracruz": "Sur",
    "Yucatán": "Sur", "Zacatecas": "Centro",
}

STATE_ABBR = {
    "Ags.": "Aguascalientes", "BC": "Baja California",
    "BCS": "Baja California Sur", "Camp.": "Campeche",
    "Coah.": "Coahuila", "Col.": "Colima", "Chis.": "Chiapas",
    "Chih.": "Chihuahua", "CDMX": "Ciudad de México",
    "Dgo.": "Durango", "Gto.": "Guanajuato", "Gro.": "Guerrero",
    "Hgo.": "Hidalgo", "Jal.": "Jalisco", "Mex.": "Estado de México",
    "Mich.": "Michoacán", "Mor.": "Morelos", "Nay.": "Nayarit",
    "NL": "Nuevo León", "Oax.": "Oaxaca", "Pue.": "Puebla",
    "Qro.": "Querétaro", "Q. Roo": "Quintana Roo",
    "SLP": "San Luis Potosí", "Sin.": "Sinaloa", "Son.": "Sonora",
    "Tab.": "Tabasco", "Tamps.": "Tamaulipas", "Tlax.": "Tlaxcala",
    "Ver.": "Veracruz", "Yuc.": "Yucatán", "Zac.": "Zacatecas",
}

print("Mapas de referencia listos.")
"""))

cells.append(code(
"""# ── Carga PM por entidad (pm_ef_2024) ───────────────────────────────────────
records = []
for sheet, nombre in STATE_ABBR.items():
    df_raw = pd.read_excel(
        "datos/pobreza_multidimensional/pm_ef_2024.xlsx", sheet_name=sheet, skiprows=5
    )
    row_data = {"estado": nombre, "region": REGIONES.get(nombre, "Centro")}
    for _, row in df_raw.iterrows():
        v  = str(row.iloc[0]).strip()
        v2 = str(row.iloc[1]).strip()
        if v == "Población en situación de pobreza":
            row_data.update({
                "pct_pobreza_2016": row.iloc[10],
                "pct_pobreza_2018": row.iloc[11],
                "pct_pobreza_2020": row.iloc[12],
                "pct_pobreza_2022": row.iloc[13],
                "pct_pobreza_2024": row.iloc[14],
                "pob_pobreza_2024_miles": row.iloc[8],
            })
        elif "pobreza extrema" in v.lower() or "pobreza extrema" in v2.lower():
            row_data.update({
                "pct_extrema_2016": row.iloc[10],
                "pct_extrema_2024": row.iloc[14],
            })
        elif v == "Población vulnerable por carencias sociales":
            row_data["pct_vulnerable_carencias_2024"] = row.iloc[14]
        elif v == "Población no pobre y no vulnerable":
            row_data["pct_no_pobre_2024"] = row.iloc[14]
        elif "rezago educativo" in v.lower() or "rezago educativo" in v2.lower():
            row_data["pct_rezago_edu_2024"] = row.iloc[14]
        elif "calidad y espacios de la vivienda" in v.lower() or \\
             "calidad y espacios" in v2.lower():
            row_data["pct_vivienda_2024"] = row.iloc[14]
        elif "servicios básicos en la vivienda" in v.lower() or \\
             "servicios básicos" in v2.lower():
            row_data["pct_sin_servicios_2024"] = row.iloc[14]
        elif "acceso a la alimentación nutritiva" in v.lower() or \\
             "acceso a la alimentación" in v2.lower():
            row_data["pct_sin_alim_2024"] = row.iloc[14]
    records.append(row_data)

df_estados = pd.DataFrame(records)
df_estados["cambio_pobreza"] = (
    df_estados["pct_pobreza_2024"] - df_estados["pct_pobreza_2016"]
)
print(f"PM por entidad: {df_estados.shape[0]} estados, {df_estados.shape[1]} variables")
df_estados[["estado", "region", "pct_pobreza_2024",
            "pct_extrema_2024", "cambio_pobreza"]].sort_values(
    "pct_pobreza_2024", ascending=False
).head(10)
"""))

cells.append(code(
"""# ── Ingreso per cápita por estado (pm_ic_2024 Cuadro 4) ─────────────────────
df_ic = pd.read_excel("datos/pobreza_multidimensional/pm_ic_2024.xlsx", sheet_name="Cuadro 4", skiprows=5)
df_ic = df_ic.iloc[:33].dropna(subset=["Entidad federativa"]).copy()
df_ic = df_ic[["Entidad federativa", 2016, 2024]].copy()
df_ic.columns = ["estado", "ingreso_2016", "ingreso_2024"]
df_ic["estado"] = (
    df_ic["estado"].str.strip()
    .replace({
        "México": "Estado de México",
        "Michoacán de Ocampo": "Michoacán",
        "Veracruz de Ignacio de la Llave": "Veracruz",
        "Coahuila de Zaragoza": "Coahuila",
    })
)
df_ic = df_ic[df_ic["estado"] != "Estados Unidos Mexicanos"].reset_index(drop=True)

df = df_estados.merge(df_ic[["estado", "ingreso_2024"]], on="estado", how="left")
df = df.sort_values("pct_pobreza_2024", ascending=False).reset_index(drop=True)
print(f"Dataset principal: {df.shape}")
df[["estado", "region", "pct_pobreza_2024",
    "pct_extrema_2024", "ingreso_2024"]].head(8)
"""))

cells.append(code(
"""# ── Pobreza Laboral Q4 2025 por estado ──────────────────────────────────────
df_pl_raw = pd.read_excel(
    "datos/pobreza_laboral/pl_2005t_2025t.xlsx", sheet_name="Cuadro 9", skiprows=5
)
last_row = df_pl_raw.dropna(subset=["Estados Unidos Mexicanos"]).tail(1).squeeze()

pl_dict = {}
for col in df_pl_raw.columns[2:]:
    nombre = (
        str(col).strip()
        .replace("Michoacán de Ocampo", "Michoacán")
        .replace("Veracruz de Ignacio de la Llave", "Veracruz")
        .replace("Coahuila de Zaragoza", "Coahuila")
        .replace("México", "Estado de México")
    )
    pl_dict[nombre] = last_row[col]

df["pct_pobreza_laboral_q4_2025"] = df["estado"].map(pl_dict)

df_lp = pd.read_excel("datos/lineas_pobreza/lp_2026.xlsx", sheet_name="Cuadro 1", skiprows=5)
df_lp.columns = ["anio", "mes", "lp_ext_rural", "lp_ext_urbano",
                 "_", "lp_rural", "lp_urbano"]
df_lp = df_lp[df_lp["mes"].notna()].copy()
df_lp["anio"] = df_lp["anio"].ffill()
df_lp = df_lp[df_lp["lp_rural"].notna()].reset_index(drop=True)
lp_anual = df_lp.groupby("anio")[
    ["lp_rural", "lp_urbano", "lp_ext_rural", "lp_ext_urbano"]
].mean().astype(float)

YEARS       = [2016, 2018, 2020, 2022, 2024]
rural_pct   = [60.49, 57.71, 56.78, 48.85, 45.78]
urbana_pct  = [38.06, 36.81, 40.05, 32.21, 25.02]
rural_ext   = [27.00, 25.02, 24.93, 19.54, 18.77]
urbana_ext  = [11.23, 10.44, 14.94,  9.61,  6.69]
nac_pct     = [43.23, 41.91, 43.91, 36.31, 29.56]

df_indig = pd.read_excel(
    "datos/derechos_sociales/bmi_2024.xlsx", sheet_name="Cuadro 1", skiprows=6
).iloc[:5].dropna(subset=["Año"]).copy()
df_indig.columns = ["anio", "indigena", "no_indigena", "brecha", "_"]
df_indig = df_indig[["anio", "indigena", "no_indigena", "brecha"]].astype(float)

print("Todos los datasets cargados correctamente.")
print(f"  df (estados + PM + PL): {df.shape}")
print(f"  lp_anual: {lp_anual.shape}  |  df_indig: {df_indig.shape}")
df[["estado", "region", "pct_pobreza_2024",
    "ingreso_2024", "pct_pobreza_laboral_q4_2025"]].head(5)
"""))

# SECCIÓN 4 — EXPLORACIÓN
cells.append(md(
"""## 4. Exploración inicial

Antes de construir la narrativa, revisamos la distribución general, las correlaciones
y las primeras señales territoriales que emergen de los datos.
"""))

cells.append(code(
"""# Estadísticas descriptivas clave
summary_cols = [
    "pct_pobreza_2024", "pct_extrema_2024", "ingreso_2024",
    "pct_rezago_edu_2024", "pct_vivienda_2024", "pct_sin_servicios_2024",
]
summary = df[summary_cols].describe().round(2)
summary.loc["rango"] = (summary.loc["max"] - summary.loc["min"]).round(2)
summary
"""))

cells.append(code(
"""# ── Distribución de pobreza por región ──────────────────────────────────────
region_order  = ["Norte", "Centro", "Sur", "CDMX"]
colors_region = [REGION_COLORS[r] for r in region_order]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "Distribución de la pobreza según región geográfica",
    subtitle="Pobreza multidimensional 2024 — porcentaje de población",
    y_title=1.01, y_sub=0.95,
)

for ax in axes:
    ax.set_facecolor(CARD_BG)
    ax.spines["left"].set_color(DIVIDER)
    ax.spines["bottom"].set_color(DIVIDER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Boxplot
data_r = [df[df["region"] == r]["pct_pobreza_2024"].values for r in region_order]
bp = axes[0].boxplot(
    data_r, patch_artist=True, widths=0.5,
    medianprops=dict(color=TEXT_MAIN, linewidth=2.5),
    whiskerprops=dict(color=TEXT_DIM), capprops=dict(color=TEXT_DIM),
    flierprops=dict(marker="o", color=ACCENT, markersize=8, alpha=0.7),
)
for patch, color in zip(bp["boxes"], colors_region):
    patch.set_facecolor(color); patch.set_alpha(0.75)
axes[0].set_xticks(range(1, 5))
axes[0].set_xticklabels(region_order, fontsize=13)
axes[0].set_ylabel("% en pobreza (2024)", fontsize=13)
axes[0].set_title("Rango por región", fontsize=15, pad=10)
axes[0].yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
axes[0].grid(axis="y", alpha=0.4)
for i, (region, vals) in enumerate(zip(region_order, data_r)):
    axes[0].text(
        i + 1, vals.max() + 1.5, f"Media: {vals.mean():.1f}%",
        ha="center", fontsize=11, color=colors_region[i], fontweight="bold",
    )

# Barras de promedio
means = [df[df["region"] == r]["pct_pobreza_2024"].mean() for r in region_order]
bars = axes[1].bar(
    region_order, means, color=colors_region,
    width=0.55, edgecolor=DARK_BG, linewidth=1.5,
)
axes[1].set_ylabel("% promedio de pobreza (2024)", fontsize=13)
axes[1].set_title("Promedio por región", fontsize=15, pad=10)
axes[1].yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
axes[1].set_ylim(0, 60)
axes[1].grid(axis="y", alpha=0.4)
for bar in bars:
    h = bar.get_height()
    axes[1].text(
        bar.get_x() + bar.get_width() / 2, h + 0.8,
        f"{h:.1f}%", ha="center", fontsize=15,
        color=TEXT_MAIN, fontweight="bold",
    )

add_source(fig)
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig("imagenes/fig_distribucion_region.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(code(
"""# ── Correlación: ingreso per cápita vs % pobreza ─────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

for _, row in df.iterrows():
    c = REGION_COLORS.get(row["region"], ACCENT2)
    ax.scatter(
        row["ingreso_2024"], row["pct_pobreza_2024"],
        color=c, s=130, alpha=0.9, zorder=4,
        edgecolors=DARK_BG, linewidths=0.8,
    )
    if (row["pct_pobreza_2024"] > 40
            or row["pct_pobreza_2024"] < 13
            or row["ingreso_2024"] > 10_500):
        ax.annotate(
            row["estado"],
            xy=(row["ingreso_2024"], row["pct_pobreza_2024"]),
            xytext=(8, 4), textcoords="offset points",
            fontsize=9.5, color=TEXT_DIM,
        )

mask = df[["ingreso_2024", "pct_pobreza_2024"]].dropna()
z = np.polyfit(mask["ingreso_2024"], mask["pct_pobreza_2024"], 1)
x_line = np.linspace(mask["ingreso_2024"].min(), mask["ingreso_2024"].max(), 200)
ax.plot(x_line, np.poly1d(z)(x_line),
        color=ACCENT, linewidth=2, linestyle="--", alpha=0.6)

corr = mask["ingreso_2024"].corr(mask["pct_pobreza_2024"])
ax.text(0.98, 0.96, f"r = {corr:.2f}", transform=ax.transAxes,
        ha="right", va="top", fontsize=15, color=ACCENT, fontweight="bold")

handles = [mpatches.Patch(color=REGION_COLORS[r], label=r) for r in REGION_COLORS]
ax.legend(handles=handles, fontsize=12, framealpha=0.3)
ax.set_xlabel("Ingreso corriente per cápita mensual (pesos de 2024)", fontsize=13)
ax.set_ylabel("Población en situación de pobreza (%)", fontsize=13)
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_title(
    "A mayor ingreso, menor pobreza — pero la brecha territorial no desaparece",
    fontsize=16, pad=14,
)
ax.grid(alpha=0.3)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_correlacion.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

# SECCIÓN 5 — ANÁLISIS TERRITORIAL
cells.append(md(
"""## 5. Análisis territorial de pobreza y desigualdad

> El mapa de la pobreza en México es también un mapa histórico, climático y político.
> El sur concentra la pobreza. El norte, la excepción. Y entre ambos,
> una brecha que no se ha cerrado en décadas.
"""))

cells.append(code(
"""# ── Ranking de estados: pobreza multidimensional 2024 ────────────────────────
fig, ax = plt.subplots(figsize=(14, 13))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

df_sorted = df.sort_values("pct_pobreza_2024")
colors_bar = [REGION_COLORS.get(r, ACCENT2) for r in df_sorted["region"]]

bars = ax.barh(
    df_sorted["estado"], df_sorted["pct_pobreza_2024"],
    color=colors_bar, height=0.7, edgecolor=DARK_BG, linewidth=0.5,
)

nacional = 29.56
ax.axvline(nacional, color=TEXT_DIM, linewidth=1.5, linestyle="--", alpha=0.7)
ax.text(nacional + 0.4, len(df_sorted) / 2,
        f"Nacional\\n{nacional:.1f}%",
        color=TEXT_DIM, fontsize=11, va="center")

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height() / 2,
            f"{w:.1f}%", va="center", ha="left",
            fontsize=11, color=TEXT_MAIN, fontweight="bold")

ax.set_xlim(0, 80)
ax.set_xlabel("Población en situación de pobreza (%)", fontsize=13)
ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.tick_params(axis="y", labelsize=12)
ax.grid(axis="x", alpha=0.3)
ax.set_title("Pobreza multidimensional por entidad federativa, 2024",
             fontsize=17, pad=14)

handles = [mpatches.Patch(color=REGION_COLORS[r], label=r) for r in REGION_COLORS]
ax.legend(handles=handles, loc="lower right", fontsize=12, framealpha=0.3)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_ranking_estados.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(code(
"""# ── Cambio en pobreza 2016 → 2024 ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 13))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

df_cambio = df.sort_values("cambio_pobreza")
colors_cambio = [ACCENT if x > 0 else GREEN for x in df_cambio["cambio_pobreza"]]
bars_c = ax.barh(
    df_cambio["estado"], df_cambio["cambio_pobreza"],
    color=colors_cambio, height=0.7, edgecolor=DARK_BG, linewidth=0.5,
)

for bar in bars_c:
    w = bar.get_width()
    x_pos = w - 0.8 if w < 0 else w + 0.3
    ha_val = "right" if w < 0 else "left"
    ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
            f"{w:+.1f} pp", va="center", ha=ha_val,
            fontsize=11, color=TEXT_MAIN, fontweight="bold")

ax.axvline(0, color=TEXT_DIM, linewidth=1.5, alpha=0.5)
ax.set_xlabel("Cambio en puntos porcentuales (2016–2024)", fontsize=13)
ax.tick_params(axis="y", labelsize=12)
ax.grid(axis="x", alpha=0.3)

handles = [
    mpatches.Patch(color=GREEN, label="Reducción de pobreza"),
    mpatches.Patch(color=ACCENT, label="Aumento de pobreza"),
]
ax.legend(handles=handles, loc="lower right", fontsize=12, framealpha=0.3)
ax.set_title(
    "Cambio en pobreza multidimensional por entidad, 2016–2024\\n(en puntos porcentuales)",
    fontsize=16, pad=14,
)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_cambio_pobreza.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(code(
"""# ── Norte vs Sur: comparación directa ───────────────────────────────────────
norte = df[df["region"] == "Norte"]
sur   = df[df["region"] == "Sur"]

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "La fractura Norte–Sur en números",
    subtitle="Promedio de indicadores clave — Norte vs Sur (2024)",
    y_title=1.01, y_sub=0.95,
)

comparisons = [
    ("% Pobreza multidimensional", "pct_pobreza_2024", "{:.1f}%"),
    ("% Pobreza extrema",          "pct_extrema_2024", "{:.1f}%"),
    ("Ingreso per cápita (pesos)", "ingreso_2024",     "${:,.0f}"),
]

for ax, (title, col, fmt) in zip(axes, comparisons):
    ax.set_facecolor(CARD_BG)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DIVIDER); ax.spines["bottom"].set_color(DIVIDER)
    vals  = [norte[col].mean(), sur[col].mean()]
    clrs  = [REGION_COLORS["Norte"], REGION_COLORS["Sur"]]
    b     = ax.bar(["Norte", "Sur"], vals, color=clrs,
                   width=0.5, edgecolor=DARK_BG, linewidth=1.5)
    for bar, v in zip(b, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(vals) * 0.02,
            fmt.format(v), ha="center", va="bottom",
            fontsize=15, fontweight="bold", color=TEXT_MAIN,
        )
    ax.set_title(title, fontsize=14, pad=10)
    ax.grid(axis="y", alpha=0.3)
    if "ingreso" in col:
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
        )
    else:
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    brecha = abs(vals[1] - vals[0])
    ax.text(0.5, 0.92, f"Brecha: {fmt.format(brecha)}",
            transform=ax.transAxes, ha="center",
            fontsize=13, color=WARM, style="italic")

add_source(fig)
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig("imagenes/fig_norte_sur.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

# SECCIÓN 6 — KPIs
cells.append(md(
"""## 6. KPIs clave para el dashboard

Los siguientes indicadores son los **números ancla** del story: cifras únicas,
comparables y con alto poder narrativo. Cada uno responde a la pregunta central.
"""))

cells.append(code(
"""# ── Panel de KPIs visuales ────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 10))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "KPIs: La brecha territorial de la pobreza en México",
    subtitle="Fuentes: INEGI PM 2024 · PL Q4 2025 · SIDS 2024",
    y_title=0.99, y_sub=0.94,
)

kpis = [
    ("Chiapas",       "el estado más pobre",     "65.97%",   "de su población en pobreza",   ACCENT),
    ("Baja California","el menos pobre",           "9.87%",    "de su población en pobreza",   GREEN),
    ("Brecha",        "Norte–Sur en pobreza",     "6.7×",     "Chiapas vs Baja California",   WARM),
    ("Rural vs Urbano","diferencia 2024",          "+20.8 pp", "más pobreza en el campo",      ACCENT2),
    ("Indígena vs No","inseg. alimentaria 2024",  "+16.3 pp", "brecha étnica persistente",    ACCENT3),
    ("Chiapas",       "pobreza laboral Q4 2025",  "59.8%",    "sin ingreso para la canasta",  ACCENT),
    ("NL vs Chiapas", "ingreso per cápita",       "3.2×",     "diferencia mensual en 2024",   WARM),
    ("Nacional",      "reducción 2016–2024",      "−13.7 pp", "de 43.2% a 29.6%",             GREEN),
]

gs = gridspec.GridSpec(
    2, 4, figure=fig, hspace=0.55, wspace=0.28,
    left=0.03, right=0.97, top=0.88, bottom=0.04,
)

for idx, (title, subtitle, value, desc, color) in enumerate(kpis):
    row_g, col_g = divmod(idx, 4)
    ax = fig.add_subplot(gs[row_g, col_g])
    ax.set_facecolor(CARD_BG)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rect = mpatches.FancyBboxPatch(
        (0.02, 0.02), 0.96, 0.96,
        boxstyle="round,pad=0.03",
        facecolor=CARD_BG, edgecolor=color, linewidth=2.5,
        transform=ax.transAxes, zorder=0,
    )
    ax.add_patch(rect)
    ax.text(0.5, 0.80, value,       ha="center", va="top", fontsize=30,
            fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.54, desc,        ha="center", va="top", fontsize=11,
            color=TEXT_DIM, transform=ax.transAxes)
    ax.text(0.5, 0.30, title,       ha="center", va="top", fontsize=14,
            fontweight="bold", color=TEXT_MAIN, transform=ax.transAxes)
    ax.text(0.5, 0.12, subtitle,    ha="center", va="top", fontsize=10,
            color=TEXT_DIM, style="italic", transform=ax.transAxes)

plt.savefig("imagenes/fig_kpis.png", dpi=130, bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

# SECCIÓN 7 — HALLAZGOS
cells.append(md(
"""## 7. Los hallazgos más potentes

### Hallazgo 1 — La lotería del lugar de nacimiento

> En México, el estado en que naciste puede predecir, con asombrosa precisión,
> si tendrás acceso a educación de calidad, agua potable, atención médica y un
> ingreso digno. No es hipérbole: es estadística.

Chiapas, Guerrero y Oaxaca concentran sistemáticamente los peores indicadores en
**todas** las dimensiones de la pobreza multidimensional. No se trata de una sola
carencia sino de una acumulación estructural que se reproduce generación tras generación.
"""))

cells.append(code(
"""# ── Heatmap: carencias sociales por estado ───────────────────────────────────
carencias_cols = [
    "pct_rezago_edu_2024", "pct_vivienda_2024",
    "pct_sin_servicios_2024", "pct_sin_alim_2024",
]
carencias_labels = [
    "Rezago educativo", "Vivienda precaria",
    "Sin serv. básicos", "Inseg. alimentaria",
]

df_heat = (
    df[["estado"] + carencias_cols]
    .copy()
    .set_index("estado")
)
df_heat.columns = carencias_labels
df_heat = df_heat.sort_values("Rezago educativo", ascending=False)

fig, ax = plt.subplots(figsize=(13, 14))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)

cmap_red = LinearSegmentedColormap.from_list(
    "red_heat", ["#1C1F2A", "#FF6B6B", "#9B1B24"]
)
im = ax.imshow(df_heat.values, aspect="auto", cmap=cmap_red,
               vmin=0, vmax=df_heat.values.max())

ax.set_xticks(range(len(carencias_labels)))
ax.set_xticklabels(carencias_labels, fontsize=13, rotation=20, ha="right")
ax.set_yticks(range(len(df_heat)))
ax.set_yticklabels(df_heat.index, fontsize=11)
ax.tick_params(colors=TEXT_MAIN)

for i in range(df_heat.shape[0]):
    for j in range(df_heat.shape[1]):
        v = df_heat.values[i, j]
        tc = TEXT_MAIN if v > 18 else TEXT_DIM
        ax.text(j, i, f"{v:.1f}%", ha="center", va="center",
                fontsize=10, color=tc, fontweight="bold")

cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02)
cb.set_label("% con carencia", fontsize=13, color=TEXT_MAIN)
cb.ax.yaxis.set_tick_params(color=TEXT_DIM, labelsize=11)
plt.setp(plt.getp(cb.ax.axes, "yticklabels"), color=TEXT_DIM)

ax.set_title(
    "Carencias sociales acumuladas por entidad federativa (2024)\\n"
    "Cada celda = % de la población con esa carencia",
    fontsize=15, pad=16,
)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_heatmap_carencias.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(md(
"""### Hallazgo 2 — El tiempo no cierra la brecha, la hereda

La pobreza nacional bajó 13.7 puntos porcentuales entre 2016 y 2024.
Pero la **brecha relativa entre los estados más pobres y los menos pobres persiste**:
las entidades del sur siguen siendo las más vulnerables, y la reducción fue proporcionalmente
mayor en los estados que ya partían de niveles más bajos.
"""))

cells.append(code(
"""# ── Evolución 2016–2024: extremos y promedio nacional ─────────────────────────
top_pobres = df.head(5)["estado"].tolist()
top_ricos  = df.tail(5)["estado"].tolist()

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

# Nacional
ax.plot(YEARS, nac_pct, color=TEXT_DIM, lw=3, linestyle="--",
        marker="o", ms=7, label="Nacional", zorder=5)

# 5 más pobres
for estado in top_pobres:
    r = df[df["estado"] == estado].iloc[0]
    vals = [r[f"pct_pobreza_{y}"] for y in [2016, 2018, 2020, 2022, 2024]]
    ax.plot(YEARS, vals, color=ACCENT, lw=1.8, alpha=0.65,
            marker="s", ms=5)
    ax.text(2024.15, vals[-1], estado.split()[0],
            fontsize=10, color=ACCENT, va="center")

# 5 menos pobres
for estado in top_ricos:
    r = df[df["estado"] == estado].iloc[0]
    vals = [r[f"pct_pobreza_{y}"] for y in [2016, 2018, 2020, 2022, 2024]]
    ax.plot(YEARS, vals, color=GREEN, lw=1.8, alpha=0.65,
            marker="s", ms=5)
    ax.text(2024.15, vals[-1], estado.split()[0],
            fontsize=10, color=GREEN, va="center")

# Área de brecha
p_vals = [df[df["estado"].isin(top_pobres)][f"pct_pobreza_{y}"].mean()
          for y in [2016, 2018, 2020, 2022, 2024]]
r_vals = [df[df["estado"].isin(top_ricos)][f"pct_pobreza_{y}"].mean()
          for y in [2016, 2018, 2020, 2022, 2024]]
ax.fill_between(YEARS, p_vals, r_vals, alpha=0.07, color=WARM)

handles = [
    plt.Line2D([0], [0], color=ACCENT, lw=2, label="5 estados más pobres"),
    plt.Line2D([0], [0], color=GREEN,  lw=2, label="5 estados menos pobres"),
    plt.Line2D([0], [0], color=TEXT_DIM, lw=2, linestyle="--", label="Nacional"),
]
ax.legend(handles=handles, fontsize=12, framealpha=0.3)
ax.set_xticks(YEARS)
ax.xaxis.set_tick_params(labelsize=13)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_ylabel("% en situación de pobreza", fontsize=13)
ax.set_title("Evolución de la pobreza 2016–2024: la brecha geográfica persiste",
             fontsize=16, pad=14)
ax.grid(alpha=0.3)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_evolucion_brecha.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(md(
"""### Hallazgo 3 — Rural vs Urbano: la segunda fractura

> Nacer en zona rural en México no es solo vivir lejos de la ciudad.
> Es tener casi el doble de probabilidad de estar en situación de pobreza.

En 2024: **45.8% rural** en pobreza vs **25.0% urbano**. En pobreza extrema:
18.8% rural frente a 6.7% urbano — una brecha de 12 puntos porcentuales
que ha persistido durante los ocho años del período de medición.
"""))

cells.append(code(
"""# ── Rural vs Urbano: evolución histórica ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "Brecha rural–urbana en pobreza multidimensional",
    subtitle="2016–2024 · % de población en situación de pobreza",
    y_title=1.01, y_sub=0.95,
)

for ax in axes:
    ax.set_facecolor(CARD_BG)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DIVIDER); ax.spines["bottom"].set_color(DIVIDER)

# Pobreza total
ax = axes[0]
ax.plot(YEARS, rural_pct,  color=ACCENT,  marker="o", ms=8, lw=2.5, label="Rural")
ax.plot(YEARS, urbana_pct, color=ACCENT2, marker="o", ms=8, lw=2.5, label="Urbano")
ax.plot(YEARS, nac_pct,    color=TEXT_DIM, marker="s", ms=6, lw=1.5,
        linestyle="--", label="Nacional")
ax.fill_between(YEARS, rural_pct, urbana_pct, alpha=0.10, color=WARM)
ax.text(2024.1, rural_pct[-1] + 0.5,  f"{rural_pct[-1]:.1f}%",
        fontsize=12, color=ACCENT, fontweight="bold")
ax.text(2024.1, urbana_pct[-1] - 2.5, f"{urbana_pct[-1]:.1f}%",
        fontsize=12, color=ACCENT2, fontweight="bold")
ax.legend(fontsize=12, framealpha=0.3)
ax.set_title("Pobreza total", fontsize=14, pad=10)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_xticks(YEARS); ax.grid(alpha=0.3)

# Pobreza extrema
ax = axes[1]
ax.plot(YEARS, rural_ext,  color=ACCENT,  marker="o", ms=8, lw=2.5, label="Rural extrema")
ax.plot(YEARS, urbana_ext, color=ACCENT2, marker="o", ms=8, lw=2.5, label="Urbana extrema")
ax.fill_between(YEARS, rural_ext, urbana_ext, alpha=0.10, color=ACCENT)
ax.text(2024.1, rural_ext[-1] + 0.5,  f"{rural_ext[-1]:.1f}%",
        fontsize=12, color=ACCENT, fontweight="bold")
ax.text(2024.1, urbana_ext[-1] - 1.8, f"{urbana_ext[-1]:.1f}%",
        fontsize=12, color=ACCENT2, fontweight="bold")
ax.legend(fontsize=12, framealpha=0.3)
ax.set_title("Pobreza extrema", fontsize=14, pad=10)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_xticks(YEARS); ax.grid(alpha=0.3)

add_source(fig)
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig("imagenes/fig_rural_urbano.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(md(
"""### Hallazgo 4 — Trabajar no garantiza salir de la pobreza

La pobreza laboral mide algo profundamente injusto: personas que **trabajan**
pero cuyo ingreso no alcanza para cubrir la canasta alimentaria básica.
En Chiapas, casi **6 de cada 10 trabajadores** están en esa situación.
"""))

cells.append(code(
"""# ── Pobreza laboral Q4 2025 vs PM 2024 ──────────────────────────────────────
df_pl = df[["estado", "region",
            "pct_pobreza_2024", "pct_pobreza_laboral_q4_2025"]].dropna()
df_pl = df_pl.sort_values("pct_pobreza_laboral_q4_2025", ascending=False)

fig, ax = plt.subplots(figsize=(14, 11))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

x = np.arange(len(df_pl))
w = 0.38
ax.bar(x - w / 2, df_pl["pct_pobreza_laboral_q4_2025"],
       width=w, color=ACCENT, label="Pobreza laboral (Q4 2025)", alpha=0.85)
ax.bar(x + w / 2, df_pl["pct_pobreza_2024"],
       width=w, color=ACCENT2, label="Pobreza multidimensional (2024)", alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(df_pl["estado"], rotation=55, ha="right", fontsize=10)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_ylabel("% de población", fontsize=13)
ax.set_title(
    "Pobreza laboral vs pobreza multidimensional por entidad",
    fontsize=16, pad=14,
)
ax.legend(fontsize=12, framealpha=0.3)
ax.grid(axis="y", alpha=0.3)
ax.axhline(29.56, color=TEXT_DIM, lw=1.2, linestyle=":", alpha=0.6)
ax.text(len(df_pl) - 0.5, 30.8, "Nac. PM 29.6%",
        fontsize=10, color=TEXT_DIM, ha="right")
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_pobreza_laboral.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

# SECCIÓN 8 — BRECHAS ESTRUCTURALES
cells.append(md(
"""## 8. Brechas estructurales: indigeneidad y territorio

> La pobreza en México no afecta a todos de la misma manera.
> Si eres indígena, mujer jefa de hogar y vives en zona rural del sur,
> las desventajas no se suman: se multiplican.
"""))

cells.append(code(
"""# ── Brecha étnica en inseguridad alimentaria ─────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "La brecha étnica en el acceso a la alimentación",
    subtitle="Hogares con jefa de hogar — % con inseguridad alimentaria · 2016–2024",
    y_title=1.01, y_sub=0.95,
)

for ax in axes:
    ax.set_facecolor(CARD_BG)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DIVIDER); ax.spines["bottom"].set_color(DIVIDER)

# Líneas temporales
ax = axes[0]
ax.plot(df_indig["anio"], df_indig["indigena"],
        color=ACCENT, marker="o", ms=8, lw=2.5, label="Indígena")
ax.plot(df_indig["anio"], df_indig["no_indigena"],
        color=ACCENT2, marker="o", ms=8, lw=2.5, label="No indígena")
ax.fill_between(df_indig["anio"], df_indig["indigena"],
                df_indig["no_indigena"], alpha=0.12, color=WARM)
last = df_indig.iloc[-1]
ax.text(2024.1, last["indigena"] + 0.3,    f"{last['indigena']:.1f}%",
        color=ACCENT,  fontsize=12, fontweight="bold")
ax.text(2024.1, last["no_indigena"] - 2.0, f"{last['no_indigena']:.1f}%",
        color=ACCENT2, fontsize=12, fontweight="bold")
ax.set_xticks([2016, 2018, 2020, 2022, 2024])
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_title("Evolución 2016–2024", fontsize=14, pad=10)
ax.legend(fontsize=12, framealpha=0.3)
ax.grid(alpha=0.3)

# Barras 2024
ax = axes[1]
cats  = ["Indigena\\n(2024)", "No indigena\\n(2024)", "Brecha\\n2016", "Brecha\\n2024"]
vals  = [30.04, 13.72, 17.46, 16.33]
clrs  = [ACCENT, ACCENT2, WARM, WARM]
bars_e = ax.bar(cats, vals, color=clrs, width=0.5,
                edgecolor=DARK_BG, linewidth=1.5)
for bar, v in zip(bars_e, vals):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{v:.1f}%", ha="center", fontsize=14,
        fontweight="bold", color=TEXT_MAIN,
    )
ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax.set_title("% con inseguridad alimentaria y brecha étnica", fontsize=14, pad=10)
ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, 40)

add_source(fig, source="INEGI – SIDS 2024")
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig("imagenes/fig_brecha_etnica.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(code(
"""# ── Ingreso per cápita: Top 8 vs Bottom 8 ────────────────────────────────────
df_ing = df.sort_values("ingreso_2024")
combined = pd.concat([df_ing.head(8), df_ing.tail(8)])

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(CARD_BG)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_color(DIVIDER)

c_ing = [REGION_COLORS.get(r, ACCENT2) for r in combined["region"]]
bars_i = ax.barh(combined["estado"], combined["ingreso_2024"],
                 color=c_ing, height=0.7, edgecolor=DARK_BG, linewidth=0.5)

for bar in bars_i:
    w = bar.get_width()
    ax.text(w + 80, bar.get_y() + bar.get_height() / 2,
            f"${w:,.0f}", va="center", ha="left",
            fontsize=11, color=TEXT_MAIN, fontweight="bold")

nacional_ing = 7468.65
ax.axvline(nacional_ing, color=TEXT_DIM, lw=1.5, linestyle="--", alpha=0.6)
ax.text(nacional_ing + 120, len(combined) / 2,
        f"Nacional\\n${nacional_ing:,.0f}", fontsize=10, color=TEXT_DIM, va="center")

ax.axhline(7.5, color=DIVIDER, lw=2, alpha=0.7)
ax.text(ax.get_xlim()[1] * 0.96, 8.2, "mayor ingreso",
        ha="right", fontsize=11, color=GREEN, fontweight="bold")
ax.text(ax.get_xlim()[1] * 0.96, 7.0, "menor ingreso",
        ha="right", fontsize=11, color=ACCENT, fontweight="bold")

ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
)
ax.set_xlabel("Ingreso corriente per cápita mensual (pesos de 2024)", fontsize=13)
ax.tick_params(axis="y", labelsize=12)
ax.set_title("8 entidades con mayor y menor ingreso per cápita (2024)",
             fontsize=16, pad=14)

handles = [mpatches.Patch(color=REGION_COLORS[r], label=r) for r in REGION_COLORS]
ax.legend(handles=handles, loc="lower right", fontsize=11, framealpha=0.3)
ax.grid(axis="x", alpha=0.3)
add_source(fig)
plt.tight_layout()
plt.savefig("imagenes/fig_ingreso_estados.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

cells.append(code(
"""# ── Líneas de Pobreza: evolución histórica 1992–2026 ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor(DARK_BG)
fig_title(
    fig,
    "El precio de la pobreza — Líneas de Pobreza 1992–2026",
    subtitle="Valor monetario mensual por persona (pesos corrientes)",
    y_title=1.01, y_sub=0.95,
)

for ax in axes:
    ax.set_facecolor(CARD_BG)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(DIVIDER); ax.spines["bottom"].set_color(DIVIDER)

pairs = [
    (axes[0], "lp_rural",     "lp_urbano",
     "LP por Ingresos\\n(canasta alimentaria + no alimentaria)"),
    (axes[1], "lp_ext_rural", "lp_ext_urbano",
     "LP Extrema por Ingresos\\n(solo canasta alimentaria)"),
]

for ax, col_r, col_u, title in pairs:
    ax.plot(lp_anual.index, lp_anual[col_r],  color=ACCENT,  lw=2.5, label="Rural")
    ax.plot(lp_anual.index, lp_anual[col_u],  color=ACCENT2, lw=2.5, label="Urbano")
    ax.fill_between(lp_anual.index, lp_anual[col_r], lp_anual[col_u],
                    alpha=0.10, color=WARM)
    last_r = lp_anual[col_r].iloc[-1]
    last_u = lp_anual[col_u].iloc[-1]
    ax.text(lp_anual.index[-1], last_r * 1.04, f"${last_r:,.0f}",
            fontsize=11, color=ACCENT, fontweight="bold", ha="right")
    ax.text(lp_anual.index[-1], last_u * 1.04, f"${last_u:,.0f}",
            fontsize=11, color=ACCENT2, fontweight="bold", ha="right")
    ax.set_title(title, fontsize=13, pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(fontsize=12, framealpha=0.3)
    ax.grid(alpha=0.3)

add_source(fig, source="INEGI – Líneas de Pobreza (LP), febrero 2026")
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig("imagenes/fig_lineas_pobreza.png", dpi=130,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
"""))

# SECCIÓN 9 — HIPÓTESIS
cells.append(md(
"""## 9. Hipótesis e interpretación contextual

Con base en el análisis, formulamos cuatro hipótesis explicativas que conectan
los patrones territoriales con causas estructurales documentadas:

**H1 — La concentración geográfica de la pobreza es herencia histórica**

Las regiones con mayor pobreza (Chiapas, Guerrero, Oaxaca, Veracruz, Puebla)
coinciden con las zonas de mayor concentración histórica de población indígena
y mayor grado de exclusión institucional desde la Colonia. Las carencias actuales
no son accidentales: son el resultado acumulado de siglos de marginación.

**H2 — El modelo exportador del norte generó asimetría estructural norte-sur**

Las entidades del norte se beneficiaron del modelo industrial maquilador y la
integración con la economía norteamericana (TLCAN/T-MEC): empleo formal, mayores
salarios, menor pobreza. Ese modelo no se replicó en el sur, que permaneció
anclado a economías primarias y de subsistencia.

**H3 — La trampa de ruralidad agrava todas las carencias simultáneamente**

En zonas rurales del sur, la distancia a servicios públicos, la baja conectividad
y la dependencia de actividades agropecuarias de baja productividad crean un ciclo
difícil de romper: sin educación → sin calificación → sin ingreso → sin salud →
sin movilidad social. Las carencias se refuerzan mutuamente.

**H4 — La brecha étnica en alimentación es proxy de exclusión profunda**

Que los hogares con jefa indígena tengan 2.2 veces más inseguridad alimentaria
no refleja solo diferencias de ingreso. Refleja también barreras de acceso a
programas sociales, discriminación en mercados laborales y ausencia de servicios
culturalmente adecuados. La etnicidad intersecta con el territorio y el género.

---

> Estas hipótesis son coherentes con evidencia del CONEVAL, la CEPAL y estudios
> comparados de desarrollo regional latinoamericano. La persistencia de las brechas
> sugiere que el crecimiento económico nacional, por sí solo, es insuficiente
> para cerrar desigualdades estructurales de origen territorial.
"""))

# SECCIÓN 10 — DASHBOARD
cells.append(md(
"""## 10. Ideas para visualizaciones del dashboard

Las siguientes piezas visuales están diseñadas para sostener la narrativa central
con máximo impacto y claridad:

| # | Visualización | Tipo | Mensaje clave |
|---|--------------|------|---------------|
| 1 | Mapa coroplético estatal | Choropleth | El color del mapa ES la historia: sur rojo, norte azul |
| 2 | Panel de KPIs | Tarjetas métricas | Chiapas 65.97% vs BC 9.87% — la brecha en un vistazo |
| 3 | Ranking horizontal | Barras | El orden de los estados cuenta la historia |
| 4 | Brecha rural-urbana | Doble línea temporal | La fractura que no cierra |
| 5 | Correlación ingreso-pobreza | Scatter | El territorio explica la posición |
| 6 | Heatmap de carencias | Mapa de calor | El sur acumula todo al mismo tiempo |
| 7 | Brecha étnica | Barras dobles | Superposición de desventajas |
| 8 | Norte vs Sur | Comparador de barras | La fractura en tres dimensiones |
| 9 | LP histórica | Área dual | El costo de sobrevivir sube siempre |
| 10 | Evolución por estado | Líneas múltiples | La brecha persiste aunque mejore el promedio |

**Paleta recomendada:**
`#0F1117` fondo · `#E63946` pobreza alta · `#457B9D` pobreza baja
`#2DC653` progreso · `#F4A261` contraste · `#F1FAEE` texto principal
"""))

# SECCIÓN 11 — CONCLUSIÓN
cells.append(md(
"""## 11. Conclusión narrativa final

> **En México, la dirección en que apunta tu certificado de nacimiento puede determinar,
> con escalofriante predictibilidad, el nivel de pobreza en el que vivirás.**

Los datos del INEGI para 2024 son contundentes:

El **29.6% de los mexicanos** vive en situación de pobreza multidimensional.
Pero ese promedio esconde una realidad profundamente desigual.

En **Chiapas**, esa cifra es **65.97%**. En Baja California, es **9.87%**.
No hay interpretación neutral para una brecha de **6.7 veces**.

El sur concentra los peores indicadores **en todas las dimensiones al mismo tiempo**:
pobreza por ingresos, rezago educativo, vivienda precaria, ausencia de servicios básicos
e inseguridad alimentaria. No es una carencia; es una acumulación estructural.

Las zonas rurales tienen casi el **doble de probabilidad** de pobreza que las urbanas.
Y los hogares indígenas tienen **2.2 veces** más inseguridad alimentaria.
Ser indígena, vivir en zona rural y nacer en el sur de México es la tormenta perfecta
de exclusiones superpuestas.

La pobreza ha mejorado: bajó 13.7 puntos porcentuales entre 2016 y 2024 a nivel nacional.
Pero la **brecha relativa entre territorios no se ha cerrado**. Los estados del norte y
las ciudades mejoran más rápido que los estados del sur.

Incluso **trabajando**, el 32.3% de los mexicanos no genera suficiente para cubrir la
canasta alimentaria básica. El trabajo no garantiza salir de la pobreza si el mercado
laboral de tu territorio está estructuralmente deprimido.

**Lo que los datos nos dicen sin ambigüedad:**
La pobreza en México no es solo un problema de decisiones individuales ni de acceso
a oportunidades en abstracto. Es una herencia territorial, histórica y estructural
que se transmite con mayor fuerza que cualquier programa social de corto plazo.

El lugar de nacimiento sigue siendo, en 2024, uno de los predictores más poderosos
del bienestar en México. Eso no es solo economía. Es inequidad sistémica acumulada.

---

*Análisis elaborado con datos oficiales del INEGI:
Pobreza Multidimensional 2024 · Líneas de Pobreza febrero 2026 · Pobreza Laboral Q4 2025 · SIDS 2024*
"""))

# GUARDAR
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0",
        },
    },
    "cells": cells,
}

with open("analisis_pobreza_mexico.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook guardado: analisis_pobreza_mexico.ipynb")
print(f"Total de celdas: {len(cells)}")
