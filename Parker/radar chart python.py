import plotly.graph_objects as go
import pandas as pd

# CLEAN HUME OUTPUT
humedata = pd.read_csv("Desktop/School/current semester/Consulting Wilford Woodruff/Hume results.csv")
humedata = humedata.iloc[:, 8:]
columns_to_drop = ["1","2","3","4","5","6","7","8","9"]
humedata = humedata.drop(columns=columns_to_drop)
means = humedata.mean()
names = humedata.columns
humemeans = pd.DataFrame({'names': names, 'means': means})
humemeans = humemeans.sort_values(by='means', ascending=False).dropna()

#getminmax
humemin = humemeans['means'].min()
humemax = humemeans['means'].max()
# Standardize between 1 and 10
humemeans['means'] = 1 + 9 * ((humemeans['means'] - humemin) / (humemax - humemin))

humemeans10 = humemeans.iloc[:10]

# CHART VARIABLES
hume1name = humemeans10.iloc[0]['names']
hume1val = round(humemeans10.iloc[0]['means'], 2)
hume2name = humemeans10.iloc[1]['names']
hume2val = round(humemeans10.iloc[1]['means'], 2)
hume3name = humemeans10.iloc[2]['names']
hume3val = round(humemeans10.iloc[2]['means'], 2)
hume4name = humemeans10.iloc[3]['names']
hume4val = round(humemeans10.iloc[3]['means'], 2)
hume5name = humemeans10.iloc[4]['names']
hume5val = round(humemeans10.iloc[4]['means'], 2)
hume6name = humemeans10.iloc[5]['names']
hume6val = round(humemeans10.iloc[5]['means'], 2)
hume7name = humemeans10.iloc[6]['names']
hume7val = round(humemeans10.iloc[6]['means'], 2)
hume8name = humemeans10.iloc[7]['names']
hume8val = round(humemeans10.iloc[7]['means'], 2)
hume9name = humemeans10.iloc[8]['names']
hume9val = round(humemeans10.iloc[8]['means'], 2)
hume10name = humemeans10.iloc[9]['names']
hume10val = round(humemeans10.iloc[9]['means'], 2)

ventmax = 0

overall_max = max(humemax, ventmax)

categories = [hume1name, hume2name, hume3name, hume4name, hume5name, hume6name, hume7name, hume8name, hume9name, hume1name]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[hume1val, hume2val, hume3val, hume4val, hume5val, hume6val, hume7val, hume8val, hume9val, hume1val],
      theta=categories,
      fill='toself',
      name='Hume'
))
fig.add_trace(go.Scatterpolar(
      r=[.1, .05, .07, .18, .13, .04, .2, .08, .12, .1],
      theta=categories,
      fill='toself',
      name='Vent'
))
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, overall_max + 0.1]
    )),
  showlegend=False,
  plot_bgcolor='white'
)

fig.show()

