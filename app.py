import streamlit as st

# ==========================================
# 0. การตั้งค่าหน้าเว็บ (Page Setup)
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>ระบบจำลองการออกแบบส่วนผสมคอนกรีตอัจฉริยะ</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #7F8C8D; margin-bottom: 30px;'>(Web-Based Intelligent Concrete Mix Design Simulation System)</h4>", unsafe_allow_html=True)

# ==========================================
# ฟังก์ชันสมองกล PFA (60 สมการจากงานวิจัย)
# ==========================================
def get_pfa(max_agg, slump, p_passing, fwc_ratio):
    pfa_percent = 0.0
    if max_agg == 10:
        if 0 <= slump <= 10:
            if p_passing == 100: pfa_percent = 13.189 * fwc_ratio + 19.873
            elif p_passing == 80: pfa_percent = 16.162 * fwc_ratio + 22.645
            elif p_passing == 60: pfa_percent = 17.771 * fwc_ratio + 28.648
            elif p_passing == 40: pfa_percent = 26.460 * fwc_ratio + 32.288
            elif p_passing == 15: pfa_percent = 29.419 * fwc_ratio + 43.729
        elif 10 < slump <= 30:
            if p_passing == 100: pfa_percent = 11.706 * fwc_ratio + 21.439
            elif p_passing == 80: pfa_percent = 13.613 * fwc_ratio + 25.198
            elif p_passing == 60: pfa_percent = 18.789 * fwc_ratio + 29.200
            elif p_passing == 40: pfa_percent = 26.455 * fwc_ratio + 33.604
            elif p_passing == 15: pfa_percent = 28.145 * fwc_ratio + 45.290
        elif 30 < slump <= 60:
            if p_passing == 100: pfa_percent = 17.176 * fwc_ratio + 21.976
            elif p_passing == 80: pfa_percent = 17.873 * fwc_ratio + 26.886
            elif p_passing == 60: pfa_percent = 15.963 * fwc_ratio + 33.169
            elif p_passing == 40: pfa_percent = 23.554 * fwc_ratio + 37.374
            elif p_passing == 15: pfa_percent = 27.580 * fwc_ratio + 49.363
        elif 60 <= slump <= 200:
            if p_passing == 100: pfa_percent = 13.215 * fwc_ratio + 26.004
            elif p_passing == 80: pfa_percent = 15.114 * fwc_ratio + 30.072
            elif p_passing == 60: pfa_percent = 17.934 * fwc_ratio + 36.495
            elif p_passing == 40: pfa_percent = 23.929 * fwc_ratio + 43.378
            elif p_passing == 15: pfa_percent = 29.258 * fwc_ratio + 55.011

    elif max_agg == 20:
        if 0 <= slump <= 10:
            if p_passing == 100: pfa_percent = 12.712 * fwc_ratio + 13.789
            elif p_passing == 80: pfa_percent = 13.999 * fwc_ratio + 16.777
            elif p_passing == 60: pfa_percent = 19.090 * fwc_ratio + 18.941
            elif p_passing == 40: pfa_percent = 23.647 * fwc_ratio + 22.000
            elif p_passing == 15: pfa_percent = 27.604 * fwc_ratio + 29.372
        elif 10 < slump <= 30:
            if p_passing == 100: pfa_percent = 13.305 * fwc_ratio + 15.162
            elif p_passing == 80: pfa_percent = 16.454 * fwc_ratio + 17.051
            elif p_passing == 60: pfa_percent = 20.044 * fwc_ratio + 19.743
            elif p_passing == 40: pfa_percent = 25.167 * fwc_ratio + 22.665
            elif p_passing == 15: pfa_percent = 28.750 * fwc_ratio + 31.736
        elif 30 < slump <= 60:
            if p_passing == 100: pfa_percent = 11.740 * fwc_ratio + 17.556
            elif p_passing == 80: pfa_percent = 17.124 * fwc_ratio + 19.879
            elif p_passing == 60: pfa_percent = 19.126 * fwc_ratio + 23.368
            elif p_passing == 40: pfa_percent = 23.693 * fwc_ratio + 27.705
            elif p_passing == 15: pfa_percent = 30.944 * fwc_ratio + 35.593
        elif 60 <= slump <= 200:
            if p_passing == 100: pfa_percent = 10.334 * fwc_ratio + 19.906
            elif p_passing == 80: pfa_percent = 16.984 * fwc_ratio + 22.161
            elif p_passing == 60: pfa_percent = 20.720 * fwc_ratio + 26.134
            elif p_passing == 40: pfa_percent = 22.921 * fwc_ratio + 32.982
            elif p_passing == 15: pfa_percent = 29.326 * fwc_ratio + 41.227

    elif max_agg == 40:
        if 0 <= slump <= 10:
            if p_passing == 100: pfa_percent = 13.064 * fwc_ratio + 9.926
            elif p_passing == 80: pfa_percent = 15.004 * fwc_ratio + 12.236
            elif p_passing == 60: pfa_percent = 17.948 * fwc_ratio + 12.654
            elif p_passing == 40: pfa_percent = 25.505 * fwc_ratio + 15.969
            elif p_passing == 15: pfa_percent = 27.679 * fwc_ratio + 22.253
        elif 10 < slump <= 30:
            if p_passing == 100: pfa_percent = 11.233 * fwc_ratio + 12.412
            elif p_passing == 80: pfa_percent = 12.836 * fwc_ratio + 14.141
            elif p_passing == 60: pfa_percent = 16.616 * fwc_ratio + 16.314
            elif p_passing == 40: pfa_percent = 23.323 * fwc_ratio + 18.640
            elif p_passing == 15: pfa_percent = 27.773 * fwc_ratio + 23.960
        elif 30 < slump <= 60:
            if p_passing == 100: pfa_percent = 10.851 * fwc_ratio + 18.334
            elif p_passing == 80: pfa_percent = 10.633 * fwc_ratio + 18.003
            elif p_passing == 60: pfa_percent = 16.657 * fwc_ratio + 20.099
            elif p_passing == 40: pfa_percent = 19.132 * fwc_ratio + 23.937
            elif p_passing == 15: pfa_percent = 29.165 * fwc_ratio + 28.711
        elif 60 <= slump <= 200:
            if p_passing == 100: pfa_percent = 13.244 * fwc_ratio + 17.106
            elif p_passing == 80: pfa_percent = 15.271 * fwc_ratio + 19.946
            elif p_passing == 60: pfa_percent = 19.427 * fwc_ratio + 22.455
            elif p_passing == 40: pfa_percent = 22.845 * fwc_ratio + 27.980
            elif p_passing == 15: pfa_percent = 29.254 * fwc_ratio + 34.333

    return pfa_percent / 100.0 

