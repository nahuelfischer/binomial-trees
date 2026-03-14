import streamlit as st
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

import matplotlib.pyplot as plt

st.set_page_config(page_title="Binomial Tree Option Pricing", layout="wide")
st.title("Binomial Tree Option Pricing")

# Helper functions
def binomial_tree_option(S0, K, T, r, sigma, N, option_type="call", option_style="european"):
    """
    Compute option price using binomial tree (CRR model).
    Returns: option price, tree of stock prices, tree of option values
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    q = (np.exp(r * dt) - d) / (u - d)
    
    # Stock price tree
    S = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            S[j, i] = S0 * (u ** (i - j)) * (d ** j)
    
    # Option value tree (backward induction)
    V = np.zeros((N + 1, N + 1))
    
    # Terminal payoff
    if option_type.lower() == "call":
        V[:, N] = np.maximum(S[:, N] - K, 0)
    else:  # put
        V[:, N] = np.maximum(K - S[:, N], 0)
    
    # Backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            discounted_value = np.exp(-r * dt) * (q * V[j, i + 1] + (1 - q) * V[j + 1, i + 1])
            
            if option_style.lower() == "american":
                # American option: check for early exercise
                if option_type.lower() == "call":
                    intrinsic_value = max(S[j, i] - K, 0)
                else:  # put
                    intrinsic_value = max(K - S[j, i], 0)
                V[j, i] = max(intrinsic_value, discounted_value)
            else:
                # European option: no early exercise
                V[j, i] = discounted_value
    
    return V[0, 0], S, V

def plot_tree(S, V, N, K, option_type, option_style):
    """Plot binomial tree with stock prices and option values."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Stock price tree
    for i in range(N + 1):
        for j in range(i + 1):
            x, y = i, i - 2 * j
            ax1.plot(x, y, 'bo', markersize=6)
            ax1.text(x, y - 0.3, f"${S[j, i]:.2f}", ha='center', fontsize=8)
            if i < N:
                ax1.plot([x, x + 1], [y, y + 1], 'b-', alpha=0.3, linewidth=1)
                ax1.plot([x, x + 1], [y, y - 1], 'b-', alpha=0.3, linewidth=1)
    
    ax1.set_xlabel("Time Steps")
    ax1.set_ylabel("State")
    ax1.set_title("Stock Price Tree")
    ax1.grid(True, alpha=0.3)
    
    # Option value tree
    for i in range(N + 1):
        for j in range(i + 1):
            x, y = i, i - 2 * j
            ax2.plot(x, y, 'ro', markersize=6)
            ax2.text(x, y - 0.3, f"${V[j, i]:.2f}", ha='center', fontsize=8)
            if i < N:
                ax2.plot([x, x + 1], [y, y + 1], 'r-', alpha=0.3, linewidth=1)
                ax2.plot([x, x + 1], [y, y - 1], 'r-', alpha=0.3, linewidth=1)
    
    ax2.set_xlabel("Time Steps")
    ax2.set_ylabel("State")
    ax2.set_title(f"{option_style.capitalize()} {option_type.capitalize()} Option Value Tree (K=${K:.2f})")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Sidebar inputs
st.sidebar.header("Option Parameters")
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
option_style = st.sidebar.selectbox("Option Style", ["european", "american"])
S0 = st.sidebar.number_input("Stock Price (S₀)", value=100.0, min_value=0.1, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=0.1, step=1.0)
T = st.sidebar.number_input("Time to Maturity (years)", value=1.0, min_value=0.01, step=0.1)
r = st.sidebar.number_input("Risk-free Rate (r)", value=0.05, step=0.01, format="%.4f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.20, step=0.01, format="%.4f")
N = st.sidebar.slider("Number of Steps", 3, 50, 10)

# Calculate button
if st.sidebar.button("Calculate Option Price"):
    try:
        option_price, S, V = binomial_tree_option(S0, K, T, r, sigma, N, option_type, option_style)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Option Price", f"${option_price:.4f}")
        with col2:
            st.metric("Strike Price", f"${K:.2f}")
        with col3:
            st.metric("Stock Price", f"${S0:.2f}")
        
        st.markdown("---")
        
        # Plot trees
        fig = plot_tree(S, V, N, K, option_type, option_style)
        st.pyplot(fig)
        
        # Summary table
        st.subheader("Tree Summary")
        summary = pd.DataFrame({
            "Metric": ["Spot Price", "Strike", "Time to Maturity", "Risk-free Rate", "Volatility", "Steps", "Option Type", "Option Style"],
            "Value": [f"${S0:.2f}", f"${K:.2f}", f"{T:.2f} yr", f"{r:.2%}", f"{sigma:.2%}", N, option_type.capitalize(), option_style.capitalize()]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Calculation error: {e}")