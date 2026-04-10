import streamlit as st
import requests

st.title("💱 Conversor de Divisas")

monedas = ["USD", "DOP", "EUR", "MXN"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):
    url = f"https://api.frankfurter.app/latest?from={base}&to={destino}"

    try:
        response = requests.get(url)
        data = response.json()

st.write(data)  # 👈 esto nos muestra lo que realmente llega

if "rates" in data:
    tasa = data["rates"][destino]
    resultado = monto * tasa
    st.success(f"Resultado: {resultado:.2f} {destino}")
else:
    st.error("La API no devolvió rates")

        st.success(f"Resultado: {resultado:.2f} {destino}")

    except Exception as e:
        st.error("Error al convertir moneda")
        st.write(e)
