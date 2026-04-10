import streamlit as st
import requests

st.title("💱 Conversor de Divisas")

monedas = ["USD", "DOP", "EUR", "MXN"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):
    url = f"https://api.exchangerate.host/convert?from={base}&to={destino}&amount={monto}"

    try:
        response = requests.get(url)
        data = response.json()

        resultado = data["result"]

        st.success(f"Resultado: {resultado:.2f} {destino}")

    except Exception as e:
        st.error("Error al convertir moneda")
        st.write(e)
