"""Dashboard Streamlit com as 3 views do PostgreSQL."""
import pandas as pd
import plotly.express as px
import streamlit as st
from db import get_engine

st.set_page_config(page_title="Dashboard IoT", layout="wide")
engine = get_engine()


@st.cache_data(ttl=300)
def load_data(view_name: str) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


st.title("Dashboard de Temperaturas IoT")

# Gráfico 1: média por dispositivo/local
st.header("Média de Temperatura por Dispositivo")
df1 = load_data("avg_temp_por_dispositivo")
st.plotly_chart(px.bar(df1, x="device_id", y="avg_temp", color="location",
                       barmode="group", text="avg_temp"),
                use_container_width=True)

# Gráfico 2: leituras por hora
st.header("Leituras por Hora do Dia")
df2 = load_data("leituras_por_hora")
st.plotly_chart(px.line(df2, x="hora", y="contagem", markers=True),
                use_container_width=True)

# Gráfico 3: máximas e mínimas por dia
st.header("Temperaturas Máximas e Mínimas por Dia")
df3 = load_data("temp_max_min_por_dia")
st.plotly_chart(px.line(df3, x="data", y=["temp_max", "temp_min"]),
                use_container_width=True)

with st.expander("Ver dados brutos das views"):
    st.dataframe(df3)
