import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.title('Streamlit 官方 Plotly 交互：精准显示点数据')

# 1. 专门加载动画的函数
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 【关键修改】：这里换成了直接指向纯 .json 数据文件的网址
lottie_url = "https://lottie.host/4671ff09-3abd-4e50-b031-92e8f2d8d677/Qs2kgYsK8b.json"
lottie_penguin = load_lottieurl(lottie_url)

# 渲染动画
if lottie_penguin:
    st_lottie(lottie_penguin, height=200)
else:
    st.error("动画加载失败，请检查网络或链接是否正确。")

st.divider()

# ----- 下方是你原来的数据处理和画图代码，保持不变 -----

# 读取并清洗数据
df = pd.read_csv('penguins.csv')
df['bill_length_mm'] = pd.to_numeric(df['bill_length_mm'], errors='coerce')
df['bill_depth_mm'] = pd.to_numeric(df['bill_depth_mm'], errors='coerce')
# 重置索引，确保索引是干净连续的数字
df_clean = df.dropna(subset=['bill_length_mm', 'bill_depth_mm']).reset_index(drop=True)

# 显式创建一个唯一标识列，用于精准匹配
df_clean['row_id'] = df_clean.index

# 创建图表
fig = px.scatter(
    df_clean, 
    x='bill_length_mm', 
    y='bill_depth_mm', 
    color='species',
    title="企鹅散点图 (点击或框选图上的点)",
    hover_data=['island', 'sex'], 
    custom_data=['row_id'] 
)

# 渲染图表并捕获事件
event = st.plotly_chart(
    fig, 
    on_select="rerun", 
    selection_mode=('box', 'lasso', 'points') 
)

st.divider()
st.subheader("🐧 选中的企鹅详细信息：")

# 解析选中的点并提取所有信息
if event and event.get("selection", {}).get("points"):
    selected_ids = [point["customdata"][0] for point in event["selection"]["points"]]
    selected_data = df_clean.loc[selected_ids].drop(columns=['row_id'])
    st.dataframe(selected_data, use_container_width=True)
else:
    st.info("👆 请在上方散点图中点击或框选任意点，这里将显示它的所有原始数据。")