import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.title('Streamlit AgGrid Example: Penguins')

penguins_df = pd.read_csv('penguins.csv')
AgGrid(penguins_df)