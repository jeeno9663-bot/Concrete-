import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# การตั้งค่าหน้าเว็บ
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design System", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# GLOBAL CSS — Engineering Dark Theme
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Base ─── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0f1117;
    color: #e2e8f0;
}
.stApp { background-color: #0f1117; }

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: #1a1f2e;
    border-right: 1px solid #2d3748;
}

/* ─── Header ─── */
.hero-block {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1a1f2e 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 40px 48px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-block::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-block::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 300px; height: 120px;
    background: radial-gradient(ellipse, rgba(16,185,129,0.08) 0%, transparent 70%);
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 0.95rem;
    color: #64748b;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.3px;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #818cf8;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 14px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}

/* ─── Section Headers ─── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid #1e293b;
}
.section-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0;
}
.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #6366f1;
    font-weight: 500;
    margin: 0;
}

/* ─── Cards / Input Groups ─── */
.card {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
    font-family: 'JetBrains Mono', monospace;
}

/* ─── Streamlit Widget Overrides ─── */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #0f1117 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stRadio"] { color: #e2e8f0 !important; }

/* ─── Slider ─── */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #6366f1 !important;
    border-color: #6366f1 !important;
}

/* ─── Buttons ─── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 14px 0 !important;
    letter-spacing: 0.3px;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background: #1e293b !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ─── Metric Cards ─── */
div[data-testid="stMetric"] {
    background: #1a1f2e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
}
div[data-testid="stMetric"] label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── Success / Warning / Error ─── */
div[data-testid="stAlert"][data-type="success"] {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
}
div[data-testid="stAlert"][data-type="warning"] {
    background: rgba(245,158,11,0.1) !important;
    border: 1px solid rgba(245,158,11,0.3) !important;
    border-radius: 10px !important;
}
div[data-testid="stAlert"][data-type="error"] {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 10px !important;
}
div[data-testid="stAlert"][data-type="info"] {
    background: rgba(99,102,241,0.1) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #a5b4fc !important;
}

/* ─── Expander ─── */
details[data-testid="stExpander"] {
    background: #1a1f2e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 10px !important;
}
details[data-testid="stExpander"] summary {
    color: #94a3b8 !important;
    font-weight: 500 !important;
}

/* ─── Dataframe ─── */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #2d3748 !important;
}

/* ─── Divider ─── */
hr { border-color: #1e293b !important; margin: 28px 0 !important; }

/* ─── Code blocks ─── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #0a0e1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #a5f3fc !important;
    font-size: 0.82rem !important;
}

/* ─── Result section ─── */
.result-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'JetBrains Mono', monospace;
    margin: 0 0 6px 0;
}
.mix-ratio-box {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-left: 3px solid #6366f1;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 16px 0;
}
.mix-ratio-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
}
.mix-ratio-label {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 4px;
}

/* ─── Footer ─── */
.footer-ref {
    background: #1a1f2e;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 32px;
}
.footer-ref-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #6366f1;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 12px;
}
.footer-ref-item {
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 6px;
    line-height: 1.6;
}

/* ─── Download button ─── */
div[data-testid="stDownloadButton"] > button {
    background: #1e293b !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    width: 100% !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    border-color: #6366f1 !important;
    color: #a5b4fc !important;
}

