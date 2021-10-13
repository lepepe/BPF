import streamlit as st
import pandas as pd
import numpy as np

# Get data
df = pd.read_csv('resumen-bos-scores.csv')
stadium = df['Estadio'].unique().tolist()
team = df['Eqp.1'].unique().tolist()

# Title
st.title('Factor Parque')

# Sidebar menu
st.sidebar.title("Menu")
stadium_list = st.sidebar.selectbox('Seleccione Estadio', options=stadium, index=0)

# Display date
st.dataframe(df)
