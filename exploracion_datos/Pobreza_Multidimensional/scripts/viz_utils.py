"""
Utilidades de visualización para el análisis de pobreza en México.
Paleta, estilos y funciones reutilizables.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

DARK_BG   = "#0F1117"
CARD_BG   = "#1E2235"
ACCENT    = "#FF3A3A"
ACCENT2   = "#5B9CC9"
ACCENT3   = "#A8DADC"
WARM      = "#FF8844"
GREEN     = "#2DC653"
TEXT_MAIN = "#F1FAEE"
TEXT_DIM  = "#A8B2C1"
DIVIDER   = "#2A2F3E"

SEQ_RED   = ["#FFF3F3", "#FFAAAA", "#FF6B6B", "#E63946", "#9B1B24", "#4A0D11"]
SEQ_BLUE  = ["#EBF4FA", "#90CAE4", "#5B9CC9", "#1E4D7B", "#0A2540"]
DIVERGING = ["#2DC653", "#A8DADC", "#F4F4F4", "#FF8844", "#FF3A3A"]

REGION_COLORS = {
    "Norte":  "#5B9CC9",
    "Centro": "#FF8844",
    "Sur":    "#FF3A3A",
    "CDMX":   "#A8DADC",
}

def set_global_style():
    plt.rcParams.update({
        "figure.facecolor":   DARK_BG,
        "axes.facecolor":     CARD_BG,
        "axes.edgecolor":     DIVIDER,
        "axes.labelcolor":    TEXT_MAIN,
        "axes.titlecolor":    TEXT_MAIN,
        "axes.titlesize":     20,
        "axes.labelsize":     15,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "xtick.color":        TEXT_DIM,
        "ytick.color":        TEXT_DIM,
        "xtick.labelsize":    13,
        "ytick.labelsize":    13,
        "legend.facecolor":   CARD_BG,
        "legend.edgecolor":   DIVIDER,
        "legend.fontsize":    13,
        "legend.labelcolor":  TEXT_MAIN,
        "text.color":         TEXT_MAIN,
        "grid.color":         DIVIDER,
        "grid.linestyle":     "--",
        "grid.alpha":         0.5,
        "figure.dpi":         150,
        "font.family":        "DejaVu Sans",
        "lines.linewidth":    3.0,
    })

set_global_style()


def fig_title(fig, title, subtitle=None, y_title=0.97, y_sub=0.92):
    fig.text(0.5, y_title, title,
             ha="center", va="top", fontsize=22, fontweight="bold",
             color=TEXT_MAIN)
    if subtitle:
        fig.text(0.5, y_sub, subtitle,
                 ha="center", va="top", fontsize=14, color=TEXT_DIM,
                 style="italic")


def add_source(fig, source="INEGI – Pobreza Multidimensional 2024 / SIDS 2024 / LP 2026 / PL 2025",
               y=0.01):
    fig.text(0.5, y, f"Fuente: {source}", ha="center",
             fontsize=11, color=TEXT_DIM)


def bar_label_outside(ax, bars, fmt="{:.1f}%", color=TEXT_MAIN, fontsize=13, pad=0.3):
    """Etiqueta fuera de las barras horizontales."""
    for bar in bars:
        w = bar.get_width()
        ax.text(w + pad, bar.get_y() + bar.get_height() / 2,
                fmt.format(w), va="center", ha="left",
                fontsize=fontsize, color=color, fontweight="bold")


def bar_label_top(ax, bars, fmt="{:.1f}%", color=TEXT_MAIN, fontsize=12, pad=0.5):
    """Etiqueta encima de barras verticales."""
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + pad,
                fmt.format(h), ha="center", va="bottom",
                fontsize=fontsize, color=color, fontweight="bold")


def colorbar_label(fig, ax, mappable, label="", fontsize=13):
    cb = fig.colorbar(mappable, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label(label, fontsize=fontsize, color=TEXT_MAIN)
    cb.ax.yaxis.set_tick_params(color=TEXT_DIM, labelsize=12)
    plt.setp(plt.getp(cb.ax.axes, "yticklabels"), color=TEXT_DIM)
    return cb


def annotate_max_min(ax, series, x_vals, fmt="{:.1f}%", color_max=ACCENT,
                     color_min=GREEN, offset=1.5):
    idx_max = series.idxmax()
    idx_min = series.idxmin()
    ax.annotate(fmt.format(series[idx_max]),
                xy=(x_vals[idx_max], series[idx_max]),
                xytext=(0, offset * 12), textcoords="offset points",
                ha="center", fontsize=12, color=color_max, fontweight="bold")
    ax.annotate(fmt.format(series[idx_min]),
                xy=(x_vals[idx_min], series[idx_min]),
                xytext=(0, -offset * 14), textcoords="offset points",
                ha="center", fontsize=12, color=color_min, fontweight="bold")
