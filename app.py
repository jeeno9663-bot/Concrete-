import streamlit as st

# ---------------- ส่วนที่ 1: ตั้งค่าหน้าจอ (Setup) ----------------
st.set_page_config(page_title="Mix Design App", layout="wide")
st.title("แอปพลิเคชันออกแบบส่วนผสมคอนกรีต")
st.write("สร้างตรรกะการคำนวณจากสมการคณิตศาสตร์แทนการเปิดตารางกราฟ")

# ---------------- ส่วนที่ 2: การสร้างช่องรับข้อมูล (Inputs) ----------------
st.sidebar.header("กรอกข้อมูลตั้งต้น")

# ให้ผู้ใช้กรอกกำลังอัด f'c
fc_prime = st.sidebar.number_input("กำลังอัด f'c (ksc)", value=280)

# ให้ผู้ใช้เลือกค่ายุบตัวและขนาดหินจาก Dropdown
slump = st.sidebar.selectbox("ค่ายุบตัว Slump (mm)", [50, 100, 150])
max_agg = st.sidebar.selectbox("ขนาดหินใหญ่สุด (mm)", [10, 20, 25])

# ---------------- ส่วนที่ 3: สมองกลคำนวณ (The Logic Function) ----------------
def calculate_mix(fc, slump, max_agg):
    
    # 1. จำลองการเผื่อค่าความปลอดภัย (Target Strength)
    fm = fc + 85
    
    # 2. หาสัดส่วน W/C ด้วยสมการเชิงเส้น
    # ยิ่งกำลังอัดเป้าหมาย (fm) สูง ค่า W/C จะยิ่งต่ำลง
    wc_ratio = 0.85 - (0.0012 * fm)
    
    # 3. หาปริมาณน้ำ (สมการจำลองความสัมพันธ์ของ Slump และขนาดหิน)
    water = 195 + (0.2 * slump) - (0.4 * max_agg)
    
    # 4. หาปริมาณปูนซีเมนต์
    cement = water / wc_ratio
    
    # 5. สมมติปริมาณหินคงที่ (เพื่อความง่ายในการเรียนรู้)
    gravel = 1050
    
    # 6. หาทรายด้วยวิธีปริมาตรสัมบูรณ์ (Absolute Volume)
    # สมมติ Specific Gravity ปูน=3.15, หิน=2.65, ทราย=2.60
    vol_water = water / 1000
    vol_cement = cement / (3.15 * 1000)
    vol_gravel = gravel / (2.65 * 1000)
    vol_air = 0.02 # เผื่ออากาศ 2%
    
    # ปริมาตรทราย = 1 คิว - ปริมาตรวัสดุอื่นๆ
    vol_sand = 1.0 - (vol_water + vol_cement + vol_gravel + vol_air)
    sand = vol_sand * (2.60 * 1000)
    
    # ส่งค่ากลับไปแสดงผล
    return cement, sand, gravel, water, wc_ratio

# ---------------- ส่วนที่ 4: สร้างปุ่มกดและแสดงผล (Output Dashboard) ----------------
st.write("---") # สร้างเส้นคั่น

# ถ้าผู้ใช้กดปุ่ม "คำนวณสัดส่วนผสม" ให้ทำคำสั่งต่อไปนี้
if st.button("คำนวณสัดส่วนผสม"):
    
    # เรียกใช้งานสมองกลในส่วนที่ 3
    c, s, g, w, wc = calculate_mix(fc_prime, slump, max_agg)
    
    st.success(f"คำนวณเสร็จสิ้น! อัตราส่วน W/C ที่เหมาะสมคือ {wc:.2f}")
    
    # แบ่งหน้าจอเป็น 4 คอลัมน์เพื่อความสวยงาม
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ปูนซีเมนต์", f"{c:.1f} kg")
    col2.metric("ทราย", f"{s:.1f} kg")
    col3.metric("หิน", f"{g:.1f} kg")
    col4.metric("น้ำ", f"{w:.1f} kg")
