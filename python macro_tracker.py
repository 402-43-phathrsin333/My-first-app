import tkinter as tk
from tkinter import ttk, messagebox

# ฐานข้อมูลสารอาหารต่อ 100 กรัม (หรือ 1 หน่วย)
NUTRITION_DATA = {
    "อกไก่สด (100g)": {"protein": 23.0, "carbs": 0.0, "fat": 1.2, "cal": 120.0, "unit": "กรัม"},
    "อกไก่สุก (100g)": {"protein": 31.0, "carbs": 0.0, "fat": 3.6, "cal": 165.0, "unit": "กรัม"},
    "ไข่ไก่ (1 ฟอง)": {"protein": 6.0, "carbs": 0.6, "fat": 5.0, "cal": 70.0, "unit": "ฟอง"},
    "ข้าวสวย (100g)": {"protein": 2.7, "carbs": 28.0, "fat": 0.3, "cal": 130.0, "unit": "กรัม"},
    "แซลมอนสด (100g)": {"protein": 20.0, "carbs": 0.0, "fat": 13.0, "cal": 208.0, "unit": "กรัม"},
    "เวย์โปรตีน (1 ช้อน 30g)": {"protein": 24.0, "carbs": 2.0, "fat": 1.5, "cal": 120.0, "unit": "ช้อน"}
}

# ตัวแปรสำหรับสะสมยอดรวมประจำวัน
daily_total = {
    "protein": 0.0,
    "carbs": 0.0,
    "fat": 0.0,
    "cal": 0.0
}

# ตัวแปรเก็บค่าล่าสุดจากการคำนวณ
current_calc = {
    "protein": 0.0,
    "carbs": 0.0,
    "fat": 0.0,
    "cal": 0.0
}

def calculate():
    try:
        selected_food = food_combobox.get()
        amount = float(entry_amount.get())
        
        if selected_food not in NUTRITION_DATA or amount <= 0:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกอาหารและใส่จำนวนที่ถูกต้อง")
            return

        data = NUTRITION_DATA[selected_food]
        multiplier = amount if ("ฟอง" in data["unit"] or "ช้อน" in data["unit"]) else (amount / 100.0)

        # เก็บค่าคำนวณรอบปัจจุบัน
        current_calc["protein"] = data["protein"] * multiplier
        current_calc["carbs"] = data["carbs"] * multiplier
        current_calc["fat"] = data["fat"] * multiplier
        current_calc["cal"] = data["cal"] * multiplier

        # แสดงผลลัพธ์มื้อนี้
        label_protein.config(text=f"{current_calc['protein']:.1f} g")
        label_carbs.config(text=f"{current_calc['carbs']:.1f} g")
        label_fat.config(text=f"{current_calc['fat']:.1f} g")
        label_cal.config(text=f"{int(current_calc['cal'])} kcal")
        
        # เปิดให้กดบันทึกได้
        btn_add.config(state="normal")
        
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกตัวเลขปริมาณให้ถูกต้อง")

def add_to_daily():
    # บวกรวมเข้า Daily Total
    daily_total["protein"] += current_calc["protein"]
    daily_total["carbs"] += current_calc["carbs"]
    daily_total["fat"] += current_calc["fat"]
    daily_total["cal"] += current_calc["cal"]
    
    # อัปเดตหน้าต่างแสดงยอดรวม
    update_daily_display()
    
    # ปิดปุ่มบันทึกชั่วคราวเพื่อกันการกดซ้ำ
    btn_add.config(state="disabled")

def update_daily_display():
    lbl_total_p.config(text=f"{daily_total['protein']:.1f} g")
    lbl_total_c.config(text=f"{daily_total['carbs']:.1f} g")
    lbl_total_f.config(text=f"{daily_total['fat']:.1f} g")
    lbl_total_cal.config(text=f"{int(daily_total['cal'])} kcal")

def reset_daily():
    if messagebox.askyesno("ยืนยัน", "ต้องการล้างยอดรวมของวันนี้ทั้งหมดใช่หรือไม่?"):
        daily_total["protein"] = 0.0
        daily_total["carbs"] = 0.0
        daily_total["fat"] = 0.0
        daily_total["cal"] = 0.0
        update_daily_display()

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("ตัวคำนวณ & บันทึก Macros ประจำวัน")
root.geometry("420x560")
root.resizable(False, False)

