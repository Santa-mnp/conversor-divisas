import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# ------------------ CONFIG ------------------
st.set_page_config(page_title="FinBank FX", page_icon="🏦", layout="wide")

# ------------------ LOGIN SIMULADO ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🏦 FinBank Login")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == "santa" and password == "finbank2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
    st.stop()

# ------------------ ESTILO FINTECH CLARO ------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
h1, h2, h3 {
    color: #0b2e63;
}
</style>
""", unsafe_allow_html=True)

st.title("🏦 FinBank FX Dashboard")

# ------------------ MONEDAS ------------------
monedas = ["USD", "EUR", "DOP"]

banderas = {
    "USD": "🇺🇸 USD",
    "EUR": "🇪🇺 EUR",
    "DOP": "🇩🇴 DOP"
}

# ------------------ HISTORIAL ------------------
if "historial" not in st.session_state:
    st.session_state.historial = []

# ------------------ TARJETAS DASHBOARD ------------------
col1, col2, col3 = st.columns(3)

col1.metric("Clientes", "1,254")
col2.metric("Operaciones", len(st.session_state.historial))
col3.metric("API Status", "Activo 🟢")

st.divider()

# ------------------ INPUTS ------------------
colA, colB = st.columns(2)

with colA:
    base = st.selectbox("Moneda base", monedas, format_func=lambda x: banderas[x])

with colB:
    destino = st.selectbox("Moneda destino", monedas, format_func=lambda x: banderas[x])

monto = st.number_input("Monto", min_value=0.0, value=1.0)

# ------------------ CONVERSIÓN ------------------
if st.button("Convertir"):

    url = f"https://open.er-api.com/v6/latest/{base}"
    data = requests.get(url).json()

    tasa = data["rates"][destino]
    resultado = monto * tasa

    fecha = (datetime.utcnow() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")

    # FORMATO BANCO (con coma)
    resultado_fmt = f"{resultado:,.2f}"

    st.success(f"Resultado: {resultado_fmt} {destino}")

    st.session_state.historial.append({
        "fecha": fecha,
        "base": base,
        "destino": destino,
        "monto": f"{monto:,.2f}",
        "resultado": resultado_fmt,
        "resultado_num": resultado
    })

# ------------------ HISTORIAL ------------------
st.subheader("📜 Historial de operaciones")

df = pd.DataFrame(st.session_state.historial)

if not df.empty:

    # filtro fecha
    filtro = st.text_input("Filtrar por fecha (YYYY-MM-DD)")
    if filtro:
        df = df[df["fecha"].str.contains(filtro)]

    st.dataframe(df.drop(columns=["resultado_num"]), use_container_width=True)

    # ------------------ GRÁFICOS ------------------
    st.subheader("📊 Evolución por moneda")

    df_usd = df[df["base"] == "USD"]
    df_eur = df[df["base"] == "EUR"]

    col1, col2 = st.columns(2)

    with col1:
        st.write("USD → conversiones")
        if not df_usd.empty:
            st.line_chart(df_usd["resultado_num"])

    with col2:
        st.write("EUR → conversiones")
        if not df_eur.empty:
            st.line_chart(df_eur["resultado_num"])

    # ------------------ EXCEL ------------------
    excel = df.drop(columns=["resultado_num"]).to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Descargar Excel",
        excel,
        "finbank_historial.csv",
        "text/csv"
    )

else:
    st.info("No hay transacciones aún")
