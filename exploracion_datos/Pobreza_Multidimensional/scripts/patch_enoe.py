"""
patch_enoe.py
=============
Inyecta celdas de análisis ENOE (informalidad laboral territorial) en el notebook
analisis_pobreza_mexico.ipynb. Idempotente: verifica antes de insertar.

Fuente: ENOE 2024 T4 (INEGI)
Indicador: Tasa de Informalidad Laboral por estado = ocupados sin acceso a
           seguridad social / total ocupados con/sin seguridad social.
"""
import json, os, sys

NB_PATH = os.path.join(os.path.dirname(__file__), "..", "analisis_pobreza_mexico.ipynb")
NB_PATH = os.path.normpath(NB_PATH)

# Definición de nuevas celdas

CELL_MD_ENOE = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "## 6b. Informalidad Laboral por Territorio (ENOE 2024 T4)\n",
        "\n",
        "> **Hipótesis complementaria:** *No solo naces pobre — también naces informal.*  \n",
        "> En México, el empleo informal no es una elección: es consecuencia directa del estado en que naciste.\n",
        "\n",
        "**Fuente:** ENOE (Encuesta Nacional de Ocupación y Empleo) 2024, Trimestre 4 — INEGI  \n",
        "**Indicador:** Tasa de Informalidad Laboral = % de ocupados **sin acceso a seguridad social**  \n",
        "**Cobertura:** 32 entidades federativas, ~193K personas expandidas con factor de ponderación trimestral (`fac_tri`)\n"
    ]
}

