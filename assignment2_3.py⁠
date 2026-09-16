import time
import streamlit as st

st.title("⏱️ เกมส์ทายประเทศ")

# รายชื่อประเทศและคำตอบเฉลย (10 ข้อ)
QUESTIONS = [
    {"label": "ข้อ 1: ไทย", "answer": "thailand"},
    {"label": "ข้อ 2: ญี่ปุ่น", "answer": "japan"},
    {"label": "ข้อ 3: เกาหลีใต้", "answer": "south korea"},
    {"label": "ข้อ 4: จีน", "answer": "china"},
    {"label": "ข้อ 5: สิงคโปร์", "answer": "singapore"},
    {"label": "ข้อ 6: เวียดนาม", "answer": "vietnam"},
    {"label": "ข้อ 7: อินเดีย", "answer": "india"},
    {"label": "ข้อ 8: ฝรั่งเศส", "answer": "france"},
    {"label": "ข้อ 9: เยอรมนี", "answer": "germany"},
    {"label": "ข้อ 10: อิตาลี", "answer": "italy"},
]

# 1. กำหนดค่าเริ่มต้นใน session_state
for i in range(1, 11):
    key = f"ans{i}_val"
    if key not in st.session_state:
        st.session_state[key] = ""


# 📌 ฟังก์ชันเคลียร์ค่าเมื่อกดปุ่มเริ่มใหม่
def reset_game():
    for i in range(1, 11):
        st.session_state[f"ans{i}_val"] = ""
    st.session_state.start = time.time()  # เริ่มเวลาใหม่
    st.session_state.is_ended = False  # ปิด Dialog


# ----------------------------------------------------
# 📌 ฟังก์ชัน MessageBox (Dialog)
# ----------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog(answers):
    st.balloons()
    score = 0

    # ตรวจคำตอบทั้ง 10 ข้อ
    for idx, item in enumerate(QUESTIONS):
        user_ans = answers[idx].strip().lower()
        correct_ans = item["answer"]

        if user_ans == correct_ans:
            st.success(f"✅ {item['label']}: ถูกต้อง")
            score += 1
        else:
            st.error(
                f"❌ {item['label']}: ยังไม่ถูกต้อง (คุณตอบ '{answers[idx]}')"
            )

    st.info(f"🏆 ได้คะแนนรวม: {score} / 10 คะแนน")

    # 📌 เกณฑ์ประเมินผู้เล่นตามใบงาน
    if 7 <= score <= 10:
        st.success("🌟 เกณฑ์ประเมิน: เก่งมากกก")
    elif 4 <= score <= 6:
        st.info("👍 เกณฑ์ประเมิน: เก่ง")
    elif 1 <= score <= 3:
        st.warning("🙂 เกณฑ์ประเมิน: ปานกลาง")
    else:
        st.error("💀 เกณฑ์ประเมิน: ปรับปรุง")


# ----------------------------------------------------
# 1. ปุ่มเริ่มเล่นเกม
# ----------------------------------------------------
st.button("🎮 เริ่มเล่นเกม", on_click=reset_game)

# 2. แถบแสดงเวลานับถอยหลัง
if "start" in st.session_state and not st.session_state.get("is_ended", False):
    time_left = int(60 - (time.time() - st.session_state.start))

    if time_left > 0:
        st.error(f"⏳ เหลือเวลา: {time_left} วินาที")
    else:
        st.session_state.is_ended = True
        st.rerun()

st.divider()

# 3. ช่องรับคำตอบ 10 ข้อ
user_answers = []
for i, q in enumerate(QUESTIONS, start=1):
    ans = st.text_input(
        f"{q['label']} (พิมพ์ชื่อประเทศภาษาอังกฤษ)",
        value=st.session_state[f"ans{i}_val"],
        key=f"input_{i}",
    )
    st.session_state[f"ans{i}_val"] = ans
    user_answers.append(ans)

# 4. ปุ่มส่งคำตอบ
if "start" in st.session_state and not st.session_state.get("is_ended", False):
    if st.button("📥 ส่งคำตอบ"):
        st.session_state.is_ended = True
        st.rerun()

    time.sleep(1)
    st.rerun()

# 5. แสดง Dialog ผลลัพธ์
if st.session_state.get("is_ended", False):
    show_result_dialog(user_answers)

st.divider()
st.write("นาย ภัทรสิน ศิลธรรม เลขที่ 43 ม.4/2
          นาย กฤษณพัฒน์ ปิมปา เลขที่ 2 ม.4/2
          นาย สิงหา ทองใจ เลขที่ 8 ม.4/2
          นาย กวินภพ สามใจ เลขที่ 43 ม.4/2")
