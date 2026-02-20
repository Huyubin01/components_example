import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.title('Streamlit 官方 Plotly 交互：精准显示点数据')

def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_penguin = load_lottieurl("C:\Users\86158\streamlit_apps\penguin_app\cutepenguin.png")
st_lottie(lottie_penguin, height=200)

# 1. 读取并清洗数据
df = pd.read_csv('penguins.csv')
df['bill_length_mm'] = pd.to_numeric(df['bill_length_mm'], errors='coerce')
df['bill_depth_mm'] = pd.to_numeric(df['bill_depth_mm'], errors='coerce')
# 重置索引，确保索引是干净连续的数字
df_clean = df.dropna(subset=['bill_length_mm', 'bill_depth_mm']).reset_index(drop=True)

# 【关键修改 1】：显式创建一个唯一标识列，用于精准匹配
df_clean['row_id'] = df_clean.index

# 2. 创建图表
fig = px.scatter(
    df_clean, 
    x='bill_length_mm', 
    y='bill_depth_mm', 
    color='species',
    title="企鹅散点图 (点击或框选图上的点)",
    hover_data=['island', 'sex'], # 可选：让鼠标悬浮时额外显示岛屿和性别
    custom_data=['row_id'] # 【关键修改 2】：把真实的行号隐藏进图表中
)

# 3. 渲染图表并捕获事件
event = st.plotly_chart(
    fig, 
    on_select="rerun", 
    selection_mode=('box', 'lasso', 'points') 
)

st.divider()
st.subheader("🐧 选中的企鹅详细信息：")

# 4. 解析选中的点并提取所有信息
if event and event.get("selection", {}).get("points"):
    # 【关键修改 3】：从 customdata 中提取我们塞进去的真实 ID
    selected_ids = [point["customdata"][0] for point in event["selection"]["points"]]
    
    # 根据 ID 提取完整数据行（并隐藏掉辅助用的 row_id 列使其更美观）
    selected_data = df_clean.loc[selected_ids].drop(columns=['row_id'])
    
    # 完美展示该点的所有信息
    st.dataframe(selected_data, use_container_width=True)
else:
    st.info("👆 请在上方散点图中点击或框选任意点，这里将显示它的所有原始数据。")