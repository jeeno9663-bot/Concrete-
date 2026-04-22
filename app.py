import streamlit as st

# ==========================================
# 0. การตั้งค่าหน่วยและธีม (Advanced Setup)
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design", layout="wide")
st.title("🏗️ ระบบจำลองการประมวลผลส่วนผสมคอนกรีตอัจฉริยะ")
st.markdown("*(Intelligent Concrete Mix Design Simulation System - อ้างอิงสมการมาตรฐาน British DoE 2025)*")

unit_system = st.sidebar.radio("ระบบหน่วย (Unit System)", ["SI Units (MPa, kg, mm)", "Inch-Pound Units (psi, lb, in)"])

# ==========================================
# 1. กำหนดเกณฑ์การออกแบบ (Design Criteria)
# ==========================================
st.header("ส่วนที่ 1: กำหนดเกณฑ์การออกแบบ (Design Criteria)")
col_a, col_b = st.columns(2)

with col_a:
    if unit_system == "SI Units (MPa, kg, mm)":
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [MPa]", min_value=10.0, max_value=80.0, value=30.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [mm]", 0.0, 200.0, 100.0)
    else:
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [psi]", min_value=1500.0, max_value=12000.0, value=4000.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [in]", 0.0, 8.0, 4.0)

with col_b:
    max_agg_str = st.selectbox("ขนาดมวลรวมสูงสุด (Max Aggregate Size)", ["10 mm", "20 mm", "40 mm"], index=1)
    max_agg = int(max_agg_str.split()[0]) 
    
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ (Control Factor)", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5

# ==========================================
# 2. ข้อมูลสมบัติวัสดุ (Material Properties)
# ==========================================
st.header("ส่วนที่ 2: ข้อมูลสมบัติวัสดุ (Material Properties)")
col_c, col_d = st.columns(2)

with col_c:
    agg_type = st.radio("ประเภทมวลรวม (Aggregate Type)", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)"])
    
    # 🎯 เพิ่มช่องรับค่า % Passing สำหรับทราย เพื่อใช้เลือกสมการ PFA ให้ถูกต้องตามวิจัย
    p_passing_str = st.selectbox("เปอร์เซ็นต์ทรายผ่านตะแกรง 600 μm", ["100%", "80%", "60%", "40%", "15%"], index=2)
    p_passing = int(p_passing_str.replace("%", ""))

with col_d:
    st.write("**ความถ่วงจำเพาะ (Specific Gravity - SSD)**")
    sg_c = st.number_input("ปูนซีเมนต์ (Cement)", value=3.15, step=0.01)
    sg_s = st.number_input("ทราย (Fine Agg.)", value=2.60, step=0.01)
    sg_g = st.number_input("หิน (Coarse Agg.)", value=2.65, step=0.01)

# ==========================================
# 3. สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)
# ==========================================
st.header("ส่วนที่ 3: สภาวะหน้างาน & สารผสมเพิ่ม (Field & Admixtures)")
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
# 🎯 ฟังก์ชันสมองกล: คำนวณ PFA 60 ชุดสมการ
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
        elif 60 < slump <= 200:
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
        elif 60 < slump <= 200:
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
        elif 60 < slump <= 200:
            if p_passing == 100: pfa_percent = 13.244 * fwc_ratio + 17.106
            elif p_passing == 80: pfa_percent = 15.271 * fwc_ratio + 19.946
            elif p_passing == 60: pfa_percent = 19.427 * fwc_ratio + 22.455
            elif p_passing == 40: pfa_percent = 22.845 * fwc_ratio + 27.980
            elif p_passing == 15: pfa_percent = 29.254 * fwc_ratio + 34.333

    return pfa_percent / 100.0 

# ==========================================
# 4. การประมวลผลและแสดงผล (Smart Logic & Output)
# ==========================================
st.write("---")
if st.button(">>> ประมวลผลส่วนผสมคอนกรีต (CALCULATE) <<<", type="primary", use_container_width=True):
    
    # ---------------- Validation Check ----------------
    fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
    
    if fm_metric > 80.0:
        st.error("⚠️ คำเตือน: ค่ากำลังอัดเกินขอบเขตของสมการมาตรฐานวิจัย (Max 80 MPa)")
    else:
        fm_target = fm_metric / control_factor 
        
        # ---------------- สมองกลประมวลผล ----------------
        # 1. หาสัดส่วน W/C (Fw/c) 
        if agg_type == "หินธรรมชาติ (Uncrushed)":
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
        
        # 2. ปริมาณน้ำอิสระ (Free Water)
        slump_mm = slump if unit_system == "SI Units (MPa, kg, mm)" else slump * 25.4
        fwc_base = 195.0 + (0.2 * slump_mm) - (0.4 * max_agg) 
        
        # ปรับลดน้ำตามคุณสมบัติน้ำยา
        fwc = fwc_base * (1 - water_reduction)
        
        # 3. ปริมาณซีเมนต์
        cc = fwc / wc 
        
        # คำนวณปริมาณน้ำยาที่ต้องตวงหน้างาน
        admix_vol_liters = (cc / 100) * (admix_dosage / 1000)
        admix_weight_kg = admix_vol_liters * admix_sg
        
        # 4. หาความหนาแน่นคอนกรีตสด (Wdcc) 
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
            
        # 5. หาปริมาณมวลรวมทั้งหมด
        ac = wdcc - cc - fwc
        
        # 🎯 6. หาสัดส่วนทราย (ดึงสมการ 60 ชุด มาใช้งานอย่างสมบูรณ์แบบ)
        pfa = get_pfa(max_agg, slump_mm, p_passing, wc)
        fac = pfa * ac
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
        st.header("ส่วนที่ 4: การแสดงผลลัพธ์ (Output Data)")
        if admix_type != "ไม่มี (None)":
            st.success(f"✅ อัลกอริทึมทำงานเสร็จสมบูรณ์ | การใช้สารลดน้ำช่วยลดปริมาณน้ำ {water_reduction*100}% | Error Margin: 0.65%-3.00%")
        else:
            st.success(f"✅ อัลกอริทึมทำงานเสร็จสมบูรณ์ | Error Margin: 0.65%-3.00%")
        
        res1, res2, res3 = st.columns(3)
        res1.metric("กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        res2.metric("อัตราส่วน W/C Ratio", f"{wc:.3f}")
        res3.metric("ความหนาแน่นคอนกรีตสด", f"{wdcc:.1f} kg/m³")
        
        st.write("---")
        st.subheader("📦 น้ำหนักวัสดุต่อ 1 ลูกบาศก์เมตร (kg/m³)")
        
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
            st.write(f"- ทราย (Batched): **{s_batched:.1f} kg** *(+ {free_water_sand:.1f} kg)*")
            st.write(f"- หิน (Batched): **{g_batched:.1f} kg** *(+ {free_water_gravel:.1f} kg)*")
            st.write(f"- น้ำ (เติมจริง): **{w_batched:.1f} kg** *(- {free_water_sand + free_water_gravel:.1f} kg)*")
            
            if admix_type != "ไม่มี (None)":
                st.info(f"🧪 **ปริมาณสารลดน้ำที่ต้องตวง:** **{admix_weight_kg:.2f} kg** (หรือประมาณ {admix_vol_liters:.2f} ลิตร)")
            
        st.info(f"⚖️ สัดส่วนผสมโดยประมาณ (Cement : Sand : Gravel) = **1 : {(fac/cc):.2f} : {(cac/cc):.2f}**")
        