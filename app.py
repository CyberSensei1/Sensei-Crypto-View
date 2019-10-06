import dash
import dash_html_components as html
import dash_core_components as dcc
import urllib
import pandas
import json
import plotly.graph_objs as go

def get_symbols():
    symbols = []
    response = urllib.request.urlopen("https://www.binance.com/api/v1/exchangeInfo")
    exchangeInfo = json.loads(response.read())
    for symbol in exchangeInfo["symbols"]:
        for attribute, value in symbol.items():
            if attribute == "symbol":
                symbols.append(value) # example usage
    return symbols

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label':'Binance:'+format(coin), 'value':coin} for coin in get_symbols()],
        value='BTCUSDT'
    ),
    dcc.Graph(
        id='graph'
    )
])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    url = "https://www.binance.com/api/v1/klines?symbol="+format(value)+"&interval=1d"
    response = urllib.request.urlopen(url)
    df = pandas.read_json(response.read())

    data = [ dict(
        type = 'candlestick',
        x=pandas.to_datetime(df[0],unit='ms'),
        open=df[1],
        high=df[2],
        low=df[3],
        close=df[4],
    )]
    
    layout = go.Layout(
    title='Sensei CryptoView - ' + format(value),
    template='plotly_dark',
    xaxis=dict(
        autorange = True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]),
            font = dict(size=11, color='#000000')
        )
    ),
    yaxis=dict(autorange= True)
    )

    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)