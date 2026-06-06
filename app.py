import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Configuration
st.set_page_config(
    page_title="RenewHub | Renewable Energy Smart Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for high-graphics look
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7d32, #1b5e20);
        color: white;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Logo and Navigation
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.title("⚡ RenewHub")

st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Select a Module",
    [
        "🏠 Dashboard",
        "☀️ Solar Efficiency Calculator",
        "💰 Cost Comparison App",
        "🔌 Bill Saver App",
        "🌍 Carbon Footprint Calc",
        "📚 Learning Portal"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Project:** Renewable Energy Smart Calculator  
**Built for:** Mechanical Engineering Viva  
**Tech:** Python, Streamlit, Plotly
""")

# --- MODULE 1: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🌱 RenewHub Smart Calculator Hub")
    st.markdown("Welcome to the all-in-one platform for renewable energy analysis and education.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Solar Potential", "173,000 TW", "Infinite")
    with col2:
        st.metric("Avg. Solar Panel Efficiency", "15-22%", "+2% YoY")
    with col3:
        st.metric("Carbon Reduction Target", "Net Zero", "by 2050")

    st.image("https://images.unsplash.com/photo-1509391366360-fe5bb6583e2f?auto=format&fit=crop&w=1200&q=80", caption="The Future is Green")
    
    st.header("Why Renewable Energy?")
    st.write("""
    Renewable energy is energy that is collected from renewable resources that are naturally replenished on a human timescale. 
    It includes sources such as sunlight, wind, rain, tides, waves, and geothermal heat.
    """)

# --- MODULE 2: SOLAR EFFICIENCY CALCULATOR ---
elif page == "☀️ Solar Efficiency Calculator":
    st.title("☀️ Solar Panel Efficiency Calculator")
    st.write("Calculate the real-world output of your solar installation.")

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Panel Area (m²)", min_value=0.1, value=1.6, step=0.1)
        intensity = st.number_input("Sunlight Intensity (W/m²)", min_value=100, value=1000, step=50)
        efficiency = st.slider("Panel Efficiency (%)", 5, 40, 18)
        sun_hours = st.slider("Daily Peak Sun Hours", 1.0, 12.0, 5.0)

    # Calculations
    power_gen = area * intensity * (efficiency / 100)
    daily_energy = (power_gen * sun_hours) / 1000  # kWh
    monthly_energy = daily_energy * 30

    with col2:
        st.subheader("Results")
        st.info(f"⚡ **Output Power:** {power_gen:.2f} Watts")
        st.success(f"🔋 **Daily Energy:** {daily_energy:.2f} kWh")
        st.warning(f"🗓️ **Monthly Energy:** {monthly_energy:.2f} kWh")
        
        # Visualization
        chart_data = pd.DataFrame({
            'Metric': ['Theoretical Max', 'Actual Output'],
            'Power (W)': [area * intensity, power_gen]
        })
        fig = px.bar(chart_data, x='Metric', y='Power (W)', color='Metric', title="Efficiency Gap")
        st.plotly_chart(fig, use_container_width=True)

# --- MODULE 3: COST COMPARISON APP ---
elif page == "💰 Cost Comparison App":
    st.title("💰 Renewable Energy Cost Comparison")
    st.write("Compare different energy sources for your project.")

    data = {
        "Source": ["Solar PV", "Wind", "Hydro", "Geothermal"],
        "Installation ($/kW)": [1200, 1500, 2500, 4000],
        "Maintenance ($/year)": [20, 45, 30, 100],
        "Lifetime (Years)": [25, 20, 50, 30],
        "Eco Impact": ["High", "Medium", "Very High", "High"]
    }
    df = pd.DataFrame(data)
    
    st.table(df)

    # Comparative Chart
    fig = px.bar(df, x='Source', y='Installation ($/kW)', 
                 color='Eco Impact', title="Installation Cost vs Environmental Impact")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### Key Insights:
    - **Solar** has the lowest entry cost and high eco-impact.
    - **Hydro** has high initial cost but longest lifetime (50+ years).
    - **Wind** is efficient but requires higher maintenance.
    """)

# --- MODULE 4: BILL SAVER APP ---
elif page == "🔌 Bill Saver App":
    st.title("🔌 Smart Electricity Bill Saver")
    st.write("Identify energy wastage and save on your monthly bills.")

    # Input Table
    if 'appliances' not in st.session_state:
        st.session_state.appliances = [
            {"Name": "AC", "Power (W)": 1500, "Hours": 8},
            {"Name": "Fridge", "Power (W)": 200, "Hours": 24},
            {"Name": "Lights", "Power (W)": 100, "Hours": 6}
        ]

    st.subheader("Your Appliances")
    edited_df = st.data_editor(pd.DataFrame(st.session_state.appliances))
    
    unit_cost = st.number_input("Cost per Unit ($/kWh)", value=0.15)
    
    # Calculation
    edited_df['Daily kWh'] = (edited_df['Power (W)'] * edited_df['Hours']) / 1000
    total_daily = edited_df['Daily kWh'].sum()
    monthly_bill = total_daily * 30 * unit_cost

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Monthly Bill", f"${monthly_bill:.2f}")
    with col2:
        st.metric("Total Monthly Consumption", f"{total_daily * 30:.1f} kWh")

    # Suggestions
    st.subheader("💡 Energy Saving Suggestions")
    if monthly_bill > 50:
        st.error("⚠️ Your bill is high! Consider switching to LED lights and using 5-star rated ACs.")
    else:
        st.success("✅ Your energy usage is efficient. Keep it up!")
    
    st.write("- **Unplug** idle electronics (Phantom load).")
    st.write("- **Clean** solar panels regularly for max efficiency.")
    st.write("- **Use** natural light during the day.")

# --- MODULE 5: CARBON FOOTPRINT CALC ---
elif page == "🌍 Carbon Footprint Calc":
    st.title("🌍 Carbon Footprint Calculator")
    st.write("Measure your environmental impact.")

    col1, col2 = st.columns(2)
    with col1:
        monthly_kwh = st.number_input("Monthly Electricity Usage (kWh)", value=300)
        gas_usage = st.number_input("Monthly Gas Usage (Therms)", value=20)
        waste = st.slider("Monthly Waste Generated (kg)", 0, 100, 20)
    
    # Constants (approximate)
    elec_factor = 0.4  # kg CO2 per kWh
    gas_factor = 5.3   # kg CO2 per Therm
    waste_factor = 0.5 # kg CO2 per kg waste

    total_co2 = (monthly_kwh * elec_factor) + (gas_usage * gas_factor) + (waste * waste_factor)
    trees_needed = total_co2 / 20 # 1 tree absorbs ~20kg CO2/year

    with col2:
        st.subheader("Your Impact")
        st.metric("Monthly Carbon Footprint", f"{total_co2:.2f} kg CO2")
        st.metric("Trees to Offset (per year)", f"{int(trees_needed)}")
        
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = total_co2,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CO2 Intensity (kg)"},
            gauge = {'axis': {'range': [None, 1000]},
                     'steps' : [
                         {'range': [0, 200], 'color': "lightgreen"},
                         {'range': [200, 500], 'color': "yellow"},
                         {'range': [500, 1000], 'color': "red"}],
                     'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 900}}))
        st.plotly_chart(fig, use_container_width=True)

# --- MODULE 6: LEARNING PORTAL ---
elif page == "📚 Learning Portal":
    st.title("📚 Renewable Energy Learning Portal")
    
    tab1, tab2, tab3 = st.tabs(["📖 Knowledge Base", "❓ Quiz", "🧮 Scientific Tools"])
    
    with tab1:
        st.header("Renewable Energy 101")
        with st.expander("What is Solar PV?"):
            st.write("Solar Photovoltaic (PV) is a technology that converts sunlight directly into electricity using semiconductors.")
        with st.expander("How does Wind Power work?"):
            st.write("Wind turbines use the kinetic energy of the wind to turn mechanical energy into electricity via a generator.")
        
    with tab2:
        st.header("Test Your Knowledge")
        q1 = st.radio("Which of these is NOT a renewable source?", ["Solar", "Coal", "Wind", "Hydro"])
        if st.button("Submit Quiz"):
            if q1 == "Coal":
                st.success("Correct! Coal is a fossil fuel.")
            else:
                st.error("Incorrect. Try again!")

    with tab3:
        st.header("Unit Converter")
        val = st.number_input("Enter Value", value=1.0)
        unit_from = st.selectbox("From", ["Joules", "kWh", "Calories"])
        if unit_from == "kWh":
            st.write(f"{val} kWh = {val * 3.6e6} Joules")
        elif unit_from == "Joules":
            st.write(f"{val} Joules = {val / 3.6e6:.6f} kWh")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("© 2026 RenewHub | Innovation for a Greener Planet")
