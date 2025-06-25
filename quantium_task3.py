import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import datetime

# Load pre-filtered sales data (only Pink Morsel)
df = pd.read_csv("format_sales1.csv", parse_dates=["date"])
df = df.sort_values("date")

# Get list of regions for dropdown
regions = df['region'].unique().tolist()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("📈 Pink Morsel Sales Visualiser - Soul Foods", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Region:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{"label": region, "value": region} for region in regions] +
                    [{"label": "All Regions", "value": "All"}],
            value="All",
            clearable=False
        ),
        html.Br(),
        html.Label("Select Date Range:", style={'fontWeight': 'bold'}),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD',
        )
    ], style={'width': '50%', 'margin': '0 auto'}),

    dcc.Graph(id='sales-line-chart'),

    html.P("🔴 Red dashed line shows price increase for Pink Morsel on Jan 15, 2021.",
           style={'textAlign': 'center', 'marginTop': '20px', 'fontStyle': 'italic'})
])

# Callback to update graph based on region and date range
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_graph(selected_region, start_date, end_date):
    # Filter by region
    if selected_region == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[df['region'] == selected_region]

    # Filter by date range
    filtered_df = filtered_df[
        (filtered_df['date'] >= start_date) &
        (filtered_df['date'] <= end_date)
    ]

    # Group by date
    sales_by_date = filtered_df.groupby("date")["sales"].sum().reset_index()

    # Create line chart
    fig = px.line(
        sales_by_date,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time - {selected_region}",
        labels={"date": "Date", "sales": "Sales"},
        markers=True
    )

    # Add red dashed line on price increase date
    price_date = datetime.datetime(2021, 1, 15)
    if start_date <= str(price_date.date()) <= end_date:
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

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
