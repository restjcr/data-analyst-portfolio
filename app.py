import streamlit as st

# Configuración inicial del front
st.set_page_config(
    page_title="Telco Customer Churn",
    layout="wide"
)

# Definimos las páginas
home        =   st.Page("pages/0_home.py", title="Home", icon="🏠")
upload      =   st.Page("pages/1_upload.py", title="Load Dataset", icon="⬆️")
eda         =   st.Page("pages/2_eda.py", title="EDA", icon="📊")

# Creamos la navegación
pg = st.navigation(
    {
        "Menu":[home, upload, eda]
    }
)

# Ejecutamos página seleccionada
pg.run()

    
st.sidebar.markdown(
    """
    <div style='
        position: fixed;
        bottom: 1rem;
        text-align: center;
        color: gray;
        font-size: 0.8em;
    '>© 2026 JCCR</div>
    """,
    unsafe_allow_html=True
)