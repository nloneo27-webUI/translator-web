import streamlit as st
import os

# 🔥 1. 先设置环境变量 (禁用 Magic，修复 iOS 报错)
os.environ["STREAMLIT_RUNNER_MAGIC_ENABLED"] = "false"

# 🔥 2. 再引入翻译库
from deep_translator import GoogleTranslator

# ==========================================
# 📱 网页版 V19.0 (修复版)
# ==========================================

# 3. 页面配置 (这行代码必须是第一个 st. 命令)
st.set_page_config(
    page_title="AI 随身译",
    page_icon="icon.png", # 确保你上传了 icon.png
    layout="centered",
    initial_sidebar_state="collapsed"
)
# 注入 CSS 优化手机端显示 (隐藏多余菜单，放大文字)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* 调整输入框文字大小 */
    .stTextArea textarea {font-size: 16px !important;}
    /* 调整按钮样式 */
    div.stButton > button {
        width: 100%;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 核心逻辑
def translate_logic(text, target_lang_code):
    try:
        # 使用 Google 翻译 (云端稳定)
        translator = GoogleTranslator(source='auto', target=target_lang_code)
        res = translator.translate(text)
        return True, res
    except Exception as e:
        return False, str(e)

# --- 界面布局 ---

st.markdown("<h3 style='text-align: center;'>🌐 AI 全能翻译助手</h3>", unsafe_allow_html=True)

# 1. 语言选择器 (横向排列，像原生App的Tab)
# 定义语言映射
lang_options = {
    "🇺🇸 英文": "en",
    "🇯🇵 日文": "ja",
    "🇰🇷 韩文": "ko",
    "🇫🇷 法文": "fr",
    "🇷🇺 俄文": "ru",
    "🇨🇳 中文": "zh-CN"
}

# 放在一行里显示
col1, col2 = st.columns([3, 7])
with col1:
    st.markdown("**目标语言:**")
with col2:
    # 默认选英文
    selected_lang = st.selectbox(
        "选择语言", 
        options=list(lang_options.keys()), 
        label_visibility="collapsed"
    )

target_code = lang_options[selected_lang]

# 2. 输入区域
text_input = st.text_area(
    "输入内容",
    height=120,
    label_visibility="collapsed",
    placeholder="在此输入内容..."
)

# 3. 翻译按钮 (蓝色醒目)
if st.button("🚀 开始翻译", type="primary", use_container_width=True):
    if not text_input.strip():
        st.toast("⚠️ 请先输入内容")
    else:
        with st.spinner("☁️ 正在请求云端..."):
            success, result = translate_logic(text_input, target_code)
            
        if success:
            st.success("✅ 翻译完成")
            
            # --- 核心优化：利用代码块实现“一键复制” ---
            # Streamlit 的 st.code 组件右上角自带一个“复制”按钮
            # 这是目前网页版实现一键复制最完美的方案
            
            st.markdown("👇 **点击右上角小图标复制译文：**")
            st.code(result, language="text")
            
            st.markdown("👇 **点击右上角小图标复制原文：**")
            st.code(text_input, language="text")
            
        else:
            st.error("❌ 翻译失败，请检查网络")

st.markdown("---")
st.caption("此输入由 neo 在 AI 上制作 | 基于 Google 神经引擎")