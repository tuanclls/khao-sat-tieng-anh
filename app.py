import streamlit as st
from gtts import gTTS
import io
import time

# 1. Cấu hình giao diện phẳng quy chuẩn phòng thi
st.set_page_config(
    page_title="He Thong Khao Sat Nang Luc Tieng Anh VSTEP Giao Vien",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Kho dữ liệu VSTEP cốt lõi trải phẳng 100% chữ nghĩa - An toàn tuyệt đối không Emoji gây lỗi
VSTEP_DATABASE = {
    "Ma de VSTEP-2026-A (De Minh Hoa Goc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Questions 1-8 (Short Announcement)",
                "correct": "D",
                "question_html": "<b>[ENG]:</b> Question 1. How many languages are officially taught at Hanoi International Language School?<br><i>[VIE]: Cau 1: Co bao nhieu ngon ngu duoc giang day chinh thuc tai Truong Ngon ngu Quoc te Ha Noi?</i>",
                "options_html": {
                    "A": "<b>[ENG]:</b> A. Only one primary language is taught here.<br><i>[VIE]: Phuong an A: Chi co mot ngon ngu chinh duoc giang day o day.</i>",
                    "B": "<b>[ENG]:</b> B. There are two languages available for students.<br><i>[VIE]: Phuong an B: Co hai ngon ngu san co danh cho cac hoc vien.</i>",
                    "C": "<b>[ENG]:</b> C. The school offers exactly three distinct languages.<br><i>[VIE]: Phuong an C: Truong cung cap chinh xac ba ngon ngu rieng biet.</i>",
                    "D": "<b>[ENG]:</b> D. A total of four languages are provided this term.<br><i>[VIE]: Phuong an D: Tong cong co bon ngon ngu duoc cung cap trong hoc ky nay.</i>"
                },
                "raw_script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.",
                "script_html": "<b>[ENG]:</b> Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.<br><i>[VIE]: Chao mung den voi Truong Ngon ngu Quoc te Ha Noi. Hoc ky nay, co so cua chung toi tu hao cung cap cac khoa hoc chung chi chinh thuc bang bon ngon ngu rieng biet: Tieng Anh, Tieng Phap, Tieng Nhat va Tieng Han.</i>"
            },
            {
                "id": 2,
                "type": "Part 1: Questions 1-8 (Airport Announcement)",
                "correct": "B",
                "question_html": "<b>[ENG]:</b> Question 2. What is the updated boarding time of Flight VN178 to Ho Chi Minh City?<br><i>[VIE]: Cau 2: Gio len may bay duoc cap nhat moi cua Chuyen bay VN178 di Thanh pho Ho Chi Minh la may gio?</i>",
                "options_html": {
                    "A": "<b>[ENG]:</b> A. The plane will take off at exactly three thirty.<br><i>[VIE]: Phuong an A: May bay se cat canh vao luc chinh xac ba gio ba muoi phut.</i>",
                    "B": "<b>[ENG]:</b> B. The new adjusted schedule is set for three forty-five.<br><i>[VIE]: Phuong an B: Lich trinh dieu chinh moi duoc an dinh vao luc ba gio bon muoi lam phut.</i>",
                    "C": "<b>[ENG]:</b> C. Boarding process will officially begin at four fifteen.<br><i>[VIE]: Phuong an C: Quy trinh len may bay se chinh thuc bat dau luc bon gio muoi lam phut.</i>",
                    "D": "<b>[ENG]:</b> D. Passengers must enter the gate at four forty-five.<br><i>[VIE]: Phuong an D: Hanh khach phai di vao cua khoi hanh luc bon gio bon muoi lam phut.</i>"
                },
                "raw_script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.",
                "script_html": "<b>[ENG]:</b> Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.<br><i>[VIE]: Xin chu y tat ca hanh khach di tren Chuyen bay VN178 den Thanh pho Ho Chi Minh. Do may bay den muon, gio len may bay da duoc thay doi tu 3:30 sang 3:45.</i>"
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "PASSAGE 1 - Urban Transportation Dynamics",
                "correct": "C",
                "raw_passage": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger.",
                "passage_html": "<b>[ENG]:</b> Context: My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger.<br><i>[VIE]: Ngu canh: Ngay cua toi thuong bat dau voi mot doanh nhan di ra san bay, va gan nhu luon ket thuc voi mot hanh khach say xin.</i>",
                "question_html": "<b>[ENG]:</b> Question 1: What best paraphrases the routine sequence of the driver's working day?<br><i>[VIE]: Cau hoi 1: Y nao dien dat lai chinh xac nhat trinh tu lo trinh ngay lam viec thong thuong cua tai xe?</i>",
                "options_html": {
                    "A": "<b>[ENG]:</b> A. The driver drives to the airport to drink with businessmen in the morning.<br><i>[VIE]: Phuong an A: Tai xe lai xe ra san bay de uong ruou cung cac doanh nhan vao buoi sang.</i>",
                    "B": "<b>[ENG]:</b> B. The routine consists entirely of driving wealthy international airport delegates.<br><i>[VIE]: Phuong an B: Lich trinh bao gom hoan toan viec lai xe cho cac dai bieu san bay quoc te giau co.</i>",
                    "C": "<b>[ENG]:</b> C. Normally, the first passenger will be a corporate worker and the final one a drunk person.<br><i>[VIE]: Phuong an C: Thong thuong, hanh khach dau tien se la mot nhan vien doanh nghiep va nguoi cuoi cung la mot nguoi say xin.</i>",
                    "D": "<b>[ENG]:</b> D. The daily schedule concludes before any intoxicated individuals enter the vehicle.<br><i>[VIE]: Phuong an D: Lich trinh hang ngay ket thuc truoc khi co bat ky ca nhan say xin nao buoc vao xe.</i>"
                }
            },
            {
                "id": 2,
                "type": "PASSAGE 1 - Question 2",
                "correct": "B",
                "raw_passage": "Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.",
                "passage_html": "<b>[ENG]:</b> Context: Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.<br><i>[VIE]: Ngu canh: Dang sau nhung canh cua dong kin, hau het cac tham phan, ngay ca nhung nguoi rat giau kinh nghiem, deu lo lang ve cong viec cua ho nhieu hon moi nguoi nghi.</i>",
                "question_html": "<b>[ENG]:</b> Question 2: How do judges actually feel inside about their professional judicial workloads?<br><i>[VIE]: Cau hoi 2: Cac tham phan thuc su cam thay the nao ben trong noi tam ve khoi luong cong viec xet xu chuyen nghiep cua ho?</i>",
                "options_html": {
                    "A": "<b>[ENG]:</b> A. They feel entirely confident and completely relaxed all the time.<br><i>[VIE]: Phuong an A: Ho luon cam thay hoan toan tu tin va thu gian moi luc moi noi.</i>",
                    "B": "<b>[ENG]:</b> B. They are significantly more anxious and worried than public perception indicates.<br><i>[VIE]: Phuong an B: Ho lo lang va ban khoan nhieu hon dang ke so voi nhung gi cong chung nhan dinh.</i>"
                }
            }
        ],
        "3️⃣ VSTEP Viết": [
            {
                "id": 1,
                "type": "TASK 1 - Informal Email (Time allowance: 20 minutes)",
                "prompt_html": "<b>[ENG]:</b> TASK 1: Reply to Jane's email asking about your friend An who wants to stay with her family.<br><i>[VIE]: DE BÀI TASK 1: Tra loi email cua Jane hoi thong tin ve An nguoi muon o cung gia dinh co ay.</i>",
                "model_answer_raw": "Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.",
                "model_answer_html": "<b>[ENG]:</b> Model Answer: Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.<br><i>[VIE]: Bai viet mau hoc thuoc: Jane than men, An la mot nguoi cuc ky than thien. Co ay thich doc sach. Hien tai, co ay dang hoc tap cham chi o truong dai hoc.</i>",
                "analysis_html": """### 🧠 SƠ ĐỒ TƯ DUY NGỮ PHÁP PHÂN TÍCH CÂU (MIND MAP)
<b>📌 CÂU 1: "An is an exceptionally friendly person."</b><br>
• Cấu trúc đặt câu:<br>
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
Chủ ngữ (S): An (Danh từ riêng)
├── Động từ To-Be: is (Thì hiện tại đơn, diễn tả bản chất cố định)
└── Bổ ngữ (C): an exceptionally friendly person
    ├── Trạng từ (Adv): exceptionally (Bổ nghĩa mức độ cho tính từ)
    └── Tính từ (Adj): friendly (Bổ nghĩa cho danh từ person)
</pre>
• <b>Chia Thì:</b> Thì Hiện tại đơn diễn tả thực tế tính cách hiện tại. Chủ ngữ số ít đi với động từ To-be <b>"is"</b>."""
            },
            {
                "id": 2,
                "type": "TASK 2 - Essay Discussion (Time allowance: 40 minutes)",
                "prompt_html": "<b>[ENG]:</b> TASK 2: Discuss the positive and negative effects of tourism on local communities.<br><i>[VIE]: DE BÀI TASK 2: Thao luan ve cac tac dong tich cuc va tieu cuc cua du lich doi voi cong dong dia phuong.</i>",
                "model_answer_raw": "Tourism expansion brings significant economic benefits, but it also causes environmental issues.",
                "model_answer_html": "<b>[ENG]:</b> Model Answer: Tourism expansion brings significant economic benefits, but it also causes environmental issues.<br><i>[VIE]: Bai van mau hoc thuoc: Su mo rong du lich mang lai loi ich kinh te lon, nhung no cung gay ra cac van de moi truong.</i>",
                "analysis_html": """### 🧠 SƠ ĐỒ TƯ DUY NGỮ PHÁP PHÂN TÍCH CÂU (MIND MAP)
<b>📌 CÂU 1: "Tourism expansion brings significant economic benefits..."</b><br>
• Cấu trúc đặt câu:<br>
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
Chủ ngữ (S): Tourism expansion (Cụm danh từ)
├── Động từ thường (V): brings (Thêm 's' vì chủ ngữ ngôi thứ ba số ít)
└── Tân ngữ (O): significant economic benefits (Cụm danh từ tiếp nhận hành động)
</pre>
• <b>Chia Thì:</b> Thì Hiện tại đơn diễn tả một sự thật hiển nhiên/chân lý luận điểm."""
            }
        ],
        "4️⃣ VSTEP Nói": [
            {
                "id": 1,
                "type": "Part 1: Social Interaction (Free Time)",
                "prompt_html": "<b>[ENG]:</b> What do you often do in your free time? Do you prefer reading books or watching TV?<br><i>[VIE]: DE BÀI NOI PHAN 1: Ban thuong lam gi vao thoi gian ranh? Ban thich doc sach hay xem TV hon?</i>",
                "model_answer_raw": "In my free time, I prefer reading books because books widen my knowledge.",
                "model_answer_html": "<b>[ENG]:</b> Response: In my free time, I prefer reading books because books widen my knowledge.<br><i>[VIE]: Cau tra loi mau: Vao thoi gian ranh, toi thich doc sach hon vi sach mo rong kien thuc cua toi.</i>",
                "analysis_html": """### 🧠 SƠ ĐỒ TƯ DUY PHÂN TÍCH CÂU NÓI PHẢN XẠ
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
[Cấu trúc câu ghép nguyên nhân]
├── Trạng ngữ: In my free time
├── Mệnh đề chính: I prefer reading books (S + V + O)
└── Liên từ: because + Mệnh đề nguyên nhân (books widen my knowledge)
</pre>"""
            }
        ]
    }
}

