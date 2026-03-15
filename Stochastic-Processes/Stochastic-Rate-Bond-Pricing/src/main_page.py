import pandas as pd
import streamlit as st
from engine.calculator import CalculationModel


# Page Configuration
st.set_page_config(page_title="ZCB Pricing Tool")

# Title and Description
st.markdown(
    "<h1 style='text-align: center;'>📊 Stochastic Interest Rate Modeling & Derivative Pricing</h1>",
    unsafe_allow_html=True,
)

st.divider()
st.subheader("ℹ️ Information")

with st.expander("🚀 Application Capabilities"):
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                ### 📈 1. Rate Simulation
                Visualize how interest rates evolve over time using a **Binomial Tree**. You can adjust volatility and time steps to see different market scenarios.
                
                ### 💰 2. ZCB Valuation
                Automatically calculate the price of a **Zero-Coupon Bond (ZCB)**. The tool determines the fair value today by looking at all possible future interest rate paths.
                """
            )

        with col2:
            st.markdown(
                """
                ### ⏳ 3. Forwards & Futures
                Compare the theoretical prices of **Forward** and **Futures** contracts. The model highlights the mathematical differences in how these two instruments are valued.
                
                ### ⚖️ 4. American Options
                Analyze **American Call/Put Options** on an underlying asset. This section calculates the "Early Exercise" benefit, and tells you whether it's better to hold the option or exercise it immediately.
                """
            )

with st.expander("📖 Mathematical Framework"):
    st.markdown(
        """
        * **Short-Rate Binomial Lattice**: Construction of a stochastic interest rate evolution tree using volatility-adjusted up ($u$) and down ($d$) factors.
        * **Zero-Coupon Bond (ZCB) Valuation**: Recursive backward induction to price ZCBs, ensuring no-arbitrage consistency with the short-rate process.
        * **Forward Contract Pricing**: Determination of the theoretical forward price $F_t$ for a bond, accounting for the time value of money and the term structure of interest rates.
        * **Futures Contract Valuation**: Computation of the futures price tree, distinguishing the martingality of futures from the discounting required for forwards.
        * **American-Style Derivatives**: Valuation of American options on interest rate products, incorporating the **Optimal Exercise Strategy** by evaluating the intrinsic value against the continuation value at every node.
        """
    )

st.divider()
st.subheader("🛠️ Tools")


# Custom CSS to center the tabs
st.markdown(
    """
    <style>
    button[data-baseweb="tab"] {
        margin: 0 auto;
    }
    div[data-testid="stTabs"] {
        justify-content: center;
    }
    div[data-testid="stHorizontalBlock"] {
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tabs Initialization
tab_rates, tab_zcb, tab_forward, tab_futures, tab_options = st.tabs(
    [
        "📈 Interest Rate Tree",
        "💰 ZCB Pricing",
        "⏩ Forward Price",
        "⏳ Futures Price",
        "⚖️ American Option",
    ]
)

##########################
# Interest Rate Tree Tab #
##########################

with tab_rates:

    st.subheader("Short-Rate Model Configuration")
    st.info("This tree forms the foundation for all subsequent valuations.")

    # Parameters that affect the entire lattice structure
    col_a, col_b = st.columns(2)

    # 1. User fills forms
    with col_a:
        r0_val = st.number_input(
            "Initial Rate (r0, in fractions)", value=0.05, format="%.3f", key="r0_tab"
        )
        n_val = st.number_input("Periods (n)", value=10, min_value=1, key="n_tab")

    with col_b:
        sigma_val = st.number_input(
            "Volatility (sigma)", value=0.10, format="%.3f", key="sig_tab"
        )
        T_val = st.number_input("Total Years (T)", value=10, min_value=1, key="T_tab")

    # 2. Button to trigger calculation
    if st.button("Generate & Save Tree"):
        # Initialize the model logic
        model = CalculationModel(n=n_val, T=T_val, r0=r0_val, sigma=sigma_val)

        # 3. Save to Session State for further purposes
        st.session_state["bond_model"] = model
        st.session_state["bond_model_ready"] = True

        st.toast("Model calculated!", icon="✅")

    # 4. Display the results if the model exists in the session
    if st.session_state.get("bond_model_ready"):
        st.subheader("Current Short-Rate Lattice")
        rate_matrix = st.session_state["bond_model"].rate_tree
        df_rates = pd.DataFrame(rate_matrix)
        df_rates.index = df_rates.index[::-1]
        st.dataframe(df_rates.style.format("{:.4f}"))
