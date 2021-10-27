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

data = df[(df['Eqp'] == team) | (df['Eqp.1'] == team)]
vs1 = df[(df['Eqp'] == team) & (df['Jc'] == 'VS')]
vs2 = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'VS')]
vs = len(vs1.index)+len(vs2.index)
hc1 = df[(df['Eqp'] == team) & (df['Jc'] == 'HC')]
hc2 = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'HC')]
hc = len(hc1.index)+len(hc2.index)

# Home Club dataframes
win_hc_df = df[(df['Eqp'] == team) & (df['Jc'] == 'HC') & (df['Re'] == 'G')]
win_hc = win_hc_df.groupby(['Jc', 'Re'], as_index=False).agg(
    {
        'C':sum,
        'H':sum,
        'E':sum,
        'inn':sum
    }
)

loss_hc_df = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'HC') & (df['Re.1'] == 'P')]
loss_hc = loss_hc_df.groupby(['Jc.1', 'Re.1'], as_index=False).agg(
    {
        'C.1':sum,
        'H.1':sum,
        'E.1':sum,
        'inn':sum
    }
).rename(
    columns={
        'Jc.1':'Jc',
        'Re.1':'Re',
        'C.1':'C',
        'H.1':'H',
        'E.1':'E'
    }
)
hc_frames = [win_hc, loss_hc]
hc_result = pd.concat(hc_frames)
hc_result.loc[1] = hc_result.sum(numeric_only=True, axis=0)
hc_result[['C','H','E','inn']] = hc_result[['C','H','E','inn']].astype(int)
hc_result = hc_result.drop(['Jc'], axis=1)
hc_result['Re'].fillna('Total', inplace = True)
hc_result.set_index('Re', inplace=True)

# Away dataframes
win_away_df = df[(df['Eqp'] == team) & (df['Jc'] == 'VS') & (df['Re'] == 'G')]
win_away = win_away_df.groupby(['Jc', 'Re'], as_index=False).agg(
    {
        'C':sum,
        'H':sum,
        'E':sum,
        'inn':sum
    }
)

loss_away_df = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'VS') & (df['Re.1'] == 'P')]
loss_away = loss_away_df.groupby(['Jc.1', 'Re.1'], as_index=False).agg(
    {
        'C.1':sum,
        'H.1':sum,
        'E.1':sum,
        'inn':sum
    }
).rename(
    columns={
        'Jc.1':'Jc',
        'Re.1':'Re',
        'C.1':'C',
        'H.1':'H',
        'E.1':'E'
    }
)
vs_frames = [win_away, loss_away]
vs_result = pd.concat(vs_frames)
vs_result.loc[1] = vs_result.sum(numeric_only=True, axis=0)
vs_result[['C','H','E','inn']] = vs_result[['C','H','E','inn']].astype(int)
vs_result = vs_result.drop(['Jc'], axis=1)
vs_result['Re'].fillna('Total', inplace = True)
vs_result.set_index('Re', inplace=True)

# Setting layout
l_col, r_col = st.columns([2,9])

# Display data
with l_col:
    st.image(f'./assets/{team.lower()}.png')

with r_col:
    st.text(f'Team: {team}')
    st.text(f'Stadium: {stadium}')
    st.text('Juegos Jugados: ' + str(len(data.index)))
    st.text('Home Club: ' + str(hc))
    st.text('Visitador: ' + str(vs))

st.subheader("Win/Lost playing Away.")
st.table(vs_result)

st.subheader("Win/Lost playing as Home Club")
st.table(hc_result)

#st.dataframe(data)
