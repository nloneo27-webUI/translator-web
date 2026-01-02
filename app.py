import streamlit as st
from deep_translator import GoogleTranslator
import time

# ==========================================
# 📱 网页版 V17.1 (云端稳定 + 自定义图标版)
# ==========================================

# 1. 页面配置
st.set_page_config(
    page_title="智能译 | Neo AI",
    page_icon="icon.png",  # 🔥 已修正：读取你上传的 icon.png 图片
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔥 强行注入苹果图标代码 (让 iPhone 添加到桌面时显示你的 logo)
# 注意：这需要 icon.png 就在仓库根目录下
st.markdown(
    """
    <link rel="apple-touch-icon" href="icon.png">
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stTextArea textarea {font-size: 16px !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 核心逻辑
def is_contains_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translate_logic(text):
    try:
        # 智能检测
        is_cn = is_contains_chinese(text)
        target = "en" if is_cn else "zh-CN"
        
        # 使用 Google 翻译 (Streamlit云端直连)
        translator = GoogleTranslator(source='auto', target=target)
        res = translator.translate(text)
        return True, res, target
    except Exception as e:
        return False, str(e), ""

# 3. 界面布局
st.markdown("<h2 style='text-align: center; color: #333;'>🌐 中英智能互译</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey; font-size: 12px;'>Google 神经引擎 · 智能双向</p>", unsafe_allow_html=True)

text_input = st.text_area(
    "输入内容",
    height=150,
    label_visibility="collapsed",
    placeholder="在此输入中文或英文...\n(服务器直连Google，极速响应)"
)

if st.button("开始翻译", type="primary", use_container_width=True):
    if not text_input.strip():
        st.toast("⚠️ 请先输入内容")
    else:
        with st.spinner("🚀 正在调用 Google 翻译..."):
            success, result, target = translate_logic(text_input)
            
        if success:
            st.success("✅ 翻译完成")
            st.text_area("结果", value=result, height=150, label_visibility="collapsed")
        else:
            st.error(f"❌ 翻译失败: {result}")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 12px;'>此输入由 neo 在 AI 上制作</div>", unsafe_allow_html=True)