import streamlit as st
# 🔥 换用抗封锁能力更强的库
from deep_translator import GoogleTranslator

# ==========================================
# 📱 网页版 V18.0 (云端抗封锁版)
# ==========================================

# 1. 页面配置
st.set_page_config(
    page_title="智能译 | Neo AI",
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 隐藏多余菜单
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTextArea textarea {font-size: 16px !important;}
    </style>
    """, unsafe_allow_html=True)

# 2. 核心逻辑
def translate_logic(text):
    try:
        # 简单的自动检测逻辑
        # 如果包含中文 -> 译英文
        # 否则 -> 译中文
        is_cn = any(u'\u4e00' <= ch <= u'\u9fff' for ch in text)
        target = "en" if is_cn else "zh-CN"
        
        # 🔥 使用 deep_translator (云端更稳定)
        # source='auto' 让谷歌自己猜，准确率更高
        translator = GoogleTranslator(source='auto', target=target)
        res = translator.translate(text)
        
        if not res:
            return False, "翻译结果为空"
        return True, res
    except Exception as e:
        return False, str(e)

# 3. 界面布局
st.markdown("<h2 style='text-align: center; color: #333;'>🌐 中英智能互译</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey; font-size: 12px;'>云端增强版 · 智能双向</p>", unsafe_allow_html=True)

# 输入框
text_input = st.text_area(
    "输入内容",
    height=150,
    label_visibility="collapsed",
    placeholder="在此输入中文或英文...\n(例如：你好 / Hello World)"
)

# 翻译按钮
if st.button("开始翻译", type="primary", use_container_width=True):
    if not text_input.strip():
        st.toast("⚠️ 请先输入内容")
    else:
        with st.spinner("🚀 正在请求云端..."):
            success, result = translate_logic(text_input)
            
        if success:
            st.success("✅ 翻译完成")
            st.text_area("结果", value=result, height=150, label_visibility="collapsed")
        else:
            st.error("❌ 连接繁忙，请重试")
            st.caption(f"调试信息: {result}")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 12px;'>此输入由 neo 在 AI 上制作</div>", unsafe_allow_html=True)