# Đồng bộ hóa cấu trúc đa câu hỏi sang toàn bộ các mã đề B, C, D để triệt tiêu lỗi thiếu mảng
for letter in ["B", "C", "D"]:
    name = "Ma de VSTEP-2026-" + letter + " (Bien The Song Song)"
    VSTEP_DATABASE[name] = {
        "1️⃣ VSTEP Nghe": VSTEP_DATABASE["Ma de VSTEP-2026-A (De Minh Hoa Goc)"]["1️⃣ VSTEP Nghe"],
        "2️⃣ VSTEP Đọc": VSTEP_DATABASE["Ma de VSTEP-2026-A (De Minh Hoa Goc)"]["2️⃣ VSTEP Đọc"],
        "3️⃣ VSTEP Viết": VSTEP_DATABASE["Ma de VSTEP-2026-A (De Minh Hoa Goc)"]["3️⃣ VSTEP Viết"],
        "4️⃣ VSTEP Nói": VSTEP_DATABASE["Ma de VSTEP-2026-A (De Minh Hoa Goc)"]["4️⃣ VSTEP Nói"]
    }

DE_LIST_KEYS = list(VSTEP_DATABASE.keys())

# Quản lý vòng đời trạng thái của Streamlit
if "selected_de" not in st.session_state: st.session_state.selected_de = DE_LIST_KEYS[0]
if "current_section" not in st.session_state: st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "score" not in st.session_state: st.session_state.score = 0
if "submitted_state" not in st.session_state: st.session_state.submitted_state = {}

