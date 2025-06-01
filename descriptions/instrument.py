import streamlit as st


def european_option():
    st.divider()
    st.markdown(
        "欧式期权（European Option）是一种金融衍生品，赋予持有人在期权到期日（maturity）以执行价格（strike price）"
        "买入或卖出标的资产的权利。"
    )

    st.markdown("欧式期权主要有两种类型：看涨期权（call option）和看跌期权（put option）。")
    st.markdown("- 看涨期权允许持有人在到期日以执行价格购买标的资产。如果到期时标的资产的价格高于行权价，持有者可以以较低的价格买入，然后以较高的市场价格卖出，从而获利。")
    st.markdown("- 看跌期权赋予持有人在到期日以执行价格出售标的资产。如果到期时标的资产的价格低于行权价，持有者可以以较高的价格卖出，然后以较低的市场价格买入，从而获利。")
