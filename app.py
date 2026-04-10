import streamlit as st
import requests

st.set_page_config(page_title="Conversor de Divisas", page_icon="💱")

st.title("💱 Conversor de Divisas PRO")

monedas = ["USD", "EUR", "DOP", "MXN"]

col1, col2 = st.columns(2)

with col1:
    base = st.selectbox("Moneda base", monedas)

with col2:
    destino = st.selectbox("Moneda destino", monedas)

monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):
    url = f"https://api.frankfurter.app/latest?from={base}"

    try:
        response = requests.get(url)
        data = response.json()

        if "rates" in data and destino in data["rates"]:
            tasa = data["rates"][destino]
            resultado = monto * tasa

            st.success("Conversión exitosa ✅")
            st.metric(label="Resultado", value=f"{resultado:.2f} {destino}")

        else:
            st.error("Moneda no disponible en la API")

    except requests.exceptions.RequestException:
        st.error("Error de conexión con la API")
