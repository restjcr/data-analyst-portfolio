import streamlit as st
import plotly.express as px
from utils.analyzer import DataAnalyzer

st.title("Análisis Exploratorio")

# Validamos existencia del dataframe
if "df" not in st.session_state:

    st.warning(
        "Primero debes cargar el dataset"
    )

    st.stop()

# Recuperamos dataset
df = st.session_state["df"]

# Objeto reutilizable para mostrar información básica del df
analyzer = DataAnalyzer(df)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
    ["1. Información general del dataset",
     "2. Clasificación de variables",
     "3. Estadisticas descriptivas",
     "4. Análisis de valores faltantes",
     "5. Distribución de variables numéricas",
     "6. Análisis de variables categóricas",
     "7. Análisis bivariado (numérico vs categórico)",
     "8. Análisis bivariado (categórico vs categórico)",
     "9. Análisis basado en parámetros seleccionados",
     "10. Hallazgos clave"])

with tab1:
    st.subheader("🟢info()")

    # Info
    info_text = analyzer.dataset_info()

    st.code(info_text)

    # Tipos de datos
    st.subheader("🟢Tipos de Datos")

    dtypes_df = analyzer.data_types().reset_index()

    dtypes_df.columns = [
        "Variable",
        "Tipo de Dato"
    ]

    dtypes_df = dtypes_df.astype(str)

    st.dataframe(
        dtypes_df.astype(str),
        width="stretch"
    )

    # Valores faltantes
    st.subheader("🟢Valores Faltantes")

    missing_df = analyzer.missing_values().reset_index()

    missing_df.columns = [
        "Variable",
        "Valores Nulos"
    ]

    st.dataframe(
        missing_df.astype(str),
        width="stretch"
    )

with tab2:
    
    st.subheader("🟢Identificación de variables")

    numeric_cols, categorical_cols = analyzer.classify_variables()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Variables Numéricas")

        st.write(numeric_cols)

        st.metric(
            "Cantidad",
            len(numeric_cols)
        )

    with col2:

        st.subheader("Variables Categóricas")

        st.write(categorical_cols)

        st.metric(
            "Cantidad",
            len(categorical_cols)
        )