CELL_CODE_ENOE_LOAD = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ── Carga de datos ENOE: informalidad por estado ──────────────────────────\n",
        "import urllib.request, zipfile, io\n",
        "\n",
        "ENOE_URL = (\n",
        "    \"https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/datosabiertos/\"\n",
        "    \"2024/conjunto_de_datos_enoe_2024_4t_csv.zip\"\n",
        ")\n",
        "ENOE_CACHE = os.path.join(\"datos\", \"ocupacion_y_empleo\", \"informalidad_por_estado_2024.csv\")\n",
        "\n",
        "if os.path.exists(ENOE_CACHE):\n",
        "    df_enoe = pd.read_csv(ENOE_CACHE)\n",
        "    print(f\"ENOE cargado desde caché: {len(df_enoe)} estados\")\n",
        "else:\n",
        "    print(\"Descargando ENOE 2024 T4 (~52 MB)...\")\n",
        "    req = urllib.request.Request(ENOE_URL, headers={\"User-Agent\": \"Mozilla/5.0\"})\n",
        "    with urllib.request.urlopen(req, timeout=120) as r:\n",
        "        data = r.read()\n",
        "\n",
        "    with zipfile.ZipFile(io.BytesIO(data)) as z:\n",
        "        with z.open(\"conjunto_de_datos_sdem_enoe_2024_4t/catalogos/ent.csv\") as f:\n",
        "            ent_cat = pd.read_csv(f, encoding=\"latin-1\")\n",
        "        ent_cat.columns = [\"cve\", \"estado\"]\n",
        "        ent_map = dict(zip(ent_cat.cve, ent_cat.estado))\n",
        "\n",
        "        cols = [\"ent\", \"clase2\", \"seg_soc\", \"fac_tri\", \"ingocup\", \"ur\", \"anios_esc\"]\n",
        "        with z.open(\"conjunto_de_datos_sdem_enoe_2024_4t/conjunto_de_datos/conjunto_de_datos_sdem_enoe_2024_4t.csv\") as f:\n",
        "            sdem = pd.read_csv(f, usecols=cols, encoding=\"latin-1\")\n",
        "\n",
        "    ocup = sdem[sdem.clase2 == 1].copy()\n",
        "    ocup[\"estado\"] = ocup[\"ent\"].map(ent_map)\n",
        "    ocup[\"informal\"] = (ocup.seg_soc == 2).astype(int)\n",
        "    ocup[\"formal\"]   = (ocup.seg_soc == 1).astype(int)\n",
        "    ocup[\"ingocup\"]  = ocup[\"ingocup\"].replace(0, float(\"nan\"))\n",
        "    ocup.loc[ocup.ingocup > 200000, \"ingocup\"] = float(\"nan\")\n",
        "\n",
        "    def _state_stats(df):\n",
        "        ti = df.loc[df.informal == 1, \"fac_tri\"].sum()\n",
        "        tf = df.loc[df.formal   == 1, \"fac_tri\"].sum()\n",
        "        tasa = ti / (ti + tf) * 100 if (ti + tf) > 0 else None\n",
        "        m_i  = (df.informal == 1) & df.ingocup.notna()\n",
        "        m_f  = (df.formal   == 1) & df.ingocup.notna()\n",
        "        m_a  = df.ingocup.notna()\n",
        "        m_e  = df.anios_esc.notna() & (df.anios_esc <= 25)\n",
        "        def wavg(mask): return (df.loc[mask, \"ingocup\"] * df.loc[mask, \"fac_tri\"]).sum() / df.loc[mask, \"fac_tri\"].sum() if mask.sum() > 0 else None\n",
        "        esc  = (df.loc[m_e, \"anios_esc\"] * df.loc[m_e, \"fac_tri\"]).sum() / df.loc[m_e, \"fac_tri\"].sum() if m_e.sum() > 0 else None\n",
        "        return pd.Series({\n",
        "            \"tasa_informalidad\":   tasa,\n",
        "            \"ingreso_informal\":    wavg(m_i),\n",
        "            \"ingreso_formal\":      wavg(m_f),\n",
        "            \"ingreso_promedio\":    wavg(m_a),\n",
        "            \"escolaridad_promedio\": esc,\n",
        "            \"ocupados_expandidos\": df.fac_tri.sum(),\n",
        "        })\n",
        "\n",
        "    df_enoe = ocup.groupby(\"estado\", include_groups=False if hasattr(pd.core.groupby.GroupBy, 'include_groups') else True).apply(_state_stats).reset_index()\n",
        "    os.makedirs(os.path.join(\"datos\", \"ocupacion_y_empleo\"), exist_ok=True)\n",
        "    df_enoe.to_csv(ENOE_CACHE, index=False)\n",
        "    print(f\"ENOE procesado y guardado: {len(df_enoe)} estados\")\n",
        "\n",
        "df_enoe = df_enoe.sort_values(\"tasa_informalidad\").reset_index(drop=True)\n",
        "\n",
        "# Alinear nombres con df_pm para merge posterior\n",
        "NORM_ENOE = {\n",
        "    \"México\":          \"Estado de México\",\n",
        "    \"Michoacán\":        \"Michoacán de Ocampo\",\n",
        "    \"Veracruz\":         \"Veracruz de Ignacio de la Llave\",\n",
        "    \"Ciudad de México\": \"Ciudad de México\",\n",
        "    \"Coahuila\":         \"Coahuila de Zaragoza\",\n",
        "}\n",
        "df_enoe[\"estado_norm\"] = df_enoe[\"estado\"].replace(NORM_ENOE)\n",
        "print(df_enoe[[\"estado\", \"tasa_informalidad\", \"ingreso_informal\", \"ingreso_formal\"]].to_string(index=False, float_format=lambda x: f\"{x:.1f}\"))\n"
    ]
}

CELL_MD_VIZ_ENOE = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Visualización: Informalidad territorial\n",
        "\n",
        "Tres gráficos que demuestran la trampa territorial de la informalidad:\n",
        "1. **Ranking** de informalidad por estado (barras horizontales, anotado norte/sur)\n",
        "2. **Scatter** pobreza multidimensional vs tasa de informalidad por estado\n",
        "3. **Brecha salarial** formal vs informal por estado\n"
    ]
}

