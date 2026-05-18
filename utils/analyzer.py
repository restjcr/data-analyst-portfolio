import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import plotly.express as px


class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    # =====================================
    # Información general del dataset
    # =====================================

    def dataset_shape(self):

        return self.df.shape

    def dataset_info(self):

        buffer = StringIO()

        self.df.info(buf=buffer)

        info_str = buffer.getvalue()

        return info_str

    def data_types(self):

        return self.df.dtypes

    def missing_values(self):

        return self.df.isnull().sum()
    
    def descriptive_stats(self):

        return self.df.describe()

    # =====================================
    # Clasificación de variables
    # =====================================

    def classify_variables(self):

        numeric_cols = self.df.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()

        categorical_cols = self.df.select_dtypes(
            include=['object']
        ).columns.tolist()

        return numeric_cols, categorical_cols

    # =====================================
    # Estadísticas descriptivas
    # =====================================

    def descriptive_stats_numerical(self):

        return self.df.describe()
    
    def descriptive_stats_categorical(self):

        return self.df.describe(include="object")
    
    # =====================================
    # Gráficos
    # =====================================

    def plot_histogram(self, column, kde=True):

        fig, ax = plt.subplots(figsize=(6,3))

        sns.histplot(
            self.df[column],
            kde=kde,
            ax=ax
        )

        ax.set_title(
            f"Distribución de {column}"
        )

        return fig
    
    def categorical_counts(self, column):

        return self.df[column].value_counts()
    
    def categorical_proportions(self, column):

        return (
            self.df[column]
            .value_counts(normalize=True) * 100
        ).round(2)
    
    def plot_categorical(self, column):

        fig, ax = plt.subplots(figsize=(6,3))

        sns.countplot(
            data=self.df,
            x=column,
            ax=ax
        )

        ax.set_title(
            f"Distribución de {column}"
        )

        plt.xticks(rotation=45)

        return fig
    
    def plot_numeric_vs_categorical(
        self,
        numeric_col,
        categorical_col
    ):

        fig, ax = plt.subplots(figsize=(6,3))

        sns.boxplot(
            data=self.df,
            x=categorical_col,
            y=numeric_col,
            ax=ax
        )

        ax.set_title(
            f"{numeric_col} vs {categorical_col}"
        )

        return fig
    
    def categorical_vs_categorical(self, col1, col2):

        cross = pd.crosstab(
            self.df[col1],
            self.df[col2]
        )

        return cross
    
    def categorical_vs_categorical_percentage(self, col1, col2):

        cross = pd.crosstab(
            self.df[col1],
            self.df[col2],
            normalize="index"
        ) * 100

        return cross.round(2)

    def plot_categorical_vs_categorical(self, col1, col2):

        cross = pd.crosstab(
            self.df[col1],
            self.df[col2],
            normalize="index"
        ) * 100

        fig, ax = plt.subplots(figsize=(6,3))

        cross.plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        ax.set_ylabel(
            "Porcentaje"
        )

        ax.set_title(
            f"{col1} vs {col2}"
        )

        plt.xticks(rotation=0)

        return fig


    def plot_histogram_plotly(self, column, kde=True):
        fig = px.histogram(
            self.df,
            x=column,
            marginal="violin" if kde else None,
            title=f"Distribución de {column}",
            template="plotly_white"
        )
        return fig

    def plot_numeric_vs_categorical_plotly(self, numeric_col, categorical_col):
        fig = px.box(
            self.df,
            x=categorical_col,
            y=numeric_col,
            color=categorical_col,
            title=f"{numeric_col} por {categorical_col}",
            template="plotly_white"
        )
        return fig

    def plot_categorical_vs_categorical_plotly(self, cat_col, target_col):
        cross_df = (
            self.df
            .groupby([cat_col, target_col])
            .size()
            .reset_index(name="Cantidad")
        )
        fig = px.bar(
            cross_df,
            x=cat_col,
            y="Cantidad",
            color=target_col,
            barmode="group",
            title=f"{cat_col} vs {target_col}",
            template="plotly_white"
        )
        return fig