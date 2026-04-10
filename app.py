import streamlit as st
import requests

st.title("💱 Conversor de Divisas")

monedas = ["USD", "EUR", "DOP"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):

    url = "https://open.er-api.com/v6/latest/" + base

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data["result"] == "success":
            tasa = data["rates"][destino]
            resultado = monto * tasa

            st.success(f"Resultado: {resultado:,.2f} {destino}")
        else:
            st.error("Error en la API")

    except:
        st.error("Error de conexión")
