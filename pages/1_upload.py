import streamlit as st
import pandas as pd

st.title("⬆️ Carga del Dataset")

uploaded_file = st.file_uploader(
    "Sube el CSV",
    type=["csv"]
)

# Si sube archivo nuevo
if uploaded_file is not None:

    df = pd.read_csv(
        uploaded_file
    )

    # Transformación del campo SeniorCitizen
    df["SeniorCitizen"] = df["SeniorCitizen"].map({
        0: "No",
        1: "Yes"
    })

    # Drop Customer ID
    df = df.drop(columns=['customerID'])

    # Casting Total Charges
    df["TotalCharges"] = (df["TotalCharges"].replace(" ", pd.NA))
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges"])

    st.session_state["df"] = df

    st.success("Dataset cargado correctamente")

# Si ya existe dataset en sesión
if "df" in st.session_state:

    df = st.session_state["df"]
    
    st.subheader("Acciones realizadas: ")

    st.markdown("""
    <div style='display: flex; gap: 1rem; margin: 1rem 0;'>
        <div style='flex: 1; background-color: #d4edda; border-left: 4px solid #28a745; border-radius: 8px; padding: 0.8rem 1rem;'>
            🧹 <b>Limpieza de registros</b><br>
            <span style='font-size: 0.9em; color: #333;'>Se eliminaron 11 filas con valores nulos en <b>TotalCharges</b></span>
        </div>
        <div style='flex: 1; background-color: #d4edda; border-left: 4px solid #28a745; border-radius: 8px; padding: 0.8rem 1rem;'>
            🗑️ <b>Columna descartada</b><br>
            <span style='font-size: 0.9em; color: #333;'>Se eliminó <b>customerID</b> por no aportar valor analítico</span>
        </div>
        <div style='flex: 1; background-color: #d4edda; border-left: 4px solid #28a745; border-radius: 8px; padding: 0.8rem 1rem;'>
            🔄 <b>Transformación de variable</b><br>
            <span style='font-size: 0.9em; color: #333;'><b>SeniorCitizen</b> convertida de 0/1 a No/Yes para mayor claridad</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Muestra del dataset resultante: ")

    st.dataframe(df.head(10))

    col1, col2, col3 = st.columns(3)

    col1.metric("📋 Filas", df.shape[0])
    col2.metric("📊 Columnas", df.shape[1])
    col3.metric("🎯 Variable Objetivo", "Churn")

else:

    st.warning("Aún no se ha cargado dataset")