/* ─── st.write text ─── */
p { color: #cbd5e1; line-height: 1.7; }
label { color: #94a3b8 !important; font-size: 0.85rem !important; }

/* ─── Tab-like sub-labels ─── */
.sub-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px;
    background: rgba(99,102,241,0.1);
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO HEADER
# ==========================================
st.markdown("""
<div class="hero-block">
    <div class="hero-badge">🧱 DoE + ACI 211.1 · v2.0</div>
    <div class="hero-title">ระบบจำลองการออกแบบส่วนผสมคอนกรีตอัจฉริยะ</div>
    <div class="hero-sub">Web-Based Intelligent Concrete Mix Design Simulation System · British DoE Method × ACI 211.1-22</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# Session State
# ==========================================
if "mix_history" not in st.session_state:
    st.session_state.mix_history = pd.DataFrame(columns=["ชื่อสูตร", "กำลังอัดเป้าหมาย (MPa)", "ต้นทุนรวม (บาท)", "การปล่อย CO2 (kg)", "W/C Ratio"])
if "current_page" not in st.session_state:
    st.session_state.current_page = "mix_design"
if "submenu_design" not in st.session_state:
    st.session_state.submenu_design = True
if "submenu_result" not in st.session_state:
    st.session_state.submenu_result = False

# ==========================================
# MULTI-LEVEL SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("""
<style>
/* ── Sidebar base ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e293b !important;
    min-width: 230px !important;
}
/* ── Hide default radio styling ── */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
/* ── Sidebar button style ── */
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-family: "Space Grotesk", sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 9px 16px !important;
    width: 100% !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(99,102,241,0.1) !important;
    color: #c7d2fe !important;
}
</style>
""", unsafe_allow_html=True)

# ── Logo / App Name ──
st.sidebar.markdown("""
<div style="padding: 20px 16px 12px; border-bottom: 1px solid #1e293b; margin-bottom: 8px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
        <div style="width:32px; height:32px; background:linear-gradient(135deg,#6366f1,#8b5cf6);
                    border-radius:8px; display:flex; align-items:center; justify-content:center;
                    font-size:1rem;">🧱</div>
        <div>
            <div style="font-size:0.85rem; font-weight:700; color:#f1f5f9;
                        font-family:Space Grotesk,sans-serif;">MixDesign AI</div>
            <div style="font-size:0.65rem; color:#6366f1; font-family:JetBrains Mono,monospace;
                        letter-spacing:0.5px;">DoE + ACI 211.1-22</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Unit System (hidden label) ──
unit_system = st.sidebar.radio(
    "unit", ["SI Units (MPa, kg, mm)", "Inch-Pound Units (psi, lb, in)"],
    label_visibility="collapsed"
)

# ── Nav helper ──
def nav_item(icon, label, page_key, indent=False):
    is_active = st.session_state.current_page == page_key
    prefix = "    " if indent else ""
    bg = "rgba(99,102,241,0.18)" if is_active else "transparent"
    color = "#a5b4fc" if is_active else "#94a3b8"
    border = "border-left:3px solid #6366f1;" if is_active else "border-left:3px solid transparent;"
    pl = "28px" if indent else "14px"
    st.sidebar.markdown(f"""
    <div onclick="void(0)" style="
    background:{bg}; {border}
    padding:8px {pl}; margin:1px 8px;
    border-radius:0 8px 8px 0; cursor:pointer;
    display:flex; align-items:center; gap:9px;">
    <span style="font-size:0.85rem;">{icon}</span>
    <span style="font-size:0.82rem; font-weight:{'600' if is_active else '400'};
    color:{color}; font-family:Space Grotesk,sans-serif;">{prefix}{label}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ปุ่มแบบซ่อน Label โดยไม่ต้องใช้ label_visibility
    if st.sidebar.button(f"{label}", key=f"nav_{page_key}", use_container_width=True):
        st.session_state.current_page = page_key
        st.rerun()

def nav_group(icon, label, open_key):
    is_open = st.session_state[open_key]
    arrow = "▾" if is_open else "▸"
    st.sidebar.markdown(f"""
    <div style="padding:9px 14px; margin:1px 8px;
    display:flex; align-items:center; gap:9px;
    cursor:pointer;">
    <span style="font-size:0.85rem;">{icon}</span>
    <span style="font-size:0.82rem; font-weight:600; color:#e2e8f0;
    font-family:Space Grotesk,sans-serif; flex:1;">{label}</span>
    <span style="font-size:0.7rem; color:#6366f1;">{arrow}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # ปุ่มแบบซ่อน Label โดยไม่ต้องใช้ label_visibility
    if st.sidebar.button(f"toggle_{open_key}", key=f"grp_{open_key}", use_container_width=True):
        st.session_state[open_key] = not st.session_state[open_key]
        st.rerun()

# ── Section: หน้าหลัก ──
st.sidebar.markdown("""
<div style="padding:4px 16px; font-size:0.62rem; color:#475569;
            font-family:JetBrains Mono,monospace; letter-spacing:1px;
            text-transform:uppercase; margin-top:8px;">เมนูหลัก</div>
""", unsafe_allow_html=True)
nav_item("🏠", "Dashboard", "dashboard")

# ── Section: ออกแบบส่วนผสม (expandable) ──
st.sidebar.markdown("""
<div style="padding:4px 16px; font-size:0.62rem; color:#475569;
            font-family:JetBrains Mono,monospace; letter-spacing:1px;
            text-transform:uppercase; margin-top:12px;">การออกแบบ</div>
""", unsafe_allow_html=True)
nav_group("📐", "ออกแบบส่วนผสม", "submenu_design")
if st.session_state.submenu_design:
    nav_item("⚙️", "กำหนดเกณฑ์ออกแบบ", "mix_design", indent=True)
    nav_item("🧪", "สมบัติวัสดุ", "materials", indent=True)
    nav_item("🏗️", "หน้างาน & สารผสมเพิ่ม", "field", indent=True)
    nav_item("💰", "ประเมินต้นทุน", "cost", indent=True)

# ── Section: ผลลัพธ์ ──
st.sidebar.markdown("""
<div style="padding:4px 16px; font-size:0.62rem; color:#475569;
            font-family:JetBrains Mono,monospace; letter-spacing:1px;
            text-transform:uppercase; margin-top:12px;">ผลการคำนวณ</div>
""", unsafe_allow_html=True)
nav_group("📊", "ผลลัพธ์ & วิเคราะห์", "submenu_result")
if st.session_state.submenu_result:
    nav_item("📋", "สัดส่วนวัสดุ", "proportions", indent=True)
    nav_item("📈", "กราฟพัฒนากำลัง", "strength_chart", indent=True)
    nav_item("🔬", "เปรียบเทียบงานวิจัย", "empirical", indent=True)

# ── Section: อื่นๆ ──
st.sidebar.markdown("""
<div style="padding:4px 16px; font-size:0.62rem; color:#475569;
            font-family:JetBrains Mono,monospace; letter-spacing:1px;
            text-transform:uppercase; margin-top:12px;">อื่นๆ</div>
""", unsafe_allow_html=True)
nav_item("⚖️", "เปรียบเทียบสูตร", "compare")
nav_item("📚", "แหล่งอ้างอิง", "references")

# ── Footer sidebar ──
st.sidebar.markdown("""
<div style="position:fixed; bottom:0; left:0; width:230px;
            padding:12px 16px; border-top:1px solid #1e293b;
            background:#0d1117;">
    <div style="font-size:0.68rem; color:#374151; font-family:JetBrains Mono,monospace;">
        v2.0 · DoE Eq.1-75 · ACI 211.1-22
    </div>
</div>
""", unsafe_allow_html=True)

# ── Page routing: Dashboard ──
if st.session_state.current_page == "dashboard":
    st.markdown("""
    <div class="hero-block">
    <div class="hero-badge">🏠 Dashboard</div>
    <div class="hero-title">ยินดีต้อนรับ</div>
    <div class="hero-sub">เลือกเมนูด้านซ้ายเพื่อเริ่มออกแบบส่วนผสมคอนกรีต</div>
    </div>
    """, unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    d1.metric("🧱 มาตรฐานที่รองรับ", "DoE + ACI 211.1")
    d2.metric("📐 สมการ PFA", "60 Equations")
    d3.metric("🌿 คำนวณ CO2", "รองรับ")
    st.info("👈 เลือก **กำหนดเกณฑ์ออกแบบ** จากเมนูซ้ายเพื่อเริ่มต้น")
    st.stop()

elif st.session_state.current_page == "references":
    st.markdown("""
    <div class="hero-block">
    <div class="hero-badge">📚 References</div>
    <div class="hero-title">แหล่งอ้างอิง</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    **[1]** Aguwa, C. & Abubakar, M. (2025). *Development of a Simplified Methodology for British DoE Concrete Mix Design Procedure using Python.* NJEAS Vol.2, Issue 2.

    **[2]** ACI PRC-211.1-22 (2022). *Selecting Proportions for Normal-Density and High-Density Concrete.* American Concrete Institute.

    **[3]** ACI 209R (1997). *Prediction of Creep, Shrinkage, and Temperature Effects in Concrete Structures.*

    **[4]** Chindaprasirt, P. et al. *High Volume Fly Ash Concrete — Experimental Data.*

    **[5]** Tangtermsirikul, S. (SIIT). *Control OPC Type 1 Mix Data.*
    """)
    st.stop()

elif st.session_state.current_page == "compare":
    st.markdown("""
    <div class="section-header">
    <div class="section-icon">⚖️</div>
    <div>
    <div class="section-num">COMPARE</div>
    <div class="section-title">เปรียบเทียบสูตรที่บันทึกไว้</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.mix_history.empty:
        st.info("ยังไม่มีสูตรที่บันทึก — กรุณาคำนวณและบันทึกสูตรก่อน")
    else:
        st.dataframe(st.session_state.mix_history, use_container_width=True, hide_index=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("**ต้นทุนรวม (฿)**")
            st.bar_chart(st.session_state.mix_history.set_index("ชื่อสูตร")["ต้นทุนรวม (บาท)"])
        with cc2:
            st.markdown("**CO2 Emission (kg)**")
            st.bar_chart(st.session_state.mix_history.set_index("ชื่อสูตร")["การปล่อย CO2 (kg)"])
        if st.button("🗑️ ล้างข้อมูล"):
            st.session_state.mix_history = pd.DataFrame(columns=["ชื่อสูตร","กำลังอัดเป้าหมาย (MPa)","ต้นทุนรวม (บาท)","การปล่อย CO2 (kg)","W/C Ratio"])
            st.rerun()
    st.stop()

# Empirical DB
empirical_db = pd.DataFrame([
    {"อ้างอิง": "Chindaprasirt et al.", "ประเภท": "เถ้าลอยแม่เมาะ (OFA 20%)", "W/B": 0.35, "28d (MPa)": 45.2, "90d (MPa)": 74.5},
    {"อ้างอิง": "Chindaprasirt et al.", "ประเภท": "เถ้าลอยคัดขนาด (CFA 20%)", "W/B": 0.35, "28d (MPa)": 76.6, "90d (MPa)": 81.4},
    {"อ้างอิง": "CANMET (Fournier)", "ประเภท": "HVFA (เถ้าลอย 56%)", "W/B": 0.32, "28d (MPa)": 40.0, "90d (MPa)": 60.0},
    {"อ้างอิง": "Laurent & Gourlay", "ประเภท": "Hempcrete", "W/B": 1.05, "28d (MPa)": 0.34, "90d (MPa)": 0.59},
    {"อ้างอิง": "Tangtermsirikul (SIIT)", "ประเภท": "Control OPC Type 1", "W/B": 0.50, "28d (MPa)": 34.5, "90d (MPa)": 38.0},
])

# ==========================================
# SECTION 1 — DESIGN CRITERIA
# ==========================================
st.markdown("""
<div class="section-header">
    <div class="section-icon">📐</div>
    <div>
        <div class="section-num">SECTION 01</div>
        <div class="section-title">กำหนดเกณฑ์การออกแบบ (Design Criteria)</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="sub-label">กำลังอัด & Slump</div>', unsafe_allow_html=True)
    if unit_system == "SI Units (MPa, kg, mm)":
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ f'c [MPa]", min_value=1.0, max_value=100.0, value=30.0)
        slump = st.slider("Slump [mm]", 0.0, 200.0, 100.0)
    else:
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ f'c [psi]", min_value=150.0, max_value=14500.0, value=4000.0)
        slump = st.slider("Slump [in]", 0.0, 8.0, 4.0)

with col_b:
    st.markdown('<div class="sub-label">ชนิดตัวอย่าง & มวลรวม</div>', unsafe_allow_html=True)
    specimen_type = st.radio("ประเภทตัวอย่างทดสอบ", ["ทรงกระบอก (Cylinder)", "ลูกบาศก์ (Cube)"])
    max_agg_str = st.selectbox("ขนาดมวลรวมสูงสุด (Max Agg.)", ["10 mm", "20 mm", "40 mm"], index=1)
    max_agg = int(max_agg_str.split()[0])

with col_c:
    st.markdown('<div class="sub-label">การควบคุมคุณภาพ & ขนาดโครงการ</div>', unsafe_allow_html=True)
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5
    project_volume = st.number_input("ปริมาตรคอนกรีตรวม (m³)", min_value=1.0, value=50.0, step=1.0)

st.markdown("---")
st.markdown('<div class="sub-label">⚗️ ข้อมูลสำหรับผสมทดลอง (Trial Mix Setup)</div>', unsafe_allow_html=True)

if specimen_type == "ทรงกระบอก (Cylinder)":
    m1, m2, m3, m4, m5 = st.columns([1,1,1,1,1.5])
    with m1: mold_dia = st.number_input("เส้นผ่านศูนย์กลาง (cm)", min_value=1.0, value=15.0, step=1.0)
    with m2: mold_h = st.number_input("ความสูง (cm)", min_value=1.0, value=30.0, step=1.0)
    with m3: num_molds = st.number_input("จำนวนก้อน", min_value=1, value=3, step=1)
    with m4: waste_pct = st.number_input("เผื่อ (%)", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    with m5:
        scale_mode = st.selectbox("รูปแบบการชั่ง", ["ชั่งเฉพาะปูนสด (Tare)", "ชั่งรวมโมลด์เปล่า"])
        mold_empty_wt = st.number_input("นน.โมลด์เปล่า (kg)", min_value=0.0, value=14.0, step=0.1) if "รวม" in scale_mode else 0.0
        mold_w = mold_l = 0.0
else:
    m1, m2, m3, m4, m5, m6 = st.columns([1,1,1,1,1,1.5])
    with m1: mold_w = st.number_input("กว้าง (cm)", min_value=1.0, value=15.0, step=0.1)
    with m2: mold_l = st.number_input("ยาว (cm)", min_value=1.0, value=15.0, step=0.1)
    with m3: mold_h = st.number_input("ลึก (cm)", min_value=1.0, value=15.0, step=0.1)
    with m4: num_molds = st.number_input("จำนวนก้อน", min_value=1, value=3, step=1)
    with m5: waste_pct = st.number_input("เผื่อ (%)", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    with m6:
        scale_mode = st.selectbox("รูปแบบการชั่ง", ["ชั่งเฉพาะปูนสด (Tare)", "ชั่งรวมโมลด์เปล่า"])
        mold_empty_wt = st.number_input("นน.โมลด์เปล่า (kg)", min_value=0.0, value=8.5, step=0.1) if "รวม" in scale_mode else 0.0

# ==========================================
# SECTION 2 — MATERIAL PROPERTIES
# ==========================================
st.markdown("""
<div class="section-header">
    <div class="section-icon">🧪</div>
    <div>
        <div class="section-num">SECTION 02</div>
        <div class="section-title">ข้อมูลสมบัติวัสดุ (Material Properties)</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_d, col_e, col_f = st.columns(3)
with col_d:
    st.markdown('<div class="sub-label">ประเภทมวลรวม</div>', unsafe_allow_html=True)
    agg_type = st.radio("มวลรวมหยาบ", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)", "มวลรวมรีไซเคิล (RCA)", "แกนกัญชง (Hemp Hurds)"])
    p_passing_str = st.selectbox("ทรายผ่านตะแกรง 600 μm", ["100%", "80%", "60%", "40%", "15%"], index=2)
    passing_600 = int(p_passing_str.replace("%", ""))

with col_e:
    st.markdown('<div class="sub-label">Specific Gravity (S.G.)</div>', unsafe_allow_html=True)
    cement_preset = st.selectbox("ชนิดปูนซีเมนต์", ["ปอร์ตแลนด์ Type 1 (S.G. 3.15)", "ปูนไฮดรอลิก (S.G. 3.10)", "กำหนดค่าเอง"])
    default_sg_c = 3.10 if "ไฮดรอลิก" in cement_preset else 3.15
    sg_c = st.number_input("S.G. ปูนซีเมนต์", value=default_sg_c, step=0.01)
    sg_s = st.number_input("S.G. ทราย", value=2.60, step=0.01)
    default_sg_g = 2.35 if "RCA" in agg_type else (0.50 if "Hemp" in agg_type else 2.65)
    sg_g = st.number_input("S.G. หิน/มวลรวมทางเลือก", value=default_sg_g, step=0.01)

with col_f:
    st.markdown('<div class="sub-label">วัสดุประสานทดแทน (SCMs)</div>', unsafe_allow_html=True)
    scm_type = st.selectbox("การใช้ SCMs", ["ไม่มี (None)", "เถ้าลอยแม่เมาะ (Class C)", "เถ้าลอยนำเข้า (Class F)", "สแลก (Slag)"])
    if scm_type != "ไม่มี (None)":
        scm_pct = st.number_input("สัดส่วนการแทนที่ปูน (%)", min_value=0.0, max_value=80.0, value=20.0, step=1.0)
        sg_scm = st.number_input("S.G. ของ SCMs", value=2.40 if "เถ้าลอย" in scm_type else 2.90, step=0.01)
    else:
        scm_pct = 0.0
        sg_scm = 1.0

# ==========================================
# SECTION 3 — FIELD & ADMIXTURES
# ==========================================
st.markdown("""
<div class="section-header">
    <div class="section-icon">🏗️</div>
    <div>
        <div class="section-num">SECTION 03</div>
        <div class="section-title">สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_g, col_h, col_i = st.columns(3)
with col_g:
    st.markdown('<div class="sub-label">ความชื้นทราย</div>', unsafe_allow_html=True)
    mc_sand = st.number_input("ความชื้นรวมทราย (%)", value=5.0, step=0.1)
    abs_sand = st.number_input("การดูดซึมทราย (%)", value=1.0, step=0.1)

with col_h:
    st.markdown('<div class="sub-label">ความชื้นหิน/มวลรวม</div>', unsafe_allow_html=True)
    default_abs_g = 15.0 if "Hemp" in agg_type else (4.0 if "RCA" in agg_type else 0.5)
    mc_gravel = st.number_input("ความชื้นรวมหิน (%)", value=2.0, step=0.1)
    abs_gravel = st.number_input("การดูดซึมหิน (%)", value=default_abs_g, step=0.1)

with col_i:
    st.markdown('<div class="sub-label">สารลดน้ำ (Admixtures)</div>', unsafe_allow_html=True)
    admix_type = st.selectbox("การใช้สารลดน้ำ", ["ไม่มี (None)", "สารลดน้ำทั่วไป (WRA)", "สารลดน้ำอย่างสูง (HRWRA)"])
    if admix_type != "ไม่มี (None)":
        water_reduction_pct = st.number_input("ประสิทธิภาพลดน้ำ (%)", value=5.0 if "WRA" in admix_type and "HRWRA" not in admix_type else 12.0)
        water_reduction = water_reduction_pct / 100.0
        admix_dosage = st.number_input("ปริมาณ (ml/ปูน 100 kg)", value=1000.0, step=50.0)
        admix_sg = st.number_input("S.G. น้ำยา", value=1.05, step=0.01)
    else:
        water_reduction = 0.0
        admix_dosage = 0.0
        admix_sg = 1.0

# ==========================================
# SECTION 4 — COST ESTIMATION
# ==========================================
st.markdown("""
<div class="section-header">
    <div class="section-icon">💰</div>
    <div>
        <div class="section-num">SECTION 04</div>
        <div class="section-title">ประเมินราคาต้นทุนวัสดุ (Cost Estimation)</div>
    </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: price_cement = st.number_input("ปูนซีเมนต์ (฿/kg)", value=3.00, step=0.1)
with c2: price_scm    = st.number_input("SCMs (฿/kg)", value=1.50, step=0.1)
with c3: price_sand   = st.number_input("ทราย (฿/kg)", value=0.50, step=0.1)
with c4: price_gravel = st.number_input("หิน/มวลรวม (฿/kg)", value=0.40, step=0.1)
with c5: price_water  = st.number_input("น้ำ (฿/kg)", value=0.02, step=0.01)
with c6: price_admix  = st.number_input("น้ำยา (฿/ลิตร)", value=50.0, step=1.0)

# ==========================================
# PFA FUNCTION (60 equations from Aguwa 2025)
# ==========================================
def calculate_pfa(max_agg, slump_mm, wc, passing_600):
    pfa = 0.0
    if max_agg == 10:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 13.18908*wc+19.8728
            elif passing_600 == 80: pfa = 16.16210*wc+22.6454
            elif passing_600 == 60: pfa = 17.77143*wc+28.6479
            elif passing_600 == 40: pfa = 26.46020*wc+32.2883
            else: pfa = 29.41890*wc+43.7290
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 11.70610*wc+21.4389
            elif passing_600 == 80: pfa = 13.61330*wc+25.1982
            elif passing_600 == 60: pfa = 18.78880*wc+29.1995
            elif passing_600 == 40: pfa = 26.45510*wc+33.6037
            else: pfa = 28.14480*wc+45.2898
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 17.17600*wc+21.9764
            elif passing_600 == 80: pfa = 17.87300*wc+26.8855
            elif passing_600 == 60: pfa = 15.96320*wc+33.1685
            elif passing_600 == 40: pfa = 23.55400*wc+37.3736
            else: pfa = 27.58010*wc+49.3627
        else:
            if passing_600 == 100: pfa = 13.21460*wc+26.0036
            elif passing_600 == 80: pfa = 15.11390*wc+30.0719
            elif passing_600 == 60: pfa = 17.93390*wc+36.4952
            elif passing_600 == 40: pfa = 23.92910*wc+43.3777
            else: pfa = 29.25830*wc+55.0112
    elif max_agg == 20:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 12.71190*wc+13.7892
            elif passing_600 == 80: pfa = 13.99890*wc+16.7774
            elif passing_600 == 60: pfa = 19.09000*wc+18.9410
            elif passing_600 == 40: pfa = 23.64690*wc+22.0002
            else: pfa = 27.60440*wc+29.3724
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 13.30500*wc+15.1615
            elif passing_600 == 80: pfa = 16.45440*wc+17.0508
            elif passing_600 == 60: pfa = 20.04360*wc+19.7431
            elif passing_600 == 40: pfa = 22.66500*wc+26.4602
            else: pfa = 28.75000*wc+31.7355
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 11.74020*wc+17.5560
            elif passing_600 == 80: pfa = 17.12400*wc+19.8785
            elif passing_600 == 60: pfa = 19.12630*wc+23.3680
            elif passing_600 == 40: pfa = 23.69300*wc+27.7049
            else: pfa = 30.94380*wc+35.5925
        else:
            if passing_600 == 100: pfa = 10.33400*wc+19.9064
            elif passing_600 == 80: pfa = 16.98350*wc+22.1610
            elif passing_600 == 60: pfa = 20.71980*wc+26.1337
            elif passing_600 == 40: pfa = 22.92080*wc+32.9819
            else: pfa = 29.32570*wc+41.2271
    elif max_agg == 40:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 13.06400*wc+9.9264
            elif passing_600 == 80: pfa = 15.00400*wc+12.2357
            elif passing_600 == 60: pfa = 17.94760*wc+12.6536
            elif passing_600 == 40: pfa = 25.50450*wc+15.9692
            else: pfa = 27.67870*wc+22.2533
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 11.23320*wc+12.4117
            elif passing_600 == 80: pfa = 12.83580*wc+14.1410
            elif passing_600 == 60: pfa = 16.61589*wc+16.3136
            elif passing_600 == 40: pfa = 23.32340*wc+18.6401
            else: pfa = 27.77270*wc+23.9597
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 10.85130*wc+18.3340
            elif passing_600 == 80: pfa = 10.63320*wc+18.0026
            elif passing_600 == 60: pfa = 16.65700*wc+20.0989
            elif passing_600 == 40: pfa = 19.13231*wc+23.9366
            else: pfa = 29.16500*wc+28.7110
        else:
            if passing_600 == 100: pfa = 13.24400*wc+17.1056
            elif passing_600 == 80: pfa = 15.27120*wc+19.9462
            elif passing_600 == 60: pfa = 19.42690*wc+22.4551
            elif passing_600 == 40: pfa = 22.84520*wc+27.9800
            else: pfa = 29.25440*wc+34.3330
    return pfa / 100.0

# ==========================================
# CALCULATE BUTTON
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⚙️  ประมวลผลส่วนผสมคอนกรีต (CALCULATE)", type="primary", use_container_width=True):

    errors = []
    if sg_c < 2.8 or sg_c > 3.3:
        errors.append("S.G. ปูนซีเมนต์ควรอยู่ระหว่าง 2.80–3.30")
    if sg_s < 2.0 or sg_s > 3.0:
        errors.append("S.G. ทรายควรอยู่ระหว่าง 2.00–3.00")
    if "Hemp" not in agg_type and (sg_g < 1.5 or sg_g > 3.5):
        errors.append("S.G. หินควรอยู่ระหว่าง 1.50–3.50")
    if mc_sand < abs_sand:
        errors.append("MC% ทราย < Absorption% — ทรายแห้งกว่า SSD ต้องเพิ่มน้ำ")
    if mc_gravel < abs_gravel:
        errors.append("MC% หิน < Absorption% — หินแห้งกว่า SSD ต้องเพิ่มน้ำ")
    for err in errors:
        st.warning(f"⚠️  {err}")

    fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
    fm_cube = fm_metric * 1.22 if specimen_type == "ทรงกระบอก (Cylinder)" else fm_metric
    fm_target = fm_cube / control_factor

    if fm_cube > 100.0 and "Hemp" not in agg_type:
        st.error("❌  ค่ากำลังอัดเป้าหมายอยู่นอกเหนือขอบเขตสมการ (Max 100 MPa)")
    else:
        if "Uncrushed" in agg_type:
            wc = (0.0002952*(fm_target**2))-(0.0312*fm_target)+1.291 if fm_target<=42 else (0.00008519*(fm_target**2))-(0.01571*fm_target)+1.0097
        else:
            wc = (0.000295*(fm_target**2))-(0.0312*fm_target)+1.351 if fm_target<=42 else (0.000008519*(fm_target**2))-(0.01571*fm_target)+1.0697

        wc = max(0.25, min(1.5 if "Hemp" in agg_type else 0.95, wc))

        slump_mm = slump if unit_system == "SI Units (MPa, kg, mm)" else slump * 25.4

        fwc_table = {
            10: {"uncrushed": [150,180,195,205], "crushed": [180,200,215,225]},
            20: {"uncrushed": [135,160,180,195], "crushed": [170,190,210,225]},
            40: {"uncrushed": [115,140,160,175], "crushed": [155,175,190,205]},
        }
        slump_idx = 0 if slump_mm<=10 else 1 if slump_mm<=30 else 2 if slump_mm<=60 else 3
        agg_key = "uncrushed" if "Uncrushed" in agg_type else "crushed"
        fwc_base = fwc_table.get(max_agg, fwc_table[20])[agg_key][slump_idx]
        fwc = fwc_base * (1 - water_reduction)

        cm_total = fwc / wc
        scm_weight = cm_total * (scm_pct / 100.0)
        cc = cm_total - scm_weight

        admix_vol_liters = (cm_total / 100) * (admix_dosage / 1000)
        admix_weight_kg = admix_vol_liters * admix_sg

        ssdd_avg = round((sg_s + sg_g) / 2, 1)
        if ssdd_avg >= 2.9: wdcc = -1.7440*fwc+2898.4795
        elif ssdd_avg == 2.8: wdcc = -1.5961*fwc+2802.5554
        elif ssdd_avg == 2.7: wdcc = -1.4480*fwc+2702.8337
        elif ssdd_avg == 2.6: wdcc = -1.2492*fwc+2410.3614
        elif ssdd_avg == 2.5: wdcc = -1.0996*fwc+2500.6876
        elif "Hemp" in agg_type: wdcc = 400.0
        else: wdcc = -0.9809*fwc+2410.3614

        ac = wdcc - cm_total - fwc
        if "Hemp" in agg_type:
            fac, cac = 0, ac
        else:
            pfa_ratio = calculate_pfa(max_agg, slump_mm, wc, passing_600)
            fac = pfa_ratio * ac
            cac = ac - fac

        s_od = fac / (1 + abs_sand/100)
        free_water_sand = s_od * ((mc_sand - abs_sand) / 100)
        s_batched = fac + free_water_sand

        g_od = cac / (1 + abs_gravel/100)
        free_water_gravel = g_od * ((mc_gravel - abs_gravel) / 100)
        g_batched = cac + free_water_gravel

        w_batched = fwc - free_water_sand - free_water_gravel

        if specimen_type == "ทรงกระบอก (Cylinder)":
            r_m = (mold_dia/2)/100
            single_mold_vol_m3 = 3.14159265*(r_m**2)*(mold_h/100)
        else:
            single_mold_vol_m3 = (mold_w/100)*(mold_l/100)*(mold_h/100)

        total_mold_vol_m3 = single_mold_vol_m3 * num_molds
        fresh_conc_weight_per_mold = single_mold_vol_m3 * wdcc
        target_scale_weight_per_mold = fresh_conc_weight_per_mold + mold_empty_wt
        trial_mix_vol = total_mold_vol_m3 * (1 + waste_pct/100)

        cost_m3 = (cc*price_cement)+(scm_weight*price_scm)+(s_batched*price_sand)+(g_batched*price_gravel)+(w_batched*price_water)+(admix_vol_liters*price_admix)
        total_project_cost = cost_m3 * project_volume
        total_co2_m3 = (cc*0.90) + (scm_weight*0.10)

        # ── SUCCESS BANNER ──
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(5,150,105,0.06));
                    border:1px solid rgba(16,185,129,0.3); border-radius:12px;
                    padding:16px 24px; margin:20px 0; display:flex; align-items:center; gap:12px;'>
            <span style='font-size:1.4rem;'>✅</span>
            <span style='color:#6ee7b7; font-weight:600; font-size:0.95rem; font-family:Space Grotesk,sans-serif;'>
                การประมวลผลเสร็จสมบูรณ์ — Calculation Completed Successfully
            </span>
        </div>
        """, unsafe_allow_html=True)

        # ── 4 KEY METRICS ──
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🎯 กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        r2.metric("💧 W/C Ratio", f"{wc:.3f}")
        r3.metric("💵 ต้นทุน/m³", f"฿{cost_m3:,.0f}")
        r4.metric("🌿 CO₂/m³", f"{total_co2_m3:.1f} kg")

        # ── MIX RATIO BOX ──
        st.markdown(f"""
        <div class="mix-ratio-box">
            <div class="result-title">อัตราส่วนผสม (Mix Ratio by Weight)</div>
            <div class="mix-ratio-val">1 : {(fac/cm_total):.2f} : {(cac/cm_total):.2f}</div>
            <div class="mix-ratio-label">วัสดุประสานรวม : ทราย : หิน &nbsp;|&nbsp; W/C = {wc:.3f} &nbsp;|&nbsp; Wdcc = {wdcc:.0f} kg/m³</div>
        </div>
        """, unsafe_allow_html=True)

        # ── EQUATION EXPANDER ──
        slump_labels = ["0–10 mm","10–30 mm","30–60 mm","60–180 mm"]
        agg_label = "Uncrushed" if "Uncrushed" in agg_type else "Crushed"
        with st.expander("🔍  แสดงสมการที่ใช้ในการคำนวณ (Show Equations Used)"):
            st.markdown("**Step 1 — Target Mean Strength (Erntroy & Shacklock)**")
            st.code(f"fm = fc_cube / CF = {fm_cube:.2f} / {control_factor} = {fm_target:.2f} MPa", language="text")
            st.markdown("**Step 2 — W/C Ratio (DoE Parabolic Eq.2–5)**")
            st.code(f"Agg type: {agg_label} | Range: {'10–42' if fm_target<=42 else '42–80'} MPa\nW/C = {wc:.4f}  (clamped 0.25–0.95)", language="text")
            st.markdown("**Step 3 — Free Water Content (DoE Table 3 Lookup)**")
            st.code(f"Max Agg {max_agg}mm | {agg_label} | Slump {slump_labels[slump_idx]}\nFWC = {fwc_base} kg/m³ × (1-{water_reduction*100:.0f}%) = {fwc:.1f} kg/m³", language="text")
            st.markdown("**Step 4 — Cementitious Content**")
            st.code(f"Cc = FWC/W/C = {fwc:.1f}/{wc:.4f} = {cm_total:.1f} kg/m³\nCement={cc:.1f} kg  |  SCMs={scm_weight:.1f} kg ({scm_pct:.0f}%)", language="text")
            st.markdown("**Step 5 — Wet Density (DoE Eq.7–12)**")
            st.code(f"SSDD_avg={ssdd_avg}  →  Wdcc = {wdcc:.0f} kg/m³", language="text")
            st.markdown("**Step 6 — Aggregate Content & PFA**")
            st.code(f"Ac = {wdcc:.0f}-{cm_total:.1f}-{fwc:.1f} = {ac:.1f} kg/m³\nPFA {pfa_ratio*100:.1f}% → Sand={fac:.1f} kg | Gravel={cac:.1f} kg", language="text")
            st.markdown("**Step 7 — Moisture Adjustment (ACI 211.1 Eq.5.3.9.1)**")
            st.code(f"Sand batched = {s_batched:.1f} kg  (free water {free_water_sand:+.2f} kg)\nGravel batched = {g_batched:.1f} kg  (free water {free_water_gravel:+.2f} kg)\nWater added = {w_batched:.1f} kg", language="text")

        st.markdown("<br>", unsafe_allow_html=True)
        out_col1, out_col2 = st.columns([1.2, 1])

        # ── LEFT COLUMN: PROPORTIONS ──
        with out_col1:
            st.markdown('<div class="result-title">สัดส่วนวัสดุต่อ 1 m³ (Proportions per 1 m³)</div>', unsafe_allow_html=True)

            st.markdown('<div class="sub-label">① SSD Weights (ทฤษฎี)</div>', unsafe_allow_html=True)
            ssd_data = {"วัสดุ": ["ปูนซีเมนต์", scm_type if scm_pct>0 else None, "ทราย (Fine Agg.)", "หิน (Coarse Agg.)", "น้ำ (Free Water)"],
                        "SSD (kg/m³)": [f"{cc:.1f}", f"{scm_weight:.1f}" if scm_pct>0 else None, f"{fac:.1f}", f"{cac:.1f}", f"{fwc:.1f}"]}
            ssd_df = pd.DataFrame(ssd_data).dropna()
            st.dataframe(ssd_df, use_container_width=True, hide_index=True)

            st.markdown('<div class="sub-label">② Batched Weights (ชั่งหน้างาน)</div>', unsafe_allow_html=True)
            bat_rows = {"วัสดุ": ["ปูนซีเมนต์"], "Batched (kg/m³)": [f"{cc:.1f}"], "หมายเหตุ": ["—"]}
            if scm_pct > 0:
                bat_rows["วัสดุ"].append(scm_type); bat_rows["Batched (kg/m³)"].append(f"{scm_weight:.1f}"); bat_rows["หมายเหตุ"].append("—")
            bat_rows["วัสดุ"].append("ทราย"); bat_rows["Batched (kg/m³)"].append(f"{s_batched:.1f}"); bat_rows["หมายเหตุ"].append(f"free {free_water_sand:+.2f} kg")
            bat_rows["วัสดุ"].append("หิน");  bat_rows["Batched (kg/m³)"].append(f"{g_batched:.1f}");  bat_rows["หมายเหตุ"].append(f"free {free_water_gravel:+.2f} kg")
            bat_rows["วัสดุ"].append("น้ำ");  bat_rows["Batched (kg/m³)"].append(f"{w_batched:.1f}");  bat_rows["หมายเหตุ"].append(f"หักออก {free_water_sand+free_water_gravel:.2f} kg")
            if admix_type != "ไม่มี (None)":
                bat_rows["วัสดุ"].append("สารลดน้ำ"); bat_rows["Batched (kg/m³)"].append(f"{admix_vol_liters:.3f} L"); bat_rows["หมายเหตุ"].append("—")
            st.dataframe(pd.DataFrame(bat_rows), use_container_width=True, hide_index=True)

            st.markdown(f'<div class="sub-label">③ Trial Mix — {num_molds} ก้อน (เผื่อ {waste_pct:.0f}%)</div>', unsafe_allow_html=True)
            st.info(f"ปริมาตรรวม {num_molds} ก้อน = {total_mold_vol_m3*1e6:.0f} cm³  |  ปริมาตรผสม (เผื่อ) = {trial_mix_vol*1e6:.0f} cm³")
            tm_rows = {"วัสดุ": ["ปูนซีเมนต์"], "ปริมาณ (kg)": [f"{cc*trial_mix_vol:.3f}"]}
            if scm_pct > 0:
                tm_rows["วัสดุ"].append(scm_type); tm_rows["ปริมาณ (kg)"].append(f"{scm_weight*trial_mix_vol:.3f}")
            tm_rows["วัสดุ"].append("ทราย (Batched)"); tm_rows["ปริมาณ (kg)"].append(f"{s_batched*trial_mix_vol:.3f}")
            tm_rows["วัสดุ"].append("หิน (Batched)");  tm_rows["ปริมาณ (kg)"].append(f"{g_batched*trial_mix_vol:.3f}")
            tm_rows["วัสดุ"].append("น้ำ (เติมจริง)"); tm_rows["ปริมาณ (kg)"].append(f"{w_batched*trial_mix_vol:.3f}")
            if admix_type != "ไม่มี (None)":
                tm_rows["วัสดุ"].append("สารลดน้ำ"); tm_rows["ปริมาณ (kg)"].append(f"{admix_vol_liters*trial_mix_vol*1000:.1f} ml")
            st.dataframe(pd.DataFrame(tm_rows), use_container_width=True, hide_index=True)

            st.markdown(f"""
            <div style='background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px 18px; margin-top:8px;'>
                <div style='font-family:JetBrains Mono,monospace; font-size:0.72rem; color:#6366f1; margin-bottom:8px; letter-spacing:1px;'>QC TARGET</div>
                <div style='font-size:0.88rem; color:#94a3b8;'>น้ำหนักปูนสด/ก้อน (ทฤษฎี): <span style='color:#f1f5f9; font-weight:600; font-family:JetBrains Mono,monospace;'>{fresh_conc_weight_per_mold:.3f} kg</span></div>
                {'<div style="font-size:0.88rem; color:#94a3b8; margin-top:4px;">เป้าหมายชั่งรวมโมลด์: <span style=\'color:#f1f5f9; font-weight:600; font-family:JetBrains Mono,monospace;\'>' + f'{target_scale_weight_per_mold:.3f} kg</span></div>' if "รวม" in scale_mode else ''}
                <div style='font-size:0.78rem; color:#475569; margin-top:6px;'>อ้างอิง Wdcc = {wdcc:.0f} kg/m³</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sub-label">④ Project BOQ</div>', unsafe_allow_html=True)
            st.info(f"ปริมาตรคอนกรีตทั้งหมด: **{project_volume:,.1f} m³**")
            boq_rows = {"รายการ": ["ปูนซีเมนต์", "ทราย", "หิน/มวลรวม", "น้ำ"], "ปริมาณรวม": [f"{(cc*project_volume/50):,.1f} ถุง (50 kg)", f"{s_batched*project_volume/1000:,.2f} ตัน", f"{g_batched*project_volume/1000:,.2f} ตัน", f"{w_batched*project_volume:,.0f} ลิตร"]}
            if scm_pct > 0:
                boq_rows["รายการ"].insert(1, scm_type); boq_rows["ปริมาณรวม"].insert(1, f"{scm_weight*project_volume/1000:,.2f} ตัน")
            st.dataframe(pd.DataFrame(boq_rows), use_container_width=True, hide_index=True)
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(139,92,246,0.06)); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:16px 20px; margin-top:8px;'>
                <div style='font-size:0.78rem; color:#818cf8; font-family:JetBrains Mono,monospace; letter-spacing:0.8px;'>TOTAL BUDGET</div>
                <div style='font-size:1.8rem; font-weight:700; color:#f1f5f9; font-family:JetBrains Mono,monospace; margin-top:4px;'>฿{total_project_cost:,.2f}</div>
                <div style='font-size:0.8rem; color:#64748b; margin-top:2px;'>= ฿{cost_m3:,.2f}/m³ × {project_volume:,.0f} m³</div>
            </div>
            """, unsafe_allow_html=True)

        # ── RIGHT COLUMN: CHARTS ──
        with out_col2:
            st.markdown('<div class="result-title">การพัฒนากำลังอัด (Strength Development)</div>', unsafe_allow_html=True)

            a_c, b_c = 4.0, 0.85
            scm_ep = (scm_pct/100)*(0.15 if "แม่เมาะ" in scm_type else 0.25 if "นำเข้า" in scm_type else 0.15 if "Slag" in scm_type else 0.0)
            scm_lb = (scm_pct/100)*(0.20 if "แม่เมาะ" in scm_type else 0.10 if "นำเข้า" in scm_type else 0.08 if "Slag" in scm_type else 0.0)
            days = [3,7,14,21,28,56,90]
            s_plain  = [fm_target*(t/(a_c+b_c*t)) for t in days]
            s_actual = [s*(1-scm_ep*max(0,(28-d)/28))*(1+scm_lb*min(1,max(0,(d-28)/62))) for s,d in zip(s_plain,days)]
            sdf = pd.DataFrame({"ปูนล้วน (MPa)":[round(x,1) for x in s_plain], "สูตรของคุณ (MPa)":[round(x,1) for x in s_actual]}, index=days)
            sdf.index.name = "อายุ (วัน)"
            st.line_chart(sdf)
            if scm_pct > 0:
                st.caption(f"⚠️ {scm_type} {scm_pct:.0f}% → กำลัง 3–7 วันต่ำกว่า แต่ 56–90 วันสูงกว่าปูนล้วน")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="result-title">สัดส่วนวัสดุ (kg/m³)</div>', unsafe_allow_html=True)
            pie_labels = ["ปูนซีเมนต์", "ทราย", "หิน", "น้ำ"]
            pie_values = [cc, fac, cac, fwc]
            if scm_pct > 0:
                pie_labels.insert(1, scm_type[:8]); pie_values.insert(1, scm_weight)
            pdf = pd.DataFrame({"kg/m³": pie_values}, index=pie_labels)
            st.bar_chart(pdf)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="result-title">ตรวจสอบกับงานวิจัย (Empirical Validation)</div>', unsafe_allow_html=True)
            st.dataframe(empirical_db, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="result-title">ดาวน์โหลด (Export CSV)</div>', unsafe_allow_html=True)
            export_df = pd.DataFrame({
                "รายการ": ["ปริมาตรรวม (m³)","กำลังอัด fm (MPa)","W/C Ratio","ปูนซีเมนต์ (kg)","SCMs (kg)","ทราย Batched (kg)","หิน Batched (kg)","น้ำ (kg)","น้ำยา (L)","ต้นทุนรวม (฿)","CO2 (kg)"],
                "ค่า": [project_volume, fm_target, wc, cc*project_volume, scm_weight*project_volume, s_batched*project_volume, g_batched*project_volume, w_batched*project_volume, admix_vol_liters*project_volume, total_project_cost, total_co2_m3*project_volume]
            })
            st.download_button("⬇️  ดาวน์โหลดไฟล์ CSV (เปิดใน Excel)", data=export_df.to_csv(index=False).encode("utf-8-sig"), file_name="MixDesign_BOQ.csv", mime="text/csv", use_container_width=True)

        # ── SAVE TO COMPARE ──
        st.markdown("---")
        st.markdown('<div class="result-title">💾 บันทึกสูตรนี้เพื่อเปรียบเทียบ</div>', unsafe_allow_html=True)
        save_col, _ = st.columns([2,3])
        with save_col:
            mix_name = st.text_input("ชื่อสูตร", "สูตรที่ 1: มาตรฐาน")
            if st.button("💾  บันทึกสูตร", use_container_width=True):
                new_row = pd.DataFrame([{"ชื่อสูตร": mix_name, "กำลังอัดเป้าหมาย (MPa)": round(fm_target,1), "ต้นทุนรวม (บาท)": round(total_project_cost,2), "การปล่อย CO2 (kg)": round(total_co2_m3*project_volume,1), "W/C Ratio": round(wc,3)}])
                st.session_state.mix_history = pd.concat([st.session_state.mix_history, new_row], ignore_index=True)
                st.success("บันทึกสำเร็จ! ดูผลได้ที่เมนู เปรียบเทียบสูตร ด้านซ้าย")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer-ref">
    <div class="footer-ref-title">📚 References — สมการและมาตรฐานที่ใช้ในระบบนี้</div>
    <div class="footer-ref-item">[1] Aguwa, C. & Abubakar, M. (2025). <em>Development of a Simplified Methodology for British DoE Concrete Mix Design Procedure using Python.</em> NJEAS Vol.2, Issue 2. — <strong>Eq.1–75 (W/C, FWC, Wdcc, PFA)</strong></div>
    <div class="footer-ref-item">[2] ACI PRC-211.1-22 (2022). <em>Selecting Proportions for Normal-Density and High-Density Concrete — Guide.</em> American Concrete Institute. — <strong>Moisture Adjustment, Exposure Class, Absolute Volume Method</strong></div>
    <div class="footer-ref-item">[3] ACI 209R (1997). <em>Prediction of Creep, Shrinkage, and Temperature Effects in Concrete Structures.</em> — <strong>f(t) = f28 × [t/(a+bt)]</strong></div>
</div>
""", unsafe_allow_html=True)
