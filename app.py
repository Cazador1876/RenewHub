import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RenewHub | Global Renewable Energy Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# MASTER CSS  — dark atlas aesthetic, cinematic transitions
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root tokens ── */
:root {
  --bg:        #090e1a;
  --bg2:       #0d1526;
  --bg3:       #111d35;
  --card:      #12203d;
  --border:    #1e3358;
  --accent1:   #00d4ff;
  --accent2:   #00ff9d;
  --accent3:   #f7b731;
  --text:      #e8f4fd;
  --muted:     #7a9cc0;
  --glow1:     rgba(0,212,255,0.18);
  --glow2:     rgba(0,255,157,0.15);
  --r:         14px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070c18 0%, #0b1628 60%, #0d1f3c 100%) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Hide default header ── */
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 1.5rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Sidebar brand ── */
.rh-brand {
  text-align: center;
  padding: 1.4rem 0 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0.8rem;
}
.rh-brand .logo-ring {
  width: 64px; height: 64px;
  border-radius: 50%;
  background: conic-gradient(var(--accent1), var(--accent2), var(--accent3), var(--accent1));
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 0.7rem;
  animation: spin 8s linear infinite;
  position: relative;
}
.rh-brand .logo-ring::after {
  content: '⚡';
  font-size: 26px;
  width: 54px; height: 54px;
  background: var(--bg);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
@keyframes spin { to { transform: rotate(360deg); } }

.rh-brand h1 {
  font-family: 'Syne', sans-serif;
  font-size: 1.55rem;
  font-weight: 800;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0; letter-spacing: 1px;
}
.rh-brand p {
  font-size: 0.68rem;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0.2rem 0 0;
}

/* ── Nav pills ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  color: var(--text) !important;
}
[data-testid="stSelectbox"] label {
  font-family: 'Syne', sans-serif !important;
  font-size: 0.75rem !important;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--muted) !important;
}

/* ── Sidebar info box ── */
.rh-info {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent2);
  border-radius: var(--r);
  padding: 0.9rem 1rem;
  font-size: 0.78rem;
  color: var(--muted) !important;
  margin-top: 1rem;
}
.rh-info strong { color: var(--accent2) !important; }

/* ── Hero banner ── */
.hero-wrap {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 2rem;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.hero-wrap img {
  width: 100%; height: 320px;
  object-fit: cover;
  display: block;
  filter: brightness(0.55) saturate(1.2);
  transition: transform 8s ease;
}
.hero-wrap:hover img { transform: scale(1.04); }
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(135deg,
    rgba(0,0,0,0.6) 0%,
    rgba(0,212,255,0.07) 50%,
    rgba(0,0,0,0.2) 100%);
  display: flex; flex-direction: column;
  justify-content: center; padding: 2.5rem 3rem;
}
.hero-tag {
  display: inline-block;
  background: rgba(0,212,255,0.18);
  border: 1px solid var(--accent1);
  border-radius: 99px;
  padding: 0.25rem 0.9rem;
  font-size: 0.72rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent1);
  margin-bottom: 0.9rem;
  width: fit-content;
  animation: fadeSlide 0.7s ease both;
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1.15;
  color: #fff;
  margin: 0 0 0.6rem;
  animation: fadeSlide 0.9s ease both;
}
.hero-title span {
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 1rem;
  color: rgba(255,255,255,0.7);
  max-width: 520px;
  animation: fadeSlide 1.1s ease both;
}
@keyframes fadeSlide {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Section header ── */
.section-hdr {
  display: flex; align-items: center; gap: 0.8rem;
  margin-bottom: 1.4rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.7rem;
}
.section-hdr .icon {
  width: 38px; height: 38px;
  background: var(--glow1);
  border: 1px solid var(--border);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.15rem;
}
.section-hdr h2 {
  font-family: 'Syne', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text) !important;
  margin: 0;
}
.section-hdr p {
  margin: 0;
  font-size: 0.78rem;
  color: var(--muted);
}

/* ── Stat cards ── */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.8rem;
  animation: fadeSlide 0.8s ease both;
}
.stat-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.2rem 1.4rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(0,212,255,0.1);
}
.stat-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px;
}
.stat-card.c1::before { background: linear-gradient(90deg, var(--accent1), transparent); }
.stat-card.c2::before { background: linear-gradient(90deg, var(--accent2), transparent); }
.stat-card.c3::before { background: linear-gradient(90deg, var(--accent3), transparent); }
.stat-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--muted);
  margin-bottom: 0.4rem;
}
.stat-value {
  font-family: 'Syne', sans-serif;
  font-size: 1.7rem;
  font-weight: 800;
  color: #fff;
  line-height: 1;
}
.stat-delta {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}
.stat-delta.up   { color: var(--accent2); }
.stat-delta.info { color: var(--accent1); }
.stat-delta.warn { color: var(--accent3); }
.stat-icon {
  position: absolute; right: 1rem; top: 50%;
  transform: translateY(-50%);
  font-size: 2.2rem;
  opacity: 0.12;
}

/* ── Info cards (feature grid) ── */
.feat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.6rem;
}
.feat-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.1rem 1.2rem;
  transition: box-shadow 0.2s, transform 0.2s;
}
.feat-card:hover {
  box-shadow: 0 8px 28px var(--glow2);
  transform: translateY(-2px);
}
.feat-card .fc-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.feat-card .fc-title {
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 0.92rem;
  color: var(--text);
  margin-bottom: 0.3rem;
}
.feat-card .fc-body {
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.55;
}

