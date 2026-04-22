import streamlit as st

# ==========================================
# 0. การตั้งค่าหน่วยและธีม (Advanced Setup)
# ==========================================
st.set_page_config(page_title="Intelligent Mix Design", layout="wide")
st.title("🏗️ ระบบจำลองการประมวลผลส่วนผสมคอนกรีตอัจฉริยะ")
st.markdown("*(Intelligent Concrete Mix Design Simulation System)*")

# [span_2](start_span)เลือกหน่วยวัด (Unit Switching Feature)[span_2](end_span)
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
    max_agg = st.selectbox("ขนาดมวลรวมสูงสุด (Max Aggregate Size)", ["10 mm", "20 mm", "40 mm"])
    # [span_3](start_span)ระดับการควบคุมคุณภาพ (Control Factor)[span_3](end_span)
    control_label = st.selectbox("ระดับการควบคุมคุณภาพ (Control Factor)", ["ดีมาก (Very Good - 0.8)", "ปานกลาง (Fair - 0.7)", "ต่ำ (Low - 0.5)"])
    control_factor = 0.8 if "0.8" in control_label else 0.7 if "0.7" in control_label else 0.5

# ==========================================
# 2. ข้อมูลสมบัติวัสดุ (Material Properties)
# ==========================================
st.header("ส่วนที่ 2: ข้อมูลสมบัติวัสดุ (Material Properties)")
col_c, col_d = st.columns(2)

with col_c:
    [span_4](start_span)agg_type = st.radio("ประเภทมวลรวม (Aggregate Type)", ["หินโม่ (Crushed)", "หินธรรมชาติ (Uncrushed)"])[span_4](end_span)
    [span_5](start_span)fm_sand = st.number_input("ค่าความละเอียดทราย (Fineness Modulus)", value=2.8)[span_5](end_span)

with col_d:
    st.write("**ความถ่วงจำเพาะ (Specific Gravity)**")
    [span_6](start_span)sg_c = st.number_input("ปูนซีเมนต์ (Cement)", value=3.15)[span_6](end_span)
    sg_s = st.number_input("ทราย (Fine Agg.)", value=2.60)
    sg_g = st.number_input("หิน (Coarse Agg.)", value=2.65)

# ==========================================
# 3. [span_7](start_span)สภาวะหน้างานจริง (Field Adjustments)[span_7](end_span)
# ==========================================
st.header("ส่วนที่ 3: สภาวะหน้างานจริง (Field Adjustments)")
col_e, col_f = st.columns(2)

with col_e:
    mc_sand = st.number_input("ความชื้นในทราย (Moisture Content %)", value=5.0)
    abs_sand = st.number_input("การดูดซึมของทราย (Absorption %)", value=1.0)

with col_f:
    mc_gravel = st.number_input("ความชื้นในหิน (Moisture Content %)", value=2.0)
    abs_gravel = st.number_input("การดูดซึมของหิน (Absorption %)", value=0.5)

# ==========================================
# 4. การประมวลผลและแสดงผล (Logic & Output)
# ==========================================
st.write("---")
if st.button(">>> ประมวลผลส่วนผสม (CALCULATE) <<<", type="primary"):
    
    # [span_8](start_span)Validation Check: ตรวจสอบขอบเขตกำลังอัด[span_8](end_span)
    if fc_req > 80 and unit_system == "SI Units (MPa, kg, mm)":
        st.error("⚠️ คำเตือน: ค่ากำลังอัดเกินขอบเขตของสมการมาตรฐาน (Max 80 MPa)")
    else:
        # [span_9](start_span)แปลงหน่วยเป็น Metric เพื่อใช้คำนวณในสมการหลัก (DoE Method)[span_9](end_span)
        fm_metric = fc_req if unit_system == "SI Units (MPa, kg, mm)" else fc_req * 0.00689476
        [span_10](start_span)fm_target = fm_metric / control_factor # คำนวณกำลังเป้าหมายตาม Control Factor[span_10](end_span)
        
        # [span_11](start_span)สมการหา W/C จากงานวิจัย Aguwa (2025)[span_11](end_span)
        if agg_type == "หินธรรมชาติ (Uncrushed)":
            wc = (0.0002952 * (fm_target**2)) - (0.0312 * fm_target) + 1.291 if fm_target <= 42 else (0.00008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0097
        else:
            wc = (0.000295 * (fm_target**2)) - (0.0312 * fm_target) + 1.351 if fm_target <= 42 else (0.000008519 * (fm_target**2)) - (0.01571 * fm_target) + 1.0697
        
        # ปริมาณน้ำ (จำลองจากตาราง DoE)
        fwc = 190.0 # kg/m3
        [span_12](start_span)cc = fwc / wc # ปริมาณซีเมนต์[span_12](end_span)
        
        # การแสดงผล
        st.header("ส่วนที่ 4: การแสดงผลลัพธ์ (Output Data)")
        res1, res2 = st.columns(2)
        
        with res1:
            st.metric("อัตราส่วน W/C Ratio", f"{wc:.2f}")
            st.metric("กำลังอัดเป้าหมาย (fm)", f"{fm_target:.1f} MPa")
        
        with res2:
            st.write("**น้ำหนักวัสดุต่อ 1 ลูกบาศก์เมตร**")
            # [span_13](start_span)คำนวณการปรับแก้ความชื้นจริงหน้างาน [cite: 869-879]
            sand_ssd = 650.0 # ค่าสมมติสำหรับตัวอย่าง
            s_od = sand_ssd / (1 + (abs_sand/100))
            s_batched = sand_ssd + (s_od * (mc_sand - abs_sand)/100)
            
            st.write(f"- ปูนซีเมนต์: {cc:.1f} kg")
            st.write(f"- น้ำอิสระ: {fwc:.1f} kg")
            st.write(f"- ทราย (Batched): {s_batched:.1f} kg")
            [cite_start]st.info(f"สัดส่วนโดยประมาณ 1 : {(sand_ssd/cc):.2f} : 3.50")[span_13](end_span)

