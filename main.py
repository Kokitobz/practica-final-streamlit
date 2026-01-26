import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import streamlit as st
import gdown
import os


# Comentario para probar git

FILE_ID = "1I--5yCp9dw0iYpZuGMyMNM6pYnpQac-5"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT = "ventas.csv"

@st.cache_data
def load_data():
    if not os.path.exists(OUTPUT):
        gdown.download(URL, OUTPUT, quiet=False)
    df = pd.read_csv(OUTPUT, parse_dates=["date"])
    return df

df = load_data()

st.info(
    """
    ℹ️ **Aviso sobre el conjunto de datos utilizado**

    Para garantizar un correcto rendimiento y estabilidad de la aplicación en Streamlit Cloud,
    el análisis se ha realizado utilizando **un único fichero CSV** del conjunto de datos disponible.

    El uso simultáneo de ambos ficheros provoca problemas de memoria y tiempos de carga excesivos 
    en el entorno de despliegue.

    Los resultados mostrados son representativos del comportamiento general de las ventas, aunque
    pueden diferir ligeramente de los valores exactos que se obtendrían utilizando el dataset completo.
    """
)



st.title("Visión Global de las Ventas")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visión Global",
    "🏬 Análisis por tienda",
    "🗺️ Análisis por estado",
    "🚀 Extra para Dirección"
])


with tab1:
    col1, col2, col3, col4 = st.columns(4)

    total_tiendas = df["store_nbr"].nunique()
    total_productos = df["family"].nunique()
    total_estados = df["state"].nunique()
    total_meses = df[["year", "month"]].drop_duplicates().shape[0]

    col1.metric("🏬 Tiendas", total_tiendas)
    col2.metric("📦 Productos", total_productos)
    col3.metric("🗺️ Estados", total_estados)
    col4.metric("📆 Meses con datos", total_meses)

    top_productos = (
        df.groupby("family")["sales"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top 10 productos más vendidos (media)")
    st.bar_chart(top_productos)

    ventas_tienda = df.groupby("store_nbr")["sales"].mean()

    st.subheader("Distribución media de ventas por tienda")
    fig, ax = plt.subplots()
    ax.boxplot(ventas_tienda)
    ax.set_ylabel("Ventas medias")
    st.pyplot(fig)

    promo_df = df[df["onpromotion"] > 0]

    top_tiendas_promo = (
        promo_df.groupby("store_nbr")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top 10 tiendas con más ventas en promoción")
    st.bar_chart(top_tiendas_promo)

    ventas_dia = (
        df.groupby("day_of_week")["sales"]
        .mean()
        .sort_values(ascending=False)
    )

    st.subheader("Ventas medias por día de la semana")
    st.bar_chart(ventas_dia)

    ventas_semana = (
        df.groupby("week")["sales"]
        .mean()
    )

    st.subheader("Ventas medias por semana del año")
    st.line_chart(ventas_semana)

    ventas_mes = (
        df.groupby("month")["sales"]
        .mean()
    )

    st.subheader("Ventas medias por mes")
    st.line_chart(ventas_mes)

with tab2:

    st.title("Análisis por tienda")

    store_selected = st.selectbox(
        "Selecciona una tienda",
        sorted(df["store_nbr"].unique())
    )

    df_store = df[df["store_nbr"] == store_selected]

    ventas_anuales = (
        df_store
        .groupby("year")["sales"]
        .sum()
        .sort_index()
    )

    st.subheader("Ventas totales por año")
    st.line_chart(ventas_anuales)

    total_productos = df_store["sales"].sum()

    st.metric(
        "Total de productos vendidos",
        f"{int(total_productos):,}".replace(",", ".")
    )

    productos_promo = df_store[df_store["onpromotion"] > 0]["sales"].sum()

    st.metric(
        "Productos vendidos en promoción",
        f"{int(productos_promo):,}".replace(",", ".")
    )

with tab3:

    st.title("Análisis por estado")

    state_selected = st.selectbox(
        "Selecciona un estado",
        sorted(df["state"].dropna().unique())
    )

    df_state = df[df["state"] == state_selected]

    transacciones_anuales = (
        df_state
        .groupby("year")["transactions"]
        .sum()
        .sort_index()
    )

    st.subheader("Transacciones totales por año")
    st.line_chart(transacciones_anuales)

    ranking_tiendas = (
        df_state
        .groupby("store_nbr")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top 10 tiendas con más ventas en el estado")
    st.bar_chart(ranking_tiendas)

    producto_top = (
        df_state
        .groupby("family")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    producto_nombre = producto_top.index[0]
    producto_ventas = producto_top.iloc[0]

    st.metric(
        "Producto más vendido en el estado",
        producto_nombre,
        f"{int(producto_ventas):,}".replace(",", ".")
    )

with tab4:
    st.title("Gráficos estratégicos de ventas")
    ventas_promo = df.copy()
    ventas_promo["promo"] = ventas_promo["onpromotion"] > 0

    ventas_totales = (
        ventas_promo
        .groupby("promo")["sales"]
        .sum()
    )

    ventas_totales.index = ["Sin promoción", "Con promoción"]

    st.subheader("Peso de las promociones en las ventas totales")
    st.bar_chart(ventas_totales)


    top_estados = (
        df.groupby("state")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader("Estados con mayor volumen de ventas")
    st.bar_chart(top_estados)

    df["promo"] = df["onpromotion"] > 0

    ventas_mes_promo = (
        df.groupby(["month", "promo"])["sales"]
        .mean()
        .unstack()
    )

    ventas_mes_promo.columns = ["Sin promoción", "Con promoción"]

    st.subheader("Estacionalidad de ventas y promociones")
    st.line_chart(ventas_mes_promo)