# ==========================================
# การจัด Layout แบบ 2 คอลัมน์ (เหมือนในภาพ)
# ==========================================
left_col, right_col = st.columns([1.2, 1.0], gap="large")

# ------------------------------------------
# ฝั่งซ้าย: ข้อมูลนำเข้า (Inputs)
# ------------------------------------------
with left_col:
    st.markdown("### 📋 เกณฑ์การออกแบบ (Design Criteria)")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fc_req = st.number_input("🎯 กำลังอัดที่ต้องการ (MPa)", min_value=10.0, max_value=80.0, value=30.0)
            slump = st.slider("🛝 ค่าความยุบตัว Slump (mm)", 0, 200, 100)
        with col2:
            max_agg_str = st.selectbox("🪨 ขนาดมวลรวมสูงสุด", ["10 mm", "20 mm", "40 mm"], index=1)
            max_agg = int(max_agg_str.split()[0])
            control_label = st.selectbox("🛡️ ระดับการควบคุมคุณภาพ", ["ดีมาก (0.8)", "ปานกลาง (0.7)", "ต่ำ (0.5)"])
            control_factor = float(control_label.split("(")[1].replace(")", ""))

    st.markdown("---")
    st.markdown("### 🧱 คุณสมบัติของวัสดุ (Material Properties)")
    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            sg_c = st.number_input("ความถ่วงจำเพาะ ปูนซีเมนต์", value=3.15, step=0.01)
            sg_s = st.number_input("ความถ่วงจำเพาะ ทราย", value=2.60, step=0.01)
            sg_g = st.number_input("ความถ่วงจำเพาะ หิน", value=2.65, step=0.01)
        with col4:
            agg_type = st.radio("ประเภทของมวลรวม", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)"])
            p_passing_str = st.selectbox("ทรายผ่านตะแกรง 600 μm (%)", ["100%", "80%", "60%", "40%", "15%"], index=2)
            passing_600 = int(p_passing_str.replace("%", ""))

    st.markdown("---")
    st.markdown("### 🌤️ สภาพหน้างานและสารผสม (Field Conditions)")
    with st.container():
        col5, col6 = st.columns(2)
        with col5:
            mc_sand = st.number_input("ความชื้น ทราย (%)", value=5.0, step=0.1)
            abs_sand = st.number_input("การดูดซึม ทราย (%)", value=1.0, step=0.1)
        with col6:
            mc_gravel = st.number_input("ความชื้น หิน (%)", value=2.0, step=0.1)
            abs_gravel = st.number_input("การดูดซึม หิน (%)", value=0.5, step=0.1)
            
        admix_type = st.selectbox("การใช้สารผสมเพิ่ม (Admixtures)", ["ไม่มี (None)", "สารลดน้ำปกติ (WRA - ลด 5%)", "สารลดน้ำอย่างสูง (HRWRA - ลด 12%)"])
        if "WRA" in admix_type and "HRWRA" not in admix_type:
            water_reduction = 0.05
        elif "HRWRA" in admix_type:
            water_reduction = 0.12
        else:
            water_reduction = 0.0

