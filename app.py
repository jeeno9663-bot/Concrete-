import streamlit as st

# ==========================================
# 1. ตั้งค่าหน้าเว็บ (UI Setup)
# ==========================================
st.set_page_config(page_title="Smart Concrete Mix (DoE Method)", layout="wide")
st.title("🏗️ Smart Concrete Mix Algorithm")
st.markdown("**ประมวลผลด้วยสมการคณิตศาสตร์อ้างอิงมาตรฐาน British DoE (Aguwa & Abubakar, 2025)**")

# ==========================================
# 2. การรับข้อมูล (Input Module)
# ==========================================
st.sidebar.header("📥 ข้อมูลตั้งต้น (Input)")
fc_target = st.sidebar.number_input("กำลังอัดเป้าหมาย Fm (N/mm² หรือ MPa)", min_value=10.0, max_value=80.0, value=40.0, step=1.0)
agg_type = st.sidebar.radio("ประเภทมวลรวม (Aggregate Type)", ["มวลรวมไม่โม่ (Uncrushed)", "มวลรวมโม่ (Crushed)"])
ssdd = st.sidebar.selectbox("ความถ่วงจำเพาะรวม (SSDD)", [2.9, 2.8, 2.7, 2.6, 2.5, 2.4], index=3)

# สมมติค่าเพื่อความเข้าใขง่ายใน Baby Project
free_water = st.sidebar.number_input("ปริมาณน้ำอิสระ Fwc (kg/m³)", value=195.0, step=5.0)

# ==========================================
# 3. สมองกลประมวลผล (Algorithm Module - British DoE)
# ==========================================
def calculate_doe_mix(Fm, agg_type, ssdd, Fwc):
    
    # 1. สมการหาอัตราส่วนน้ำต่อซีเมนต์ (Fw/c)
    if agg_type == "มวลรวมไม่โม่ (Uncrushed)":
        if Fm <= 42:
            Fwc_ratio = (0.0002952 * (Fm**2)) - (0.0312 * Fm) + 1.291 # Eq (2)
        else:
            Fwc_ratio = (0.00008519 * (Fm**2)) - (0.01571 * Fm) + 1.0097 # Eq (3)
    else: # มวลรวมโม่ (Crushed)
        if Fm <= 42:
            Fwc_ratio = (0.000295 * (Fm**2)) - (0.0312 * Fm) + 1.351 # Eq (4)
        else:
            Fwc_ratio = (0.000008519 * (Fm**2)) - (0.01571 * Fm) + 1.0697 # Eq (5)
            
    # 2. สมการที่ 6: ปริมาณซีเมนต์ (Cement Content)
    Cc = Fwc / Fwc_ratio
    
    # 3. สมการความหนาแน่นคอนกรีตสด (Wdcc) ตามค่า SSDD
    if ssdd == 2.9:
        Wdcc = -1.7440 * Fwc + 2898.4795 # Eq (7)
    elif ssdd == 2.8:
        Wdcc = -1.5961 * Fwc + 2802.5554 # Eq (8)
    elif ssdd == 2.7:
        Wdcc = -1.4480 * Fwc + 2702.8337 # Eq (9)
    elif ssdd == 2.6:
        Wdcc = -1.2492 * Fwc + 2410.3614 # Eq (10)
    elif ssdd == 2.5:
        Wdcc = -1.0996 * Fwc + 2500.6876 # Eq (11)
    else:
        Wdcc = -0.9809 * Fwc + 2410.3614 # Eq (12)
        
    # 4. สมการที่ 13: ปริมาณมวลรวมรวม (Total Aggregate)
    Ac = Wdcc - Cc - Fwc
    
    # 5. สมการสัดส่วนมวลรวมละเอียด (Pfa) 
    # *จำลองการใช้สมการที่ (37) สำหรับขนาด 20mm, Slump 0-10mm ทราย 40% เพื่อเป็นโมเดลต้นแบบ
    Pfa_percent = (23.6469 * Fwc_ratio) + 22.0002
    Pfa = Pfa_percent / 100.0
    
    # 6. สมการที่ 74 และ 75: แยกปริมาณทรายและหิน
    Fac = Pfa * Ac
    Cac = Ac - Fac
    
    return Cc, Fac, Cac, Fwc, Fwc_ratio, Wdcc

# ==========================================
# 4. การแสดงผล (Output Dashboard)
# ==========================================
st.write("---")
if st.button("🚀 รันอัลกอริทึม (Calculate Mix)", type="primary"):
    
    # ดึงสมองกลมาทำงาน
    Cc, Fac, Cac, Fwc, Fwc_ratio, Wdcc = calculate_doe_mix(fc_target, agg_type, ssdd, free_water)
    
    st.success(f"✅ ประมวลผลสำเร็จ! (Target W/C Ratio = {Fwc_ratio:.3f}) | ความหนาแน่นเป้าหมาย = {Wdcc:.1f} kg/m³")
    
    # ส่วนแสดงผลลัพธ์
    st.subheader("📊 สัดส่วนผสมทางทฤษฎี (kg/m³)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ปูนซีเมนต์ (Cement)", f"{Cc:.1f} kg")
    col2.metric("ทราย (Fine Agg.)", f"{Fac:.1f} kg")
    col3.metric("หิน (Coarse Agg.)", f"{Cac:.1f} kg")
    col4.metric("น้ำ (Free Water)", f"{Fwc:.1f} kg")
    
    st.info("💡 หมายเหตุ: อัลกอริทึมนี้ใช้สมการพหุนามและสมการเชิงเส้นตามงานวิจัย Aguwa & Abubakar (2025) ทดแทนการเปิดตารางมาตรฐาน British DoE")
