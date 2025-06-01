import streamlit as st

st.set_page_config(page_title="Option Pricing App", layout="wide", initial_sidebar_state="auto")
st.title("📈 :blue[Option Pricing Dashboard]")

st.markdown("""
Choose an option product from the sidebar:
""")

st.page_link("pages/1_EuropeanOption.py", label="➡️ Go to European Option")
st.page_link("pages/2_SingleTouchOption.py", label="➡️ Go to Single Touch Option")
st.page_link("pages/3_DoubleTouchOption.py", label="➡️ Go to Double Touch Option")
st.page_link("pages/4_SingleBarrierOption.py", label="➡️ Go to Single Barrier Option")
st.page_link("pages/5_DoubleBarrierOption.py", label="➡️ Go to Double Barrier Option")

st.markdown("---")
st.caption("© 2025 Option Pricing App | Designed by Steven Wang 🚀")