# ------------------------------------------
# ฝั่งขวา: ปุ่มคำนวณ & แสดงผลลัพธ์ (Calculation & Output)
# ------------------------------------------
with right_col:
    st.markdown("<div style='background-color:#2980B9; padding:10px; border-radius:5px;'><h3 style='color:white; text-align:center; margin:0;'>📊 การประมวลผลและผลลัพธ์</h3></div>", unsafe_allow_html=True)
    st.write("") # เว้นบรรทัด
    
    # 🎯 ปุ่มคำนวณขนาดใหญ่
    calculate_btn = st.button("▶️ ประมวลผล (Calculate)", type="primary", use_container_width=True)

    if calculate_btn:
        # --- สมองกลประมวลผล ---
        fm_target = fc_req / control_factor
        
        if agg_type == "หินธรรมชาติ (Uncrushed)":
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
            
        fwc_base = 195.0 + (0.2 * slump) - (0.4 * max_agg)
        fwc = fwc_base * (1 - water_reduction)
        cc = fwc / wc
        
        ssdd_avg = round((sg_s + sg_g) / 2, 1)
        if ssdd_avg >= 2.9: wdcc = -1.7440 * fwc + 2898.4795
        elif ssdd_avg == 2.8: wdcc = -1.5961 * fwc + 2802.5554
        elif ssdd_avg == 2.7: wdcc = -1.4480 * fwc + 2702.8337
        elif ssdd_avg == 2.6: wdcc = -1.2492 * fwc + 2410.3614
        elif ssdd_avg == 2.5: wdcc = -1.0996 * fwc + 2500.6876
        else: wdcc = -0.9809 * fwc + 2410.3614
            
        ac = wdcc - cc - fwc
        pfa_ratio = get_pfa(max_agg, slump, passing_600, wc)
        fac = pfa_ratio * ac
        cac = ac - fac
        
        # --- ปรับแก้ความชื้น ---
        s_od = fac / (1 + (abs_sand / 100))
        s_batched = fac + (s_od * ((mc_sand - abs_sand) / 100))
        g_od = cac / (1 + (abs_gravel / 100))
        g_batched = cac + (g_od * ((mc_gravel - abs_gravel) / 100))
        w_batched = fwc - (s_batched - fac) - (g_batched - cac)

        # --- แสดงผลอัตราส่วนผสม ---
        st.markdown("### ➗ อัตราส่วนผสม (Mix Ratio)")
        st.info(f"#### **1 : {(fac/cc):.2f} : {(cac/cc):.2f}** \n*(ปูนซีเมนต์ : ทราย : หิน)*")
        st.write(f"*(อ้างอิง W/C Ratio = {wc:.3f} | กำลังอัดเป้าหมาย = {fm_target:.1f} MPa)*")
        
        # --- แสดงผลสัดส่วนต่อ 1 ลบ.ม. ---
        st.markdown("### 📦 สัดส่วนต่อ 1 ลูกบาศก์เมตร (Batched kg/m³)")
        
        # จัด Layout คล้ายการ์ดในภาพ
        c1, c2 = st.columns([1.5, 1])
        with c1: st.markdown("#### 🛢️ ปูนซีเมนต์ (Cement)")
        with c2: st.markdown(f"#### **{cc:.1f}** kg")
        
        c3, c4 = st.columns([1.5, 1])
        with c3: st.markdown("#### 💧 น้ำ (Water)")
        with c4: st.markdown(f"#### **{w_batched:.1f}** kg")
        
        c5, c6 = st.columns([1.5, 1])
        with c5: st.markdown("#### 🏜️ ทราย (Fine Agg)")
        with c6: st.markdown(f"#### **{s_batched:.1f}** kg")
        
        c7, c8 = st.columns([1.5, 1])
        with c7: st.markdown("#### 🪨 หิน (Coarse Agg)")
        with c8: st.markdown(f"#### **{g_batched:.1f}** kg")
        
        if water_reduction > 0:
            st.success(f"🧪 หมายเหตุ: ลดปริมาณน้ำลง {int(water_reduction*100)}% เนื่องจากการใช้สารผสมเพิ่ม")