with tab3:

    st.subheader("🟢 Estadísticas Descriptivas Numéricas")

    stats_numerical_df = analyzer.descriptive_stats_numerical()

    st.dataframe(
        stats_numerical_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("🟢 Estadísticas Descriptivas Categóricas")

    stats_categorical_df = analyzer.descriptive_stats_categorical()

    st.dataframe(
        stats_categorical_df,
        use_container_width=True
    )


with tab4:

    st.subheader("🟢 Valores Faltantes")

    missing_df = (
        analyzer
        .missing_values()
        .reset_index()
    )

    missing_df.columns = [
        "Variable",
        "Valores Faltantes"
    ]

    missing_df = missing_df[
        missing_df["Valores Faltantes"] > 0
    ]

    if missing_df.empty:
        st.success(
            "No se encontraron valores faltantes"
        )

    else:
        st.dataframe(
            missing_df.astype(str),
            width="stretch"
        )

with tab5:
    st.subheader("Distribución de variables numéricas")

    show_kde = st.checkbox("Mostrar curva KDE", value=True)

    numeric_cols, _ = analyzer.classify_variables()

    selected_col = st.selectbox(
        "Selecciona una variable numérica",
        numeric_cols
    )

    fig = analyzer.plot_histogram(
        selected_col,
        kde=show_kde
    )

    col1, col2 = st.columns([3,1])

    with col1:

        st.pyplot(fig)

    with col2:

        st.metric(
            "Media",
            round(df[selected_col].mean(), 2)
        )

        st.metric(
            "Mediana",
            round(df[selected_col].median(), 2)
        )

        st.metric(
            "Desv. Std",
            round(df[selected_col].std(), 2)
        )

with tab6:
    st.subheader("Análisis de variables categóricas")

    _, categorical_cols = analyzer.classify_variables()

    selected_cat = st.selectbox(
        "Selecciona variable categórica",
        categorical_cols
    )

    col1, col2 = st.columns([2,1])

    with col1:

        fig = analyzer.plot_categorical(
            selected_cat
        )

        st.pyplot(fig)

    with col2:

        st.markdown("### Conteos")

        counts_df = (
            analyzer
            .categorical_counts(selected_cat)
            .reset_index()
        )

        counts_df.columns = [
            "Categoría",
            "Cantidad"
        ]

        st.dataframe(
            counts_df.astype(str),
            width="stretch"
        )

        st.markdown("### Proporciones (%)")

        prop_df = (
            analyzer
            .categorical_proportions(selected_cat)
            .reset_index()
        )

        prop_df.columns = [
            "Categoría",
            "Porcentaje"
        ]

        st.dataframe(
            prop_df.astype(str),
            width="stretch"
        )

with tab7:
    st.subheader("Análisis bivariado (numérico vs categórico)")

    numeric_cols, categorical_cols = analyzer.classify_variables()

    col1, col2 = st.columns(2)

    with col1:
        selected_numeric = st.selectbox(
            "Variable numérica",
            numeric_cols,
            key="tab7_numeric"
        )

    with col2:
        selected_categorical = st.selectbox(
            "Variable categórica",
            categorical_cols,
            key="tab7_categorical"
        )

    fig = analyzer.plot_numeric_vs_categorical(
        selected_numeric,
        selected_categorical
    )
    
    st.pyplot(fig)

with tab8:
    st.subheader("Análisis bivariado (categórico vs categórico)")

    _, categorical_cols = analyzer.classify_variables()

    col1, col2 = st.columns(2)

    with col1:
        selected_categorical_1 = st.selectbox(
            "Variable categórica 1",
            categorical_cols,
            index=categorical_cols.index("Contract"),
            key="tab8_categorical_1"
        )

    with col2:
        selected_categorical_2 = st.selectbox(
            "Variable categórica 2",
            categorical_cols,
            index=categorical_cols.index("Churn"),
            key="tab8_categorical_2"
        )

    fig = analyzer.plot_categorical_vs_categorical(
        selected_categorical_1,
        selected_categorical_2
    )

    st.pyplot(fig)

    cross_df = (
        analyzer
        .categorical_vs_categorical_percentage(
            selected_categorical_1,
            selected_categorical_2
        )
    )

    st.dataframe(
        cross_df.astype(str),
        width="stretch"
    )


# with tab9:

#     st.subheader("Análisis basado en parámetros seleccionados")

#     numeric_cols, categorical_cols = (
#         analyzer.classify_variables()
#     )

#     selected_numeric = st.selectbox(
#         "Selecciona variable numérica",
#         numeric_cols,
#         key = "numeric_boxplot"
#     )

#     selected_categorical = st.selectbox(
#         "Selecciona variable categórica",
#         categorical_cols,
#         key="categorical_boxplot"

#     )

#     st.subheader(
#         "Distribución Numérica"
#     )

#     fig_hist = analyzer.plot_histogram(
#         selected_numeric
#     )

#     st.pyplot(fig_hist)


#     st.subheader(
#         "Análisis Bivariado"
#     )

#     fig_box = analyzer.plot_numeric_vs_categorical(
#         selected_numeric,
#         selected_categorical
#     )

#     st.pyplot(fig_box)

#     counts_df = (
#         analyzer
#         .categorical_counts(
#             selected_categorical
#         )
#         .reset_index()
#     )

#     counts_df.columns = [
#         "Categoría",
#         "Cantidad"
#     ]

#     st.dataframe(
#         counts_df.astype(str),
#         width="stretch"
#     )

#     selected_categories = st.multiselect(
#         "Selecciona variables categóricas",
#         categorical_cols,
#         default=["Contract", "InternetService"]
#     )

#     for cat_col in selected_categories:

#         st.markdown(f"## {cat_col}")

#         fig = analyzer.plot_categorical_vs_categorical(
#             cat_col,
#             "Churn"
#         )

#         st.pyplot(fig)

with tab9:
    st.subheader("Análisis basado en parámetros seleccionados")

    numeric_cols, categorical_cols = analyzer.classify_variables()

    col1, col2 = st.columns(2)

    with col1:
        selected_numeric = st.selectbox(
            "Selecciona variable numérica",
            numeric_cols,
            key="numeric_boxplot"
        )

    with col2:
        selected_categorical = st.selectbox(
            "Selecciona variable categórica",
            categorical_cols,
            key="categorical_boxplot"
        )

    # Histograma interactivo
    st.subheader("Distribución Numérica")

    show_kde = st.checkbox("Mostrar violin marginal", value=False, key="kde_tab9")

    fig_hist = analyzer.plot_histogram_plotly(
        selected_numeric,
        kde=show_kde
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Boxplot bivariado interactivo
    st.subheader("Análisis Bivariado")

    fig_box = analyzer.plot_numeric_vs_categorical_plotly(
        selected_numeric,
        selected_categorical
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Tabla de conteos
    counts_df = (
        analyzer
        .categorical_counts(selected_categorical)
        .reset_index()
    )
    counts_df.columns = ["Categoría", "Cantidad"]
    st.dataframe(counts_df.astype(str), width="stretch")

    # Barras agrupadas vs Churn por múltiples categóricas
    st.subheader("Comparación vs Churn")

    selected_categories = st.multiselect(
        "Selecciona variables categóricas",
        categorical_cols,
        default=["Contract", "InternetService"]
    )

    for cat_col in selected_categories:
        fig = analyzer.plot_categorical_vs_categorical_plotly(
            cat_col,
            "Churn"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab10:
    st.subheader("Insights")
    st.markdown("Variables con mayor influencia en la fuga de clientes (Churn)")

    # --- Hallazgo 1: Contract ---
    st.markdown("### 1. Tipo de Contrato")
    fig1 = analyzer.plot_categorical_vs_categorical_plotly("Contract", "Churn")
    st.plotly_chart(fig1, use_container_width=True, key="tab10_insight_1")
    st.info("💡 **Hallazgo 1:** ...")

    # --- Hallazgo 2: tenure ---
    st.markdown("### 2. Tiempo de Permanencia")
    fig2 = px.histogram(
        df,
        x="tenure",
        color="Churn",
        barmode="overlay",
        opacity=0.7,
        title="Distribución de tenure por Churn",
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True, key="tab10_insight_2")
    st.info("💡 **Hallazgo 2:** ...")

    # --- Hallazgo 3: MonthlyCharges ---
    st.markdown("### 3. Cargo Mensual")
    fig3 = px.box(
        df,
        x="Churn",
        y="MonthlyCharges",
        color="Churn",
        title="MonthlyCharges por Churn",
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True, key="tab10_insight_3")
    st.info("💡 **Hallazgo 3:** ...")

    # --- Hallazgo 4: InternetService ---
    st.markdown("### 4. Tipo de Servicio de Internet")
    fig4 = analyzer.plot_categorical_vs_categorical_plotly("InternetService", "Churn")
    st.plotly_chart(fig4, use_container_width=True, key="tab10_insight_4")
    st.info("💡 **Hallazgo 4:** ...")

    # --- Hallazgo 5: TechSupport ---
    st.markdown("### 5. Soporte Técnico")
    fig5 = analyzer.plot_categorical_vs_categorical_plotly("TechSupport", "Churn")
    st.plotly_chart(fig5, use_container_width=True, key="tab10_insight_5")
    st.info("💡 **Hallazgo 5:** ...")