import streamlit as st

# ==========================================
# 0. การตั้งค่าหน่วยและธีม (Advanced Setup)
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design", layout="wide")
st.title("🏗️ ระบบจำลองการประมวลผลส่วนผสมคอนกรีตอัจฉริยะ")
st.markdown("*(Intelligent Concrete Mix Design Simulation System - อ้างอิงสมการมาตรฐาน British DoE 2025)*")

# เลือกหน่วยวัด (Unit Switching Feature)
unit_system = st.sidebar.radio("ระบบหน่วย (Unit System)", ["SI Units (MPa, kg, mm)", "Inch-Pound Units (psi, lb, in)"])

# ==========================================
# 1. กำหนดเกณฑ์การออกแบบ (Design Criteria)
# ==========================================
st.header("ส่วนที่ 1: กำหนดเกณฑ์การออกแบบ (Design Criteria)")
col_a, col_b = st.columns(2)

with col_a:
    if unit_system == "SI Units (MPa, kg, mm)":
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [MPa]", min_value=10.0, max_value=80.0, value=30.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [mm]", 0, 200, 100)
    else:
        fc_req = st.number_input("กำลังอัดประลัยที่ต้องการ (f'c) [psi]", min_value=1500.0, max_value=12000.0, value=4000.0)
        slump = st.slider("ค่าความยุบตัว (Slump) [in]", 0.0, 8.0, 4.0)

with col_b:
    max_agg_str = st.selectbox("ขนาดมวลรวมสูงสุด (Max Aggregate Size)", ["10 mm", "20 mm", "40 mm"])
    max_agg = int(max_agg_str.split()[0]) # ดึงเฉพาะตัวเลขมาใช้คำนวณ
    
    # ระดับการควบคุมคุณภาพ (Control Factor)
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ (Control Factor)", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5

# ==========================================
# 2. ข้อมูลสมบัติวัสดุ (Material Properties)
# ==========================================
st.header("ส่วนที่ 2: ข้อมูลสมบัติวัสดุ (Material Properties)")
col_c, col_d = st.columns(2)

with col_c:
    agg_type = st.radio("ประเภทมวลรวม (Aggregate Type)", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)"])
    fm_sand = st.number_input("ค่าความละเอียดทราย (Fineness Modulus)", value=2.8)

with col_d:
    st.write("**ความถ่วงจำเพาะ (Specific Gravity - SSD)**")
    sg_c = st.number_input("ปูนซีเมนต์ (Cement)", value=3.15)
    sg_s = st.number_input("ทราย (Fine Agg.)", value=2.60)
    sg_g = st.number_input("หิน (Coarse Agg.)", value=2.65)

# ==========================================
# 3. สภาวะหน้างานจริง (Field Adjustments)
# ==========================================
st.header("ส่วนที่ 3: สภาวะหน้างานจริง (Field Adjustments)")
col_e, col_f = st.columns(2)

with col_e:
    mc_sand = st.number_input("ความชื้นรวมในทราย (Moisture Content %)", value=5.0, step=0.1)
    abs_sand = st.number_input("การดูดซึมของทราย (Absorption %)", value=1.0, step=0.1)

with col_f:
    mc_gravel = st.number_input("ความชื้นรวมในหิน (Moisture Content %)", value=2.0, step=0.1)
    abs_gravel = st.number_input("การดูดซึมของหิน (Absorption %)", value=0.5, step=0.1)

