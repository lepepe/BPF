import streamlit as st
import pandas as pd
import numpy as np

# Get data
df = pd.read_csv('resumen-bos-scores.csv')
tdf = pd.read_csv('teams.csv')
hrdf = pd.read_csv('homeruns.csv')
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

# Main data
data = df[(df['Eqp'] == team) | (df['Eqp.1'] == team)]

# Away | Visitador
vs1 = df[(df['Eqp'] == team) & (df['Jc'] == 'VS')]
vs2 = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'VS')]
vs = len(vs1.index)+len(vs2.index)
hrvs1 = hrdf[(hrdf['Eqp Po'] == team) & (~hrdf['Estadio'].str.contains(stadium, na=False))]
hrvs2 = hrdf[(hrdf['Eqp Pe'] == team) & (~hrdf['Estadio'].str.contains(stadium, na=False))]
hr_vs_po = str(len(hrvs1.index))
hr_vs_pe = str(len(hrvs2.index))

# Home Club | En cassa
hc1 = df[(df['Eqp'] == team) & (df['Jc'] == 'HC')]
hc2 = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'HC')]
hc = len(hc1.index)+len(hc2.index)
hrhc1 = hrdf[(hrdf['Eqp Po'] == team) & (hrdf['Estadio'].str.contains(stadium, na=False))]
hrhc2 = hrdf[(hrdf['Eqp Pe'] == team) & (hrdf['Estadio'].str.contains(stadium, na=False))]
hr_hc_po = str(len(hrhc1.index))
hr_hc_pe = str(len(hrhc2.index))

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

win_hc_df_allowed = df[(df['Eqp'] == team) & (df['Jc'] == 'HC') & (df['Re'] == 'G')]
win_hc_allowed = win_hc_df_allowed.groupby(['Jc', 'Re'], as_index=False).agg(
    {
        'C.1':sum,
        'H.1':sum,
        'E.1':sum,
        'inn':sum
    }
).rename(
    columns={
        'C.1':'C',
        'H.1':'H',
        'E.1':'E'
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

loss_hc_df_allowed = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'HC') & (df['Re.1'] == 'P')]
loss_hc_allowed = loss_hc_df.groupby(['Jc.1', 'Re.1'], as_index=False).agg(
    {
        'C':sum,
        'H':sum,
        'E':sum,
        'inn':sum
    }
).rename(
    columns={
        'Jc.1':'Jc',
        'Re.1':'Re',
    }
)

hc_frames = [win_hc, loss_hc]
hc_result = pd.concat(hc_frames)
hc_result.loc[1] = hc_result.sum(numeric_only=True, axis=0)
hc_result[['C','H','E','inn']] = hc_result[['C','H','E','inn']].astype(int)
hc_result = hc_result.drop(['Jc'], axis=1)
hc_result['Re'].fillna('Total', inplace = True)
hc_result.set_index('Re', inplace=True)

hc_frames_allowed = [win_hc_allowed, loss_hc_allowed]
hc_result_allowed = pd.concat(hc_frames_allowed)
hc_result_allowed.loc[1] = hc_result_allowed.sum(numeric_only=True, axis=0)
hc_result_allowed[['C','H','E','inn']] = hc_result_allowed[['C','H','E','inn']].astype(int)
hc_result_allowed = hc_result_allowed.drop(['Jc'], axis=1)
hc_result_allowed['Re'].fillna('Total', inplace = True)
hc_result_allowed.set_index('Re', inplace=True)

# Away dataframes
# CHE awarded runs
win_away_df = df[(df['Eqp'] == team) & (df['Jc'] == 'VS') & (df['Re'] == 'G')]
win_away = win_away_df.groupby(['Jc', 'Re'], as_index=False).agg(
    {
        'C':sum,
        'H':sum,
        'E':sum,
        'inn':sum
    }
)

