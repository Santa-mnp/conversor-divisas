import streamlit as st
import requests

API_KEY = "78897b05d7-5f5121bb62-td95qf"

st.title("💱 Conversor de Divisas")

monedas = ["USD", "DOP", "EUR", "MXN"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"

    response = requests.get(url)
    data = response.json()

    tasa = data["conversion_rates"][destino]
    resultado = monto * tasa

    st.success(f"Resultado: {resultado:.2f} {destino}")