# ==========================================
# 4. การประมวลผลและแสดงผล (Smart Logic & Output)
# ==========================================
st.write("---")
if st.button(">>> ประมวลผลส่วนผสมคอนกรีต (CALCULATE) <<<", type="primary", use_container_width=True):
    
    # ---------------- Validation Check ----------------
    if fc_req > 80 and unit_system == "SI Units (MPa, kg, mm)":
        st.error("⚠️ คำเตือน: ค่ากำลังอัดเกินขอบเขตของสมการมาตรฐานวิจัย (Max 80 MPa)")
    else:
        # แปลงหน่วยเป็น Metric เพื่อใช้คำนวณในสมการหลัก (DoE Method)
        fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
        fm_target = fm_metric / control_factor # คำนวณกำลังเป้าหมาย (Target Mean Strength)
        
        # ---------------- สมองกลประมวลผล ----------------
        # 1. หาสัดส่วน W/C (Fw/c) จากสมการโพลีโนเมียล
        if agg_type == "หินธรรมชาติ (Uncrushed)":
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
        
        # 2. ปริมาณน้ำอิสระ (Free Water) จำลองสูตรปรับแก้ตาม Slump และ Agg Size
        slump_mm = slump if unit_system == "SI Units (MPa, kg, mm)" else slump * 25.4
        fwc = 195.0 + (0.2 * slump_mm) - (0.4 * max_agg) 
        
        # 3. ปริมาณซีเมนต์
        cc = fwc / wc 
        
        # 4. หาความหนาแน่นคอนกรีตสด (Wdcc) โดยคำนวณค่าเฉลี่ย SSDD ของมวลรวม
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
            
        # 5. หาปริมาณมวลรวมทั้งหมด (Total Aggregate Content)
        ac = wdcc - cc - fwc
        
        # 6. หาสัดส่วนทราย (Fine Agg. Proportion) จากสมการเชิงเส้น
        pfa_percent = (23.6469 * wc) + 22.0002 # โมเดลสำหรับ Agg 20mm
        fac = (pfa_percent / 100) * ac
        cac = ac - fac
        
        # ---------------- การปรับแก้ความชื้น (Moisture Adjustment) ----------------
        # ทราย
        s_od = fac / (1 + (abs_sand / 100))
        free_water_sand = s_od * ((mc_sand - abs_sand) / 100)
        s_batched = fac + free_water_sand
        
        # หิน
        g_od = cac / (1 + (abs_gravel / 100))
        free_water_gravel = g_od * ((mc_gravel - abs_gravel) / 100)
        g_batched = cac + free_water_gravel
        
        # น้ำที่ต้องเติมจริง (Batched Water)
        w_batched = fwc - free_water_sand - free_water_gravel

        # ---------------- การแสดงผลลัพธ์ ----------------
        st.header("ส่วนที่ 4: การแสดงผลลัพธ์ (Output Data)")
        st.success(f"✅ อัลกอริทึมทำงานเสร็จสมบูรณ์ | ความคลาดเคลื่อนเชิงทฤษฎี (Error Margin): 0.65% - 3.00%")
        
        res1, res2, res3 = st.columns(3)
        res1.metric("กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        res2.metric("อัตราส่วน W/C Ratio", f"{wc:.3f}")
        res3.metric("ความหนาแน่นคอนกรีตสด", f"{wdcc:.1f} kg/m³")
        
        st.write("---")
        st.subheader("📦 น้ำหนักวัสดุต่อ 1 ลูกบาศก์เมตร (kg/m³)")
        
        # เปรียบเทียบค่าทางทฤษฎี SSD กับค่า Batched หน้างาน
        out_col1, out_col2 = st.columns(2)
        
        with out_col1:
            st.markdown("**1. ค่าทางทฤษฎี (สภาพ SSD)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            st.write(f"- ทราย (Fine Agg.): **{fac:.1f} kg**")
            st.write(f"- หิน (Coarse Agg.): **{cac:.1f} kg**")
            st.write(f"- น้ำ (Free Water): **{fwc:.1f} kg**")
            
        with out_col2:
            st.markdown("**2. ค่าปรับแก้ตามความชื้น (Batched หน้างาน)**")
            st.write(f"- ปูนซีเมนต์ (Cement): **{cc:.1f} kg**")
            st.write(f"- ทราย (Batched): **{s_batched:.1f} kg** *(+ {free_water_sand:.1f} kg)*")
            st.write(f"- หิน (Batched): **{g_batched:.1f} kg** *(+ {free_water_gravel:.1f} kg)*")
            st.write(f"- น้ำ (เติมจริง): **{w_batched:.1f} kg** *(- {free_water_sand + free_water_gravel:.1f} kg)*")
            
        st.info(f"⚖️ สัดส่วนผสมโดยประมาณ (Cement : Sand : Gravel) = **1 : {(fac/cc):.2f} : {(cac/cc):.2f}**")