/* ── Result box ── */
.res-box {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 1.3rem 1.5rem;
  margin-bottom: 0.8rem;
}
.res-box .rb-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--muted);
  margin-bottom: 0.3rem;
}
.res-box .rb-val {
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
}
.rb-val.cyan  { color: var(--accent1); }
.rb-val.green { color: var(--accent2); }
.rb-val.gold  { color: var(--accent3); }

/* ── Table ── */
[data-testid="stDataFrame"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  color: var(--muted) !important;
  border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--accent1) !important;
  border-bottom: 2px solid var(--accent1) !important;
}

/* ── Sliders & inputs ── */
[data-testid="stSlider"] .rc-slider-track { background: var(--accent1) !important; }
[data-testid="stSlider"] .rc-slider-handle {
  border-color: var(--accent1) !important;
  background: var(--bg2) !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
  background: var(--bg3) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
  background: linear-gradient(135deg, var(--accent1), #0086b3) !important;
  color: #000 !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.55rem 1.5rem !important;
  transition: opacity 0.2s, transform 0.15s !important;
  box-shadow: 0 4px 18px rgba(0,212,255,0.25) !important;
}
[data-testid="stButton"] > button:hover {
  opacity: 0.88 !important;
  transform: translateY(-1px) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
  border-radius: var(--r) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
  background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
}

/* ── Metric overrides ── */
[data-testid="stMetric"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  padding: 1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'Syne', sans-serif !important; }

/* ── Plotly transparent bg ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Image sections ── */
.img-panel {
  border-radius: var(--r);
  overflow: hidden;
  position: relative;
  box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.img-panel img {
  width: 100%; display: block;
  transition: transform 6s ease;
}
.img-panel:hover img { transform: scale(1.05); }
.img-panel .img-caption {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.75));
  padding: 1rem 1.2rem 0.8rem;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.8);
}

/* ── Footer ── */
.rh-footer {
  text-align: center;
  padding: 0.6rem;
  font-size: 0.7rem;
  color: var(--muted);
  border-top: 1px solid var(--border);
  margin-top: 2rem;
}

/* ── Data editor ── */
[data-testid="stDataEditor"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label { color: var(--text) !important; }

/* ── Section divider ── */
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="rh-brand">
  <div class="logo-ring"></div>
  <h1>RenewHub</h1>
  <p>Global Energy Platform</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navigate",
    [
        "🌍 Dashboard",
        "☀️ Solar Calculator",
        "💰 Cost Comparison",
        "🔌 Bill Saver",
        "🌱 Carbon Footprint",
        "📚 Learning Portal",
    ],
)

