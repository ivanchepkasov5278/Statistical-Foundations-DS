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

    # User fills forms
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

    # Button to trigger calculation
    if st.button("Generate & Save Tree"):

        # Initialize the model logic
        model = CalculationModel(n=n_val, T=T_val, r0=r0_val, sigma=sigma_val)

        # Save to Session State for further purposes
        st.session_state["bond_model"] = model
        st.session_state["bond_model_ready"] = True

        st.toast("The Binomial Model Calculated!", icon="✅")

    # Display the results if the model exists in the session
    if st.session_state.get("bond_model_ready"):
        st.subheader("Current Short-Rate Lattice (%)")
        rate_matrix = st.session_state["bond_model"].rate_tree
        df_rates = pd.DataFrame(rate_matrix * 100)
        df_rates.index = df_rates.index[::-1]
        st.dataframe(df_rates.style.format("{:.4f}"))

###################
# ZCB Pricing Tab #
###################

with tab_zcb:
    st.subheader("Zero-Coupon Bond (ZCB) Valuation")
    st.info("The ZCB price is calculated using the corresponding binomial tree.")

    # State Check
    if not st.session_state.get("bond_model_ready"):
        st.warning("⚠️ Please generate the Interest Rate Tree first.")
    else:
        model = st.session_state["bond_model"]

        if st.button("Calculate ZCB Matrix"):
            # Calculate and store in session_state immediately
            st.session_state["zcb_matrix"] = model.get_zcb_price(t=model.n)
            st.session_state["zcb_ready"] = True
            st.toast("ZCB Matrix Сalculated!", icon="✅")

        # Display Results
        if st.session_state.get("zcb_ready"):
            current_zcb = st.session_state["zcb_matrix"]
            st.metric(label="Current ZCB Price", value=f"{current_zcb[-1, 0]:.2f}%")
            st.subheader("ZCB Valuation Matrix (%)")
            df_zcb = pd.DataFrame(current_zcb)
            df_zcb.index = df_zcb.index[::-1]
            st.dataframe(df_zcb.style.format("{:.4f}"))

#####################
# Forward Price Tab #
#####################

with tab_forward:
    st.subheader("Forward Contract Valuation")
    st.info(
        "The forward contract price of the ZCB can be calculated for a specific execution time."
    )

    # State Check
    if not st.session_state.get("zcb_ready"):
        st.warning("⚠️ You must calculate the ZCB price in the previous tab first.")
    else:
        model = st.session_state["bond_model"]

        # User Input for Expiration
        t_val = st.number_input(
            "Execution Time (t)",
            min_value=1,
            max_value=int(model.n),
            value=min(5, int(model.n)),
            key="fwd_t_input",
        )

        # Calculation Button
        if st.button("Calculate Forward Price"):
            f_price = model.get_forward_price(t=t_val)

            # Save to session_state
            st.session_state["f_price_val"] = f_price
            st.session_state["f_t_used"] = t_val
            st.session_state["forward_ready"] = True
            st.toast("Forward Price Calculated!", icon="✅")

        # Persistent Display
        if st.session_state.get("forward_ready"):
            st.metric(
                label=f"Forward Price (t={st.session_state['f_t_used']})",
                value=f"{st.session_state['f_price_val']:.2f}%",
            )

######################
# Futures Price Tab  #
######################

