import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load and sort data
df = pd.read_csv("format_sales1.csv", parse_dates=["date"])
df = df.sort_values(by="date")

# Initialize app
app = Dash(__name__)

# Define layout
app.layout = html.Div(
    children=[
        html.H1("📈 Pink Morsel Sales Dashboard", style={
            "textAlign": "center", "color": "#e91e63", "padding": "20px"
        }),

        html.Div([
            html.Label("Select Region:", style={"fontWeight": "bold", "fontSize": "16px"}),
            dcc.RadioItems(
                id='region-radio',
                options=[
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'},
                    {'label': 'All', 'value': 'all'}
                ],
                value='all',
                labelStyle={'display': 'block', 'margin': '5px 0'}
            )
        ], style={
            "width": "200px", "padding": "20px", "backgroundColor": "#fce4ec",
            "borderRadius": "10px", "margin": "auto"
        }),

        dcc.Graph(id="sales-line-chart", style={"marginTop": "40px"}),

        html.P("🔴 Red dashed line marks the Pink Morsel price increase on Jan 15, 2021.",
               style={"textAlign": "center", "fontStyle": "italic", "color": "#555"})
    ],
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#fff0f5", "padding": "20px"}
)

# Callback
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value")
)
def update_chart(selected_region):
    # Filter by region
    if selected_region == "all":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["region"] == selected_region]

    # Group sales by date
    sales_by_date = filtered_df.groupby("date")["sales"].sum().reset_index()

    # Create chart
    fig = px.line(
        sales_by_date,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time - {selected_region.capitalize()} Region" if selected_region != "all" else "All Regions",
        labels={"date": "Date", "sales": "Sales"},
        markers=True
    )

    fig.update_traces(line=dict(color="#BF81E8", width=2.5))  # hot pink and thicker line

    # Add red dashed line for Jan 15, 2021
    fig.add_shape(
        type="line",
        x0="2021-01-15", x1="2021-01-15",
        y0=0, y1=sales_by_date["sales"].max(),
        line=dict(color="red", dash="dash")
    )

    fig.add_annotation(
        x="2021-01-15",
        y=sales_by_date["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    return fig

# Run
if __name__ == '__main__':
    app.run(debug=True)
