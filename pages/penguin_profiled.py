import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report

st.title('Streamlit 官方 Plotly 交互与数据报告')

# 1. 加载动画的函数
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://lottie.host/4671ff09-3abd-4e50-b031-92e8f2d8d677/Qs2kgYsK8b.json"
lottie_penguin = load_lottieurl(lottie_url)

# 渲染动画
if lottie_penguin:
    st_lottie(lottie_penguin, height=200)
else:
    st.error("动画加载失败，请检查网络或链接是否正确。")

st.divider()

# 2. 读取并清洗数据
df = pd.read_csv('penguins.csv')
df['bill_length_mm'] = pd.to_numeric(df['bill_length_mm'], errors='coerce')
df['bill_depth_mm'] = pd.to_numeric(df['bill_depth_mm'], errors='coerce')
# 重置索引，确保索引是干净连续的数字
df_clean = df.dropna(subset=['bill_length_mm', 'bill_depth_mm']).reset_index(drop=True)

# 显式创建一个唯一标识列，用于精准匹配
df_clean['row_id'] = df_clean.index

# 3. 创建图表
fig = px.scatter(
    df_clean, 
    x='bill_length_mm', 
    y='bill_depth_mm', 
    color='species',
    title="企颠散点图 (点击或框选图上的点)",
    hover_data=['island', 'sex'], 
    custom_data=['row_id'] 
)

# 渲染图表并捕获事件 (官方原生写法)
event = st.plotly_chart(
    fig, 
    on_select="rerun", 
    selection_mode=('box', 'lasso', 'points') 
)

st.divider()
st.subheader("🐧 选中的企鹅详细信息：")

# 4. 解析选中的点并提取所有信息
if event and event.get("selection", {}).get("points"):
    selected_ids = [point["customdata"][0] for point in event["selection"]["points"]]
    selected_data = df_clean.loc[selected_ids].drop(columns=['row_id'])
    # 【修复】：使用最新的宽度自适应参数
    st.dataframe(selected_data, width='stretch')
else:
    st.info("👆 请在上方散点图中点击或框选任意点，这里将显示它的所有原始数据。")

st.divider()

# 5. 整合 Pandas Profiling 数据分析报告
st.subheader('📊 Pandas Profiling of Penguin Dataset')

# 使用 Streamlit 缓存，防止每次点击图表都重新生成报告
@st.cache_resource
def generate_profile(dataframe):
    return ProfileReport(dataframe, explorative=True)

# 加载报告并展示
penguin_profile = generate_profile(df_clean)
st_profile_report(penguin_profile)