import streamlit as st
from streamlit import title

from geo_ubills import generate_script

st.title("🌍地理视频脚本生成器")
with st.sidebar:
    openai_api_key = st.text_input("请输入Deepseek API 密钥",type ="password")
    st.markdown("[获取Deepseek API 密钥](https://platform.deepseek.com/api_keys)")
subject =st.text_input("💡 请输入视频的主题")
video_length = st.number_input("⏰ 请输入视频的时长（分钟）",min_value=0.1,step=0.1)
creativity = st.slider("✨ 请选择视频脚本的创意程度(数字小说明越严谨，数字大说明更多样）",min_value=0.0,max_value=1.0,value=0.3,step=0.1)

submit = st.button("生成脚本")
if submit and not openai_api_key:
    st.info("请先输入Deepseek API 密钥")
    st.stop()
if submit and not subject:
    st.info("请先输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频时长不能小于0.1分钟")
    st.stop()
if submit:
    with st.spinner(("正在生成脚本...")):
        title_simplified, script_simplified, search_result_simplified = generate_script(subject,video_length,creativity,openai_api_key)
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题:")
    st.write(title_simplified)
    st.subheader("📒 视频脚本:")
    st.write(script_simplified)
    with st.expander("🔍 维基百科搜索结果"):
        st.write(search_result_simplified)