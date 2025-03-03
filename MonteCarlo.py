import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#######################################
# 1) Define callback function to reset defaults
#######################################
def reset_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 1.0
    st.session_state["r_slider"] = 0.05
    st.session_state["sigma_slider"] = 0.2
    st.session_state["option_type_radio"] = 'call'
    st.session_state["num_paths_slider"] = 10000

#######################################
# 2) Monte Carlo Simulation Function for European Option Pricing
#######################################
def monte_carlo_option_price(S, K, T, r, sigma, option_type='call', num_paths=10000):
    # Generate terminal stock prices using geometric Brownian motion
    Z = np.random.standard_normal(num_paths)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Calculate option payoffs
    if option_type == 'call':
        payoff = np.maximum(S_T - K, 0)
    else:
        payoff = np.maximum(K - S_T, 0)
    
    # Discount the average payoff back to present value
    price = np.exp(-r * T) * np.mean(payoff)
    return price, S_T

#######################################
# 3) Configure the Streamlit app
#######################################
st.set_page_config(layout="wide")
st.title("📊 Monte Carlo Simulation for Option Pricing")
st.markdown("Explore how random sampling and geometric Brownian motion can be used to price options. This tool simulates multiple paths to estimate a European option's price.")

# Sidebar for input parameters, disclaimers, and authorship info
with st.sidebar:
    st.header("⚙️ Parameters")
    
    # Reset button
    st.button("↺ Reset Parameters", on_click=reset_parameters)
    
    S = st.slider("Current Stock Price (S)", 50.0, 150.0, 100.0, key='S_slider')
    K = st.slider("Strike Price (K)", 50.0, 150.0, 100.0, key='K_slider')
    T = st.slider("Time to Maturity (years)", 0.1, 5.0, 1.0, key='T_slider')
    r = st.slider("Risk-Free Interest Rate (r)", 0.0, 0.2, 0.05, key='r_slider')
    sigma = st.slider("Volatility (σ)", 0.1, 1.0, 0.2, key='sigma_slider')
    option_type = st.radio("Option Type", ["call", "put"], key='option_type_radio')
    num_paths = st.slider("Number of Simulation Paths", 1000, 50000, 10000, step=1000, key='num_paths_slider')
    
    # Option to show multi-step sample paths (for full-path simulation)
    show_sample_paths = st.checkbox("Show Sample Paths (Multi-step)", value=False)
    
    st.markdown("---")
    st.markdown(
    """
    **⚠️ Disclaimer**  
    *Educational purposes only. No accuracy guarantees. Do not use options as an investment tool if you are not a qualified professional investor.*  
    
    <small>
    The author does not engage in option trading and does not endorse it for non-professional investors. 
    All information provided is for educational purposes only and should not be construed as financial or 
    investment advice. Option trading involves significant risks and may not be suitable for all investors. 
    Always consult a qualified financial professional before making any investment decisions.
    </small>
    """,
    unsafe_allow_html=True
    )
    
    st.markdown("""
    <div style="margin-top: 20px;">
        <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.en" target="_blank">
            <img src="https://licensebuttons.net/l/by-nc/4.0/88x31.png" alt="CC BY-NC 4.0">
        </a>
        <br>
        <span style="font-size: 0.8em;">By Luís Simões da Cunha</span>
    </div>
    """, unsafe_allow_html=True)

#######################################
# 4) Create tabs for different sections
#######################################
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎮 Interactive Tool", 
    "📚 Theory Behind the Model", 
    "📖 Comprehensive Tutorial", 
    "🛠️ Practical Labs",
    "🧠 The Very Basics of Options"
])

