import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# การตั้งค่าหน้าเว็บ
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design System", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>ระบบจำลองการออกแบบส่วนผสมคอนกรีตอัจฉริยะ</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #7F8C8D; margin-bottom: 30px;'>(Web-Based Intelligent Concrete Mix Design Simulation System)</h4>", unsafe_allow_html=True)

if 'mix_history' not in st.session_state:
    st.session_state.mix_history = pd.DataFrame(columns=["ชื่อสูตร", "กำลังอัดเป้าหมาย (MPa)", "ต้นทุนรวม (บาท)", "การปล่อย CO2 (kg)", "W/C Ratio"])

unit_system = st.sidebar.radio("ระบบหน่วย (Unit System)", ["SI Units (MPa, kg, mm)", "Inch-Pound Units (psi, lb, in)"])

# ==========================================
# ฐานข้อมูลงานวิจัยอ้างอิง (Empirical Database from Literature)
# ==========================================
empirical_db = pd.DataFrame([
    {"อ้างอิง": "Chindaprasirt et al.", "ประเภท": "เถ้าลอยแม่เมาะ (OFA 20%)", "W/B": 0.35, "Strength_28d": 45.2, "Strength_90d": 74.5},
    {"อ้างอิง": "Chindaprasirt et al.", "ประเภท": "เถ้าลอยคัดขนาด (CFA 20%)", "W/B": 0.35, "Strength_28d": 76.6, "Strength_90d": 81.4},
    {"อ้างอิง": "Chindaprasirt et al.", "ประเภท": "เถ้าลอยแม่เมาะ (OFA 40%)", "W/B": 0.35, "Strength_28d": 56.6, "Strength_90d": 61.4},
    {"อ้างอิง": "CANMET (Fournier & Malhotra)", "ประเภท": "HVFA (เถ้าลอย 56%)", "W/B": 0.32, "Strength_28d": 40.0, "Strength_90d": 60.0},
    {"อ้างอิง": "Laurent & Gourlay (France)", "ประเภท": "Hempcrete (แกนกัญชง)", "W/B": 1.05, "Strength_28d": 0.34, "Strength_90d": 0.59},
    {"อ้างอิง": "Tangtermsirikul (SIIT)", "ประเภท": "Control OPC (Type 1)", "W/B": 0.50, "Strength_28d": 34.5, "Strength_90d": 38.0}
])

# ==========================================
# 1. กำหนดเกณฑ์การออกแบบและขนาดโครงการ
# ==========================================
st.header("1. กำหนดเกณฑ์การออกแบบ (Design Criteria)")
col_a, col_b, col_c = st.columns(3)

with col_a:
    if unit_system == "SI Units (MPa, kg, mm)":
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [MPa]", min_value=1.0, max_value=100.0, value=30.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [mm]", 0.0, 200.0, 100.0)
    else:
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [psi]", min_value=150.0, max_value=14500.0, value=4000.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [in]", 0.0, 8.0, 4.0)

with col_b:
    specimen_type = st.radio("ประเภทตัวอย่างทดสอบ (Specimen Type)", ["ทรงกระบอก (Cylinder)", "ลูกบาศก์ (Cube)"])
    max_agg_str = st.selectbox("ขนาดมวลรวมสูงสุด (Max Aggregate Size)", ["10 mm", "20 mm", "40 mm"], index=1)
    max_agg = int(max_agg_str.split()[0]) 

with col_c:
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ (Control Factor)", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5
    project_volume = st.number_input("ปริมาตรคอนกรีตทั้งโครงการ (ลบ.ม.)", min_value=1.0, value=50.0, step=1.0)

