import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import datetime

# Load pre-filtered Pink Morsel sales data
df = pd.read_csv("format_sales1.csv", parse_dates=["date"])
df = df.sort_values("date")

# Group by date
sales_by_date = df.groupby("date")["sales"].sum().reset_index()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("📈 Pink Morsel Sales Visualiser - Soul Foods", style={'textAlign': 'center'}),

    dcc.Graph(id='sales-line-chart'),

    html.P("🔴 Red dashed line shows price increase for Pink Morsel on Jan 15, 2021.",
           style={'textAlign': 'center', 'marginTop': '20px', 'fontStyle': 'italic'})
])

# Update graph once at load (no interaction)
@app.callback(
    dash.dependencies.Output('sales-line-chart', 'figure'),
    dash.dependencies.Input('sales-line-chart', 'id')  # dummy input just to trigger once
)
def update_graph(_):
    # Create line chart
    fig = px.line(
        sales_by_date,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time - All Regions",
        labels={"date": "Date", "sales": "Sales"},
        markers=True
    )

    # Add red dashed line for price increase
    price_date = datetime.datetime(2021, 1, 15)
    fig.add_shape(
        type="line",
        x0=price_date,
        y0=0,
        x1=price_date,
        y1=sales_by_date["sales"].max(),
        line=dict(color="red", dash="dash")
    )
    fig.add_annotation(
        x=price_date,
        y=sales_by_date["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
