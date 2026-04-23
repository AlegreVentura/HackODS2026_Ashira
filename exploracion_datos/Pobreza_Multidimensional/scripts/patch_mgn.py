"""
Inyecta las celdas del Marco Geoestadístico Nacional (MGN) en el notebook existente.

Posiciones de inserción:
  - Después de la celda [08] (último bloque de carga de datos)  → descarga + merge MGN
  - Después de la celda [13] (encabezado sección 5)             → coropléticos

Uso:
    python scripts/patch_mgn.py
    python -m nbconvert --to notebook --execute --inplace
           --ExecutePreprocessor.timeout=300
           analisis_pobreza_mexico.ipynb
"""
import json, uuid, os

NOTEBOOK = "analisis_pobreza_mexico.ipynb"

def uid():
    return uuid.uuid4().hex[:8]

def md(source):
    return {"cell_type": "markdown", "id": uid(), "metadata": {}, "source": source}

def code(source):
    return {
        "cell_type": "code", "id": uid(), "metadata": {},
        "source": source, "outputs": [], "execution_count": None,
    }


# BLOQUE A — Marco Geoestadístico Nacional: descarga y preparación
# (insertar DESPUÉS de la celda [08])

CELL_MGN_MD = md(
"""### Marco Geoestadístico Nacional (MGN)

El **Marco Geoestadístico Nacional** del INEGI es la fuente oficial de límites
territoriales de México. Nos proporciona los polígonos de las 32 entidades federativas
necesarios para construir mapas coropléticos.

**Fuente:** API REST de INEGI — Marco Geoestadístico Nacional
`https://geoservicios.inegi.org.mx/arcgis/rest/services/marcogeoestadistico/MapServer/1/query`

El notebook intenta descargar directamente desde la API oficial de INEGI.
Si no está disponible (ambiente sin conexión o servicio temporalmente caído),
usa automáticamente la fuente de respaldo y guarda en caché local el resultado.
La caché evita descargas repetidas en ejecuciones posteriores.
""")

CELL_MGN_LOAD = code(
"""import requests, json, geopandas as gpd
from io import StringIO

MGN_PATH = "datos/marco_geoestadistico/entidades.geojson"
os.makedirs("datos/marco_geoestadistico", exist_ok=True)

if not os.path.exists(MGN_PATH):
    INEGI_API = (
        "https://geoservicios.inegi.org.mx/arcgis/rest/services/"
        "marcogeoestadistico/MapServer/1/query"
        "?where=1%3D1"
        "&outFields=CVE_ENT%2CNOMGEO"
        "&returnGeometry=true"
        "&f=geojson"
        "&outSR=4326")
    RESPALDO = (
        "https://raw.githubusercontent.com/"
        "angelnmara/geojson/master/mexicoHigh.json")

    fuente_usada = None
    for label, url in [("API INEGI (MGN oficial)", INEGI_API),
                        ("Respaldo (derivado de INEGI MGN)", RESPALDO)]:
        try:
            r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            geojson_data = r.json()
            if "features" in geojson_data and len(geojson_data["features"]) >= 30:
                fuente_usada = label
                break
        except Exception as e:
            print(f"  [{label}] no disponible: {e}")

    if fuente_usada is None:
        raise RuntimeError("No se pudo obtener el MGN desde ninguna fuente.")

    with open(MGN_PATH, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, ensure_ascii=False)
    print(f"Descargado y guardado en cache: {MGN_PATH}")
    print(f"Fuente: {fuente_usada}")
else:
    print(f"Cargando desde cache local: {MGN_PATH}")

gdf = gpd.read_file(MGN_PATH)

# La API INEGI usa NOMGEO; el respaldo usa 'name'
if "NOMGEO" in gdf.columns:
    gdf = gdf.rename(columns={"NOMGEO": "estado_geo"})
elif "name" in gdf.columns:
    gdf = gdf.rename(columns={"name": "estado_geo"})

# Mapeo de nombres largos → nombres cortos del dataset principal
NORM = {
    "México": "Estado de México",
    "Veracruz de Ignacio de la Llave": "Veracruz",
    "Michoacán de Ocampo": "Michoacán",
    "Coahuila de Zaragoza": "Coahuila",
}
gdf["estado_geo"] = gdf["estado_geo"].replace(NORM)

gdf_pm = gdf.merge(df, left_on="estado_geo", right_on="estado", how="left")

# Verificar cobertura
sin_match = gdf_pm[gdf_pm["pct_pobreza_2024"].isna()]["estado_geo"].tolist()
if sin_match:
    print(f"AVISO — sin datos para: {sin_match}")
else:
    print(f"Merge completo: {len(gdf_pm)} entidades con datos de pobreza.")

gdf_pm = gdf_pm.to_crs(epsg=6372)   # proyección oficial INEGI para México
print(f"CRS: {gdf_pm.crs.name}")
""")