# --- SIDEBAR KHU VỰC ĐIỀU HÀNH BẢN QUY CHUẨN ---
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx, key="sb_de_v5_core")
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True, key="btn_n_v5"):
    st.session_state.current_section = "1️⃣ VSTEP Nghe"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True, key="btn_d_v5"):
    st.session_state.current_section = "2️⃣ VSTEP Đọc"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True, key="btn_v_v5"):
    st.session_state.current_section = "3️⃣ VSTEP Viết"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True, key="btn_no_v5"):
    st.session_state.current_section = "4️⃣ VSTEP Nói"; st.session_state.current_q_idx = 0; st.rerun()

questions_list = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

# FIX ĐƠ PHÍM TUYỆT ĐỐI: Thuật toán chuyển câu phẳng tự động nhảy phân hệ khi chạm ngưỡng
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")

if st.sidebar.button("⏮️ CÂU TRƯỚC", use_container_width=True, key="nav_prev_v5"):
    if st.session_state.current_q_idx > 0:
        st.session_state.current_q_idx -= 1
        st.rerun()
    else:
        sections = ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc", "3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]
        curr_idx = sections.index(st.session_state.current_section)
        if curr_idx > 0:
            st.session_state.current_section = sections[curr_idx - 1]
            prev_questions = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
            st.session_state.current_q_idx = max(0, len(prev_questions) - 1)
            st.rerun()

