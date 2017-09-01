def test():
    with open('/home/vishnu/Elements/Data/espn_boxscore.csv', 'r') as file:
        data = [x.split(',', 1) for x in file.read().split('\n')]
    data = {x[0]:x[1].split('#') for x in data if len(x) == 2 and x[0] != ''}
    pass


import plotly
import plotly.graph_objs as go

trace0 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='markers',
    marker=dict(
        color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',
               'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
        opacity=[1, 0.8, 0.6, 0.4],
        size=[200, 60, 80, 100],
    )
)

data = [trace0]

plotly.offline.plot({
    "data": [trace0],
    "layout": go.Layout(title="yok")
})