# BLOQUE B — Coropléticos (insertar DESPUÉS del encabezado de sección 5)

CELL_CHORO_MD = md(
"""### El mapa que lo dice todo

> Antes de cualquier barra, cualquier número, cualquier argumento verbal —
> este mapa.
> El patrón norte-sur emerge sin necesidad de explicación.
> El color habla solo.

El coroplético de pobreza multidimensional 2024 es el argumento visual más
contundente de esta narrativa: el territorio condiciona la pobreza de forma
sistemática, no aleatoria.
""")

CELL_CHOROPLETH = code(
"""from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.patheffects as pe

CMAP = LinearSegmentedColormap.from_list(
    "pobreza",
    ["#2DC653", "#F4A261", "#E63946"],
    N=256,
)

fig, axes = plt.subplots(1, 2, figsize=(20, 10),
                          gridspec_kw={"width_ratios": [1.6, 1]})
fig.patch.set_facecolor(DARK_BG)

ax_map = axes[0]
ax_map.set_facecolor(DARK_BG)
ax_map.axis("off")

vmin, vmax = 0, 70
norm = Normalize(vmin=vmin, vmax=vmax)

gdf_pm.plot(
    column="pct_pobreza_2024",
    ax=ax_map,
    cmap=CMAP,
    norm=norm,
    linewidth=0.4,
    edgecolor="#0F1117",
    missing_kwds={"color": "#2A2F3E", "label": "Sin dato"},
)

# Colorbar
sm = ScalarMappable(cmap=CMAP, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax_map, orientation="horizontal",
                    fraction=0.03, pad=0.02, aspect=40)
cbar.set_label("% población en situación de pobreza (2024)",
               fontsize=13, color=TEXT_MAIN)
cbar.ax.xaxis.set_tick_params(color=TEXT_DIM, labelsize=12)
plt.setp(plt.getp(cbar.ax.axes, "xticklabels"), color=TEXT_DIM)

# Anotaciones: estados extremos
DESTACAR = {
    "Chiapas":    (dict(ha="left",  va="center"), ( 3e5,  1.8e6)),
    "Guerrero":   (dict(ha="left",  va="center"), (-2e5,  2.0e6)),
    "Oaxaca":     (dict(ha="left",  va="bottom"), ( 2e5,  1.9e6)),
    "Baja California": (dict(ha="left", va="bottom"), ( 5e5, 3.3e6)),
    "Nuevo León": (dict(ha="right", va="center"), (-3e5, 2.8e6)),
}
for estado, (kwargs, xy_offset) in DESTACAR.items():
    row = gdf_pm[gdf_pm["estado_geo"] == estado]
    if row.empty:
        continue
    cx = float(row.geometry.centroid.x)
    cy = float(row.geometry.centroid.y)
    pct = float(row["pct_pobreza_2024"].values[0])
    ax_map.annotate(
        f"{estado}\\n{pct:.1f}%",
        xy=(cx, cy),
        xytext=(cx + xy_offset[0], cy + xy_offset[1]),
        fontsize=10, color=TEXT_MAIN, fontweight="bold",
        arrowprops=dict(arrowstyle="-", color=TEXT_DIM, lw=0.8),
        **kwargs,
    )

ax_map.set_title("Pobreza multidimensional 2024 por entidad federativa",
                 fontsize=16, color=TEXT_MAIN, pad=14)

ax_bar = axes[1]
ax_bar.set_facecolor(CARD_BG)
ax_bar.spines["top"].set_visible(False); ax_bar.spines["right"].set_visible(False)
ax_bar.spines["left"].set_color(DIVIDER); ax_bar.spines["bottom"].set_color(DIVIDER)

df_ext = df.sort_values("pct_pobreza_2024")
top5   = df_ext.tail(5)[["estado", "pct_pobreza_2024"]].iloc[::-1]
bot5   = df_ext.head(5)[["estado", "pct_pobreza_2024"]]
df_panel = pd.concat([top5, bot5])
colores_panel = (
    [ACCENT] * 5 + [GREEN] * 5
)

bars = ax_bar.barh(df_panel["estado"], df_panel["pct_pobreza_2024"],
                   color=colores_panel, height=0.65,
                   edgecolor=DARK_BG, linewidth=0.5)
for bar in bars:
    w = bar.get_width()
    ax_bar.text(w + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{w:.1f}%", va="center", fontsize=12,
                color=TEXT_MAIN, fontweight="bold")

ax_bar.axvline(29.56, color=TEXT_DIM, lw=1.3, linestyle="--", alpha=0.6)
ax_bar.text(29.56 + 0.4, -0.5, "Nacional\\n29.6%",
            fontsize=10, color=TEXT_DIM, va="top")
ax_bar.set_xlim(0, 80)
ax_bar.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
ax_bar.tick_params(axis="y", labelsize=11)
ax_bar.grid(axis="x", alpha=0.3)
ax_bar.set_title("Los 5 más pobres vs los 5 menos pobres",
                 fontsize=13, pad=10)

handles = [
    mpatches.Patch(color=ACCENT, label="Mayor pobreza (sur)"),
    mpatches.Patch(color=GREEN,  label="Menor pobreza (norte)"),
]
ax_bar.legend(handles=handles, fontsize=11, framealpha=0.3)

fig.text(0.5, 0.97,
         "El territorio condiciona la pobreza — México 2024",
         ha="center", fontsize=22, fontweight="bold", color=TEXT_MAIN)
fig.text(0.5, 0.93,
         "Marco Geoestadístico Nacional · INEGI · Pobreza Multidimensional 2024",
         ha="center", fontsize=13, color=TEXT_DIM, style="italic")

plt.tight_layout(rect=[0, 0.0, 1, 0.91])
plt.savefig("imagenes/fig_mapa_pobreza.png", dpi=140,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
""")

