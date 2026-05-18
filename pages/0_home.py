import streamlit as st

# --- Hero ---
st.title("📉 Customer Churn")
st.subheader("Análisis Exploratorio de Datos")

st.markdown("""
Este proyecto tiene como objetivo analizar el comportamiento de los clientes 
de una empresa de telecomunicaciones para identificar patrones asociados a la 
**fuga de clientes (Churn)**, utilizando un enfoque exploratorio y visual.
""")

st.divider()

# --- Datos del autor ---
st.markdown("### 👤 Autor")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nombre", "José Cuentas Ramirez")

with col2:
    st.metric("Especialización", "Python for Analytics")

with col3:
    st.metric("Año", "2026")

st.divider()

# --- Descripción del dataset ---
st.markdown("### 📁 Sobre el Dataset")

st.markdown("""
El dataset **TelcoCustomerChurn.csv** contiene información sobre los clientes 
de una empresa de telecomunicaciones, incluyendo sus servicios contratados, 
facturación mensual, tiempo de permanencia y si abandonaron la empresa o no.

Durante el último periodo, la empresa registró un incremento en su tasa de fuga 
de **+0.5 puntos porcentuales**, pasando de 2% a 2.5%, contexto agravado por 
la coyuntura del COVID-19.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Filas iniciales", "7,043 clientes")

with col2:
    st.metric("Columnas iniciales", "21 variables")

with col3:
    st.metric("Variable objetivo", "Churn")

st.divider()

# --- Tecnologías ---
st.markdown("### 🛠️ Tecnologías Utilizadas")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.info("🐍 Python")

with col2:
    st.info("🐼 Pandas")

with col3:
    st.info("🌐 Streamlit")

with col4:
    st.info("📈 Plotly")

with col5:
    st.info("🎨 Seaborn")

with col6:
    st.info("📉 Matplotlib")