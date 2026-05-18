import streamlit as st
import pandas as pd

st.title("Carga del Dataset")

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

    st.dataframe(df.head())

    col1, col2 = st.columns(2)

    col1.metric("Filas", df.shape[0])
    col2.metric("Columnas", df.shape[1])

else:

    st.warning("Aún no se ha cargado dataset")