with tab_futures:
    st.subheader("Futures Contract Valuation")
    st.info("The value at each node is the expected value of the next period's prices.")

    # State Check
    if not st.session_state.get("zcb_ready"):
        st.warning("⚠️ You must calculate the ZCB matrix in the second tab first.")
    else:
        model = st.session_state["bond_model"]
        zcb_tree = st.session_state["zcb_matrix"]

        # User Input for Expiration
        k_val = st.number_input(
            "Futures Expiration (k)",
            min_value=1,
            max_value=int(model.n),
            value=min(6, int(model.n)),
            key="futures_k_input",
        )

        # Calculation Button
        if st.button("Calculate Futures Lattice"):
            futures_matrix = model.get_futures_price(asset_tree=zcb_tree, k=k_val)

            # Save to session_state
            st.session_state["futures_matrix"] = futures_matrix
            st.session_state["futures_k_used"] = k_val
            st.session_state["futures_ready"] = True
            st.toast("Futures lattice generated!", icon="✅")

        # Persistent Display
        if st.session_state.get("futures_ready"):

            f_matrix = st.session_state["futures_matrix"]

            # Metric for the price today
            st.metric(label=f"Current Futures Price", value=f"{f_matrix[-1, 0]:.4f}%")

            st.subheader(
                f"Futures Price Lattice (k={st.session_state['futures_k_used']})"
            )

            # Formatting the DataFrame
            df_futures = pd.DataFrame(f_matrix)
            df_futures.index = df_futures.index[::-1]
            st.dataframe(df_futures.style.format("{:.4f}"))

##########################
#  American Option Tab   #
##########################

with tab_options:
    st.subheader("American Option Valuation")
    st.info(
        "American options can be exercised at any time up to expiration. "
        "The model evaluates the 'Early Exercise' condition at every node."
    )

    # Broad State Check
    if not st.session_state.get("zcb_ready"):
        st.warning("⚠️ You must calculate the ZCB matrix in the second tab first.")
    else:
        model = st.session_state["bond_model"]

        # Asset Selection Logic
        st.markdown("### Asset Configuration")
        asset_choice = st.radio(
            "Select Underlying Asset:",
            ["Futures Contract", "Zero-Coupon Bond (ZCB)"],
            horizontal=True,
            key="underlying_selector",
        )

        # Specific State Checks for the chosen asset
        asset_ready = False
        underlying_tree = None

        if asset_choice == "Zero-Coupon Bond (ZCB)":
            if st.session_state.get("zcb_ready"):
                underlying_tree = st.session_state["zcb_matrix"]
                asset_ready = True
            else:
                st.error(
                    "❌ You must calculate the ZCB Matrix in the 'ZCB Pricing' tab first."
                )

        else:  # Futures Contract
            if st.session_state.get("futures_ready"):
                underlying_tree = st.session_state["futures_matrix"]
                asset_ready = True
            else:
                st.error(
                    "❌ You must calculate the Futures Lattice in the 'Futures Price' tab first."
                )

        # Input Parameters (Only show if asset is ready)
        if asset_ready:
            col_opt1, col_opt2, col_opt3 = st.columns(3)

            with col_opt1:
                strike = st.number_input(
                    "Strike Price (E)", value=70, step=1, key="opt_strike"
                )

            with col_opt2:
                option_type = st.selectbox(
                    "Option Type", ["Call", "Put"], key="opt_type"
                )

            with col_opt3:
                max_k = underlying_tree.shape[1] - 1
                k_val_opt = st.number_input(
                    "Expiration (k)",
                    min_value=1,
                    max_value=max_k,
                    value=max_k,
                    key="opt_k",
                )

            # Calculation
            if st.button("Calculate American Option"):
                # Pass k_val_opt instead of the raw shape
                opt_matrix = model.get_american_option_price(
                    asset_tree=underlying_tree,
                    k=k_val_opt,
                    call=(option_type == "Call"),
                    strike=strike,
                )

                st.session_state["opt_matrix"] = opt_matrix
                st.session_state["opt_ready"] = True
                st.session_state["opt_asset_used"] = asset_choice
                st.toast(f"Option on {asset_choice} Calculated!", icon="✅")

            # Persistent Display
            if st.session_state.get("opt_ready"):
                st.metric(
                    label=f"American {option_type} on {st.session_state['opt_asset_used']}",
                    value=f"{st.session_state['opt_matrix'][-1, 0]:.4f}%",
                )

                df_opt = pd.DataFrame(st.session_state["opt_matrix"])
                df_opt.index = df_opt.index[::-1]
                st.dataframe(df_opt.style.format("{:.4f}"))
