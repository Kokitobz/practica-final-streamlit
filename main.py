import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import streamlit as st
import gdown
import os



def load_data():
    FILE_ID_1 = "1I--5yCp9dw0iYpZuGMyMNM6pYnpQac-5"
    FILE_ID_2 = "1z2zRcWSP3RnKLGijY0w6FNOXxiUZSthf"

    url_1 = f"https://drive.google.com/uc?id={FILE_ID_1}"
    url_2 = f"https://drive.google.com/uc?id={FILE_ID_2}"

    file_1 = "ventas_2013_2015.csv"
    file_2 = "ventas_2015_2018.csv"

    if not os.path.exists(file_1):
        gdown.download(url_1, file_1, quiet=False)

    if not os.path.exists(file_2):
        gdown.download(url_2, file_2, quiet=False)

    df1 = pd.read_csv(file_1, parse_dates=["date"])
    df2 = pd.read_csv(file_2, parse_dates=["date"])

    # Concatenación vertical
    df = pd.concat([df1, df2], ignore_index=True)

    return df

df = load_data()

st.title("📊 Visión Global de las Ventas")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visión Global",
    "🏬 Análisis por tienda",
    "🗺️ Análisis por estado",
    "🚀 Insights para Dirección"
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

    st.subheader("🔝 Top 10 productos más vendidos (media)")
    st.bar_chart(top_productos)

    ventas_tienda = df.groupby("store_nbr")["sales"].mean()

    st.subheader("🏬 Distribución media de ventas por tienda")
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

    st.subheader("🔥 Top 10 tiendas con más ventas en promoción")
    st.bar_chart(top_tiendas_promo)

    ventas_dia = (
        df.groupby("day_of_week")["sales"]
        .mean()
        .sort_values(ascending=False)
    )

    st.subheader("📅 Ventas medias por día de la semana")
    st.bar_chart(ventas_dia)

    ventas_semana = (
        df.groupby("week")["sales"]
        .mean()
    )

    st.subheader("📈 Ventas medias por semana del año")
    st.line_chart(ventas_semana)

    ventas_mes = (
        df.groupby("month")["sales"]
        .mean()
    )

    st.subheader("📆 Ventas medias por mes")
    st.line_chart(ventas_mes)

with tab2:

    st.title("🏬 Análisis por tienda")

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

    st.subheader("📈 Ventas totales por año")
    st.line_chart(ventas_anuales)

    total_productos = df_store["sales"].sum()

    st.metric(
        "📦 Total de productos vendidos",
        f"{int(total_productos):,}".replace(",", ".")
    )

    productos_promo = df_store[df_store["onpromotion"] > 0]["sales"].sum()

    st.metric(
        "🔥 Productos vendidos en promoción",
        f"{int(productos_promo):,}".replace(",", ".")
    )

with tab3:

    st.title("🗺️ Análisis por estado")

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

    st.subheader("📈 Transacciones totales por año")
    st.line_chart(transacciones_anuales)

    ranking_tiendas = (
        df_state
        .groupby("store_nbr")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("🏆 Top 10 tiendas con más ventas en el estado")
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
        "📦 Producto más vendido en el estado",
        producto_nombre,
        f"{int(producto_ventas):,}".replace(",", ".")
    )

with tab4:
    st.title("🚀 Insights estratégicos de ventas")
    promo_effect = (
        df.assign(promo=lambda x: x["onpromotion"] > 0)
        .groupby("promo")["sales"]
        .mean()
    )

    promo_effect.index = ["Sin promoción", "Con promoción"]

    st.subheader("🎯 Impacto medio de las promociones")
    st.bar_chart(promo_effect)

    top_estados = (
        df.groupby("state")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader("🗺️ Estados con mayor volumen de ventas")
    st.bar_chart(top_estados)

    top_productos = (
        df.groupby("family")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.subheader("🏆 Familias de productos más rentables")
    st.bar_chart(top_productos)

    df["promo"] = df["onpromotion"] > 0

    ventas_mes_promo = (
        df.groupby(["month", "promo"])["sales"]
        .mean()
        .unstack()
    )

    ventas_mes_promo.columns = ["Sin promoción", "Con promoción"]

    st.subheader("📆 Estacionalidad de ventas y promociones")
    st.line_chart(ventas_mes_promo)