win_away_df_allowed = df[(df['Eqp'] == team) & (df['Jc'] == 'VS') & (df['Re'] == 'G')]
win_away_allowed = win_away_df_allowed.groupby(['Jc', 'Re'], as_index=False).agg(
    {
        'C.1':sum,
        'H.1':sum,
        'E.1':sum,
        'inn':sum
    }
).rename(
    columns={
        'C.1':'C',
        'H.1':'H',
        'E.1':'E'
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

loss_away_df_allowed = df[(df['Eqp.1'] == team) & (df['Jc.1'] == 'VS') & (df['Re.1'] == 'P')]
loss_away_allowed = loss_away_df_allowed.groupby(['Jc.1', 'Re.1'], as_index=False).agg(
    {
        'C':sum,
        'H':sum,
        'E':sum,
        'inn':sum
    }
).rename(
    columns={
        'Jc.1':'Jc',
        'Re.1':'Re',
    }
)

vs_frames = [win_away, loss_away]
vs_result = pd.concat(vs_frames)
vs_result.loc[1] = vs_result.sum(numeric_only=True, axis=0)
vs_result[['C','H','E','inn']] = vs_result[['C','H','E','inn']].astype(int)
vs_result = vs_result.drop(['Jc'], axis=1)
vs_result['Re'].fillna('Total', inplace = True)
vs_result.set_index('Re', inplace=True)

vs_frames_allowed = [win_away_allowed, loss_away_allowed]
vs_result_allowed = pd.concat(vs_frames_allowed)
vs_result_allowed.loc[1] = vs_result_allowed.sum(numeric_only=True, axis=0)
vs_result_allowed[['C','H','E','inn']] = vs_result_allowed[['C','H','E','inn']].astype(int)
vs_result_allowed = vs_result_allowed.drop(['Jc'], axis=1)
vs_result_allowed['Re'].fillna('Total', inplace = True)
vs_result_allowed.set_index('Re', inplace=True)

hr_vs_po = int(str(len(hrvs1.index)))
hr_vs_pe = int(str(len(hrvs2.index)))
hr_hc_po = int(str(len(hrhc1.index)))
hr_hc_pe = int(str(len(hrhc2.index)))

hr_summary = [{'HR HC PO': hr_hc_po, 'HR HC PE': hr_hc_pe, 'HR VS PO': hr_vs_po, 'HR VS PE': hr_vs_pe}]
hr_data_frame = pd.DataFrame(hr_summary)

# Setting layout
l_col, m_col, r_col = st.columns([3,3,6])
l_md6, r_md6 = st.columns([6,6])

# Display data
with l_col:
    st.image(f'./assets/{team.lower()}.png')

with m_col:
    st.text(f'Team: {team}')
    st.text(f'Stadium: {stadium}')
    st.text('Juegos Jugados: ' + str(len(data.index)))
    st.text('Home Club: ' + str(hc))
    st.text('Visitador: ' + str(vs))

with r_col:
    st.subheader("Homeruns Away/HomeClub")
    st.table(hr_data_frame)

    #FP= ((Rhome+RAhome)/Ghome) / ((Raway+RAaway)/Gaway
    runs_awarded_home_club = hc_result.iloc[2]['C']
    runs_allowed_home_club = hc_result_allowed.iloc[2]['C']
    runs_awarded_away = vs_result.iloc[2]['C']
    runs_allowed_away = vs_result_allowed.iloc[2]['C']

    bpf_runs = ((runs_awarded_home_club+runs_allowed_home_club)/hc) / ((runs_awarded_away+runs_allowed_away)/vs)
    bpf_hr = ((hr_hc_po+hr_hc_pe)/hc) / ((hr_vs_po+hr_vs_pe)/vs)

    st.info('Batting Park Factor (Runs): ' + str(round(bpf_runs, 4)) )
    st.info('Batting Park Factor (Homeruns): ' + str(round(bpf_hr, 4)) )

with  l_md6:
    st.subheader("Win/Lost playing away awarded.")
    st.table(vs_result)

    st.subheader("Win/Lost playing as Home Club awarded")
    st.table(hc_result)

with  r_md6:
    st.subheader("Win/Lost playing away allowed.")
    st.table(vs_result_allowed)

    st.subheader("Win/Lost playing as Home Club allowed")
    st.table(hc_result_allowed)

#st.dataframe(hrvs1)
