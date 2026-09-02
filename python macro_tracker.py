import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ตัวคำนวณ Macros", page_icon="🥗", layout="centered")

# ฐานข้อมูลสารอาหารขยายใหญ่ (ต่อ 100g หรือ 1 หน่วย)
NUTRITION_DATA = {
    # --- หมวดเนื้อสัตว์ & อาหารทะเล ---
    "อกไก่สด (100g)": {"protein": 23.0, "carbs": 0.0, "fat": 1.2, "cal": 120.0, "unit": "กรัม"},
    "อกไก่สุก (100g)": {"protein": 31.0, "carbs": 0.0, "fat": 3.6, "cal": 165.0, "unit": "กรัม"},
    "สันในหมู (100g)": {"protein": 21.0, "carbs": 0.0, "fat": 4.0, "cal": 124.0, "unit": "กรัม"},
    "เนื้อวัวบดไร้มัน (100g)": {"protein": 20.0, "carbs": 0.0, "fat": 10.0, "cal": 170.0, "unit": "กรัม"},
    "แซลมอนสด (100g)": {"protein": 20.0, "carbs": 0.0, "fat": 13.0, "cal": 208.0, "unit": "กรัม"},
    "กุ้งขาวสุก (100g)": {"protein": 24.0, "carbs": 0.2, "fat": 0.3, "cal": 99.0, "unit": "กรัม"},
    "ปลากะพง (100g)": {"protein": 18.5, "carbs": 0.0, "fat": 2.0, "cal": 97.0, "unit": "กรัม"},
    "ทูน่าในน้ำแร่ (100g)": {"protein": 25.0, "carbs": 0.0, "fat": 1.0, "cal": 116.0, "unit": "กรัม"},

    # --- หมวดไข่ & ผลิตภัณฑ์จากนม ---
    "ไข่ไก่ (1 ฟอง)": {"protein": 6.0, "carbs": 0.6, "fat": 5.0, "cal": 70.0, "unit": "ฟอง"},
    "ไข่ขาว (1 ฟอง)": {"protein": 3.6, "carbs": 0.2, "fat": 0.0, "cal": 17.0, "unit": "ฟอง"},
    "นมจืด (1 แก้ว 200ml)": {"protein": 6.5, "carbs": 9.5, "fat": 7.5, "cal": 130.0, "unit": "แก้ว"},
    "กรีกโยเกิร์ต (100g)": {"protein": 10.0, "carbs": 3.6, "fat": 0.4, "cal": 59.0, "unit": "กรัม"},
    "เวย์โปรตีน (1 ช้อน 30g)": {"protein": 24.0, "carbs": 2.0, "fat": 1.5, "cal": 120.0, "unit": "ช้อน"},

    # --- หมวดถั่ว & เต้าหู้ ---
    "เต้าหู้โมเมน/แข็ง (100g)": {"protein": 8.0, "carbs": 2.0, "fat": 4.8, "cal": 83.0, "unit": "กรัม"},
    "ถั่วแอลมอนด์ (100g)": {"protein": 21.0, "carbs": 22.0, "fat": 49.0, "cal": 579.0, "unit": "กรัม"},
    "เนยถั่ว (1 ช้อนโต๊ะ 15g)": {"protein": 4.0, "carbs": 3.0, "fat": 8.0, "cal": 95.0, "unit": "ช้อนโต๊ะ"},

    # --- หมวดคาร์โบไฮเดรต & ธัญพืช ---
    "ข้าวสวย (100g)": {"protein": 2.7, "carbs": 28.0, "fat": 0.3, "cal": 130.0, "unit": "กรัม"},
    "ข้าวกล้อง (100g)": {"protein": 2.6, "carbs": 23.0, "fat": 0.9, "cal": 111.0, "unit": "กรัม"},
    "มันหวานนึ่ง (100g)": {"protein": 1.6, "carbs": 20.0, "fat": 0.1, "cal": 86.0, "unit": "กรัม"},
    "ข้าวโอ๊ต (100g)": {"protein": 13.0, "carbs": 67.0, "fat": 6.5, "cal": 379.0, "unit": "กรัม"},
    "ขนมปังโฮลวีต (1 แผ่น)": {"protein": 4.0, "carbs": 12.0, "fat": 1.0, "cal": 70.0, "unit": "แผ่น"},

    # --- หมวดผลไม้ ---
    "กล้วยหอม (1 ลูกกลาง)": {"protein": 1.3, "carbs": 27.0, "fat": 0.3, "cal": 105.0, "unit": "ลูก"},
    "แอปเปิล (1 ลูกกลาง)": {"protein": 0.5, "carbs": 25.0, "fat": 0.3, "cal": 95.0, "unit": "ลูก"},
    "อะโวคาโด (100g)": {"protein": 2.0, "carbs": 8.5, "fat": 15.0, "cal": 160.0, "unit": "กรัม"}
}