CELL_CHORO2 = code(
"""# ── Segundo mapa: cambio 2016 → 2024 (¿quién avanzó más?) ────────────────────
CMAP_DIV = LinearSegmentedColormap.from_list(
    "cambio",
    ["#2DC653", "#F1FAEE", "#E63946"],
    N=256,
)

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(DARK_BG)
ax.axis("off")

lim = max(abs(gdf_pm["cambio_pobreza"].min()),
          abs(gdf_pm["cambio_pobreza"].max()))
norm_div = Normalize(vmin=-lim, vmax=lim)

gdf_pm.plot(
    column="cambio_pobreza",
    ax=ax,
    cmap=CMAP_DIV,
    norm=norm_div,
    linewidth=0.5,
    edgecolor="#0F1117",
    missing_kwds={"color": "#2A2F3E"},
)

sm2 = ScalarMappable(cmap=CMAP_DIV, norm=norm_div)
sm2.set_array([])
cbar2 = fig.colorbar(sm2, ax=ax, orientation="horizontal",
                     fraction=0.025, pad=0.02, aspect=45)
cbar2.set_label("Cambio en puntos porcentuales (verde = mejoró, rojo = empeoró)",
                fontsize=13, color=TEXT_MAIN)
cbar2.ax.xaxis.set_tick_params(color=TEXT_DIM, labelsize=12)
plt.setp(plt.getp(cbar2.ax.axes, "xticklabels"), color=TEXT_DIM)

# Anotaciones
DESTACAR2 = {
    "Chiapas":    ( 3e5,  1.8e6),
    "Guerrero":   (-2e5,  2.0e6),
    "Ciudad de México": (-3e5,  2.35e6),
    "Tabasco":    ( 2e5,  1.7e6),
}
for estado, xy_offset in DESTACAR2.items():
    row = gdf_pm[gdf_pm["estado_geo"] == estado]
    if row.empty:
        continue
    cx = float(row.geometry.centroid.x)
    cy = float(row.geometry.centroid.y)
    cambio = float(row["cambio_pobreza"].values[0])
    color_ann = GREEN if cambio < 0 else ACCENT
    ax.annotate(
        f"{estado}\\n{cambio:+.1f} pp",
        xy=(cx, cy),
        xytext=(cx + xy_offset[0], cy + xy_offset[1]),
        fontsize=10, color=color_ann, fontweight="bold",
        arrowprops=dict(arrowstyle="-", color=TEXT_DIM, lw=0.8),
        ha="left", va="center",
    )

fig.text(0.5, 0.97,
         "Reducción de la pobreza 2016 → 2024 por entidad",
         ha="center", fontsize=20, fontweight="bold", color=TEXT_MAIN)
fig.text(0.5, 0.93,
         "Verde: mejoró · Rojo: empeoró · Blanco: sin cambio significativo",
         ha="center", fontsize=13, color=TEXT_DIM, style="italic")

plt.tight_layout(rect=[0, 0.0, 1, 0.91])
plt.savefig("imagenes/fig_mapa_cambio.png", dpi=140,
            bbox_inches="tight", facecolor=DARK_BG)
plt.show()
""")