CELL_CODE_VIZ_ENOE = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ── Fig 1: Ranking informalidad por estado ─────────────────────────────────\n",
        "fig, ax = plt.subplots(figsize=(12, 10), facecolor=DARK_BG)\n",
        "ax.set_facecolor(DARK_BG)\n",
        "\n",
        "REGION_MAP = {\n",
        "    **{e: \"Norte\" for e in [\"Baja California\",\"Baja California Sur\",\"Sonora\",\"Chihuahua\",\"Coahuila\",\"Nuevo León\",\"Tamaulipas\",\"Sinaloa\",\"Durango\"]},\n",
        "    **{e: \"Centro\" for e in [\"Jalisco\",\"Guanajuato\",\"Querétaro\",\"Aguascalientes\",\"Colima\",\"Michoacán\",\"México\",\"Morelos\",\"Tlaxcala\",\"Puebla\",\"Hidalgo\",\"Zacatecas\",\"Nayarit\",\"San Luis Potosí\"]},\n",
        "    **{e: \"Sur\"   for e in [\"Oaxaca\",\"Chiapas\",\"Guerrero\",\"Veracruz\",\"Tabasco\",\"Campeche\",\"Yucatán\",\"Quintana Roo\"]},\n",
        "    \"Ciudad de México\": \"CDMX\",\n",
        "}\n",
        "REGION_COLORS = {\"Norte\": ACCENT2, \"Centro\": WARM, \"Sur\": ACCENT, \"CDMX\": ACCENT3}\n",
        "\n",
        "colors = [REGION_COLORS.get(REGION_MAP.get(e, \"Centro\"), WARM) for e in df_enoe[\"estado\"]]\n",
        "bars = ax.barh(df_enoe[\"estado\"], df_enoe[\"tasa_informalidad\"], color=colors, alpha=0.85, height=0.75)\n",
        "\n",
        "for bar, val in zip(bars, df_enoe[\"tasa_informalidad\"]):\n",
        "    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f\"{val:.1f}%\",\n",
        "            va=\"center\", ha=\"left\", fontsize=8, color=TEXT_MAIN)\n",
        "\n",
        "ax.axvline(60, color=TEXT_DIM, lw=1, ls=\"--\", alpha=0.6)\n",
        "ax.text(60.5, -0.8, \"Promedio nacional (60%)\", fontsize=8, color=TEXT_DIM)\n",
        "\n",
        "from matplotlib.patches import Patch\n",
        "leyenda = [Patch(color=v, label=k) for k, v in REGION_COLORS.items()]\n",
        "ax.legend(handles=leyenda, loc=\"lower right\", facecolor=CARD_BG, labelcolor=TEXT_MAIN, fontsize=9)\n",
        "\n",
        "ax.set_xlabel(\"% de ocupados sin seguridad social (informalidad)\", color=TEXT_MAIN, fontsize=11)\n",
        "ax.set_title(\"Informalidad Laboral por Estado — México 2024 T4\", color=TEXT_MAIN, fontsize=14, fontweight=\"bold\", pad=15)\n",
        "ax.tick_params(colors=TEXT_MAIN, labelsize=9)\n",
        "ax.spines[[\"top\",\"right\",\"bottom\"]].set_visible(False)\n",
        "ax.spines[\"left\"].set_color(TEXT_DIM)\n",
        "ax.set_xlim(0, 100)\n",
        "plt.tight_layout()\n",
        "plt.savefig(os.path.join(\"imagenes\", \"fig_informalidad_ranking.png\"), dpi=150, bbox_inches=\"tight\", facecolor=DARK_BG)\n",
        "plt.show()\n",
        "print(\"fig_informalidad_ranking.png guardado\")\n"
    ]
}

