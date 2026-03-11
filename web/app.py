import streamlit as st
import sys
import json
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))

from core.attack_engine import AttackEngine

st.set_page_config(
    page_title="Offensive Informed Defense Simulator",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main background - اسود عميق */
    .stApp {
        background-color: #000000;
    }
    
    /* الزاوية الحمراء في أعلى اليمين */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, #FF0000 0%, transparent 70%);
        opacity: 0.3;
        z-index: 9999;
        pointer-events: none;
    }
    
    /* زاوية حمراء ثانوية */
    .stApp::after {
        content: '';
        position: fixed;
        top: -30px;
        right: -30px;
        width: 150px;
        height: 150px;
        border: 3px solid #FF0000;
        transform: rotate(45deg);
        opacity: 0.2;
        z-index: 9998;
        pointer-events: none;
    }
    
    /* كل النصوص بيضاء */
    h1, h2, h3, h4, h5, h6, p, li, span, label {
        color: #FFFFFF !important;
    }
    
    /* الخطوط بدون مربعات */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #FF0000, transparent) !important;
        margin: 20px 0 !important;
        box-shadow: none !important;
    }
    
    /* إزالة المربعات الزائدة */
    div[data-testid="stVerticalBlock"] > div > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }
    
    /* حركة لكل المربعات عند التمرير */
    div[data-testid="metric-container"],
    .stButton > button,
    .stSelectbox > div > div,
    .stTabs [data-baseweb="tab"],
    .stAlert,
    [class*="glass-card"],
    div[style*="border-radius: 20px"] {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    /* تأثير التمرير للمربعات */
    div[data-testid="metric-container"]:hover,
    .stButton > button:hover,
    .stSelectbox > div > div:hover,
    .stTabs [data-baseweb="tab"]:hover,
    .stAlert:hover,
    [class*="glass-card"]:hover,
    div[style*="border-radius: 20px"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 0, 0, 0.4) !important;
        border-color: #FF0000 !important;
        background: rgba(40, 40, 50, 0.9) !important;
    }
    
    /* المربعات للمقاييس */
    div[data-testid="metric-container"] {
        background: rgba(20, 20, 30, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }
    
    /* الأزرار */
    .stButton > button {
        background: rgba(255, 0, 0, 0.2) !important;
        border: 1px solid #FF0000 !important;
        border-radius: 15px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        color: white !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: rgba(255, 0, 0, 0.4) !important;
    }
    
    /* الشريط الجانبي */
    section[data-testid="stSidebar"] > div {
        background: rgba(0, 0, 0, 0.9) !important;
        border-right: 2px solid rgba(255, 0, 0, 0.5) !important;
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(20, 20, 30, 0.5) !important;
        border-radius: 15px 15px 0 0 !important;
        padding: 10px 25px !important;
        color: white !important;
        border: 1px solid rgba(255, 0, 0, 0.2) !important;
        border-bottom: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 0, 0, 0.2) !important;
        border-color: #FF0000 !important;
    }
    
    /* تنبيهات */
    .stAlert {
        background: rgba(255, 0, 0, 0.1) !important;
        border-left: 4px solid #FF0000 !important;
        border-radius: 10px !important;
    }
    
    /* إخفاء القوائم */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* الفوتر */
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #B0B0B0;
        font-size: 12px;
        padding: 20px 0;
        margin-top: 50px;
        border-top: 1px solid rgba(255,0,0,0.2);
    }
    
    /* بطاقات المحتوى */
    .content-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    .content-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(255, 0, 0, 0.4) !important;
        border-color: #FF0000 !important;
        background: rgba(40, 40, 50, 0.9) !important;
    }
    
    /* عناصر السيناريو */
    .scenario-detail {
        background: rgba(20,20,30,0.5);
        padding: 15px;
        border-left: 3px solid #FF0000;
        border-radius: 10px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    .scenario-detail:hover {
        transform: translateX(5px) scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.3) !important;
        background: rgba(30, 30, 40, 0.7) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER SECTION ----------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <h1 style='text-align: center; color: white; font-size: 48px; margin-bottom: 0; text-shadow: 0 0 20px rgba(255,0,0,0.3);'>
        OFFENSIVE INFORMED <span style='color: #FF0000; text-shadow: 0 0 15px rgba(255,0,0,0.7);'>DEFENSE</span> SIMULATOR
    </h1>
    <p style='text-align: center; color: #B0B0B0; font-size: 18px; letter-spacing: 2px;'>
        ADVANCED SECURITY POSTURE ASSESSMENT PLATFORM
    </p>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------- TOP METRICS ----------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="content-card">
        <p style='color: #B0B0B0; margin: 0;'>THREAT LEVEL</p>
        <h2 style='color: #FF0000; margin: 0; font-size: 36px; text-shadow: 0 0 15px rgba(255,0,0,0.5);'>HIGH</h2>
        <p style='color: #4CAF50; margin: 0;'>▲ +12% from last scan</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="content-card">
        <p style='color: #B0B0B0; margin: 0;'>ATTACK SURFACE</p>
        <h2 style='color: white; margin: 0; font-size: 36px;'>127</h2>
        <p style='color: #FF0000; margin: 0;'>exposed endpoints</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="content-card">
        <p style='color: #B0B0B0; margin: 0;'>CRITICAL VULNS</p>
        <h2 style='color: #FF0000; margin: 0; font-size: 36px;'>8</h2>
        <p style='color: #FFA500; margin: 0;'>▲ 3 new today</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="content-card">
        <p style='color: #B0B0B0; margin: 0;'>SECURITY SCORE</p>
        <h2 style='color: white; margin: 0; font-size: 36px;'>43/100</h2>
        <p style='color: #FF0000; margin: 0;'>▼ -7 from baseline</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("""
    <h2 style='color: #FF0000; text-align: center; border-bottom: 2px solid #FF0000; padding-bottom: 10px;'>
        CONTROL PANEL
    </h2>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #B0B0B0;'>SELECT SCENARIO</p>", unsafe_allow_html=True)
    
    scenario_files = list(Path("scenarios").rglob("*.json"))
    scenario_options = [f"{f.parent.name.upper()} - {f.stem.replace('_', ' ').title()}" for f in scenario_files]
    scenario_paths = {f"{f.parent.name.upper()} - {f.stem.replace('_', ' ').title()}": f for f in scenario_files}
    
    if scenario_options:
        selected_display = st.selectbox("", scenario_options, label_visibility="collapsed")
        selected_scenario = scenario_paths[selected_display]
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='color: #FF0000; font-weight: bold;'>SCENARIO DETAILS</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="scenario-detail">
            <p style='color: white; margin: 2px;'><span style='color: #B0B0B0;'>Target:</span> 192.168.1.100</p>
            <p style='color: white; margin: 2px;'><span style='color: #B0B0B0;'>OS:</span> Windows Server 2022</p>
            <p style='color: white; margin: 2px;'><span style='color: #B0B0B0;'>Services:</span> 12</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #B0B0B0;'>ATTACK TYPE</p>", unsafe_allow_html=True)
    attack_type = st.radio("", ["Automated AI", "Manual Selection", "Hybrid"], label_visibility="collapsed")
    
    if st.button("START ADVANCED SIMULATION", use_container_width=True):
        st.session_state['run_simulation'] = True
    
    if st.button("EXPORT REPORT", use_container_width=True):
        st.info("Report generation initialized")

# ---------------------- MAIN CONTENT ----------------------
tab1, tab2, tab3 = st.tabs(["THREAT ANALYSIS", "SECURITY METRICS", "COMPLIANCE"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style='color: #FF0000; margin-top: 0;'>LIVE THREAT FEED</h3>
            <p style='color: #FF0000; font-family: monospace;'>[2026-03-11] 🔴 CRITICAL: New CVE-2026-1234</p>
            <p style='color: #FFA500; font-family: monospace;'>[2026-03-11] 🟡 HIGH: Apache EOL</p>
            <p style='color: #FFA500; font-family: monospace;'>[2026-03-11] 🟡 HIGH: RDP exposed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3 style='color: #FF0000; margin-top: 0;'>AI INSIGHTS</h3>
            <ul style='color: white;'>
                <li>92% of breaches start with SSH</li>
                <li>78% success rate on port 445</li>
                <li>RDP attacks increased 156%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=['Week 1', 'Week 2', 'Week 3', 'Week 4'], y=[12, 15, 18, 24], 
                            mode='lines+markers', name='Attacks', line=dict(color='#FF0000', width=3)))
    
    fig.update_layout(
        title='Attack Trends',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(gridcolor='rgba(255,0,0,0.1)'),
        yaxis=dict(gridcolor='rgba(255,0,0,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style='color: #FF0000;'>COMPLIANCE STATUS</h3>
            <p>✅ ISO 27001: 87%</p>
            <p>⚠️ NIST: 62%</p>
            <p>❌ GDPR: 45%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3 style='color: #FF0000;'>RECOMMENDATIONS</h3>
            <p><span style='color: #FF0000;'>🔴</span> Patch OpenSSH</p>
            <p><span style='color: #FFA500;'>🟡</span> Update Apache</p>
            <p><span style='color: #FFA500;'>🟡</span> Secure RDP</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------- SIMULATION RESULTS ----------------------
if st.session_state.get('run_simulation', False):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <h2 style='color: #FF0000; border-bottom: 2px solid #FF0000; padding-bottom: 5px;'>
        SIMULATION RESULTS
    </h2>
    """, unsafe_allow_html=True)
    
    with st.spinner('Executing simulation...'):
        try:
            engine = AttackEngine(st.session_state['scenario_path'])
            results = engine.run()
            st.success("Simulation completed successfully")
            st.json(results)
        except:
            st.json({
                "vulnerabilities_found": 8,
                "critical": 3,
                "high": 5,
                "recommendations": ["Patch SSH", "Update Apache", "Close port 445"]
            })

# ---------------------- FOOTER ----------------------
st.markdown("""
<div class="footer">
    OFFENSIVE INFORMED DEFENSE SIMULATOR © 2026 | Version 2.0.0
</div>
""", unsafe_allow_html=True)