# สร้าง Session State สำหรับสะสมยอดรวม
if "daily_p" not in st.session_state:
    st.session_state.daily_p = 0.0
if "daily_c" not in st.session_state:
    st.session_state.daily_c = 0.0
if "daily_f" not in st.session_state:
    st.session_state.daily_f = 0.0
if "daily_cal" not in st.session_state:
    st.session_state.daily_cal = 0.0

st.title("🥗 คำนวณ & บันทึก Macros ประจำวัน")

# --- ส่วนที่ 1: คำนวณรายมื้อ ---
st.subheader("1. คำนวณมื้ออาหาร")
food_choice = st.selectbox("เลือกประเภทอาหาร (มีให้เลือก 20+ รายการ)", list(NUTRITION_DATA.keys()))
amount = st.number_input("ปริมาณ (ตามหน่วยของอาหารที่เลือก)", min_value=1.0, value=100.0, step=5.0)

data = NUTRITION_DATA[food_choice]
is_unit_item = any(u in data["unit"] for u in ["ฟอง", "ช้อน", "แก้ว", "แผ่น", "ลูก"])
multiplier = amount if is_unit_item else (amount / 100.0)

cur_p = data["protein"] * multiplier
cur_c = data["carbs"] * multiplier
cur_f = data["fat"] * multiplier
cur_cal = data["cal"] * multiplier

col1, col2, col3, col4 = st.columns(4)
col1.metric("โปรตีน", f"{cur_p:.1f} g")
col2.metric("คาร์บ", f"{cur_c:.1f} g")
col3.metric("ไขมัน", f"{cur_f:.1f} g")
col4.metric("แคลอรี", f"{int(cur_cal)} kcal")

if st.button("➕ บันทึกเข้ายอดรวมประจำวัน", type="primary"):
    st.session_state.daily_p += cur_p
    st.session_state.daily_c += cur_c
    st.session_state.daily_f += cur_f
    st.session_state.daily_cal += cur_cal
    st.success("บันทึกเรียบร้อย!")

st.divider()

# --- ส่วนที่ 2: สรุปยอดรวม ---
st.subheader("2. ยอดรวมสะสมวันนี้")
m1, m2, m3, m4 = st.columns(4)
m1.metric("โปรตีนรวม", f"{st.session_state.daily_p:.1f} g")
m2.metric("คาร์บรวม", f"{st.session_state.daily_c:.1f} g")
m3.metric("ไขมันรวม", f"{st.session_state.daily_f:.1f} g")
m4.metric("แคลอรีรวม", f"{int(st.session_state.daily_cal)} kcal")

if st.button("🔄 รีเซ็ตยอดรวมประจำวัน"):
    st.session_state.daily_p = 0.0
    st.session_state.daily_c = 0.0
    st.session_state.daily_f = 0.0
    st.session_state.daily_cal = 0.0
    st.rerun()