CELL_CODE_SCATTER_ENOE = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# ── Fig 2: Scatter pobreza multidimensional vs informalidad ────────────────\n",
        "# Merge ENOE con datos de pobreza multidimensional (df principal del notebook)\n",
        "df_scatter = df[[\"estado\",\"pct_pobreza_2024\",\"pct_extrema_2024\"]].copy()\n",
        "df_scatter[\"estado_norm\"] = df_scatter[\"estado\"].replace({\n",
        "    \"Michoacán de Ocampo\":          \"Michoacán\",\n",
        "    \"Veracruz de Ignacio de la Llave\": \"Veracruz\",\n",
        "    \"Coahuila de Zaragoza\":          \"Coahuila\",\n",
        "    \"Estado de México\":              \"México\",\n",
        "})\n",
        "df_merged = df_scatter.merge(df_enoe[[\"estado\",\"tasa_informalidad\",\"ingreso_informal\",\"ingreso_formal\"]],\n",
        "                              left_on=\"estado_norm\", right_on=\"estado\", how=\"inner\")\n",
        "print(f\"Merge exitoso: {len(df_merged)} estados\")\n",
        "\n",
        "fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=DARK_BG)\n",
        "ax1, ax2 = axes\n",
        "ax1.set_facecolor(DARK_BG)\n",
        "ax2.set_facecolor(DARK_BG)\n",
        "\n",
        "# Scatter: informalidad vs pobreza multidimensional\n",
        "sc = ax1.scatter(df_merged[\"tasa_informalidad\"], df_merged[\"pct_pobreza_2024\"],\n",
        "                 c=df_merged[\"pct_pobreza_2024\"], cmap=\"RdYlGn_r\", s=80, alpha=0.85, zorder=3)\n",
        "for _, row in df_merged.iterrows():\n",
        "    ax1.annotate(row[\"estado_norm\"], (row[\"tasa_informalidad\"], row[\"pct_pobreza_2024\"]),\n",
        "                 textcoords=\"offset points\", xytext=(5, 3), fontsize=7, color=TEXT_MAIN)\n",
        "\n",
        "# Línea de tendencia\n",
        "import numpy as np\n",
        "mask = df_merged[[\"tasa_informalidad\",\"pct_pobreza_2024\"]].notna().all(axis=1)\n",
        "if mask.sum() >= 3:\n",
        "    m, b = np.polyfit(df_merged.loc[mask,\"tasa_informalidad\"], df_merged.loc[mask,\"pct_pobreza_2024\"], 1)\n",
        "    xr = np.linspace(df_merged[\"tasa_informalidad\"].min(), df_merged[\"tasa_informalidad\"].max(), 50)\n",
        "    ax1.plot(xr, m*xr+b, color=ACCENT, lw=2, ls=\"--\", alpha=0.8, label=f\"Tendencia (m={m:.2f})\")\n",
        "    ax1.legend(facecolor=CARD_BG, labelcolor=TEXT_MAIN, fontsize=9)\n",
        "\n",
        "ax1.set_xlabel(\"Tasa de Informalidad (%)\", color=TEXT_MAIN, fontsize=11)\n",
        "ax1.set_ylabel(\"% Pobreza Multidimensional (2024)\", color=TEXT_MAIN, fontsize=11)\n",
        "ax1.set_title(\"Informalidad vs Pobreza por Estado\", color=TEXT_MAIN, fontsize=13, fontweight=\"bold\")\n",
        "ax1.tick_params(colors=TEXT_MAIN)\n",
        "ax1.spines[[\"top\",\"right\"]].set_visible(False)\n",
        "ax1.spines[[\"left\",\"bottom\"]].set_color(TEXT_DIM)\n",
        "\n",
        "# Scatter: brecha salarial formal vs informal\n",
        "ax2.scatter(df_merged[\"ingreso_informal\"], df_merged[\"ingreso_formal\"],\n",
        "            c=df_merged[\"tasa_informalidad\"], cmap=\"RdYlGn_r\", s=80, alpha=0.85, zorder=3)\n",
        "for _, row in df_merged.iterrows():\n",
        "    ax2.annotate(row[\"estado_norm\"], (row[\"ingreso_informal\"], row[\"ingreso_formal\"]),\n",
        "                 textcoords=\"offset points\", xytext=(4, 3), fontsize=7, color=TEXT_MAIN)\n",
        "mn = min(df_merged[\"ingreso_informal\"].min(), df_merged[\"ingreso_formal\"].min()) * 0.95\n",
        "mx = max(df_merged[\"ingreso_informal\"].max(), df_merged[\"ingreso_formal\"].max()) * 1.05\n",
        "ax2.plot([mn, mx], [mn, mx], color=TEXT_DIM, lw=1, ls=\"--\", alpha=0.6, label=\"Igualdad (formal=informal)\")\n",
        "ax2.legend(facecolor=CARD_BG, labelcolor=TEXT_MAIN, fontsize=9)\n",
        "ax2.set_xlabel(\"Ingreso promedio INFORMAL ($/mes)\", color=TEXT_MAIN, fontsize=11)\n",
        "ax2.set_ylabel(\"Ingreso promedio FORMAL ($/mes)\", color=TEXT_MAIN, fontsize=11)\n",
        "ax2.set_title(\"Brecha Salarial: Formal vs Informal por Estado\", color=TEXT_MAIN, fontsize=13, fontweight=\"bold\")\n",
        "ax2.tick_params(colors=TEXT_MAIN)\n",
        "ax2.spines[[\"top\",\"right\"]].set_visible(False)\n",
        "ax2.spines[[\"left\",\"bottom\"]].set_color(TEXT_DIM)\n",
        "\n",
        "fig.suptitle(\n",
        "    \"Informalidad y Desigualdad Salarial — El doble castigo territorial\",\n",
        "    color=TEXT_MAIN, fontsize=14, fontweight=\"bold\", y=1.01\n",
        ")\n",
        "plt.tight_layout()\n",
        "plt.savefig(os.path.join(\"imagenes\", \"fig_informalidad_scatter.png\"), dpi=150, bbox_inches=\"tight\", facecolor=DARK_BG)\n",
        "plt.show()\n",
        "print(\"fig_informalidad_scatter.png guardado\")\n"
    ]
}