st.write("---")
st.write("**ข้อมูลสำหรับการผสมทดลองในห้องปฏิบัติการ (Trial Mix Setup)**")
if specimen_type == "ทรงกระบอก (Cylinder)":
    mold_1, mold_2, mold_3, mold_4, mold_5 = st.columns([1, 1, 1, 1, 1.5])
    with mold_1: mold_dia = st.number_input("เส้นผ่านศูนย์กลาง (cm)", min_value=1.0, value=15.0, step=1.0)
    with mold_2: mold_h = st.number_input("ความสูง (cm)", min_value=1.0, value=30.0, step=1.0)
    with mold_3: num_molds = st.number_input("จำนวนก้อน", min_value=1, value=3, step=1)
    with mold_4: waste_pct = st.number_input("เผื่อปริมาณ (%)", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    with mold_5:
        scale_mode = st.selectbox("รูปแบบการชั่งน้ำหนัก", ["ชั่งเฉพาะปูนสด (Tare ตาชั่ง)", "ชั่งรวมน้ำหนักโมลด์เปล่า"])
        if scale_mode == "ชั่งรวมน้ำหนักโมลด์เปล่า":
            mold_empty_wt = st.number_input("นน.โมลด์เปล่า (เฉลี่ย kg)", min_value=0.0, value=14.0, step=0.1)
        else:
            mold_empty_wt = 0.0
    mold_w = mold_l = 0.0 
else:
    mold_1, mold_2, mold_3, mold_4, mold_5, mold_6 = st.columns([1, 1, 1, 1, 1, 1.5])
    with mold_1: mold_w = st.number_input("กว้างเฉลี่ย (cm)", min_value=1.0, value=15.0, step=0.1)
    with mold_2: mold_l = st.number_input("ยาวเฉลี่ย (cm)", min_value=1.0, value=15.0, step=0.1)
    with mold_3: mold_h = st.number_input("ลึกเฉลี่ย (cm)", min_value=1.0, value=15.0, step=0.1)
    with mold_4: num_molds = st.number_input("จำนวนก้อน", min_value=1, value=3, step=1)
    with mold_5: waste_pct = st.number_input("เผื่อปริมาณ (%)", min_value=0.0, max_value=50.0, value=15.0, step=1.0)
    with mold_6:
        scale_mode = st.selectbox("รูปแบบการชั่งน้ำหนัก", ["ชั่งเฉพาะปูนสด (Tare ตาชั่ง)", "ชั่งรวมน้ำหนักโมลด์เปล่า"])
        if scale_mode == "ชั่งรวมน้ำหนักโมลด์เปล่า":
            mold_empty_wt = st.number_input("นน.โมลด์เปล่า (เฉลี่ย kg)", min_value=0.0, value=8.5, step=0.1)
        else:
            mold_empty_wt = 0.0

# ==========================================
# 2. ข้อมูลสมบัติวัสดุ และ วัสดุประสานทดแทน
# ==========================================
st.header("2. ข้อมูลสมบัติวัสดุ (Material Properties)")
col_d, col_e, col_f = st.columns(3)

with col_d:
    st.write("**ประเภทมวลรวมและวัสดุทางเลือก**")
    agg_type = st.radio("ประเภทมวลรวมหยาบ", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)", "มวลรวมรีไซเคิล (RCA)", "แกนกัญชง (Hemp Hurds - Bio-based)"])
    p_passing_str = st.selectbox("ทรายผ่านตะแกรง 600 μm", ["100%", "80%", "60%", "40%", "15%"], index=2)
    passing_600 = int(p_passing_str.replace("%", ""))

with col_e:
    st.write("**ความถ่วงจำเพาะ (Specific Gravity)**")
    cement_preset = st.selectbox("ชนิดปูนซีเมนต์ (Cement Type)", [
        "ปอร์ตแลนด์ Type 1 (S.G. 3.15)", 
        "ปูนซีเมนต์ไฮดรอลิก (S.G. 3.10)", 
        "กำหนดค่าเอง (Custom)"
    ])
    default_sg_c = 3.10 if "ไฮดรอลิก" in cement_preset else 3.15
    sg_c = st.number_input("S.G. ปูนซีเมนต์", value=default_sg_c, step=0.01)
    sg_s = st.number_input("S.G. ทราย", value=2.60, step=0.01)
    
    if "RCA" in agg_type:
        default_sg_g = 2.35
    elif "Hemp" in agg_type:
        default_sg_g = 0.50
    else:
        default_sg_g = 2.65
    sg_g = st.number_input("S.G. หิน/มวลรวมทางเลือก", value=default_sg_g, step=0.01)

with col_f:
    st.write("**วัสดุประสานทดแทน (SCMs)**")
    scm_type = st.selectbox("การใช้ SCMs", ["ไม่มี (None)", "เถ้าลอยแม่เมาะ (Class C)", "เถ้าลอยนำเข้า (Class F)", "สแลก (Slag)"])
    if scm_type != "ไม่มี (None)":
        scm_pct = st.number_input("สัดส่วนการแทนที่ปูนซีเมนต์ (%)", min_value=0.0, max_value=80.0, value=20.0, step=1.0)
        sg_scm = st.number_input("S.G. ของ SCMs", value=2.40 if "เถ้าลอย" in scm_type else 2.90, step=0.01)
    else:
        scm_pct = 0.0
        sg_scm = 1.0

# ==========================================
# 3. สภาวะหน้างาน & สารผสมเพิ่ม
# ==========================================
st.header("3. สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)")
col_g, col_h, col_i = st.columns(3)

with col_g:
    st.write("**ความชื้นในทราย**")
    mc_sand = st.number_input("ความชื้นรวมทราย (%)", value=5.0, step=0.1)
    abs_sand = st.number_input("การดูดซึมทราย (%)", value=1.0, step=0.1)

with col_h:
    st.write("**ความชื้นในหิน/มวลรวมทางเลือก**")
    default_abs_g = 15.0 if "Hemp" in agg_type else (4.0 if "RCA" in agg_type else 0.5)
    mc_gravel = st.number_input("ความชื้นรวมหิน (%)", value=2.0, step=0.1)
    abs_gravel = st.number_input("การดูดซึมหิน (%)", value=default_abs_g, step=0.1)

with col_i:
    st.write("**สารลดน้ำ (Admixtures)**")
    admix_type = st.selectbox("การใช้สารลดน้ำ", ["ไม่มี (None)", "สารลดน้ำทั่วไป (WRA)", "สารลดน้ำอย่างสูง (HRWRA)"])
    if admix_type != "ไม่มี (None)":
        water_reduction_pct = st.number_input("ประสิทธิภาพการลดน้ำ (%)", value=5.0 if "WRA" in admix_type and "HRWRA" not in admix_type else 12.0)
        water_reduction = water_reduction_pct / 100.0
        admix_dosage = st.number_input("ปริมาณ (ml / ปูน 100 kg)", value=1000.0, step=50.0)
        admix_sg = st.number_input("S.G. น้ำยา", value=1.05, step=0.01)
    else:
        water_reduction = 0.0
        admix_dosage = 0.0
        admix_sg = 1.0

# ==========================================
# 4. ประเมินราคาต้นทุนวัสดุ
# ==========================================
st.header("4. ประเมินราคาต้นทุนวัสดุ (Cost Estimation)")
cost_1, cost_2, cost_3, cost_4, cost_5, cost_6 = st.columns(6)
with cost_1: price_cement = st.number_input("ปูนซีเมนต์ (บาท/kg)", value=3.00, step=0.1)
with cost_2: price_scm = st.number_input("SCMs (บาท/kg)", value=1.50, step=0.1)
with cost_3: price_sand = st.number_input("ทราย (บาท/kg)", value=0.50, step=0.1)
with cost_4: price_gravel = st.number_input("หิน/มวลรวม (บาท/kg)", value=0.40, step=0.1)
with cost_5: price_water = st.number_input("น้ำ (บาท/kg)", value=0.02, step=0.01)
with cost_6: price_admix = st.number_input("น้ำยา (บาท/ลิตร)", value=50.0, step=1.0)

# ==========================================
# ฟังก์ชันสมองกล: คำนวณ PFA 60 ชุดสมการ
# ==========================================
def calculate_pfa(max_agg, slump_mm, wc, passing_600):
    pfa = 0.0
    if max_agg == 10:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 13.18908 * wc + 19.8728
            elif passing_600 == 80: pfa = 16.16210 * wc + 22.6454
            elif passing_600 == 60: pfa = 17.77143 * wc + 28.6479
            elif passing_600 == 40: pfa = 26.46020 * wc + 32.2883
            else: pfa = 29.41890 * wc + 43.7290
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 11.70610 * wc + 21.4389
            elif passing_600 == 80: pfa = 13.61330 * wc + 25.1982
            elif passing_600 == 60: pfa = 18.78880 * wc + 29.1995
            elif passing_600 == 40: pfa = 26.45510 * wc + 33.6037
            else: pfa = 28.14480 * wc + 45.2898
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 17.17600 * wc + 21.9764
            elif passing_600 == 80: pfa = 17.87300 * wc + 26.8855
            elif passing_600 == 60: pfa = 15.96320 * wc + 33.1685
            elif passing_600 == 40: pfa = 23.55400 * wc + 37.3736
            else: pfa = 27.58010 * wc + 49.3627
        else: 
            if passing_600 == 100: pfa = 13.21460 * wc + 26.0036
            elif passing_600 == 80: pfa = 15.11390 * wc + 30.0719
            elif passing_600 == 60: pfa = 17.93390 * wc + 36.4952
            elif passing_600 == 40: pfa = 23.92910 * wc + 43.3777
            else: pfa = 29.25830 * wc + 55.0112
    elif max_agg == 20:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 12.71190 * wc + 13.7892
            elif passing_600 == 80: pfa = 13.99890 * wc + 16.7774
            elif passing_600 == 60: pfa = 19.09000 * wc + 18.9410
            elif passing_600 == 40: pfa = 23.64690 * wc + 22.0002
            else: pfa = 27.60440 * wc + 29.3724
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 13.30500 * wc + 15.1615
            elif passing_600 == 80: pfa = 16.45440 * wc + 17.0508
            elif passing_600 == 60: pfa = 20.04360 * wc + 19.7431
            elif passing_600 == 40: pfa = 22.6650 * wc + 26.4602 
            else: pfa = 28.75000 * wc + 31.7355
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 11.74020 * wc + 17.5560
            elif passing_600 == 80: pfa = 17.12400 * wc + 19.8785
            elif passing_600 == 60: pfa = 19.12630 * wc + 23.368
            elif passing_600 == 40: pfa = 23.69300 * wc + 27.7049
            else: pfa = 30.94380 * wc + 35.5925
        else: 
            if passing_600 == 100: pfa = 10.33400 * wc + 19.9064
            elif passing_600 == 80: pfa = 16.98350 * wc + 22.1610
            elif passing_600 == 60: pfa = 20.71980 * wc + 26.1337
            elif passing_600 == 40: pfa = 22.92080 * wc + 32.9819
            else: pfa = 29.32570 * wc + 41.2271
    elif max_agg == 40:
        if 0 <= slump_mm <= 10:
            if passing_600 == 100: pfa = 13.06400 * wc + 9.9264
            elif passing_600 == 80: pfa = 15.00400 * wc + 12.2357
            elif passing_600 == 60: pfa = 17.94760 * wc + 12.6536
            elif passing_600 == 40: pfa = 25.50450 * wc + 15.9692
            else: pfa = 27.67870 * wc + 22.2533
        elif 10 < slump_mm <= 30:
            if passing_600 == 100: pfa = 11.23320 * wc + 12.4117
            elif passing_600 == 80: pfa = 12.83580 * wc + 14.1410
            elif passing_600 == 60: pfa = 16.61589 * wc + 16.3136
            elif passing_600 == 40: pfa = 23.32340 * wc + 18.6401
            else: pfa = 27.77270 * wc + 23.9597
        elif 30 < slump_mm <= 60:
            if passing_600 == 100: pfa = 10.85130 * wc + 18.3340
            elif passing_600 == 80: pfa = 10.63320 * wc + 18.0026
            elif passing_600 == 60: pfa = 16.65700 * wc + 20.0989
            elif passing_600 == 40: pfa = 19.13231 * wc + 23.9366
            else: pfa = 29.16500 * wc + 28.7110
        else: 
            if passing_600 == 100: pfa = 13.24400 * wc + 17.1056
            elif passing_600 == 80: pfa = 15.27120 * wc + 19.9462
            elif passing_600 == 60: pfa = 19.42690 * wc + 22.4551
            elif passing_600 == 40: pfa = 22.84520 * wc + 27.9800
            else: pfa = 29.25440 * wc + 34.3330
            
    return pfa / 100.0 

# ==========================================
# 5. การประมวลผลและแสดงผล
# ==========================================
st.write("---")
if st.button("ประมวลผลส่วนผสมคอนกรีต (CALCULATE)", type="primary", use_container_width=True):

    errors = []
    if sg_c < 2.8 or sg_c > 3.3:
        errors.append("คำเตือน: ค่า S.G. ปูนซีเมนต์ควรอยู่ระหว่าง 2.80 - 3.30")
    if sg_s < 2.0 or sg_s > 3.0:
        errors.append("คำเตือน: ค่า S.G. ทรายควรอยู่ระหว่าง 2.00 - 3.00")
    if "Hemp" not in agg_type and (sg_g < 1.5 or sg_g > 3.5):
        errors.append("คำเตือน: ค่า S.G. หินควรอยู่ระหว่าง 1.50 - 3.50")
    if mc_sand < abs_sand:
        errors.append("คำเตือน: ความชื้นทราย (MC%) ต่ำกว่าการดูดซึม (Absorption%) - ทรายแห้งกว่า SSD")
    if mc_gravel < abs_gravel:
        errors.append("คำเตือน: ความชื้นหิน (MC%) ต่ำกว่าการดูดซึม (Absorption%) - หินแห้งกว่า SSD")

    for err in errors:
        st.warning(err)

    fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
    fm_cube = fm_metric * 1.22 if specimen_type == "ทรงกระบอก (Cylinder)" else fm_metric
    fm_target = fm_cube / control_factor
    
    if fm_cube > 100.0 and "Hemp" not in agg_type:
        st.error("คำเตือน: ค่ากำลังอัดเป้าหมายอยู่นอกเหนือสมการมาตรฐานวิจัยเชิงประจักษ์")
    else:
        if "Uncrushed" in agg_type:
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
        
        # สำหรับ Hempcrete ยอมให้ W/C สูงได้
        if "Hemp" in agg_type:
            wc = max(0.25, min(1.5, wc))
        else:
            wc = max(0.25, min(0.95, wc))

        slump_mm = slump if unit_system == "SI Units (MPa, kg, mm)" else slump * 25.4

        fwc_table = {
            10: {"uncrushed": [150, 180, 195, 205], "crushed": [180, 200, 215, 225]},
            20: {"uncrushed": [135, 160, 180, 195], "crushed": [170, 190, 210, 225]},
            40: {"uncrushed": [115, 140, 160, 175], "crushed": [155, 175, 190, 205]},
        }
        slump_idx = 0 if slump_mm <= 10 else 1 if slump_mm <= 30 else 2 if slump_mm <= 60 else 3
        agg_key = "uncrushed" if "Uncrushed" in agg_type else "crushed"
        fwc_base = fwc_table.get(max_agg, fwc_table[20])[agg_key][slump_idx]
        fwc = fwc_base * (1 - water_reduction)
        
        cm_total = fwc / wc 
        scm_weight = cm_total * (scm_pct / 100.0)
        cc = cm_total - scm_weight
        
        admix_vol_liters = (cm_total / 100) * (admix_dosage / 1000)
        admix_weight_kg = admix_vol_liters * admix_sg
        
        ssdd_avg = round((sg_s + sg_g) / 2, 1)
        if ssdd_avg >= 2.9: wdcc = -1.7440 * fwc + 2898.4795
        elif ssdd_avg == 2.8: wdcc = -1.5961 * fwc + 2802.5554
        elif ssdd_avg == 2.7: wdcc = -1.4480 * fwc + 2702.8337
        elif ssdd_avg == 2.6: wdcc = -1.2492 * fwc + 2410.3614
        elif ssdd_avg == 2.5: wdcc = -1.0996 * fwc + 2500.6876
        elif "Hemp" in agg_type: wdcc = 400.0 # ความหนาแน่นโดยประมาณของ Hempcrete
        else: wdcc = -0.9809 * fwc + 2410.3614
            
        ac = wdcc - cm_total - fwc
        
        if "Hemp" in agg_type:
            fac = 0 # Hempcrete มักไม่ใช้ทราย
            cac = ac
        else:
            pfa_ratio = calculate_pfa(max_agg, slump_mm, wc, passing_600)
            fac = pfa_ratio * ac
            cac = ac - fac
        
        s_od = fac / (1 + (abs_sand / 100))
        free_water_sand = s_od * ((mc_sand - abs_sand) / 100)
        s_batched = fac + free_water_sand
        
        g_od = cac / (1 + (abs_gravel / 100))
        free_water_gravel = g_od * ((mc_gravel - abs_gravel) / 100)
        g_batched = cac + free_water_gravel
        
        w_batched = fwc - free_water_sand - free_water_gravel
        
        if specimen_type == "ทรงกระบอก (Cylinder)":
            r_m = (mold_dia / 2.0) / 100.0
            h_m = mold_h / 100.0
            single_mold_vol_m3 = 3.1415926535 * (r_m**2) * h_m
        else:
            single_mold_vol_m3 = (mold_w / 100.0) * (mold_l / 100.0) * (mold_h / 100.0)
            
        total_mold_vol_m3 = single_mold_vol_m3 * num_molds
        fresh_conc_weight_per_mold = single_mold_vol_m3 * wdcc
        total_fresh_conc_weight = total_mold_vol_m3 * wdcc
        target_scale_weight_per_mold = fresh_conc_weight_per_mold + mold_empty_wt
        
        trial_mix_vol = total_mold_vol_m3 * (1 + (waste_pct / 100.0))

        cost_m3 = (cc * price_cement) + (scm_weight * price_scm) + (s_batched * price_sand) + (g_batched * price_gravel) + (w_batched * price_water) + (admix_vol_liters * price_admix)
        total_project_cost = cost_m3 * project_volume
        
        co2_cement = cc * 0.90 
        co2_scm = scm_weight * 0.10
        total_co2_m3 = co2_cement + co2_scm

        st.success("การประมวลผลเสร็จสมบูรณ์ (Calculation Completed Successfully)")
        
        res1, res2, res3, res4 = st.columns(4)
        res1.metric("กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        res2.metric("อัตราส่วน W/C Ratio", f"{wc:.3f}")
        res3.metric("ต้นทุนวัสดุโดยประมาณ", f"{cost_m3:,.2f} บาท/m3")
        res4.metric("การปล่อย CO2", f"{total_co2_m3:.1f} kg/m3")
        
        st.write("---")
        out_col1, out_col2 = st.columns([1.2, 1])
        
        with out_col1:
            st.markdown("### สัดส่วนวัสดุต่อ 1 ลูกบาศก์เมตร (Proportions per 1 m3)")
            st.markdown("**1. ค่าทางทฤษฎี (สภาพอิ่มตัวผิวแห้ง - SSD)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            if scm_pct > 0:
                st.write(f"- วัสดุประสานทดแทน ({scm_type}): **{scm_weight:.1f} kg**")
            st.write(f"- ทราย (Fine Agg.): **{fac:.1f} kg**")
            st.write(f"- หิน/มวลรวมทางเลือก (Coarse Agg.): **{cac:.1f} kg**")
            st.write(f"- น้ำ (Free Water): **{fwc:.1f} kg**")
            
            st.write("") 
            st.markdown("**2. ค่าสำหรับชั่งหน้างานจริง (Batched Weights)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            if scm_pct > 0:
                st.write(f"- วัสดุประสานทดแทน ({scm_type}): **{scm_weight:.1f} kg**")
            st.write(f"- ทราย (Batched): **{s_batched:.1f} kg** (+ {free_water_sand:.1f} kg)")
            st.write(f"- หิน (Batched): **{g_batched:.1f} kg** (+ {free_water_gravel:.1f} kg)")
            st.write(f"- น้ำ (เติมจริง): **{w_batched:.1f} kg** (- {free_water_sand + free_water_gravel:.1f} kg)")
            if admix_type != "ไม่มี (None)":
                st.write(f"- ปริมาณสารลดน้ำ: **{admix_vol_liters:.2f} ลิตร**")

            st.write("")
            st.markdown(f"### 3. สัดส่วนสำหรับหล่อตัวอย่าง {num_molds} ก้อน (Trial Mix)")
            st.info(f"ปริมาตรรวม {num_molds} ก้อน: {total_mold_vol_m3:.6f} ลบ.ม. | ปริมาตรเผื่อผสม ({waste_pct:.0f}%): {trial_mix_vol:.6f} ลบ.ม.")
            st.write(f"- ปูนซีเมนต์: **{cc * trial_mix_vol:.2f} kg**")
            if scm_pct > 0:
                st.write(f"- {scm_type}: **{scm_weight * trial_mix_vol:.2f} kg**")
            st.write(f"- ทราย (Batched): **{s_batched * trial_mix_vol:.2f} kg**")
            st.write(f"- หิน (Batched): **{g_batched * trial_mix_vol:.2f} kg**")
            st.write(f"- น้ำ (เติมจริง): **{w_batched * trial_mix_vol:.2f} kg**")
            if admix_type != "ไม่มี (None)":
                st.write(f"- สารลดน้ำ: **{admix_vol_liters * trial_mix_vol * 1000:.1f} ml**")
            
            st.markdown("**เป้าหมายการตรวจสอบหน้าแล็บ (Quality Control)**")
            st.write(f"- น้ำหนักปูนสดต่อ 1 ก้อน (ตามทฤษฎี): **{fresh_conc_weight_per_mold:.2f} kg**")
            if scale_mode == "ชั่งรวมน้ำหนักโมลด์เปล่า":
                st.write(f"- น้ำหนักเป้าหมายเมื่อชั่ง 1 ก้อนพร้อมโมลด์: **{target_scale_weight_per_mold:.2f} kg**")
            st.write(f"*(อ้างอิงจากความหนาแน่นปูนสด Wdcc ที่คำนวณได้ = {wdcc:.0f} kg/m3)*")

        with out_col2:
            st.markdown("### กราฟคาดการณ์การพัฒนากำลังอัด (Strength Development)")
            
            a_coeff, b_coeff = 4.0, 0.85 

            if "แม่เมาะ" in scm_type:
                scm_early_penalty = (scm_pct / 100) * 0.15 # แม่เมาะมี CaO สูง กำลังตกน้อยกว่า
                scm_late_bonus    = (scm_pct / 100) * 0.20
            elif "นำเข้า" in scm_type:
                scm_early_penalty = (scm_pct / 100) * 0.25 
                scm_late_bonus    = (scm_pct / 100) * 0.10
            elif "Slag" in scm_type:
                scm_early_penalty = (scm_pct / 100) * 0.15
                scm_late_bonus    = (scm_pct / 100) * 0.08
            else:
                scm_early_penalty = 0.0
                scm_late_bonus = 0.0

            days = [3, 7, 14, 21, 28, 56, 90]
            strengths_plain = [fm_target * (t / (a_coeff + b_coeff * t)) for t in days]
            strengths_actual = [
                s * (1 - scm_early_penalty * max(0, (28 - d) / 28))
                  * (1 + scm_late_bonus    * min(1, max(0, (d - 28) / 62)))
                for s, d in zip(strengths_plain, days)
            ]
            
            strength_df = pd.DataFrame({
                "สูตรของคุณ (MPa)": [round(x, 1) for x in strengths_actual],
            }, index=days)
            strength_df.index.name = "อายุ (วัน)"
            st.line_chart(strength_df)
            
            # 🎯 เมนูตรวจสอบความแม่นยำกับงานวิจัย (Empirical Validation)
            st.markdown("### ตรวจสอบความแม่นยำกับงานวิจัย (Empirical Data)")
            st.info("อ้างอิงฐานข้อมูลจากเปเปอร์วิชาการเพื่อเทียบเคียงกับสูตรที่คุณออกแบบ")
            st.dataframe(empirical_db)

        st.write("---")
        st.markdown("### บันทึกเพื่อเปรียบเทียบสูตร (Mix Design Comparison)")
        mix_name = st.text_input("ตั้งชื่อสูตรนี้เพื่อบันทึก", "สูตรที่ 1: มาตรฐาน")
        
        if st.button("บันทึกสูตรเข้าสู่ตารางเปรียบเทียบ"):
            new_row = pd.DataFrame([{
                "ชื่อสูตร": mix_name,
                "กำลังอัดเป้าหมาย (MPa)": fm_target,
                "ต้นทุนรวม (บาท)": total_project_cost,
                "การปล่อย CO2 (kg)": total_co2_m3 * project_volume,
                "W/C Ratio": wc
            }])
            st.session_state.mix_history = pd.concat([st.session_state.mix_history, new_row], ignore_index=True)
            
        if not st.session_state.mix_history.empty:
            st.dataframe(st.session_state.mix_history, use_container_width=True)
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.markdown("**เปรียบเทียบต้นทุนรวม (บาท)**")
                st.bar_chart(st.session_state.mix_history.set_index("ชื่อสูตร")["ต้นทุนรวม (บาท)"])
            with comp_col2:
                st.markdown("**เปรียบเทียบปริมาณ CO2 (kg)**")
                st.bar_chart(st.session_state.mix_history.set_index("ชื่อสูตร")["การปล่อย CO2 (kg)"])
                
            if st.button("ล้างข้อมูลเปรียบเทียบ"):
                st.session_state.mix_history = pd.DataFrame(columns=["ชื่อสูตร", "กำลังอัดเป้าหมาย (MPa)", "ต้นทุนรวม (บาท)", "การปล่อย CO2 (kg)", "W/C Ratio"])
                st.rerun()