st.sidebar.markdown("""
<div class="rh-info">
  <strong>RenewHub v2.0</strong><br>
  Built by Roboo Technicians · UET Taxila<br><br>
  <strong>Stack:</strong> Python · Streamlit · Plotly<br>
  <strong>Category:</strong> Renewable Energy ICT
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY SHARED THEME
# ─────────────────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,21,38,0.9)",
    font=dict(color="#e8f4fd", family="DM Sans"),
    margin=dict(t=50, b=40, l=30, r=20),
    xaxis=dict(gridcolor="#1e3358", zerolinecolor="#1e3358"),
    yaxis=dict(gridcolor="#1e3358", zerolinecolor="#1e3358"),
    colorway=["#00d4ff", "#00ff9d", "#f7b731", "#ff6b9d", "#a78bfa"],
)


def apply_theme(fig):
    fig.update_layout(**PLOT_LAYOUT)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 — DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if page == "🌍 Dashboard":

    # Hero
    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1509391366360-fe5bb6583e2f?auto=format&fit=crop&w=1400&q=85" />
      <div class="hero-overlay">
        <div class="hero-tag">🌍 Global Renewable Intelligence</div>
        <div class="hero-title">Power the World<br>with <span>Clean Energy</span></div>
        <div class="hero-sub">Analyse, simulate, and learn — everything you need to accelerate the energy transition.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    st.markdown("""
    <div class="stat-grid">
      <div class="stat-card c1">
        <div class="stat-label">Global Solar Potential</div>
        <div class="stat-value">173,000<span style="font-size:1rem;color:var(--muted)"> TW</span></div>
        <div class="stat-delta info">↑ Infinite & daily-renewed</div>
        <div class="stat-icon">☀️</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-label">Avg. Panel Efficiency</div>
        <div class="stat-value">22<span style="font-size:1rem;color:var(--muted)">%</span></div>
        <div class="stat-delta up">↑ +2 % YoY in 2024</div>
        <div class="stat-icon">⚡</div>
      </div>
      <div class="stat-card c3">
        <div class="stat-label">Global Net-Zero Target</div>
        <div class="stat-value">2050</div>
        <div class="stat-delta warn">IEA Scenario B</div>
        <div class="stat-icon">🌱</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Energy mix chart
    st.markdown("""
    <div class="section-hdr">
      <div class="icon">📊</div>
      <div><h2>Global Electricity Mix 2024</h2>
      <p>Renewable share by source — worldwide installed capacity</p></div>
    </div>
    """, unsafe_allow_html=True)

    mix_df = pd.DataFrame({
        "Source":  ["Solar PV", "Wind", "Hydro", "Geothermal", "Biomass", "Coal", "Gas", "Nuclear", "Oil"],
        "TWh":     [1650, 2300, 4300, 95, 640, 10200, 6500, 2800, 920],
        "Type":    ["Clean","Clean","Clean","Clean","Clean","Fossil","Fossil","Low-C","Fossil"]
    })

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = px.bar(mix_df, x="TWh", y="Source", orientation="h",
                     color="Type",
                     color_discrete_map={"Clean": "#00d4ff", "Fossil": "#ff6b4a", "Low-C": "#a78bfa"},
                     title="Global Power Generation (TWh)")
        apply_theme(fig)
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(mix_df, values="TWh", names="Source",
                      hole=0.52,
                      color_discrete_sequence=["#00d4ff","#00ff9d","#f7b731","#a78bfa","#ff9f43",
                                               "#ff6b4a","#e74c3c","#8e44ad","#95a5a6"],
                      title="Share by Source")
        apply_theme(fig2)
        fig2.update_traces(textfont_size=11)
        st.plotly_chart(fig2, use_container_width=True)

    # Three image feature cards
    st.markdown("""
    <div class="section-hdr" style="margin-top:0.5rem">
      <div class="icon">🔍</div>
      <div><h2>Explore the Platform</h2>
      <p>Six integrated modules for energy professionals & students</p></div>
    </div>
    """, unsafe_allow_html=True)

    im1, im2, im3 = st.columns(3)
    imgs = [
        ("https://images.unsplash.com/photo-1497440001374-f26997328c1b?auto=format&fit=crop&w=600&q=80",
         "☀️ Solar Calculator", "Model real-world panel output with irradiance & efficiency inputs."),
        ("https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=600&q=80",
         "💨 Cost Comparison", "Side-by-side LCOE & installation costs for all major sources."),
        ("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=600&q=80",
         "🌱 Carbon Tracker", "Quantify your footprint and plan offset strategies."),
    ]
    for col, (url, title, desc) in zip([im1, im2, im3], imgs):
        with col:
            st.markdown(f"""
            <div class="img-panel">
              <img src="{url}" style="height:180px;object-fit:cover;">
              <div class="img-caption"><strong>{title}</strong><br>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Why renewable
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-hdr">
      <div class="icon">💡</div>
      <div><h2>Why Renewable Energy?</h2></div>
    </div>
    <div class="feat-grid">
      <div class="feat-card">
        <div class="fc-icon">♾️</div>
        <div class="fc-title">Infinite Resource</div>
        <div class="fc-body">Sun, wind, and water are naturally replenished — unlike finite fossil fuels that took millions of years to form.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">🏭</div>
        <div class="fc-title">Zero Emissions</div>
        <div class="fc-body">Operating renewables produces no CO₂. Displacing coal with solar eliminates up to 950 g CO₂ per kWh.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">💵</div>
        <div class="fc-title">Falling Costs</div>
        <div class="fc-body">Solar PV LCOE fell 90 % in a decade — now the cheapest electricity source in history, per IRENA 2023.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">🔒</div>
        <div class="fc-title">Energy Security</div>
        <div class="fc-body">Local generation reduces dependence on imported fuel, stabilising national energy prices and supply chains.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">👷</div>
        <div class="fc-title">Green Jobs</div>
        <div class="fc-body">The renewable sector employed 13.7 million people globally in 2022 — growing at 5 % annually.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">🌡️</div>
        <div class="fc-title">Climate Action</div>
        <div class="fc-body">Reaching 1.5 °C target requires renewables to supply 90 % of global electricity by 2050.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 — SOLAR CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────
elif page == "☀️ Solar Calculator":

    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=1400&q=80" />
      <div class="hero-overlay">
        <div class="hero-tag">☀️ Solar PV Module</div>
        <div class="hero-title">Solar Panel<br><span>Efficiency Calculator</span></div>
        <div class="hero-sub">Model real-world output from area, irradiance, efficiency and peak sun hours.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""<div class="section-hdr"><div class="icon">⚙️</div>
        <div><h2>Panel Parameters</h2></div></div>""", unsafe_allow_html=True)

        area = st.number_input("Panel Area (m²)", min_value=0.1, value=1.6, step=0.1,
                               help="Standard residential panel: ~1.6–1.8 m²")
        intensity = st.number_input("Solar Irradiance (W/m²)", min_value=100, value=1000, step=50,
                                    help="Peak STC value = 1000 W/m². Pakistan avg: 550–700 W/m²")
        efficiency = st.slider("Panel Efficiency (%)", 5, 40, 20,
                               help="Mono-PERC: 20–22%, HJT: 22–24%, Thin-film: 10–13%")
        sun_hours  = st.slider("Daily Peak Sun Hours (h)", 1.0, 12.0, 5.5,
                               help="Islamabad ≈ 5.5h, Quetta ≈ 6.5h, Karachi ≈ 6.0h")
        temp_coeff = st.slider("Temperature Derating (%)", 0, 20, 10,
                               help="Typical modules lose ~0.4%/°C above 25°C")

        panels = st.number_input("Number of Panels", min_value=1, value=10, step=1)

    # Core calculations
    eff_real    = efficiency * (1 - temp_coeff / 100)
    power_panel = area * intensity * (eff_real / 100)
    power_total = power_panel * panels
    daily_kwh   = (power_total * sun_hours) / 1000
    monthly_kwh = daily_kwh * 30
    annual_kwh  = daily_kwh * 365
    co2_saved   = annual_kwh * 0.4  # kg
    trees_eq    = co2_saved / 20

    with right:
        st.markdown("""<div class="section-hdr"><div class="icon">📈</div>
        <div><h2>Results</h2></div></div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="res-box">
          <div class="rb-label">Output per Panel (STC-derated)</div>
          <div class="rb-val cyan">{power_panel:.1f} W</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Total Array Power ({panels} panels)</div>
          <div class="rb-val green">{power_total/1000:.2f} kW</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Daily Energy Generation</div>
          <div class="rb-val cyan">{daily_kwh:.2f} kWh/day</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Monthly / Annual Generation</div>
          <div class="rb-val gold">{monthly_kwh:.0f} kWh &nbsp;|&nbsp; {annual_kwh:.0f} kWh</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Annual CO₂ Saved (vs grid)</div>
          <div class="rb-val green">{co2_saved:.0f} kg CO₂ &nbsp;≈&nbsp; {trees_eq:.0f} trees/yr</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts row
    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    with c1:
        gap_df = pd.DataFrame({
            "Type": ["Theoretical Max", "Temp-Derated", "Actual Output"],
            "Power (W)": [area*intensity, area*intensity*(efficiency/100), power_panel]
        })
        fig = px.bar(gap_df, x="Type", y="Power (W)", color="Type",
                     color_discrete_sequence=["#1e3358", "#00d4ff", "#00ff9d"],
                     title="Efficiency Waterfall (per panel)")
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Sun hours sensitivity
        hrs = list(range(1, 13))
        fig2 = go.Figure(go.Scatter(
            x=hrs,
            y=[(power_total * h) / 1000 for h in hrs],
            mode="lines+markers",
            line=dict(color="#00d4ff", width=2.5),
            marker=dict(color="#00ff9d", size=7),
            fill="tozeroy",
            fillcolor="rgba(0,212,255,0.08)"
        ))
        fig2.add_vline(x=sun_hours, line_dash="dot", line_color="#f7b731",
                       annotation_text=f"{sun_hours}h selected")
        fig2.update_layout(**PLOT_LAYOUT,
                           title="Daily Output vs. Sun Hours",
                           xaxis_title="Sun Hours",
                           yaxis_title="kWh/day")
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        # Monthly generation bar
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        season = [0.8,0.85,0.95,1.05,1.1,1.08,1.0,1.0,1.05,1.0,0.88,0.78]
        monthly_vals = [daily_kwh * 30 * s for s in season]
        fig3 = go.Figure(go.Bar(
            x=months, y=monthly_vals,
            marker=dict(
                color=monthly_vals,
                colorscale=[[0,"#0d1526"],[0.5,"#00d4ff"],[1,"#00ff9d"]],
            )
        ))
        fig3.update_layout(**PLOT_LAYOUT, title="Seasonal Generation Profile")
        st.plotly_chart(fig3, use_container_width=True)

    # Tip image strip
    st.markdown("""
    <div class="img-panel" style="margin-top:1rem">
      <img src="https://images.unsplash.com/photo-1509391366360-fe5bb6583e2f?auto=format&fit=crop&w=1400&q=75" style="height:200px;filter:brightness(0.5)saturate(1.3);">
      <div class="img-caption" style="font-size:0.88rem">
        <strong>Pro Tip:</strong> Tilt panels at your latitude angle (e.g. 33° for Islamabad) facing south
        for maximum annual yield. Clean panels fortnightly to avoid dust-related losses of up to 25%.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 — COST COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
elif page == "💰 Cost Comparison":

    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=1400&q=80" />
      <div class="hero-overlay">
        <div class="hero-tag">💰 Cost Intelligence</div>
        <div class="hero-title">Energy Source<br><span>Cost Comparison</span></div>
        <div class="hero-sub">Compare LCOE, installation, maintenance and lifetime for every major renewable source.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    data = {
        "Source":               ["Solar PV", "Wind Onshore", "Wind Offshore", "Hydro", "Geothermal", "Biomass"],
        "Install ($/kW)":       [1050, 1450, 3000, 2500, 4200, 3500],
        "O&M ($/kW·yr)":        [17,   40,   85,   30,   100,  80],
        "Lifetime (yr)":        [25,   20,   25,   50,   30,   20],
        "LCOE (¢/kWh)":         [3.7,  3.2,  8.0,  5.0,  7.0,  10.0],
        "Capacity Factor (%)":  [20,   35,   42,   45,   90,   80],
        "Eco Score":            [9, 8, 8, 7, 8, 6],
    }
    df = pd.DataFrame(data)

    st.markdown("""<div class="section-hdr"><div class="icon">📊</div>
    <div><h2>Comparison Table</h2><p>Global average figures — 2024 IRENA estimates</p></div></div>""",
                unsafe_allow_html=True)
    st.dataframe(df.style.highlight_min(subset=["LCOE (¢/kWh)","Install ($/kW)"], color="#0d2b1d")
                          .highlight_max(subset=["Lifetime (yr)","Capacity Factor (%)"], color="#0a1e30"),
                 use_container_width=True, hide_index=True)

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.scatter(df, x="Install ($/kW)", y="LCOE (¢/kWh)",
                         size="Lifetime (yr)", color="Capacity Factor (%)",
                         text="Source",
                         color_continuous_scale="Teal",
                         title="LCOE vs. Installation Cost (bubble = lifetime)")
        fig.update_traces(textposition="top center", textfont_size=11)
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        colors = ["#00d4ff","#00ff9d","#a78bfa","#f7b731","#ff6b4a","#ff9f43"]
        for i, row in df.iterrows():
            fig2.add_trace(go.Bar(
                name=row["Source"],
                x=["Install ($/kW)", "O&M ($/kW·yr)", "LCOE (¢/kWh)×100"],
                y=[row["Install ($/kW)"], row["O&M ($/kW·yr)"], row["LCOE (¢/kWh)"] * 100],
                marker_color=colors[i]
            ))
        fig2.update_layout(**PLOT_LAYOUT, barmode="group", title="Multi-Cost Comparison")
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig3 = px.bar(df, x="Source", y="Capacity Factor (%)", color="Source",
                      color_discrete_sequence=colors,
                      title="Capacity Factor by Source (%)")
        apply_theme(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.line_polar(df, r="Eco Score", theta="Source", line_close=True,
                             color_discrete_sequence=["#00ff9d"],
                             title="Eco Impact Score (0–10)")
        fig4.update_traces(fill="toself", fillcolor="rgba(0,255,157,0.12)")
        apply_theme(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    <div class="feat-grid" style="margin-top:0.5rem">
      <div class="feat-card">
        <div class="fc-icon">☀️</div>
        <div class="fc-title">Solar PV wins on cost</div>
        <div class="fc-body">Lowest LCOE globally as of 2023. Ideal for rooftop & utility-scale in sunny regions like Pakistan (Quetta: 2800+ kWh/kWp·yr).</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">💨</div>
        <div class="fc-title">Wind leads in capacity factor</div>
        <div class="fc-body">Onshore wind in Class 4+ sites (~7.5 m/s) achieves 35–42% CF — better year-round baseload than solar.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">💧</div>
        <div class="fc-title">Hydro for longevity</div>
        <div class="fc-body">50+ year asset life and 45% CF make hydro the most reliable dispatchable renewable where topography allows.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 — BILL SAVER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🔌 Bill Saver":

    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1584433144859-1fc3ab64a957?auto=format&fit=crop&w=1400&q=80" />
      <div class="hero-overlay">
        <div class="hero-tag">🔌 Bill Intelligence</div>
        <div class="hero-title">Smart Electricity<br><span>Bill Saver</span></div>
        <div class="hero-sub">Audit your appliances, predict monthly costs, and unlock personalised saving strategies.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if "appliances" not in st.session_state:
        st.session_state.appliances = [
            {"Appliance": "Air Conditioner",   "Power (W)": 1500, "Hours/Day": 8,  "Qty": 1},
            {"Appliance": "Refrigerator",       "Power (W)": 200,  "Hours/Day": 24, "Qty": 1},
            {"Appliance": "LED Lights",         "Power (W)": 60,   "Hours/Day": 6,  "Qty": 8},
            {"Appliance": "Water Heater",       "Power (W)": 2000, "Hours/Day": 1,  "Qty": 1},
            {"Appliance": "Washing Machine",    "Power (W)": 500,  "Hours/Day": 1,  "Qty": 1},
            {"Appliance": "TV + Devices",       "Power (W)": 250,  "Hours/Day": 5,  "Qty": 2},
        ]

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown("""<div class="section-hdr"><div class="icon">📋</div>
        <div><h2>Appliance Audit</h2><p>Edit rows to match your home</p></div></div>""",
                    unsafe_allow_html=True)
        edited_df = st.data_editor(
            pd.DataFrame(st.session_state.appliances),
            use_container_width=True,
            num_rows="dynamic",
        )
        unit_cost = st.number_input("Electricity Tariff (PKR or $/kWh)", value=0.15, step=0.01)

    edited_df["Daily kWh"] = (edited_df["Power (W)"] * edited_df["Hours/Day"] * edited_df.get("Qty", 1)) / 1000
    total_daily   = edited_df["Daily kWh"].sum()
    monthly_kwh_b = total_daily * 30
    monthly_bill  = monthly_kwh_b * unit_cost

    with right:
        st.markdown("""<div class="section-hdr"><div class="icon">💡</div>
        <div><h2>Bill Summary</h2></div></div>""", unsafe_allow_html=True)

        savings_led  = 0.75 * edited_df.loc[edited_df["Appliance"].str.contains("Light", na=False), "Daily kWh"].sum() * 30 * unit_cost
        savings_ac   = 0.30 * edited_df.loc[edited_df["Appliance"].str.contains("Air", na=False),   "Daily kWh"].sum() * 30 * unit_cost

        st.markdown(f"""
        <div class="res-box">
          <div class="rb-label">Estimated Monthly Bill</div>
          <div class="rb-val {'cyan' if monthly_bill < 30 else 'gold' if monthly_bill < 80 else 'cyan'}">
            ${monthly_bill:.2f}
          </div>
        </div>
        <div class="res-box">
          <div class="rb-label">Monthly Consumption</div>
          <div class="rb-val green">{monthly_kwh_b:.1f} kWh</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Potential Savings — Switch to LED</div>
          <div class="rb-val gold">${savings_led:.2f} / month</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Potential Savings — 5-Star AC</div>
          <div class="rb-val gold">${savings_ac:.2f} / month</div>
        </div>
        """, unsafe_allow_html=True)

        level = min(monthly_bill / 100, 1.0)
        st.progress(level, text=f"Bill intensity: {'🟢 Low' if level<0.4 else '🟡 Medium' if level<0.7 else '🔴 High'}")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(edited_df, values="Daily kWh", names="Appliance",
                     hole=0.5,
                     color_discrete_sequence=["#00d4ff","#00ff9d","#f7b731","#a78bfa","#ff9f43","#ff6b4a"],
                     title="Daily kWh Breakdown by Appliance")
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Weekly projection
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        variation = [1.0, 0.95, 0.98, 1.02, 1.05, 1.2, 1.15]
        daily_proj = [total_daily * v for v in variation]
        fig2 = go.Figure(go.Bar(
            x=days, y=daily_proj,
            marker=dict(color=daily_proj,
                        colorscale=[[0,"#0d2540"],[0.5,"#00d4ff"],[1,"#f7b731"]]),
        ))
        fig2.update_layout(**PLOT_LAYOUT, title="Typical Weekly Usage (kWh/day)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="section-hdr"><div class="icon">💰</div>
    <div><h2>Energy Saving Strategies</h2></div></div>
    <div class="feat-grid">
      <div class="feat-card">
        <div class="fc-icon">🌡️</div>
        <div class="fc-title">AC Smart Settings</div>
        <div class="fc-body">Set AC to 24–26°C — each degree below 24 adds ~6% energy use. Use inverter ACs rated 5-star for 40–50% savings.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">💡</div>
        <div class="fc-title">LED Lighting</div>
        <div class="fc-body">Replace all incandescent bulbs with LED — uses 75% less energy with 25x longer lifespan. Cheapest ROI upgrade.</div>
      </div>
      <div class="feat-card">
        <div class="fc-icon">🔌</div>
        <div class="fc-title">Kill Phantom Load</div>
        <div class="fc-body">Idle electronics (TVs, chargers on standby) waste 5–10% of household energy. Use smart power strips.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 — CARBON FOOTPRINT
# ─────────────────────────────────────────────────────────────────────────────
elif page == "🌱 Carbon Footprint":

    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1400&q=80" />
      <div class="hero-overlay">
        <div class="hero-tag">🌱 Climate Intelligence</div>
        <div class="hero-title">Carbon Footprint<br><span>Calculator</span></div>
        <div class="hero-sub">Measure your household or facility CO₂ output and design an offset roadmap.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("""<div class="section-hdr"><div class="icon">⚙️</div>
        <div><h2>Your Activity Data</h2></div></div>""", unsafe_allow_html=True)

        monthly_kwh_c = st.number_input("Monthly Electricity (kWh)", value=350)
        gas_usage     = st.number_input("Monthly Gas Usage (Therms)", value=20)
        transport_km  = st.number_input("Monthly Car Travel (km)", value=800)
        flights       = st.number_input("Flights per year", value=2, step=1)
        waste         = st.slider("Monthly Waste Generated (kg)", 0, 150, 25)
        diet          = st.selectbox("Diet Type", ["Vegan", "Vegetarian", "Flexitarian", "Omnivore", "High-Meat"])

        diet_factor = {"Vegan":0.8, "Vegetarian":1.2, "Flexitarian":1.8, "Omnivore":2.5, "High-Meat":3.3}[diet]

    ELEC    = 0.4
    GAS     = 5.3
    TRANS   = 0.21   # kg CO2/km
    FLIGHT  = 255    # kg CO2/flight (avg)
    WASTE   = 0.5

    monthly_co2 = (monthly_kwh_c * ELEC) + (gas_usage * GAS) + \
                  (transport_km * TRANS) + (flights * FLIGHT / 12) + \
                  (waste * WASTE) + (diet_factor * 30)

    annual_co2  = monthly_co2 * 12
    trees_needed = annual_co2 / 20
    world_avg   = 4600  # kg/yr
    pct         = annual_co2 / world_avg * 100

    with right:
        st.markdown("""<div class="section-hdr"><div class="icon">📊</div>
        <div><h2>Your Footprint</h2></div></div>""", unsafe_allow_html=True)

        color = "#00ff9d" if annual_co2 < 3000 else "#f7b731" if annual_co2 < 6000 else "#ff6b4a"
        st.markdown(f"""
        <div class="res-box">
          <div class="rb-label">Monthly CO₂ Footprint</div>
          <div class="rb-val" style="color:{color}">{monthly_co2:.0f} kg CO₂</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Annual CO₂ Footprint</div>
          <div class="rb-val" style="color:{color}">{annual_co2:.0f} kg CO₂/yr</div>
        </div>
        <div class="res-box">
          <div class="rb-label">vs World Average (4,600 kg/yr)</div>
          <div class="rb-val gold">{pct:.0f}%</div>
        </div>
        <div class="res-box">
          <div class="rb-label">Trees Required to Offset (1 yr)</div>
          <div class="rb-val green">{int(trees_needed)} trees</div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=annual_co2,
            delta={"reference": world_avg, "valueformat": ".0f",
                   "increasing": {"color": "#ff6b4a"}, "decreasing": {"color": "#00ff9d"}},
            number={"suffix": " kg", "font": {"color": color}},
            title={"text": "Annual CO₂ (kg)", "font": {"color": "#e8f4fd"}},
            gauge={
                "axis": {"range": [0, 12000], "tickcolor": "#7a9cc0"},
                "bar":  {"color": color},
                "bgcolor": "#0d1526",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 2000],    "color": "#0d2b1d"},
                    {"range": [2000, 5000], "color": "#1c2a0d"},
                    {"range": [5000, 12000],"color": "#2b1212"},
                ],
                "threshold": {"line": {"color": "#f7b731", "width": 3},
                              "thickness": 0.75, "value": world_avg}
            }
        ))
        fig_g.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#e8f4fd"), height=280,
                            margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    sources = ["Electricity", "Gas", "Transport", "Flights", "Waste", "Diet"]
    vals    = [monthly_kwh_c*ELEC, gas_usage*GAS, transport_km*TRANS,
               flights*FLIGHT/12, waste*WASTE, diet_factor*30]

    with c1:
        fig = px.pie(values=vals, names=sources,
                     hole=0.5, title="Monthly Footprint Breakdown",
                     color_discrete_sequence=["#00d4ff","#00ff9d","#f7b731","#ff9f43","#a78bfa","#ff6b4a"])
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # 12-month projection
        months2 = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        m_vals  = [monthly_co2 * s for s in [1.1,1.05,0.95,0.9,0.85,0.8,0.82,0.85,0.9,1.0,1.05,1.12]]
        fig2 = go.Figure(go.Scatter(
            x=months2, y=m_vals,
            fill="tozeroy",
            line=dict(color="#00d4ff", width=2.5),
            fillcolor="rgba(0,212,255,0.07)"
        ))
        fig2.update_layout(**PLOT_LAYOUT, title="Monthly CO₂ Projection (kg)")
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        cats = ["Your Footprint", "World Avg", "EU Avg", "UK Target 2030", "Net Zero"]
        vals2= [annual_co2/1000, 4.6, 6.8, 2.5, 0.0]
        fig3 = go.Figure(go.Bar(
            x=cats, y=vals2,
            marker_color=["#00d4ff","#f7b731","#ff9f43","#00ff9d","#a78bfa"],
        ))
        fig3.update_layout(**PLOT_LAYOUT, title="CO₂ Benchmarks (tonne/yr)", yaxis_title="t CO₂/yr")
        st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6 — LEARNING PORTAL
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📚 Learning Portal":

    st.markdown("""
    <div class="hero-wrap">
      <img src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1400&q=80" />
      <div class="hero-overlay">
        <div class="hero-tag">📚 Knowledge Hub</div>
        <div class="hero-title">Renewable Energy<br><span>Learning Portal</span></div>
        <div class="hero-sub">Knowledge base · Interactive quiz · Scientific unit converter — all in one place.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 Knowledge Base", "❓ Quiz", "🧮 Unit Converter"])

    # ── TAB 1 — KNOWLEDGE BASE
    with tab1:
        st.markdown("""<div class="section-hdr"><div class="icon">📖</div>
        <div><h2>Renewable Energy 101</h2><p>Expand any topic to learn more</p></div></div>""",
                    unsafe_allow_html=True)

        topics = [
            ("☀️ Solar Photovoltaic (PV)",
             "Solar PV converts sunlight directly into electricity through the photovoltaic effect. "
             "When photons hit a semiconductor (typically silicon), they knock electrons loose, "
             "creating a direct current (DC). An inverter converts this to AC for household use. "
             "Modern mono-crystalline panels achieve 20–24% efficiency. Pakistan has 300+ sunny days/year "
             "— making it one of the highest-potential solar markets globally.",
             "https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?auto=format&fit=crop&w=800&q=70"),

            ("💨 Wind Power",
             "Wind turbines extract kinetic energy from moving air. A typical 3-blade horizontal-axis "
             "turbine with a 90 m rotor diameter captures energy according to P = ½ρAv³, where ρ is "
             "air density, A is swept area, and v is wind speed. Even doubling wind speed increases "
             "power 8×. Onshore wind LCOE now rivals natural gas in most markets.",
             "https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=800&q=70"),

            ("💧 Hydroelectric Power",
             "Hydro converts gravitational potential energy of water into electricity. Power = ρgQh·η, "
             "where Q is flow rate (m³/s), h is head height (m), and η is turbine efficiency (~90%). "
             "It provides 16% of world electricity — the largest renewable source. Run-of-river plants "
             "have minimal environmental impact vs large reservoirs.",
             "https://images.unsplash.com/photo-1555566084-a5b5f2e6e8e1?auto=format&fit=crop&w=800&q=70"),

            ("🌋 Geothermal Energy",
             "Heat from Earth's core (~5500°C) is accessed by drilling wells 1–10 km deep. "
             "Steam or hot water drives turbines. Capacity factors reach 85–95% — nearly baseload "
             "reliability. Iceland gets 30% of electricity from geothermal. Pakistan's Thar and "
             "Balochistan regions have untapped geothermal potential.",
             "https://images.unsplash.com/photo-1496483648148-47c686dc86a8?auto=format&fit=crop&w=800&q=70"),

            ("🔋 Energy Storage & Grid",
             "Intermittent renewables (solar, wind) require storage or grid balancing. Lithium-ion "
             "battery costs fell 97% since 1991 — now $139/kWh. Pumped hydro stores 94% of global "
             "grid energy. Emerging: green hydrogen, flow batteries, compressed air, gravity storage.",
             "https://images.unsplash.com/photo-1618044733300-9472054094ee?auto=format&fit=crop&w=800&q=70"),
        ]

        for title, body, img_url in topics:
            with st.expander(title):
                co1, co2 = st.columns([2, 1])
                with co1:
                    st.markdown(f"""<p style="color:var(--muted);font-size:0.88rem;line-height:1.7">{body}</p>""",
                                unsafe_allow_html=True)
                with co2:
                    st.markdown(f"""
                    <div class="img-panel">
                      <img src="{img_url}" style="height:130px;object-fit:cover;">
                    </div>""", unsafe_allow_html=True)

    # ── TAB 2 — QUIZ
    with tab2:
        st.markdown("""<div class="section-hdr"><div class="icon">❓</div>
        <div><h2>Test Your Knowledge</h2><p>5-question renewable energy quiz</p></div></div>""",
                    unsafe_allow_html=True)

        questions = [
            ("Which source is NOT renewable?",
             ["Solar", "Coal", "Wind", "Hydro"], "Coal",
             "Coal is a fossil fuel formed over millions of years — not replenished on human timescales."),
            ("What does LCOE stand for?",
             ["Lowest Cost of Energy", "Levelised Cost of Energy", "Linear Cost over Emissions", "Load Cost of Equipment"],
             "Levelised Cost of Energy",
             "LCOE is the average net present cost of electricity over a generator's lifetime — the standard metric for comparing energy sources."),
            ("Which renewable has the highest capacity factor?",
             ["Solar PV", "Onshore Wind", "Geothermal", "Tidal"],
             "Geothermal",
             "Geothermal plants run at 85–95% capacity factor — near-baseload reliability since heat is always available underground."),
            ("Solar PV converts sunlight into electricity via the:",
             ["Thermal effect", "Photovoltaic effect", "Piezoelectric effect", "Thermoelectric effect"],
             "Photovoltaic effect",
             "The PV effect — discovered by Edmond Becquerel in 1839 — is when photons knock electrons loose in a semiconductor, generating current."),
            ("IEA's Net Zero scenario requires renewables to supply ___ of global electricity by 2050:",
             ["50%", "70%", "90%", "100%"],
             "90%",
             "The IEA Net Zero Emissions by 2050 report targets ~90% renewable electricity share, with the remainder from nuclear and low-carbon dispatchable sources."),
        ]

        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}
        if "quiz_submitted" not in st.session_state:
            st.session_state.quiz_submitted = False

        for i, (q, opts, _, _) in enumerate(questions):
            key = f"q{i}"
            st.markdown(f"**Q{i+1}. {q}**")
            st.session_state.quiz_answers[key] = st.radio("", opts, key=key, label_visibility="collapsed")
            st.markdown("")

        if st.button("✅ Submit Quiz"):
            st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:
            score = 0
            for i, (q, opts, correct, explanation) in enumerate(questions):
                key = f"q{i}"
                ans = st.session_state.quiz_answers.get(key)
                if ans == correct:
                    st.success(f"Q{i+1} ✅ Correct! — {explanation}")
                    score += 1
                else:
                    st.error(f"Q{i+1} ❌ Correct answer: **{correct}** — {explanation}")

            pct_score = score / len(questions) * 100
            st.markdown(f"""
            <div class="res-box" style="margin-top:1rem;text-align:center">
              <div class="rb-label">Your Score</div>
              <div class="rb-val {'green' if pct_score>=80 else 'gold' if pct_score>=60 else 'cyan'}">{score}/{len(questions)} — {pct_score:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 3 — UNIT CONVERTER
    with tab3:
        st.markdown("""<div class="section-hdr"><div class="icon">🧮</div>
        <div><h2>Scientific Unit Converter</h2><p>Energy, power & emissions</p></div></div>""",
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("⚡ Energy Converter")
            val_e = st.number_input("Value", value=1.0, key="eval")
            from_e = st.selectbox("From", ["kWh", "Joules", "Calories (kcal)", "BTU", "MWh", "toe"])

            ENERGY_J = {"kWh": 3.6e6, "Joules": 1, "Calories (kcal)": 4184,
                        "BTU": 1055.06, "MWh": 3.6e9, "toe": 4.187e10}
            val_j = val_e * ENERGY_J[from_e]

            st.markdown(f"""
            <div class="res-box">
              <div class="rb-label">Equivalent Values</div>
              <div class="fc-body" style="color:var(--text)">
                🔵 <b>{val_j/3.6e6:.4f} kWh</b><br>
                🟢 <b>{val_j:,.0f} J</b><br>
                🟡 <b>{val_j/4184:.2f} kcal</b><br>
                🔴 <b>{val_j/1055.06:.2f} BTU</b><br>
                🟣 <b>{val_j/3.6e9:.6f} MWh</b>
              </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.subheader("🌱 CO₂ Equivalence")
            kwh_val = st.number_input("kWh consumed", value=100.0, key="co2kwh")
            grid_factor = st.selectbox("Grid Carbon Factor",
                                       ["Pakistan (0.45 kg/kWh)", "World Avg (0.43 kg/kWh)",
                                        "EU (0.23 kg/kWh)", "France (0.06 kg/kWh)", "Custom"])
            factors = {"Pakistan (0.45 kg/kWh)": 0.45, "World Avg (0.43 kg/kWh)": 0.43,
                       "EU (0.23 kg/kWh)": 0.23, "France (0.06 kg/kWh)": 0.06}
            if grid_factor == "Custom":
                cf = st.number_input("Enter factor (kg CO₂/kWh)", value=0.45)
            else:
                cf = factors[grid_factor]

            co2 = kwh_val * cf
            trees_y = co2 / 20
            km_eq   = co2 / 0.21

            st.markdown(f"""
            <div class="res-box">
              <div class="rb-label">CO₂ Emitted</div>
              <div class="rb-val green">{co2:.2f} kg CO₂</div>
            </div>
            <div class="res-box">
              <div class="rb-label">Equivalent to</div>
              <div class="fc-body" style="color:var(--text)">
                🌳 {trees_y:.1f} trees absorbing CO₂ for 1 year<br>
                🚗 {km_eq:.0f} km driven in a petrol car<br>
                ✈️ {co2/255:.2f} average short-haul flights
              </div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rh-footer">
  🌍 RenewHub v2.0 &nbsp;·&nbsp; Built by <strong>Roboo Technicians</strong> · UET Taxila &nbsp;·&nbsp;
  Python · Streamlit · Plotly &nbsp;·&nbsp; © 2026 — Innovation for a Greener Planet
</div>
""", unsafe_allow_html=True)
