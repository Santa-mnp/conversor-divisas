import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="FinFX Converter", page_icon="💱", layout="wide")

st.title("💱 FinFX Converter | PRO")

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

    response = requests.get(url)
    data = response.json()

    tasa = data["rates"][destino]
    resultado = monto * tasa

    # 🇩🇴 hora RD
    tz = pytz.timezone("America/Santo_Domingo")
    hora_rd = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    st.success(f"Resultado: {resultado:,.2f} {destino}")

    st.session_state.historial.append({
        "fecha (RD)": hora_rd,
        "base": base,
        "destino": destino,
        "monto": monto,
        "resultado": f"{resultado:,.2f}"
    })

# 📜 HISTORIAL
st.subheader("📜 Historial de conversiones")

df = pd.DataFrame(st.session_state.historial)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # 📥 DESCARGA EXCEL
    excel = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar historial", excel, "historial.csv", "text/csv")

    # 📊 GRÁFICO
    df["resultado_num"] = df["resultado"].str.replace(",", "").astype(float)
    st.subheader("📊 Evolución de conversiones")
    st.line_chart(df["resultado_num"])
else:
    st.info("No hay conversiones aún")
