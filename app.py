import streamlit as st
import translators as ts
import time

# ==========================================
# 📱 网页版 V16.0 (手机体验优化 + Bing内核)
# ==========================================

# 1. 页面配置：设置网页标题、图标、布局
st.set_page_config(
    page_title="智能译 | Neo AI",
    page_icon="🌐",
    layout="centered", # 手机端居中显示
    initial_sidebar_state="collapsed" # 隐藏侧边栏，让界面更像App
)

# 2. 隐藏 Streamlit 默认的汉堡菜单和页脚，让界面更干净
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTextArea textarea {font-size: 16px !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. 核心逻辑函数
def is_contains_chinese(check_str):
    """判断是否包含中文"""
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translate_logic(text):
    """调用微软 Bing 进行翻译"""
    try:
        # 智能检测方向
        is_cn = is_contains_chinese(text)
        # 如果是中文 -> 译英文 (你也可以改成日文，看需求)
        # 如果是外文 -> 译中文
        target = "en" if is_cn else "zh-CN"
        
        # 调用 translators 库的 bing 引擎
        res = ts.translate_text(text, translator='bing', to_language=target)
        return True, res, target
    except Exception as e:
        return False, str(e), ""

# 4. 界面布局

# 标题栏
st.markdown("<h2 style='text-align: center; color: #333;'>🌐 中英智能互译</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey; font-size: 12px;'>微软 Bing 引擎 · 智能双向</p>", unsafe_allow_html=True)

# 输入区域 (高度适中，方便手指点击)
text_input = st.text_area(
    "输入内容",
    height=150,
    label_visibility="collapsed", # 隐藏标签，更简洁
    placeholder="在此输入中文或英文...\n\n系统会自动检测语言并互译。"
)

# 翻译按钮 (primary 类型会显示醒目的颜色，use_container_width 让按钮填满屏幕宽度)
if st.button("开始翻译", type="primary", use_container_width=True):
    if not text_input.strip():
        st.toast("⚠️ 请先输入内容") # 手机风格的轻提示
    else:
        # 显示加载转圈圈
        with st.spinner("☁️ 正在请求云端..."):
            success, result, target = translate_logic(text_input)
            
        if success:
            # 成功提示
            st.success("✅ 翻译完成")
            # 结果显示区
            st.text_area(
                "结果",
                value=result,
                height=150,
                label_visibility="collapsed"
            )
            st.caption("💡 提示：在手机上长按上方文字即可复制")
        else:
            st.error(f"❌ 翻译失败: {result}")
            st.info("请检查网络连接，或稍后再试。")

# 底部署名
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 12px; font-style: italic;'>此输入由 neo 在 AI 上制作</div>", 
    unsafe_allow_html=True
)