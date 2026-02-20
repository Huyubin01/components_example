import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

st.title('企鹅数据可视化诊断')

# 1. 检查数据读取
df = pd.read_csv('penguins.csv')

# 打印列名（非常重要，检查是否有隐藏空格）
st.write("实际检测到的列名:", [f"'{c}'" for c in df.columns.tolist()])

# 2. 强制转换数据类型并清洗
# 有些 CSV 文件首行可能有乱码，或者列名带空格
# 我们手动指定列名，并处理掉可能的空值
try:
    # 如果你的列名带空格，这里会自动报错，提示你修改
    df['bill_length_mm'] = pd.to_numeric(df['bill_length_mm'], errors='coerce')
    df['bill_depth_mm'] = pd.to_numeric(df['bill_depth_mm'], errors='coerce')
    
    # 过滤掉数值不全的行
    df_clean = df.dropna(subset=['bill_length_mm', 'bill_depth_mm'])
    
    st.write(f"原始行数: {len(df)}，清洗后有效行数: {len(df_clean)}")

    if len(df_clean) > 0:
        fig = px.scatter(
            df_clean, 
            x='bill_length_mm', 
            y='bill_depth_mm', 
            color='species',
            title="散点图成功加载"
        )
        # 先用标准 chart 看看有没有点
        st.plotly_chart(fig)
        
        # 再用事件捕捉
        st.subheader("点击图中的点试试：")
        selected_points = plotly_events(fig)
        st.write("选中的数据:", selected_points)
    else:
        st.error("错误：清洗后没有发现有效的数值数据！请检查 CSV 文件内容。")
        st.write("数据前几行预览：", df.head())

except KeyError as e:
    st.error(f"找不到列名：{e}。请对照上面的『实际检测到的列名』修改代码。")