# INYECTAR EN EL NOTEBOOK

with open(NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

# ── Anchor 1: última celda de carga de datos (cell [08])
# Buscamos la celda que contiene "# Pobreza Laboral Q4 2025 por estado"
def find_cell(keyword):
    for i, c in enumerate(cells):
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        if keyword in src:
            return i
    return None

idx_load = find_cell("Pobreza Laboral Q4 2025 por estado")
# ── Anchor 2: encabezado sección 5
idx_s5 = find_cell("## 5. Análisis territorial")

if idx_load is None or idx_s5 is None:
    raise RuntimeError(
        f"No se encontraron anclas. idx_load={idx_load}, idx_s5={idx_s5}")

print(f"Ancla carga datos: celda [{idx_load}]")
print(f"Ancla sección 5:   celda [{idx_s5}]")

# Comprobar si ya se inyectó antes (idempotente)
already_mgn   = any("Marco Geoestadístico" in ("".join(c["source"]) if isinstance(c["source"], list) else c["source"])
                    for c in cells)
already_choro = any("fig_mapa_pobreza" in ("".join(c["source"]) if isinstance(c["source"], list) else c["source"])
                    for c in cells)

if already_mgn and already_choro:
    print("Las celdas MGN ya están presentes. Sin cambios.")
else:
    # Insertar bloque B primero (índice mayor → no desplaza el índice A)
    if not already_choro:
        insert_b = idx_s5 + 1   # después del header de sección 5
        for cell_b in reversed([CELL_CHORO_MD, CELL_CHOROPLETH, CELL_CHORO2]):
            cells.insert(insert_b, cell_b)
        print(f"Bloque B (coropléticos) insertado en posición {insert_b}")

    # Insertar bloque A
    if not already_mgn:
        insert_a = idx_load + 1
        for cell_a in reversed([CELL_MGN_MD, CELL_MGN_LOAD]):
            cells.insert(insert_a, cell_a)
        print(f"Bloque A (MGN) insertado en posición {insert_a}")

    nb["cells"] = cells
    with open(NOTEBOOK, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Notebook actualizado: {len(nb['cells'])} celdas totales.")