#######################################
# Tab 1: Interactive Tool
#######################################
with tab1:
    st.header("Interactive Monte Carlo Simulation Tool")
    
    # Run the Monte Carlo simulation and get the option price and simulated terminal prices
    price, S_T = monte_carlo_option_price(S, K, T, r, sigma, option_type, num_paths)
    st.success(f"### Estimated Option Price: **€{price:.2f}**")
    
    # Display two columns: one for the histogram and one for sample paths
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribution of Simulated Terminal Stock Prices")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(S_T, bins=50, color='darkorange', edgecolor='black', alpha=0.7)
        ax.set_title("Histogram of Terminal Stock Prices")
        ax.set_xlabel("Terminal Stock Price (S_T)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    
    with col2:
        if show_sample_paths:
            st.markdown("#### Sample Simulated Paths")
            num_steps = 100  # number of time steps for full path simulation
            dt = T / num_steps
            num_sample_paths = 5  # display 5 sample paths
            paths = np.zeros((num_steps + 1, num_sample_paths))
            paths[0] = S
            for i in range(1, num_steps + 1):
                Z = np.random.standard_normal(num_sample_paths)
                paths[i] = paths[i - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
            fig2, ax2 = plt.subplots(figsize=(7, 4))
            t_grid = np.linspace(0, T, num_steps + 1)
            for j in range(num_sample_paths):
                ax2.plot(t_grid, paths[:, j], label=f'Path {j+1}')
            ax2.set_title("Sample Geometric Brownian Motion Paths")
            ax2.set_xlabel("Time (Years)")
            ax2.set_ylabel("Stock Price")
            ax2.legend()
            st.pyplot(fig2)
        else:
            st.markdown("Check the box in the sidebar to view multi-step sample paths.")

############################
# Tab 2: Theory Behind the Model
############################
with tab2:
    st.markdown(r"""
    ## Monte Carlo Simulation: Theoretical Overview
    
    **What It Is:**  
    Monte Carlo simulation employs random sampling to numerically solve complex problems, 
    including the pricing of derivatives. It simulates many possible outcomes by modeling 
    the underlying asset’s evolution using a stochastic process (geometric Brownian motion).
    
    **Core Concept:**  
    For a European option, the terminal stock price $S_T$ is given by:
    
    $$
    S_T = S \cdot \exp\Bigl(\bigl(r - \tfrac{1}{2}\sigma^2\bigr)T + \sigma\sqrt{T}\,Z\Bigr), \quad Z \sim \mathcal{N}(0,1).
    $$

    The option price is then estimated by discounting the expected payoff:
    
    $$
    \text{Option Price} = e^{-rT}\,\mathbb{E}\Bigl[\max(S_T - K, 0)\Bigr].
    $$

    *(For a put option, use $\max(K - S_T, 0)$ instead.)*

    **Why Teach It:**  
    - **Flexibility:** Easily extended to path-dependent options like Asian or barrier options.  
    - **Intuition:** Visualizes the uncertainty and risk inherent in financial markets.  
    - **Practicality:** Powerful when no closed-form solution is available.
    """)


############################
# Tab 3: Comprehensive Tutorial
############################
with tab3:
    st.markdown(r"""
    ## Comprehensive Tutorial on Monte Carlo Simulation for Option Pricing
    
    **Step 1: Modeling the Underlying Asset**  
    The stock follows geometric Brownian motion. For maturity $T$, simulate 
    the terminal price $S_T$ using:
    
    $$
    S_T = S \cdot \exp\Bigl(\bigl(r - \tfrac{1}{2}\sigma^2\bigr)T + \sigma\sqrt{T}\,Z\Bigr).
    $$

    **Step 2: Calculating the Payoff**  
    - **Call Option:** $\max(S_T - K, 0)$  
    - **Put Option:** $\max(K - S_T, 0)$

    **Step 3: Discounting the Payoff**  
    Discount the expected payoff by $e^{-rT}$:
    
    $$
    \text{Option Price} = e^{-rT}\,\frac{1}{N}\sum_{i=1}^{N}\text{Payoff}_i.
    $$

    **Step 4: Averaging Over Simulations**  
    Approximate the option price by averaging discounted payoffs across all paths.

    **Example Walkthrough:**  
    1. Set $S=100$, $K=100$, $T=1$ year, $r=0.05$, $\sigma=0.2$.  
    2. Simulate 10,000 terminal stock prices.  
    3. For a call, compute $\max(S_T - 100, 0)$ for each simulation.  
    4. Discount payoffs by $e^{-0.05}$ and average to estimate the price.
    
    **Implementation Tips:**  
    - Vectorize with NumPy for efficiency.  
    - Experiment with parameter changes to observe price effects.
    """)

#######################################
# Tab 4: Practical Labs
#######################################
with tab4:
    st.header("Practical Labs for Monte Carlo Simulation")
    st.markdown("""
    Explore practical scenarios to strengthen your understanding of Monte Carlo methods in option pricing.
    
    **Lab Scenarios:**
    - **Lab 1: Convergence Analysis**  
      See how price estimates stabilize as you increase the number of paths.
    - **Lab 2: Volatility Impact**  
      Observe how higher σ affects terminal price distributions and option prices.
    - **Lab 3: Time Horizon Effects**  
      Vary T to see how longer or shorter maturities change the distribution and pricing.
    - **Lab 4: Call vs. Put Comparison**  
      Compare call and put prices under the same simulation conditions.
    - **Lab 5: Extended Applications**  
      Think about path-dependent options (e.g., Asian) by simulating the full path and averaging prices.
    """)
    
    lab_choice = st.radio(
        "Select a Lab to View:",
        ("Lab 1: Convergence Analysis",
         "Lab 2: Volatility Impact",
         "Lab 3: Time Horizon Effects",
         "Lab 4: Call vs. Put Comparison",
         "Lab 5: Extended Applications"),
        index=0
    )
    
    if lab_choice == "Lab 1: Convergence Analysis":
        st.subheader("Lab 1: Convergence Analysis")
        st.markdown("""
        **Objective:**  
        Examine how the number of simulation paths affects the accuracy and stability of the option price.
        
        **Steps:**  
        1. Move the "Number of Simulation Paths" slider in the sidebar.
        2. Notice how the price estimate stabilizes as the number of paths grows.
        """)
    elif lab_choice == "Lab 2: Volatility Impact":
        st.subheader("Lab 2: Volatility Impact")
        st.markdown("""
        **Objective:**  
        Study how volatility (σ) affects both the distribution of terminal prices and the resulting option price.
        
        **Steps:**  
        1. Adjust the "Volatility (σ)" slider.
        2. Observe the histogram and see how the option price changes.
        """)
    elif lab_choice == "Lab 3: Time Horizon Effects":
        st.subheader("Lab 3: Time Horizon Effects")
        st.markdown("""
        **Objective:**  
        Investigate how varying time to maturity (T) influences the option price and the distribution of outcomes.
        
        **Steps:**  
        1. Adjust the "Time to Maturity" slider.
        2. Compare short-dated vs. long-dated scenarios.
        """)
    elif lab_choice == "Lab 4: Call vs. Put Comparison":
        st.subheader("Lab 4: Call vs. Put Comparison")
        st.markdown("""
        **Objective:**  
        Compare pricing for calls vs. puts with the same parameters.
        
        **Steps:**  
        1. Switch between "call" and "put" in the sidebar.
        2. Note the differences in payoff structures and prices.
        """)
    else:
        st.subheader("Lab 5: Extended Applications")
        st.markdown("""
        **Objective:**  
        Consider how Monte Carlo can be extended to path-dependent derivatives.
        
        **Steps:**  
        1. To price an Asian option, simulate the entire path and average the stock price over time.
        2. Use that average in your payoff formula.
        3. This same approach generalizes to many exotic derivatives.
        """)

#######################################
# Tab 5: The Very Basics of Options
#######################################
with tab5:
    st.header("The Very Basics of Options")
    st.markdown("""
<div style="
    background-color: #f8d7da; 
    color: #721c24; 
    padding: 20px; 
    border-radius: 8px; 
    margin-bottom: 20px;
">
  <h4 style="margin-top: 0;">
    <strong>IMPORTANT DISCLAIMER</strong>
  </h4>
  <ul style="list-style-type: disc; padding-left: 1.5em;">
    <li>Options are a <em>powerful, complex tool</em> widely used by professional investors who typically have 
      <strong>many years of formal education and intensive training</strong>.</li>
    <li>Even these professionals often <strong>fail to outperform</strong> a simple buy-and-hold strategy 
      in a diversified index, as <strong>Warren Buffett</strong> and numerous 
      <strong>Nobel Prize-winning economists</strong> have demonstrated.</li>
    <li>The reality is that <strong>markets are smarter</strong> than any individual, making consistent 
      outperformance extremely difficult.</li>
    <li>If you’d like more insight into how challenging it is to "beat the market," watch 
      <a href="https://www.youtube.com/watch?v=SwkjqGd8NC4" 
         style="color: #721c24; text-decoration: underline;">How to Win the Loser's Game: Full Version</a>, 
      and explore the 
      <a href="https://rationalreminder.ca/podcast" 
         style="color: #721c24; text-decoration: underline;">Rational Reminder podcast</a>.</li>
    <li>The author’s main interest here is <strong>intellectual curiosity</strong> about the science and tools of finance, 
      not promoting active option trading.</li>
    <li>This material is <strong>purely educational</strong>. The author does <strong>not</strong> recommend any retail investor 
      engage in options trading.</li>
  </ul>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 1. What Are Options?

    **Options** are **contracts** that let you "lock in" a price to **buy** or **sell** a stock, 
    without forcing you to actually do it. Think of them like a **reservation**:
    - A **Call Option** is a reservation to **buy** a stock at a certain *strike price* before expiration.
    - A **Put Option** is a reservation to **sell** a stock at a certain *strike price* before expiration.

    ---

    ### 2. Why Do People Use Options?

    1. **Potential Profit**:  
       - If you think a stock will go **up**, you might buy a call.  
       - If you think it will go **down**, you might buy a put.
    2. **Hedging**:  
       - Protect existing stock positions from large losses by buying puts.
    3. **Income Generation**:  
       - Sell options (like insurance) to collect premium, though this carries significant risk if the market moves against you.

    ---

    ### 3. How Does Monte Carlo Fit In?

    - **Monte Carlo Simulation** helps price options by simulating many possible future stock paths.
    - It’s especially useful for **path-dependent** options (e.g., Asian, Barrier) where closed-form solutions may not exist.

    **Key Point**: You can adjust parameters (volatility, interest rates, time to expiration) to see how they affect the simulated distribution of stock prices and, in turn, the option’s estimated value.
    """)