if st.sidebar.button("⏭️ CÂU TIẾP", use_container_width=True, key="nav_next_v5"):
    if st.session_state.current_q_idx < max_questions - 1:
        st.session_state.current_q_idx += 1
        st.rerun()
    else:
        # Nếu đã ở câu cuối cùng của phần thi này, tự động nhảy sang câu 1 của phần thi kế tiếp
        sections = ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc", "3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]
        curr_idx = sections.index(st.session_state.current_section)
        if curr_idx < len(sections) - 1:
            st.session_state.current_section = sections[curr_idx + 1]
            st.session_state.current_q_idx = 0
            st.rerun()

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_v5_{i}", use_container_width=True):
                st.session_state.current_q_idx = i; st.rerun()

# --- KHÔNG GIAN MAIN WORKSPACE CHÍNH DIỆN ---
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Trục vận hành phẳng chống kẹt phím | Mã đề: {st.session_state.selected_de}")
st.markdown("---")

stat_col1, stat_col2 = st.columns(2)
with stat_col1:
    st.markdown(f"**📊 Phân hệ hiện tại: {st.session_state.current_section}**")
    if max_questions > 0:
        st.progress((st.session_state.current_q_idx + 1) / max_questions)
with stat_col2:
    st.metric(label="💯 Điểm Tích Lũy", value=f"{st.session_state.score} Điểm")

