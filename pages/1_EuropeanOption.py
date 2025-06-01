import streamlit as st
import pandas as pd

from descriptions.black_scholes import model_description, european_option_pricing_formula
from descriptions.instrument import european_option
from plots import european_option_plot
from utils.constants import *
from utils.enums import EuropeanOptionType
from utils.registry import get_price, get_greeks

color = "blue"
st.title(f":{color}[**European Option**]")

with st.expander("ℹ️ Instructions", expanded=True):
    st.write(f"""
    - Select :{color}[**option parameters**] and :{color}[**pricing model/method**].
    - Click :{color}[**🚀 Show**] to see the result.
    """)

col1, col2, col3 = st.columns(3)

with col1:
    st.header(f"⚙️ :{color}[**Settings**]")
    model = st.selectbox(f":{color}[**Pricing Model**]", ["Black-Scholes", "Heston"], index=0)
    method = st.selectbox(f":{color}[**Pricing Method**]", ["Close-Form", "Monte Carlo", "PDE Finite Difference"], index=0)
    selected_greeks = st.multiselect(f":{color}[**Choose greeks**]", options=GREEKS, default=[DELTA, GAMMA, VEGA, THETA])
    st.markdown("---")
    show_button = st.button("🚀 Show", use_container_width=True)

with col2:
    st.header(f"📑 :{color}[**Attributes**]")
    # option_type = st.selectbox(f":{color}[**Option Type**]", EuropeanOptionType.to_list(case="upper"))
    option_type = st.selectbox(
        f":{color}[**Option Type**]",
        options=list(EuropeanOptionType),
        format_func=lambda m: m.value.upper()
    )
    K = st.number_input(f":{color}[**Strike Price**]", value=100.0)
    T = st.number_input(f":{color}[**Time to Maturity (years)**]", value=0.25)

with col3:
    st.header(f"🛠 :{color}[**Parameters**]")
    S = st.number_input(f":{color}[**Spot Price**]", value=100.0)
    r = st.number_input(f":{color}[**Domestic Rate (%)**]", value=3.0)
    q = st.number_input(f":{color}[**Foreign Rate (%)**]", value=1.0)
    sigma = st.number_input(f":{color}[**Volatility (%)**]", value=25.0)

r /= 100.0
q /= 100.0
sigma /= 100.0

params = dict(option_type=option_type, S=S, K=K, T=T, r=r, q=q, sigma=sigma)
inst_name = "European Option"

if show_button:
    price = get_price(model=model, instrument=inst_name, method=method, param=params)
    greeks = get_greeks(model=model, instrument=inst_name, method=method, param=params, selected=selected_greeks)

    if price is not None:
        st.success("✅ Calculation Successful!")
        st.metric(label="📈 Option Price", value=f"${price:.4f}")
        st.dataframe(pd.DataFrame(greeks).T, use_container_width=True)

        st.plotly_chart(
            european_option_plot.plot_price(model=model, instrument=inst_name, method=method, param=params)
        )

        if selected_greeks:
            st.plotly_chart(
                european_option_plot.plot_greeks(model=model, instrument=inst_name, method=method, param=params,
                                                 selected=selected_greeks)
            )
    else:
        st.warning("⚠️ This combination is not implemented yet.")


with st.expander("📚 Model Description"):
    european_option()
    model_description()
    european_option_pricing_formula()
