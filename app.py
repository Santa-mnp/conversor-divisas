import streamlit as st
import requests

st.title("💱 Conversor de Divisas")

monedas = ["USD", "EUR", "DOP"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):

    url = f"https://api.exchangerate.host/convert?from={base}&to={destino}&amount={monto}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        resultado = data.get("result")

        if resultado is not None:
            st.success(f"Resultado: {resultado:.2f} {destino}")
        else:
            st.error("No se pudo obtener la conversión. Intenta de nuevo.")

    except Exception:
        st.error("Error de conexión con la API")