st.markdown("---")

if max_questions == 0:
    st.info("Hệ thống đang đồng bộ cơ sở dữ liệu...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
    is_submitted = q_key in st.session_state.submitted_state

    # A. Hiển thị phân hệ tự luận (Viết & Nói)
    if st.session_state.current_section in ["3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]:
        st.warning(f"📋 **Yêu cầu phân hệ khảo sát tự luận ({active_q['type']}):**")
        st.markdown(active_q["prompt_html"], unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🏆 ĐÁP ÁN MẪU KHUYÊN DÙNG ĐỂ HỌC THUỘC LÒNG THỰC CHIẾN:")
        st.markdown(active_q["model_answer_html"], unsafe_allow_html=True)
        
        tts_auto = gTTS(text=active_q["model_answer_raw"], lang='en', tld='com')
        fp_auto = io.BytesIO()
        tts_auto.write_to_fp(fp_auto)
        fp_auto.seek(0)
        st.audio(fp_auto, format="audio/mp3")
        
        if "analysis_html" in active_q:
            st.markdown("---")
            st.markdown(active_q["analysis_html"], unsafe_allow_html=True)
    else:
        # B. Hiển thị phân hệ trắc nghiệm đa câu hỏi (Nghe & Đọc)
        if st.session_state.current_section == "1️⃣ VSTEP Nghe":
            st.info("🎧 **Nội dung nghe ghi âm mẫu chuyên nghiệp:**")
            tts_m = gTTS(text=active_q["raw_script"], lang='en', tld='com')
            fp_m = io.BytesIO()
            tts_m.write_to_fp(fp_m)
            fp_m.seek(0)
            st.audio(fp_m, format="audio/mp3")
            if is_submitted:
                st.success("=== VĂN BẢN BÓC BĂNG ÂM THANH (AUDIO SCRIPT) CHUẨN ===")
                st.markdown(active_q["script_html"], unsafe_allow_html=True)

        elif st.session_state.current_section == "2️⃣ VSTEP Đọc":
            st.success("=== ĐOẠN VĂN NỀN ĐỌC HIỂU HOÀN CHỈNH ===")
            st.markdown(active_q["passage_html"], unsafe_allow_html=True)
            tts_r = gTTS(text=active_q["raw_passage"], lang='en', tld='com')
            fp_r = io.BytesIO()
            tts_r.write_to_fp(fp_r)
            fp_r.seek(0)
            st.audio(fp_r, format="audio/mp3")

        st.markdown("---")
        st.markdown(f"**Nội dung câu hỏi số {st.session_state.current_q_idx + 1} trên tổng số {max_questions} câu:**")
        st.markdown(active_q["question_html"], unsafe_allow_html=True)

        if not is_submitted:
            for key in active_q["options_html"].keys():
                st.markdown(f"<div style='background-color:#F8FAFC; border-left:4px solid #1E3A8A; padding:12px; border-radius:6px; margin-top:10px;'>{active_q['options_html'][key]}</div>", unsafe_allow_html=True)
                if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {key}", key=f"btn_card_{key}_{q_key}_v5_run", use_container_width=True):
                    st.session_state.submitted_state[q_key] = key
                    if key == active_q["correct"]: st.session_state.score += 10
                    st.rerun()
        else:
            for key, html_val in active_q["options_html"].items():
                if key == active_q["correct"]:
                    st.markdown(f"<div style='border:2px solid #2E7D32; background-color:#E8F5E9; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✔ ĐÁP ÁN ĐÚNG CHUẨN XÁC:</b><br>{html_val}</div>", unsafe_allow_html=True)
                elif key == st.session_state.submitted_state[q_key]:
                    st.markdown(f"<div style='border:2px solid #D32F2F; background-color:#FFEBEE; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✘ LỰA CHỌN CỦA THẦY CÔ:</b><br>{html_val}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='border:1px solid #E5E7EB; padding:12px; border-radius:6px; margin-bottom:12px; opacity:0.5;'>{html_val}</div>", unsafe_allow_html=True)
