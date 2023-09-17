import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlite3

app = dash.Dash(__name__)

# レイアウト定義
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=1*1000),  # 1秒ごとに更新
])

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(n):
    conn = sqlite3.connect('sensors.db')
    cursor = conn.cursor()

    # データの読み込み
    cursor.execute("SELECT timestamp, temperature, voltage FROM sensor_data ORDER BY timestamp DESC LIMIT 100")
    data = cursor.fetchall()

    timestamps = [row[0] for row in reversed(data)]
    temperatures = [row[1] for row in reversed(data)]
    voltages = [row[2] for row in reversed(data)]

    conn.close()

    # プロットの更新
    trace1 = go.Scatter(x=timestamps, y=temperatures, name='Temperature', mode='lines+markers')
    trace2 = go.Scatter(x=timestamps, y=voltages, name='Voltage', mode='lines+markers')

    return {'data': [trace1, trace2], 'layout': go.Layout(title='Sensor Data')}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0') #default port 8050
