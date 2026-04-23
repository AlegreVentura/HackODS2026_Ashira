"""
Funciones para parsear los tabulados ampliados del Censo 2020 (INEGI).
Los tabulados tienen formato multi-header con filas por entidad federativa,
sexo (Total/Hombres/Mujeres) y tipo de estimador (Valor/Error estándar/etc.).

Solo extraemos: Estimador == "Valor", Sexo == "Total".
"""

import pandas as pd
import openpyxl


ESTADOS_32 = [
    "01 Aguascalientes", "02 Baja California", "03 Baja California Sur",
    "04 Campeche", "05 Coahuila de Zaragoza", "06 Colima", "07 Chiapas",
    "08 Chihuahua", "09 Ciudad de México", "10 Durango", "11 Guanajuato",
    "12 Guerrero", "13 Hidalgo", "14 Jalisco", "15 México",
    "16 Michoacán de Ocampo", "17 Morelos", "18 Nayarit", "19 Nuevo León",
    "20 Oaxaca", "21 Puebla", "22 Querétaro", "23 Quintana Roo",
    "24 San Luis Potosí", "25 Sinaloa", "26 Sonora", "27 Tabasco",
    "28 Tamaulipas", "29 Tlaxcala", "30 Veracruz de Ignacio de la Llave",
    "31 Yucatán", "32 Zacatecas",
]

ESTADOS_CORTOS = {
    "01 Aguascalientes": "Aguascalientes",
    "02 Baja California": "Baja California",
    "03 Baja California Sur": "Baja California Sur",
    "04 Campeche": "Campeche",
    "05 Coahuila de Zaragoza": "Coahuila",
    "06 Colima": "Colima",
    "07 Chiapas": "Chiapas",
    "08 Chihuahua": "Chihuahua",
    "09 Ciudad de México": "CDMX",
    "10 Durango": "Durango",
    "11 Guanajuato": "Guanajuato",
    "12 Guerrero": "Guerrero",
    "13 Hidalgo": "Hidalgo",
    "14 Jalisco": "Jalisco",
    "15 México": "Estado de México",
    "16 Michoacán de Ocampo": "Michoacán",
    "17 Morelos": "Morelos",
    "18 Nayarit": "Nayarit",
    "19 Nuevo León": "Nuevo León",
    "20 Oaxaca": "Oaxaca",
    "21 Puebla": "Puebla",
    "22 Querétaro": "Querétaro",
    "23 Quintana Roo": "Quintana Roo",
    "24 San Luis Potosí": "San Luis Potosí",
    "25 Sinaloa": "Sinaloa",
    "26 Sonora": "Sonora",
    "27 Tabasco": "Tabasco",
    "28 Tamaulipas": "Tamaulipas",
    "29 Tlaxcala": "Tlaxcala",
    "30 Veracruz de Ignacio de la Llave": "Veracruz",
    "31 Yucatán": "Yucatán",
    "32 Zacatecas": "Zacatecas",
}

REGIONES = {
    "Aguascalientes": "Centro", "Baja California": "Norte",
    "Baja California Sur": "Norte", "Campeche": "Sur",
    "Coahuila": "Norte", "Colima": "Centro", "Chiapas": "Sur",
    "Chihuahua": "Norte", "CDMX": "CDMX", "Durango": "Norte",
    "Guanajuato": "Centro", "Guerrero": "Sur", "Hidalgo": "Centro",
    "Jalisco": "Centro", "Estado de México": "Centro",
    "Michoacán": "Centro", "Morelos": "Centro", "Nayarit": "Norte",
    "Nuevo León": "Norte", "Oaxaca": "Sur", "Puebla": "Centro",
    "Querétaro": "Centro", "Quintana Roo": "Sur",
    "San Luis Potosí": "Norte", "Sinaloa": "Norte", "Sonora": "Norte",
    "Tabasco": "Sur", "Tamaulipas": "Norte", "Tlaxcala": "Centro",
    "Veracruz": "Sur", "Yucatán": "Sur", "Zacatecas": "Norte",
}


def extraer_valores_estado(filepath, sheet, col_indices, col_names,
                           sexo_col=1, estimador_col=2, data_start_row=9,
                           extra_filter_col=None, extra_filter_val="Total"):
    """
    Extrae valores por entidad federativa de un tabulado del Censo 2020.

    Parameters
    ----------
    filepath : str — ruta al .xlsx
    sheet : str — nombre de la hoja (ej: '02', '04')
    col_indices : list[int] — índices (0-based) de las columnas de datos a extraer
    col_names : list[str] — nombres para esas columnas
    sexo_col : int | None — índice de la columna con Sexo (None para ignorar)
    estimador_col : int — índice de la columna con tipo de estimador
    data_start_row : int — fila donde empiezan los datos (1-based)
    extra_filter_col : int | None — columna adicional para filtrar (ej: condición de habla)
    extra_filter_val : str — valor requerido en extra_filter_col

    Returns
    -------
    pd.DataFrame con columnas: estado, region, + col_names
    """
    wb = openpyxl.load_workbook(filepath, read_only=True)
    ws = wb[sheet]

    records = []
    for row in ws.iter_rows(min_row=data_start_row, values_only=True):
        entity = str(row[0]).strip() if row[0] else ""
        sexo = str(row[sexo_col]).strip() if sexo_col is not None and row[sexo_col] else "Total"
        estimador = str(row[estimador_col]).strip() if row[estimador_col] else ""

        if entity not in ESTADOS_32 and entity != "Estados Unidos Mexicanos":
            continue
        if sexo != "Total" or estimador != "Valor":
            continue
        if extra_filter_col is not None:
            extra_val = str(row[extra_filter_col]).strip() if row[extra_filter_col] else ""
            if extra_val != extra_filter_val:
                continue

        estado = ESTADOS_CORTOS.get(entity, entity)
        vals = {}
        for ci, cn in zip(col_indices, col_names):
            try:
                vals[cn] = float(row[ci]) if row[ci] is not None else None
            except (ValueError, TypeError):
                vals[cn] = None
        vals["estado"] = estado
        records.append(vals)

    wb.close()
    df = pd.DataFrame(records)
    df["region"] = df["estado"].map(REGIONES)
    return df
