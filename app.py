import streamlit as st

# ==========================================
# 0. การตั้งค่าหน่วยและธีม (Advanced Setup)
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design", layout="wide", initial_sidebar_state="expanded")

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>ระบบจำลองการออกแบบส่วนผสมคอนกรีตอัจฉริยะ</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #7F8C8D; margin-bottom: 30px;'>(Web-Based Intelligent Concrete Mix Design Simulation System)</h4>", unsafe_allow_html=True)

unit_system = st.sidebar.radio("ระบบหน่วย (Unit System)", ["SI Units (MPa, kg, mm)", "Inch-Pound Units (psi, lb, in)"])

# ==========================================
# 1. กำหนดเกณฑ์การออกแบบ (Design Criteria)
# ==========================================
st.header("กำหนดเกณฑ์การออกแบบ (Design Criteria)")
col_a, col_b = st.columns(2)

with col_a:
    if unit_system == "SI Units (MPa, kg, mm)":
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [MPa]", min_value=10.0, max_value=80.0, value=30.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [mm]", 0.0, 200.0, 100.0)
    else:
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [psi]", min_value=1500.0, max_value=12000.0, value=4000.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [in]", 0.0, 8.0, 4.0)
        
    specimen_type = st.radio("ประเภทตัวอย่างทดสอบ (Specimen Type)", ["ทรงกระบอก (Cylinder)", "ลูกบาศก์ (Cube)"])

with col_b:
    max_agg_str = st.selectbox("ขนาดมวลรวมสูงสุด (Max Aggregate Size)", ["10 mm", "20 mm", "40 mm"], index=1)
    max_agg = int(max_agg_str.split()[0]) 
    
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ (Control Factor)", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5

# ==========================================
# 2. ข้อมูลสมบัติวัสดุ (Material Properties)
# ==========================================
st.header("ข้อมูลสมบัติวัสดุ (Material Properties)")
col_c, col_d = st.columns(2)

with col_c:
    agg_type = st.radio("ประเภทมวลรวม (Aggregate Type)", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)"])
    
    p_passing_str = st.selectbox("เปอร์เซ็นต์ทรายผ่านตะแกรง 600 μm", ["100%", "80%", "60%", "40%", "15%"], index=2)
    passing_600 = int(p_passing_str.replace("%", ""))

with col_d:
    st.write("**ความถ่วงจำเพาะ (Specific Gravity - SSD)**")
    sg_c = st.number_input("ปูนซีเมนต์ (Cement)", value=3.15, step=0.01)
    sg_s = st.number_input("ทราย (Fine Agg.)", value=2.60, step=0.01)
    sg_g = st.number_input("หิน (Coarse Agg.)", value=2.65, step=0.01)

# ==========================================
# 3. สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)
# ==========================================
st.header("สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)")
col_e, col_f, col_g = st.columns(3)

with col_e:
    st.write("**ความชื้นในทราย**")
    mc_sand = st.number_input("ความชื้นรวมทราย (%)", value=5.0, step=0.1)
    abs_sand = st.number_input("การดูดซึมทราย (%)", value=1.0, step=0.1)

with col_f:
    st.write("**ความชื้นในหิน**")
    mc_gravel = st.number_input("ความชื้นรวมหิน (%)", value=2.0, step=0.1)
    abs_gravel = st.number_input("การดูดซึมหิน (%)", value=0.5, step=0.1)

