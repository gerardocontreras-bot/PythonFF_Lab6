import plotly as pl
import plotly.express as px
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import openpyxl

df = pd.read_excel("edadmedia.xlsx")


df_long = df.melt(
    id_vars="Year",
    var_name="Departamento",
    value_name="EdadMedia"
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
app.title = "Evolución Edad Media por Departamento GT"

app.layout = html.Div([
    html.H2("Evolución de la Edad Media por Departamento en Guatemala"),

    # Dropdown para seleccionar departamentos
    dcc.Dropdown(
        id="dept-dropdown",
        options=[
            {"label": "Guatemala", "value": "Guatemala"},
            {"label": "Quetzaltenango", "value": "Quetzaltenango"},
            {"label": "Sololá", "value": "Sololá"},
            {"label": "Quiché", "value": "Quiche"},
            {"label": "Escuintla", "value": "Escuintla"}
        ],
        value=["Guatemala", "Quetzaltenango"],  # valores por defecto
        multi=True,
        placeholder="Selecciona uno o varios departamentos..."
    ),

    # Gráfica animada
    dcc.Graph(id="line-chart")
])

@app.callback(
    Output("line-chart", "figure"),
    Input("dept-dropdown", "value")
)
def update_chart(selected_departments):
    # Filtrar según lo seleccionado
    filtered_df = df_long[df_long["Departamento"].isin(selected_departments)]

    # Crear la figura animada
    fig = px.line(
        filtered_df,
        x="Year",
        y="EdadMedia",
        color="Departamento",
        line_group="Departamento",
        animation_frame="Year",
        hover_name="Departamento",
        range_y=[df_long["EdadMedia"].min() - 1, df_long["EdadMedia"].max() + 1],
        title="Evolución de la edad media por departamento"
    )

    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Edad media",
        legend_title="Departamento",
        template="plotly_white"
    )
    return fig


# === CORRER LA APP ===
if __name__ == "__main__":
    app.run(port=10000, debug=False, host="0.0.0.0")
