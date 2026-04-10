import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Banco FX", page_icon="🏦", layout="wide")

# 🎨 ESTILO BANCO (CSS simple)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1 {
        color: #0b3d91;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Banco FX | Conversor de Divisas")

monedas = ["USD", "EUR", "DOP"]

banderas = {
    "USD": "🇺🇸 USD",
    "EUR": "🇪🇺 EUR",
    "DOP": "🇩🇴 DOP"
}

if "historial" not in st.session_state:
    st.session_state.historial = []

col1, col2 = st.columns(2)

with col1:
    base = st.selectbox("Moneda base", monedas, format_func=lambda x: banderas[x])

with col2:
    destino = st.selectbox("Moneda destino", monedas, format_func=lambda x: banderas[x])

monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):

    url = f"https://open.er-api.com/v6/latest/{base}"
    data = requests.get(url).json()

    tasa = data["rates"][destino]
    resultado = monto * tasa

    # 🇩🇴 Hora RD sin pytz
    rd_time = datetime.utcnow() - timedelta(hours=4)
    fecha = rd_time.strftime("%Y-%m-%d %H:%M:%S")

    st.success(f"Resultado: {resultado:,.2f} {destino}")

    st.session_state.historial.append({
        "fecha": fecha,
        "base": base,
        "destino": destino,
        "monto": monto,
        "resultado": round(resultado, 2)
    })

# 📊 DASHBOARD
st.subheader("📊 Historial de operaciones")

df = pd.DataFrame(st.session_state.historial)

if not df.empty:

    # 🔎 FILTRO POR FECHA
    fecha_filtro = st.text_input("Filtrar por fecha (YYYY-MM-DD)")

    if fecha_filtro:
        df = df[df["fecha"].str.contains(fecha_filtro)]

    st.dataframe(df, use_container_width=True)

    # 📈 GRÁFICO
    st.line_chart(df["resultado"])

else:
    st.info("No hay transacciones aún")
