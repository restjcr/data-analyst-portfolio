import streamlit as st
import plotly.express as px
from utils.analyzer import DataAnalyzer

st.title("📊 Análisis Exploratorio")

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
    st.subheader("🟢 Distribución de variables numéricas")

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
    st.subheader("🟢 Análisis de variables categóricas")

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
    st.subheader("🟢 Análisis bivariado (numérico vs categórico)")

    numeric_cols, _ = analyzer.classify_variables()

    # col1, col2 = st.columns(2)

    # with col1:
    #     selected_numeric = st.selectbox(
    #         "Variable numérica",
    #         numeric_cols,
    #         key="tab7_numeric"
    #     )

    # with col2:
    #     selected_categorical = st.selectbox(
    #         "Variable categórica",
    #         categorical_cols,
    #         key="tab7_categorical"
    #     )

    selected_numeric = st.selectbox(
        "Variable numérica",
        numeric_cols,
        key="tab7_numeric"
    )

    selected_categorical = "Churn"


    fig = analyzer.plot_numeric_vs_categorical(
        selected_numeric,
        selected_categorical
    )
    
    st.pyplot(fig)

with tab8:
    st.subheader("🟢 Análisis bivariado (categórico vs categórico)")

    _, categorical_cols = analyzer.classify_variables()

    # col1, col2 = st.columns(2)

    # with col1:
    #     selected_categorical_1 = st.selectbox(
    #         "Variable categórica 1",
    #         categorical_cols,
    #         index=categorical_cols.index("Contract"),
    #         key="tab8_categorical_1"
    #     )

    # with col2:
    #     selected_categorical_2 = st.selectbox(
    #         "Variable categórica 2",
    #         categorical_cols,
    #         index=categorical_cols.index("Churn"),
    #         key="tab8_categorical_2"
    #     )

    selected_categorical_1 = st.selectbox(
        "Variable categórica",
        categorical_cols,
        index=categorical_cols.index("Contract"),
        key="tab8_categorical_1"
    )

    selected_categorical_2 = "Churn"  

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
    st.subheader("🟢 Análisis basado en parámetros seleccionados")

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
    st.subheader("🟢 Insights")
    st.markdown("Variables con mayor influencia en la fuga de clientes (Churn)")

    # # --- Hallazgo 1: Contract ---
    # st.markdown("### 1. Tipo de Contrato")
    # fig1 = analyzer.plot_categorical_vs_categorical_plotly("Contract", "Churn")
    # st.plotly_chart(fig1, use_container_width=True, key="tab10_insight_1")
    # st.info("💡 **Hallazgo 1:** ...")

    st.markdown("### 1. Tipo de Contrato")

    churn_contract = (
        df.groupby("Contract")["Churn"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index(name="Porcentaje")
    )

    fig1 = px.bar(
        churn_contract,
        x="Porcentaje",
        y="Contract",
        color="Churn",
        barmode="group",
        orientation="h",
        text="Porcentaje",
        title="Tasa de Churn (%) por Tipo de Contrato",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={
            "Contract": ["Month-to-month", "One year", "Two year"]
        }        
    )

    fig1.update_traces(texttemplate="%{text}%", textposition="outside")

    st.plotly_chart(fig1, use_container_width=True, key="tab10_insight_1")
    st.info("💡 **Hallazgo 1:** Los clientes con contrato mes a mes tienen un churn de (42.7%) respecto al total de la base de esta categoría. " \
    "Se distancia notablemente de los ratios de churn de los contratos de un año (11.3%) y más aún de los de dos años (2.8%). Esto puede estar asociado a " \
    "que los contratos de más de un mes pueden presentar descuentos, y que los clientes reconocen que abandonar este contrato les puede " \
    "hacer perder este beneficio en caso quieran volver a contratar el servicio.")

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
    st.info("💡 **Hallazgo 2:** Clientes con más antigüedad tienden a realizar menos solicitudes de cancelación respecto a los que recien inician en la " \
    "compañía. (380) clientes cancelaron el servicio en el primer mes de contrato. Resulta crucial realizar una auditoría sobre los asesores de venta y revisar principalmente " \
    "la calidad del ofrecimiento. Incluso, se pueden iniciar campañas de penalización monetaria para aquellas contratas que venden 'humo' o engañan al cliente.")

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
    st.info("💡 **Hallazgo 3:** Los clientes que fugaron de la empresa tienen una mayor mediana (79.65) del costo mensual respecto a los que no fugaron (64.45). Implica que es " \
    "muy probable que hayan contratado un paquete con agregados pero que finalmente no utilizaron mucho y ya no querían continuar pagando por algo que no van a utilizar. Ofrecer un " \
    "producto de acuerdo a las necesidades del cliente es crucial para evitar el early churn. Además se pueden hacer campañas proactivas para " \
    "realizar un downgrade plan más descuento y mantener al cliente con su servicio.")

    # --- Hallazgo 4: InternetService ---
    # st.markdown("### 4. Tipo de Servicio de Internet")
    # fig4 = analyzer.plot_categorical_vs_categorical_plotly("InternetService", "Churn")
    # st.plotly_chart(fig4, use_container_width=True, key="tab10_insight_4")
    # st.info("💡 **Hallazgo 4:** ...")
    # --- Hallazgo 4: InternetService ---

    st.markdown("### 4. Tipo de Servicio de Internet")

    internet_types = df["InternetService"].unique()

    cols = st.columns(len(internet_types))

    for i, service in enumerate(internet_types):
        with cols[i]:
            subset = df[df["InternetService"] == service]
            churn_counts = subset["Churn"].value_counts()

            fig = px.pie(
                values=churn_counts.values,
                names=churn_counts.index,
                title=f"{service}",
                hole=0.4,
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            st.plotly_chart(fig, use_container_width=True, key=f"tab10_pie_{service}")

    st.info("💡 **Hallazgo 4:** Los clientes con el tipo de tecnología fibra óptica tienen un churn por encima de los (41%), lo que está ligado puramente a que los clientes" \
    " pensaban que iban a tener más estabilidad y velocidad por un precio más alto pero que lamentablemente no cumplió lo esperado. Por otra parte la tecnología" \
    " DSL se ve más estable con un churn de (19%), lo que puede estar asociado también a la antigüedad de los clientes. Normalmente a los nuevos" \
    " se le ofrece la fibra óptica, pero ya vimos que el early churn en este caso de estudio es alto.")

    # --- Hallazgo 5: TechSupport ---
    # st.markdown("### 5. Soporte Técnico")
    # fig5 = analyzer.plot_categorical_vs_categorical_plotly("TechSupport", "Churn")
    # st.plotly_chart(fig5, use_container_width=True, key="tab10_insight_5")
    # st.info("💡 **Hallazgo 5:** ...")

    # --- Hallazgo 5: TechSupport ---
    st.markdown("### 5. Soporte Técnico")

    churn_rate = (
        df.groupby("TechSupport")["Churn"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index(name="Porcentaje")
    )

    fig5 = px.bar(
        churn_rate,
        x="TechSupport",
        y="Porcentaje",
        color="Churn",
        barmode="group",
        text="Porcentaje",
        title="Tasa de Churn (%) por Soporte Técnico",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig5.update_traces(texttemplate="%{text}%", textposition="outside")

    st.plotly_chart(fig5, use_container_width=True, key="tab10_insight_5")
    st.info("💡 **Hallazgo 5:** Los clientes sin servicio de soporte técnico tienen un churn de (41.6%) respecto a los clientes que sí lo tienen (15.2%), viendose " \
    "lo valioso que representa la venta del soporte técnico. Con algún descuento promocional de entrada puede servir como una herramienta de fidelización importante para la empresa.")