# หัวข้อ
lbl_header = tk.Label(root, text="คำนวณ & บันทึก สารอาหารประจำวัน", font=("Arial", 14, "bold"))
lbl_header.pack(pady=10)

# --- ส่วนคำนวณมื้ออาหาร ---
frame_input = tk.LabelFrame(root, text=" 1. คำนวณรายมื้อ ", font=("Arial", 10, "bold"), padx=10, pady=10)
frame_input.pack(fill="x", padx=15, pady=5)

lbl_food = tk.Label(frame_input, text="เลือกอาหาร:")
lbl_food.grid(row=0, column=0, sticky="w", pady=2)

food_combobox = ttk.Combobox(frame_input, values=list(NUTRITION_DATA.keys()), state="readonly", width=25)
food_combobox.current(0)
food_combobox.grid(row=0, column=1, pady=2)

lbl_amount = tk.Label(frame_input, text="ปริมาณ (g/ฟอง):")
lbl_amount.grid(row=1, column=0, sticky="w", pady=2)

entry_amount = tk.Entry(frame_input, width=27)
entry_amount.insert(0, "100")
entry_amount.grid(row=1, column=1, pady=2)

btn_calc = tk.Button(frame_input, text="คำนวณ", bg="#007bff", fg="white", font=("Arial", 9, "bold"), command=calculate)
btn_calc.grid(row=2, column=0, columnspan=2, sticky="we", pady=(8, 2))

# แสดงผลมื้อนี้
frame_res = tk.Frame(frame_input, bg="#e9ecef", bd=1, relief="solid")
frame_res.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

label_protein = tk.Label(frame_res, text="0.0 g", bg="#e9ecef", font=("Arial", 9, "bold"))
label_protein.grid(row=0, column=0, padx=8, pady=4)
label_carbs = tk.Label(frame_res, text="0.0 g", bg="#e9ecef", font=("Arial", 9, "bold"))
label_carbs.grid(row=0, column=1, padx=8, pady=4)
label_fat = tk.Label(frame_res, text="0.0 g", bg="#e9ecef", font=("Arial", 9, "bold"))
label_fat.grid(row=0, column=2, padx=8, pady=4)
label_cal = tk.Label(frame_res, text="0 kcal", bg="#e9ecef", font=("Arial", 9, "bold"), fg="#d9534f")
label_cal.grid(row=0, column=3, padx=8, pady=4)

btn_add = tk.Button(frame_input, text="+ บันทึกเข้ายอดรวมประจำวัน", bg="#28a745", fg="white", font=("Arial", 10, "bold"), state="disabled", command=add_to_daily)
btn_add.grid(row=4, column=0, columnspan=2, sticky="we", pady=5)

# --- ส่วนสรุปยอดรวมทั้งวัน ---
frame_daily = tk.LabelFrame(root, text=" 2. สรุปยอดรวมสะสมวันนี้ ", font=("Arial", 10, "bold"), padx=10, pady=10)
frame_daily.pack(fill="x", padx=15, pady=10)

daily_items = [
    ("โปรตีนสะสม:", "lbl_total_p", 0),
    ("คาร์บสะสม:", "lbl_total_c", 1),
    ("ไขมันสะสม:", "lbl_total_f", 2),
    ("แคลอรีรวม:", "lbl_total_cal", 3)
]

labels_daily = {}
for text, key, row in daily_items:
    lbl_title = tk.Label(frame_daily, text=text, font=("Arial", 10))
    lbl_title.grid(row=row, column=0, padx=10, pady=4, sticky="w")
    
    lbl_val = tk.Label(frame_daily, text="0.0 g" if row < 3 else "0 kcal", font=("Arial", 10, "bold"), fg="#28a745" if row < 3 else "#d9534f")
    lbl_val.grid(row=row, column=1, padx=10, pady=4, sticky="e")
    labels_daily[key] = lbl_val

lbl_total_p = labels_daily["lbl_total_p"]
lbl_total_c = labels_daily["lbl_total_c"]
lbl_total_f = labels_daily["lbl_total_f"]
lbl_total_cal = labels_daily["lbl_total_cal"]

btn_reset = tk.Button(frame_daily, text="รีเซ็ตยอดรวมประจำวัน", bg="#dc3545", fg="white", font=("Arial", 9), command=reset_daily)
btn_reset.grid(row=4, column=0, columnspan=2, sticky="we", pady=(10, 0))

root.mainloop()