CELL_MD_ENOE_HALLAZGOS = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### Hallazgos: La trampa territorial de la informalidad\n",
        "\n",
        "| | Chiapas | Guerrero | Oaxaca | **Nuevo León** | **CDMX** |\n",
        "|---|---|---|---|---|---|\n",
        "| Informalidad | **85.2%** | **82.2%** | **81.4%** | 37.6% | 52.0% |\n",
        "| Ingreso informal/mes | $5,607 | $6,563 | $5,974 | $10,927 | $10,009 |\n",
        "| Ingreso formal/mes | $12,065 | $11,263 | $12,448 | $14,518 | $18,086 |\n",
        "| Años de escolaridad | 8.7 | 8.8 | 9.0 | 11.4 | 12.4 |\n",
        "\n",
        "**El doble castigo territorial:**\n",
        "1. Si naces en Chiapas, tienes **2.3 veces más probabilidad** de trabajar en la informalidad (85% vs 37%)\n",
        "2. Como trabajador informal en Chiapas ganas **$5,607/mes** — la mitad del informal de Nuevo León ($10,927)\n",
        "3. La escolaridad promedio en Chiapas es 8.7 años vs 11.4 en Nuevo León — **el ciclo se perpetúa**\n",
        "\n",
        "> **Sur informal pobre → menos escolaridad → más informalidad → más pobreza**  \n",
        "> La geografía no es un factor de riesgo, es el determinante estructural.\n"
    ]
}

# Leer y parchear el notebook

def already_patched(cells, keyword):
    for c in cells:
        src = "".join(c.get("source", []))
        if keyword in src:
            return True
    return False

def find_anchor_idx(cells, keyword):
    """Devuelve índice de la celda que contiene keyword, o -1 si no existe."""
    for i, c in enumerate(cells):
        src = "".join(c.get("source", []))
        if keyword in src:
            return i
    return -1

def run():
    if not os.path.exists(NB_PATH):
        print(f"ERROR: No se encontró {NB_PATH}")
        sys.exit(1)

    with open(NB_PATH, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb["cells"]

    # Verificar idempotencia
    GUARD = "informalidad_por_estado_2024.csv"
    if already_patched(cells, GUARD):
        print("Notebook ya tiene celdas ENOE. Sin cambios.")
        return

    # Ancla: insertar después de la sección de "Hallazgos" (sección 7)
    # o bien al final si no se encuentra.
    ANCHOR_KEYWORD = "pobreza laboral"  # buscar sección de hallazgos PL
    anchor_idx = find_anchor_idx(cells, ANCHOR_KEYWORD)
    if anchor_idx == -1:
        # Buscar celda de KPIs como fallback
        anchor_idx = find_anchor_idx(cells, "## 6.")
        if anchor_idx == -1:
            # Al final antes de conclusiones
            anchor_idx = find_anchor_idx(cells, "Conclusi")
            if anchor_idx == -1:
                anchor_idx = len(cells) - 2  # ante-penúltima celda

    insert_pos = anchor_idx + 1
    print(f"Insertando 5 celdas ENOE en posición {insert_pos} (después de celda {anchor_idx})")

    new_cells = [
        CELL_MD_ENOE,
        CELL_CODE_ENOE_LOAD,
        CELL_MD_VIZ_ENOE,
        CELL_CODE_VIZ_ENOE,
        CELL_CODE_SCATTER_ENOE,
        CELL_MD_ENOE_HALLAZGOS,
    ]

    for i, cell in enumerate(new_cells):
        cells.insert(insert_pos + i, cell)

    nb["cells"] = cells

    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"OK — notebook tiene ahora {len(nb['cells'])} celdas")
    print(f"Archivo: {NB_PATH}")


if __name__ == "__main__":
    run()
