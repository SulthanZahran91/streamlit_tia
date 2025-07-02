import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- App Title ---
st.title("Interactive Profitability Model")
st.markdown("Use the sliders in the sidebar to adjust the model parameters and see how they affect the profit curves.")

# --- Sidebar for Sliders ---
st.sidebar.header("Model Parameters")

# 1) Core economic parameters
st.sidebar.subheader("1) Core Economic Parameters")
pi      = st.sidebar.slider("Potential profit per outlet (π)", 0.0, 1.0, 0.23, 0.01)
C_op    = st.sidebar.slider("Constant operational cost (C_op)", 0.0, 1.0, 0.20, 0.01)

# 2) Endogenous-overhead parameters
st.sidebar.subheader("2) Endogenous Overhead")
H       = st.sidebar.slider("Fixed HQ overhead (H)", 0.0, 5e7, 1e7, step=1e6, format="%.0e")
v       = st.sidebar.slider("Per-outlet variable cost (v)", 0.0, 5e4, 5e3, step=1e3, format="%.0e")
N       = st.sidebar.slider("Total number of outlets (N)", 1, 10000, 500, 50)

# 3) Effort / incentive parameters
st.sidebar.subheader("3) Effort & Incentives")
a_star  = st.sidebar.slider("Chosen effort level (a*)", 0.0, 10.0, 1.0, 0.1)
beta    = st.sidebar.slider("Franchisee efficiency (β)", 0.1, 10.0, 1.0, 0.1)
kappa   = st.sidebar.slider("Effort cost curvature (κ)", 0.1, 10.0, 1.0, 0.1)

# 4) Duplication-penalty parameter
st.sidebar.subheader("4) Duplication Penalty")
delta   = st.sidebar.slider("Duplication penalty (δ)", 0.0, 1.0, 0.10, 0.01)


# --- Model Calculations ---

# Model helper functions
c = lambda a: 0.5 * kappa * a**2
p = lambda a: 1 - np.exp(-beta * a)
C_op_F = lambda F: H + v * (1 - F) * N

# Domain of F (Franchise Ratio)
F = np.linspace(0, 1, 200)

# Compute profit curves
# Using np.maximum to prevent negative profits for C_op_F calculation
P_base = (1 - F) * (pi - C_op) + F * (p(a_star) * pi - c(a_star))
P_endh = (1 - F) * (pi - C_op_F(F)/N) + F * (p(a_star) * pi - c(a_star)) # Note: C_op_F is a total cost, so we divide by N for per-outlet cost
P_dup  = P_endh - delta * F * (1 - F)


# --- Plotting ---
# --- Plotting ---
plt.style.use('seaborn-v0_8-darkgrid') # Use a visually appealing style
fig, ax = plt.subplots(figsize=(10, 7)) # Make the figure a bit taller

# Plot each curve with thicker lines and distinct styles for clarity
ax.plot(F, P_base, label="P_base: Baseline Profit", linewidth=2.5)
ax.plot(F, P_endh, label="P_endh: Endogenous Overhead", linewidth=2.5, linestyle='--')
ax.plot(F, P_dup,  label="P_dup: Duplication Penalty", linewidth=2.0, linestyle=':')

ax.set_title("Profitability Models vs. Franchise Ratio", fontsize=16, weight='bold')
ax.set_xlabel("Franchise Ratio (F)", fontsize=12)
ax.set_ylabel("System Profit per Outlet (P)", fontsize=12)

# Enhance grid and legend
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(title="Profit Models", fontsize=10)

# Make the zero line more prominent
ax.axhline(0, color='lightgray', linewidth=1.0, linestyle='-')

# --- DYNAMIC Y-AXIS LIMITS ---
# This is the most important fix. It calculates the limits based on the
# actual data being plotted, ensuring all lines are visible.
all_p_values = np.concatenate([P_base, P_endh, P_dup])
p_min, p_max = all_p_values.min(), all_p_values.max()
padding = (p_max - p_min) * 0.1 # Add 10% padding to the top and bottom
ax.set_ylim(p_min - padding, p_max + padding)

# Display plot in Streamlit
st.pyplot(fig)


# --- Displaying The Equations ---
st.header("Model Equations")
st.markdown("Where **F** is the Franchise Ratio (the proportion of outlets that are franchised).")

st.subheader("Profit Curves")
st.latex(r'''
P_{\text{base}}(F) = (1-F)(\pi - C_{\text{op}}) + F \cdot (p(a^*) \cdot \pi - c(a^*))
''')
st.latex(r'''
P_{\text{endh}}(F) = (1-F) \left( \pi - \frac{C_{\text{op,F}}(F)}{N} \right) + F \cdot (p(a^*) \cdot \pi - c(a^*))
''')
st.latex(r'''
P_{\text{dup}}(F) = P_{\text{endh}}(F) - \delta \cdot F \cdot (1-F)
''')

st.subheader("Helper Functions")
st.latex(r'''
p(a) = 1 - e^{-\beta a} \quad (\text{Probability of success})
''')
st.latex(r'''
c(a) = \frac{1}{2} \kappa a^2 \quad (\text{Cost of effort})
''')
st.latex(r'''
C_{\text{op,F}}(F) = H + v \cdot (1-F) \cdot N \quad (\text{Total operational cost})
''')