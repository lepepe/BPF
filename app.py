import streamlit as st
import pandas as pd
import numpy as np

# Get data
df = pd.read_csv('resumen-bos-scores.csv')
tdf = pd.read_csv('teams.csv')
team_name = tdf['Team'].unique().tolist()

# Title
st.title('Batting Park Factor')
st.write(
    "Batting Park Factor, also simply called Park Factor or BPF, is a baseball statistic that indicates the difference"
    "between runs scored in a team's home and road games. Most commonly used as a metric in the sabermetric community,"
    "it has found more general usage in recent years. It is helpful in assessing how much a specific ballpark contributes"
    "to the offensive production of a team or player."
)

# Sidebar menu
st.sidebar.title("Menu")
team_selector = st.sidebar.selectbox('Teams', options=team_name, index=0)
team_id = tdf[(tdf['Team']) == team_selector]['ID']
stadiums = tdf[(tdf['Team']) == team_selector]['Stadium']
team = team_id.iloc[0]
stadium = stadiums.iloc[0]


data = df[(df['Eqp'] == team) | (df['Vs'] == team)]
vs1 = df[(df['Eqp'] == team) & (df['Jc'] == 'VS')]
vs2 = df[(df['Vs'] == team) & (df['Jc.1'] == 'VS')]
vs = len(vs1.index)+len(vs2.index)
hc1 = df[(df['Eqp'] == team) & (df['Jc'] == 'HC')]
hc2 = df[(df['Vs'] == team) & (df['Jc.1'] == 'HC')]
hc = len(hc1.index)+len(hc2.index)

# Setting layout
left_column, right_column = st.columns([3,9])

# Display data
with left_column:
    st.image(f'./assets/{team.lower()}.png')

with right_column:
    st.text(f'Team: {team}')
    st.text(f'Stadium: {stadium}')
    st.text('Juegos Jugados: ' + str(len(data.index)))
    st.text('Home Club: ' + str(hc))
    st.text('Visitador: ' + str(vs))

st.dataframe(data)