with col_g:
    st.write("**คุณสมบัติสารผสมเพิ่ม (Admixture Properties)**")
    admix_type = st.selectbox("การใช้สารลดน้ำ", ["ไม่มี (None)", "กำหนดค่าเอง (Custom WRA/HRWRA)"])
    
    if admix_type != "ไม่มี (None)":
        water_reduction_pct = st.number_input("ประสิทธิภาพการลดน้ำ (%)", min_value=0.0, max_value=40.0, value=12.0, step=1.0)
        water_reduction = water_reduction_pct / 100.0
        
        admix_dosage = st.number_input("ปริมาณการใช้ (ml ต่อ ปูน 100 kg)", value=1000.0, step=50.0)
        admix_sg = st.number_input("ความถ่วงจำเพาะน้ำยา (S.G.)", value=1.05, step=0.01)
    else:
        water_reduction = 0.0
        admix_dosage = 0.0
        admix_sg = 1.0

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
            elif passing_600 == 40: pfa = 25.16660 * wc + 22.6650
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
# 4. การประมวลผลและแสดงผล (Calculation & Output)
# ==========================================
st.header("การประมวลผลและผลลัพธ์ (Calculation & Output)")
st.write("---")
if st.button("ประมวลผลส่วนผสมคอนกรีต (CALCULATE)", type="primary", use_container_width=True):
    
    # ---------------- ตรรกะการแปลงค่า Cylinder เป็น Cube ----------------
    fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
    
    if specimen_type == "ทรงกระบอก (Cylinder)":
        fm_cube = fm_metric * 1.22
    else:
        fm_cube = fm_metric
        
    fm_target = fm_cube / control_factor
    
    # ---------------- Validation Check ----------------
    if fm_cube > 80.0:
        st.error("คำเตือน: ค่ากำลังอัดเทียบเท่า Cube เกินขอบเขตของสมการมาตรฐานวิจัย (Max 80 MPa)")
    else:
        # ---------------- สมองกลประมวลผล ----------------
        if agg_type == "หินธรรมชาติ (Uncrushed)":
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
        
        slump_mm = slump if unit_system == "SI Units (MPa, kg, mm)" else slump * 25.4
        fwc_base = 195.0 + (0.2 * slump_mm) - (0.4 * max_agg) 
        
        fwc = fwc_base * (1 - water_reduction)
        cc = fwc / wc 
        
        admix_vol_liters = (cc / 100) * (admix_dosage / 1000)
        admix_weight_kg = admix_vol_liters * admix_sg
        
        ssdd_avg = round((sg_s + sg_g) / 2, 1)
        if ssdd_avg >= 2.9:
            wdcc = -1.7440 * fwc + 2898.4795
        elif ssdd_avg == 2.8:
            wdcc = -1.5961 * fwc + 2802.5554
        elif ssdd_avg == 2.7:
            wdcc = -1.4480 * fwc + 2702.8337
        elif ssdd_avg == 2.6:
            wdcc = -1.2492 * fwc + 2410.3614
        elif ssdd_avg == 2.5:
            wdcc = -1.0996 * fwc + 2500.6876
        else:
            wdcc = -0.9809 * fwc + 2410.3614
            
        ac = wdcc - cc - fwc
        
        pfa_ratio = calculate_pfa(max_agg, slump_mm, wc, passing_600)
        fac = pfa_ratio * ac
        cac = ac - fac
        
        # ---------------- การปรับแก้ความชื้น (Moisture Adjustment) ----------------
        s_od = fac / (1 + (abs_sand / 100))
        free_water_sand = s_od * ((mc_sand - abs_sand) / 100)
        s_batched = fac + free_water_sand
        
        g_od = cac / (1 + (abs_gravel / 100))
        free_water_gravel = g_od * ((mc_gravel - abs_gravel) / 100)
        g_batched = cac + free_water_gravel
        
        w_batched = fwc - free_water_sand - free_water_gravel

        # ---------------- การแสดงผลลัพธ์ ----------------
        if admix_type != "ไม่มี (None)":
            st.success(f"อัลกอริทึมทำงานเสร็จสมบูรณ์ | การใช้สารลดน้ำช่วยลดปริมาณน้ำ {water_reduction*100}% | Error Margin: 0.65%-3.00%")
        else:
            st.success(f"อัลกอริทึมทำงานเสร็จสมบูรณ์ | Error Margin: 0.65%-3.00%")
        
        res1, res2, res3 = st.columns(3)
        res1.metric("กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        res2.metric("อัตราส่วน W/C Ratio", f"{wc:.3f}")
        res3.metric("ความหนาแน่นคอนกรีตสด", f"{wdcc:.1f} kg/m³")
        
        st.write("---")
        st.subheader("น้ำหนักวัสดุต่อ 1 ลูกบาศก์เมตร (kg/m³)")
        
        out_col1, out_col2 = st.columns(2)
        
        with out_col1:
            st.markdown("**1. ค่าทางทฤษฎี (สภาพอิ่มตัวผิวแห้ง - SSD)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            st.write(f"- ทราย (Fine Agg.): **{fac:.1f} kg**")
            st.write(f"- หิน (Coarse Agg.): **{cac:.1f} kg**")
            st.write(f"- น้ำ (Free Water): **{fwc:.1f} kg**")
            
        with out_col2:
            st.markdown("**2. ค่าสำหรับชั่งหน้างานจริง (Batched Weights)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            st.write(f"- ทราย (Batched): **{s_batched:.1f} kg** (+ {free_water_sand:.1f} kg)")
            st.write(f"- หิน (Batched): **{g_batched:.1f} kg** (+ {free_water_gravel:.1f} kg)")
            st.write(f"- น้ำ (เติมจริง): **{w_batched:.1f} kg** (- {free_water_sand + free_water_gravel:.1f} kg)")
            
            if admix_type != "ไม่มี (None)":
                st.info(f"ปริมาณสารลดน้ำที่ต้องตวง: **{admix_weight_kg:.2f} kg** (หรือประมาณ {admix_vol_liters:.2f} ลิตร)")
            
        st.info(f"สัดส่วนผสมโดยประมาณ (Cement : Sand : Gravel) = **1 : {(fac/cc):.2f} : {(cac/cc):.2f}**")