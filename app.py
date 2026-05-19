# =========================================================
# BANK MARKETING ANALYTICS APP
# Proyecto EDA con Streamlit
# Autor: Jesus Alexander Ortiz Cahuana
# Especialización: Python for Analytics
# Año: 2026
# =========================================================

# =========================
# IMPORTACIONES
# =========================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Configuración visual
st.set_page_config(
    page_title="Bank Marketing Analytics",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")


# =========================================================
# CLASE PRINCIPAL (POO)
# =========================================================

class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    # ==========================================
    # VARIABLES NUMÉRICAS
    # ==========================================
    def numerical_columns(self):
        return self.df.select_dtypes(include=np.number).columns.tolist()

    # ==========================================
    # VARIABLES CATEGÓRICAS
    # ==========================================
    def categorical_columns(self):
        return self.df.select_dtypes(include='object').columns.tolist()

    # ==========================================
    # ESTADÍSTICAS DESCRIPTIVAS
    # ==========================================
    def descriptive_stats(self):
        return self.df.describe()

    # ==========================================
    # VALORES NULOS
    # ==========================================
    def missing_values(self):
        return self.df.isnull().sum()

    # ==========================================
    # INFORMACIÓN GENERAL
    # ==========================================
    def dataset_info(self):
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 Navegación")

menu = st.sidebar.radio(
    "Selecciona un módulo:",
    [
        "🏠 Home",
        "📂 Carga Dataset",
        "📊 EDA",
        "📌 Conclusiones"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Proyecto desarrollado con Streamlit")


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.title("📊 Bank Marketing Analytics")

    st.markdown("""
    ## Bienvenido al Proyecto de Análisis Exploratorio de Datos

    Esta aplicación interactiva permite analizar información de campañas
    de marketing bancario utilizando herramientas de análisis de datos
    y visualización en Python.
    """)

    # =====================================================
    # KPIs
    # =====================================================

    st.markdown("---")

    st.subheader("📈 Indicadores Generales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Clientes", "41,188")

    with col2:
        st.metric("Variables", "21")

    with col3:
        st.metric("Aceptación", "11.3%")

    with col4:
        st.metric("Campañas", "6 meses")

    # =====================================================
    # OBJETIVO Y TECNOLOGÍAS
    # =====================================================

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 Objetivo")

        st.write("""
        Analizar los factores que influyen en la aceptación de campañas
        de marketing mediante técnicas de análisis exploratorio de datos (EDA).
        """)

    with col2:

        st.subheader("🛠 Tecnologías Utilizadas")

        st.write("""
        - Python
        - Pandas
        - NumPy
        - Streamlit
        - Matplotlib
        - Seaborn
        """)

    # =====================================================
    # AUTOR
    # =====================================================

    st.markdown("---")

    st.subheader("👨‍💻 Autor")

    st.write("""
    - Nombre: Jesus Alexander Ortiz Cahuana
    - Especialización: Python for Analytics
    - Año: 2026
    """)

# =========================================================
# CARGA DEL DATASET
# =========================================================

elif menu == "📂 Carga Dataset":

    st.title("📂 Carga del Dataset")

    uploaded_file = st.file_uploader(
        "Sube el archivo BankMarketing.csv",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file, sep=";")

        st.success("✅ Dataset cargado correctamente")

        st.subheader("Vista previa del dataset")

        st.dataframe(df.head())

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Filas", df.shape[0])

        with col2:
            st.metric("Columnas", df.shape[1])

    else:
        st.warning("⚠️ Debes cargar un archivo CSV para continuar.")


# =========================================================
# EDA
# =========================================================

elif menu == "📊 EDA":

    st.title("📊 Análisis Exploratorio de Datos (EDA)")

    uploaded_file = st.file_uploader(
        "Sube nuevamente el dataset para análisis",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file, sep=";")

        analyzer = DataAnalyzer(df)

        num_cols = analyzer.numerical_columns()
        cat_cols = analyzer.categorical_columns()

        # =====================================================
        # TABS
        # =====================================================

        tabs = st.tabs([
            "📌 Información General",
            "📈 Variables Numéricas",
            "📊 Variables Categóricas",
            "🔍 Análisis Bivariado",
            "⚙️ Análisis Dinámico",
            "💡 Hallazgos"
        ])

        # =====================================================
        # TAB 1
        # =====================================================

        with tabs[0]:

            st.subheader("📌 Información General del Dataset")

            st.subheader("📌 Resumen del Dataset")
            col1, col2, col3 = st.columns(3)
            
            with col1:  
                st.metric("Filas", df.shape[0])
                
            with col2:
                st.metric("Columnas", df.shape[1])
                
            with col3:
                st.metric("Valores Nulos", int(df.isnull().sum().sum()))

            st.subheader("Valores Nulos")

            missing = analyzer.missing_values()

            st.dataframe(missing)

            fig, ax = plt.subplots(figsize=(10, 4))
            
            missing = df.isnull().sum()
            
            missing_filtered = missing[missing > 0]
            
            if len(missing_filtered) > 0:
                fig, ax = plt.subplots(figsize=(10,4))
                missing_filtered.sort_values().plot(
                    kind='barh',
                    ax=ax
                )
                
                ax.set_title("Valores nulos por variable")
                st.pyplot(fig)
                
            else:
                st.success("✅ El dataset no contiene valores nulos.")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            st.subheader("Clasificación de Variables")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Variables Numéricas")
                st.write(num_cols)

            with col2:
                st.write("### Variables Categóricas")
                st.write(cat_cols)

        # =====================================================
        # TAB 2
        # =====================================================

        with tabs[1]:

            st.subheader("📈 Estadísticas Descriptivas")

            st.dataframe(analyzer.descriptive_stats())

            st.markdown("---")

            st.subheader("Distribución de Variables Numéricas")

            selected_num = st.selectbox(
                "Selecciona una variable numérica",
                num_cols
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            sns.histplot(
                data=df,
                x=selected_num,
                kde=True,
                bins=30,
                ax=ax
            )
            
            ax.set_title(f"Distribución de {selected_num}", fontsize=16)
            ax.set_xlabel(selected_num)
            ax.set_ylabel("Frecuencia")

            ax.set_title(f"Distribución de {selected_num}")

            st.pyplot(fig)

            st.info(f"""
            La variable {selected_num} presenta una distribución
            que permite identificar concentración de valores,
            dispersión y posibles valores atípicos.
            """)

        # =====================================================
        # TAB 3
        # =====================================================

        with tabs[2]:

            st.subheader("📊 Análisis de Variables Categóricas")

            selected_cat = st.selectbox(
                "Selecciona una variable categórica",
                cat_cols
            )

            counts = df[selected_cat].value_counts()

            st.dataframe(counts)

            fig, ax = plt.subplots(figsize=(10, 5))

            sns.countplot(
                data=df,
                y=selected_cat,
                order=df[selected_cat].value_counts().index,
                ax=ax
            )

            ax.set_title(f"Frecuencia de {selected_cat}")

            st.pyplot(fig)

        # =====================================================
        # TAB 4
        # =====================================================

        with tabs[3]:

            st.subheader("🔍 Análisis Bivariado")

            analysis_type = st.selectbox(
                "Selecciona tipo de análisis",
                [
                    "Numérico vs Categórico",
                    "Categórico vs Categórico"
                ]
            )

            # ==========================================
            # NUMÉRICO VS CATEGÓRICO
            # ==========================================

            if analysis_type == "Numérico vs Categórico":

                selected_num = st.selectbox(
                    "Variable numérica",
                    num_cols,
                    key="num_bi"
                )

                selected_cat = st.selectbox(
                    "Variable categórica",
                    cat_cols,
                    key="cat_bi"
                )

                fig, ax = plt.subplots(figsize=(10, 5))

                sns.boxplot(
                    x=selected_cat,
                    y=selected_num,
                    data=df,
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

            # ==========================================
            # CATEGÓRICO VS CATEGÓRICO
            # ==========================================

            else:

                cat1 = st.selectbox(
                    "Primera variable",
                    cat_cols,
                    key="cat1"
                )

                cat2 = st.selectbox(
                    "Segunda variable",
                    cat_cols,
                    key="cat2"
                )

                cross = pd.crosstab(df[cat1], df[cat2])

                st.dataframe(cross)

                fig, ax = plt.subplots(figsize=(10, 5))

                sns.countplot(
                    x=cat1,
                    hue=cat2,
                    data=df,
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

        # =====================================================
        # TAB 5
        # =====================================================

        with tabs[4]:

            st.subheader("⚙️ Análisis Dinámico")

            selected_columns = st.multiselect(
                "Selecciona columnas",
                df.columns
            )

            if len(selected_columns) > 0:
                st.dataframe(df[selected_columns].head())

            if len(num_cols) > 0:

                selected_slider = st.selectbox(
                    "Selecciona variable para filtrar",
                    num_cols
                )

                min_value = int(df[selected_slider].min())
                max_value = int(df[selected_slider].max())

                selected_range = st.slider(
                    "Selecciona rango",
                    min_value,
                    max_value,
                    (min_value, max_value)
                )

                filtered_df = df[
                    (df[selected_slider] >= selected_range[0]) &
                    (df[selected_slider] <= selected_range[1])
                ]

                st.write("### Datos Filtrados")

                st.dataframe(filtered_df.head())

                st.write(f"Cantidad de registros: {filtered_df.shape[0]}")

        # =====================================================
        # TAB 6
        # =====================================================

        with tabs[5]:

            st.subheader("💡 Hallazgos Clave")

            st.success("""
            1. La duración del contacto presenta una fuerte relación
            con la aceptación de la campaña.

            2. Los clientes contactados mediante celular muestran
            mejores resultados frente al teléfono tradicional.

            3. Algunas ocupaciones presentan mayor frecuencia
            de aceptación de campañas.

            4. Los clientes con múltiples contactos previos
            tienden a responder de manera diferente.

            5. Las variables económicas permiten identificar
            comportamientos relevantes del mercado.
            """)

            st.subheader("📌 Insights de Negocio")

            st.info("""
            Los resultados obtenidos permiten comprender mejor el comportamiento
            de los clientes y optimizar futuras campañas comerciales.
            """)

    else:
        st.warning("⚠️ Debes cargar el dataset para ejecutar el EDA.")


# =========================================================
# CONCLUSIONES
# =========================================================

elif menu == "📌 Conclusiones":

    st.title("📌 Conclusiones Finales")

    st.markdown("""
    ## Principales Conclusiones

    ### 1.
    La duración de las llamadas influye significativamente
    en la aceptación de campañas de marketing.

    ### 2.
    El canal de contacto celular presenta mejores resultados
    que otros medios de comunicación.

    ### 3.
    Existen perfiles ocupacionales con mayor predisposición
    a aceptar campañas bancarias.

    ### 4.
    Las campañas repetitivas pueden reducir la efectividad
    comercial de la organización.

    ### 5.
    El análisis exploratorio permite generar estrategias
    comerciales basadas en evidencia y comportamiento real.
    """)

    st.markdown("---")

    st.subheader("🚀 Reflexión Final")

    st.write("""
    Este proyecto permitió aplicar conceptos fundamentales de análisis de datos,
    visualización, programación orientada a objetos y desarrollo de aplicaciones
    interactivas utilizando Streamlit.
    """)