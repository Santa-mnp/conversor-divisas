import streamlit as st

st.title("💱 Conversor de Divisas (modo simple)")

tasas = {
    "USD": {"DOP": 58.5, "EUR": 0.92, "MXN": 17.0},
    "DOP": {"USD": 0.017, "EUR": 0.016, "MXN": 0.29},
    "EUR": {"USD": 1.09, "DOP": 63.5, "MXN": 18.5},
    "MXN": {"USD": 0.059, "DOP": 3.4, "EUR": 0.054}
}

monedas = ["USD", "DOP", "EUR", "MXN"]

base = st.selectbox("Moneda base", monedas)
destino = st.selectbox("Moneda destino", monedas)
monto = st.number_input("Monto", min_value=0.0, value=1.0)

if st.button("Convertir"):
    if base == destino:
        resultado = monto
    else:
        resultado = monto * tasas[base][destino]

    st.success(f"Resultado: {resultado:.2f} {destino}")
