import streamlit as st
import requests

st.title("💱 Conversor de Divisas")

monedas = ["USD", "EUR", "DOP"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):

    url = f"https://api.frankfurter.app/latest?from={base}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        rates = data.get("rates", {})

        if destino in rates:
            tasa = rates[destino]
            resultado = monto * tasa

            st.success("Conversión exitosa ✅")
            st.metric("Resultado", f"{resultado:.2f} {destino}")
        else:
            st.error("Moneda no disponible en la API")

    except Exception as e:
        st.error("Error conectando con la API")
