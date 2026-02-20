import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

st.title('Streamlit Plotly Events Example: Penguins')
df = pd.read_csv('penguins.csv')
fig = px.scatter(df, x='bill_length_mm', y='bill_depth_mm',color='species')
plotly_events(fig)