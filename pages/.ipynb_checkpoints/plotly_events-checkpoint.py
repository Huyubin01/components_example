import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events
import os

st.title('Streamlit Plotly Events Example: Penguins')

# 检查文件是否存在
file_path = 'penguins.csv'
if not os.path.exists(file_path):
    st.error(f"找不到文件: {file_path}，当前路径下有: {os.listdir('.')}")
else:
    df = pd.read_csv(file_path)
    
    if df.empty:
        st.warning("CSV 文件是空的！")
    else:
        # 自动清洗数据，确保绘图列是数值型
        df['bill_length_mm'] = pd.to_numeric(df['bill_length_mm'], errors='coerce')
        df['bill_depth_mm'] = pd.to_numeric(df['bill_depth_mm'], errors='coerce')
        df = df.dropna(subset=['bill_length_mm', 'bill_depth_mm'])

        fig = px.scatter(df, x='bill_length_mm', y='bill_depth_mm', color='species')
        
        # 增加一个简单的 st.plotly_chart 对比，看看是不是组件问题
        # st.plotly_chart(fig) 
        
        selected_points = plotly_events(fig)
        st.write("你选中的点：", selected_points)