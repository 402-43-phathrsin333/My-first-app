import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ตัวคำนวณ Macros", page_icon="🥗", layout="centered")

# ฐานข้อมูลสารอาหาร
NUTRITION_DATA = {
    "อกไก่สด (100g)": {"protein": 23.0, "carbs": 0.0, "fat": 1.2, "cal": 120.0, "unit": "กรัม"},
    "อกไก่สุก (100g)": {"protein": 31.0, "carbs": 0.0, "fat": 3.6, "cal": 165.0, "unit": "กรัม"},
    "ไข่ไก่ (1 ฟอง)": {"protein": 6.0, "carbs": 0.6, "fat": 5.0, "cal": 70.0, "unit": "ฟอง"},
    "ข้าวสวย (100g)": {"protein": 2.7, "carbs": 28.0, "fat": 0.3, "cal": 130.0, "unit": "กรัม"},
    "แซลมอนสด (100g)": {"protein": 20.0, "carbs": 0.0, "fat": 13.0, "cal": 208.0, "unit": "กรัม"},
    "เวย์โปรตีน (1 ช้อน 30g)": {"protein": 24.0, "carbs": 2.0, "fat": 1.5, "cal": 120.0, "unit": "ช้อน"}
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
food_choice = st.selectbox("เลือกประเภทอาหาร", list(NUTRITION_DATA.keys()))
amount = st.number_input("ปริมาณ (g / ฟอง / ช้อน)", min_value=1.0, value=100.0, step=10.0)

data = NUTRITION_DATA[food_choice]
multiplier = amount if ("ฟอง" in data["unit"] or "ช้อน" in data["unit"]) else (amount / 100.0)

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
