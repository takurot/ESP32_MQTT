import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlite3

app = dash.Dash(__name__)

# レイアウト定義
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=3*1000),  # 1秒ごとに更新
])

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(n):
    conn = sqlite3.connect('sensors.db')
    cursor = conn.cursor()

    # データの読み込み
    cursor.execute("SELECT voltage, temperature FROM readings")
    data = cursor.fetchall()

    temperatures = [row[0] for row in reversed(data)]
    voltages = [row[1] for row in reversed(data)]
    
    # print(temperatures, voltages)

    conn.close()

    # プロットの更新
    trace1 = go.Scatter(y=temperatures, name='Temperature', mode='lines+markers')
    trace2 = go.Scatter(y=voltages, name='Voltage', mode='lines+markers')

    return {'data': [trace1, trace2], 'layout': go.Layout(title='Sensor Data')}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0') #default port 8050
