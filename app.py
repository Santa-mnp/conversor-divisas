import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Conversor PRO", page_icon="💱", layout="centered")

st.title("💱 Conversor de Divisas PRO")

# 🏳️ Banderas (visual pro)
banderas = {
    "USD": "🇺🇸 USD",
    "EUR": "🇪🇺 EUR",
    "DOP": "🇩🇴 DOP"
}

monedas = list(banderas.keys())

# 📊 historial en sesión
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

    try:
        response = requests.get(url)
        data = response.json()

        tasa = data["rates"][destino]
        resultado = monto * tasa

        st.success(f"Resultado: {resultado:,.2f} {destino}")

        # 🧾 guardar historial
        st.session_state.historial.append({
    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "base": base,
    "destino": destino,
    "monto": monto,
    "resultado": f"{resultado:,.2f}"
})

    except:
        st.error("Error en la conversión")

# 📜 HISTORIAL
st.subheader("📜 Historial de conversiones")

if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df, use_container_width=True)

    # 📈 gráfico simple
    st.subheader("📈 Evolución de conversiones")
    st.line_chart(df["resultado"])
else:
    st.info("Aún no hay conversiones")
