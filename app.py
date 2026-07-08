import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from gtts import gTTS
import re
import io
import base64
import time

# Thiết lập cấu hình phòng khảo thí thực chiến quy chuẩn chuyên nghiệp
st.set_page_config(
    page_title="Hệ Thống Khảo Sát Năng Lực Tiếng Anh VSTEP Giáo Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHO DỮ LIỆU ĐỀ THI ĐA BIẾN THỂ VSTEP-2026: ĐỒNG BỘ TOÀN DIỆN 4 MÃ ĐỀ ĐA CÂU HỎI Chống ĐƠ NÚT
VSTEP_DATABASE = {
    "Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Question 1",
                "correct": "D",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> 1. How many languages are taught at Hanoi International Language School?<br><small><font color="#4B5563">🎵 IPA: /haʊ ˈmɛni ˈlæŋɡwɪdʒɪz ɑːr tɔːt æt hæˈnɔɪ.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Câu 1: Có bao nhiêu ngôn ngữ được giảng dạy tại Trường Ngôn ngữ Quốc tế Hà Nội?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 1 language<br><small><font color="#4B5563">🎵 IPA: /wʌn ˈlæŋɡwɪdʒ/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 1 ngôn ngữ</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 2 languages<br><small><font color="#4B5563">🎵 IPA: /tuː ˈlæŋɡwɪdʒɪz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 2 ngôn ngữ</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 3 languages<br><small><font color="#4B5563">🎵 IPA: /θriː ˈlæŋɡwɪdʒɪz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 3 ngôn ngữ</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 4 languages<br><small><font color="#4B5563">🎵 IPA: /fɔːr ˈlæŋɡwɪdʒɪz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 4 ngôn ngữ</font></i>"""
                },
                "raw_script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.<br><i><font color="#059669">🇻🇳 VIE: Chào mừng đến với Trường Ngôn ngữ Quốc tế Hà Nội. Học kỳ này, cơ sở của chúng tôi tự hào cung cấp các khóa học chứng chỉ chính thức bằng bốn ngôn ngữ riêng biệt: Tiếng Anh, Tiếng Pháp, Tiếng Nhật và Tiếng Hàn.</font></i>"""
            },
            {
                "id": 2,
                "type": "Part 1: Question 2",
                "correct": "B",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> 2. What is the boarding time of Flight VN178?<br><small><font color="#4B5563">🎵 IPA: /wɒt ɪz ðə ˈbɔːrdɪŋ taɪm ɒv flaɪt viː ɛn wʌn ˈsɛvən eɪt/</font></small><br><i><font color="#059669">🇻🇳 VIE: Câu 2: Giờ lên máy bay của Chuyến bay VN178 là mấy giờ?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 3.30<br><small><font color="#4B5563">🎵 IPA: /θriː ˈθɜːrti/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 3 giờ 30 phút</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 3.45<br><small><font color="#4B5563">🎵 IPA: /θriː fɔːrti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 3 giờ 45 phút</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 4.15<br><small><font color="#4B5563">🎵 IPA: /fɔːr fɪfˈtiːn/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 4 giờ 15 phút</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 4.45<br><small><font color="#4B5563">🎵 IPA: /fɔːr fɔːrti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 4 giờ 45 phút</font></i>"""
                },
                "raw_script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. The boarding time has been rescheduled from 3:30 to 3:45.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. The boarding time has been rescheduled from 3:30 to 3:45.<br><i><font color="#059669">🇻🇳 VIE: Xin chú ý tất cả hành khách đi trên Chuyến bay VN178 đến Thành phố Hồ Chí Minh. Giờ lên máy bay đã được thay đổi từ 3:30 sang 3:45.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "Passage 1: Question 1",
                "correct": "C",
                "raw_passage": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: My day typically starts with a business person going to the airport, and nearly always ends with a drunk.<br><i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Ngày của tôi thường bắt đầu với một doanh nhân đi ra sân bay, và gần như luôn kết thúc với một người say xỉn.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What best paraphrases the routine statement?<br><i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Câu nào diễn đạt lại tốt nhất nhận định về lộ trình hàng ngày?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Normally, I will take a business person and a drunk at the airport.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Thông thường, tôi đón doanh nhân và người say ở sân bay.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Normally, my first passenger will be a businessman and my last one a drunk.<br><i><font color="#059669">🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên là doanh nhân và người cuối cùng là người say.</font></i>"""
                }
            },
            {
                "id": 2,
                "type": "Passage 1: Question 2",
                "correct": "B",
                "raw_passage": "Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.<br><i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Đằng sau những cánh cửa đóng kín, hầu hết các thẩm phán, ngay cả những người rất giàu kinh nghiệm, đều lo lắng về công việc của họ nhiều hơn mọi người nghĩ.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 2: How do judges actually feel about their judicial work?<br><i><font color="#059669">🇻🇳 VIE: Câu hỏi 2: Các thẩm phán thực sự cảm thấy thế nào về công việc xét xử của họ?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. They feel completely confident and relaxed.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Họ cảm thấy hoàn toàn tự tin và thư giãn.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. They are more anxious and worried than people think.<br><i><font color="#059669">🇻🇳 VIE: Phương án B: Họ lo lắng và băn khoăn nhiều hơn mọi người nghĩ.</font></i>"""
                }
            }
        ]
    }
}

# TẠO TỰ ĐỘNG DỮ LIỆU ĐA CÂU HỎI SONG SONG CHO CÁC MÃ ĐỀ B, C, D ĐỂ TRÁNH LỖI KẸT SỐ CÂU
for letter in ["B", "C", "D"]:
    de_name = f"Mã đề VSTEP-2026-{letter} (Biến Thể Song Song {['B','C','D'].index(letter)+1})"
    VSTEP_DATABASE[de_name] = {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1, "type": "Part 1: Q1", "correct": "A",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> [Code {letter}] 1. What industry is discussed today?<br><i><font color="#059669">🇻🇳 VIE: [Mã đề {letter}] Câu 1: Ngành công nghiệp nào được thảo luận hôm nay?</font></i>""",
                "options_html": {"A": """<b><font color="#1E3A8A">ENG:</font></b> A. Ecotourism.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Du lịch sinh thái.</font></i>""", "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Banking.<br><i><font color="#059669">🇻🇳 VIE: Phương án B: Ngân hàng.</font></i>"""},
                "raw_script": "Today we will focus our attention directly on the ecotourism expansion.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Today we will focus our attention directly on the ecotourism expansion.<br><i><font color="#059669">🇻🇳 VIE: Hôm nay chúng ta sẽ tập trung sự chú ý trực tiếp vào sự phát triển du lịch sinh thái.</font></i>"""
            },
            {
                "id": 2, "type": "Part 1: Q2", "correct": "B",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> [Code {letter}] 2. What time does the workshop open?<br><i><font color="#059669">🇻🇳 VIE: [Mã đề {letter}] Câu 2: Hội thảo bắt đầu lúc mấy giờ?</font></i>""",
                "options_html": {"A": """<b><font color="#1E3A8A">ENG:</font></b> A. 8.00 AM<br><i><font color="#059669">🇻🇳 VIE: Phương án A: 8 giờ sáng</font></i>""", "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 9.00 AM<br><i><font color="#059669">🇻🇳 VIE: Phương án B: 9 giờ sáng</font></i>"""},
                "raw_script": "Please note that the specialized training workshop will begin at 9:00 AM sharp.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Please note that the specialized training workshop will begin at 9:00 AM sharp.<br><i><font color="#059669">🇻🇳 VIE: Vui lòng lưu ý rằng hội thảo tập huấn chuyên sâu sẽ bắt đầu vào đúng 9 giờ sáng.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1, "type": "Passage 1: Q1", "correct": "B",
                "raw_passage": "Developing systematic knowledge inside classroom settings requires dedication.",
                "passage_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Context: Developing systematic knowledge inside classroom settings requires dedication.<br><i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Việc phát triển kiến thức có hệ thống trong môi trường lớp học đòi hỏi sự cống hiến.</font></i>""",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Question 1: What does developing knowledge require?<br><i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Việc phát triển kiến thức đòi hỏi điều gì?</font></i>""",
                "options_html": {"A": """<b><font color="#1E3A8A">ENG:</font></b> A. Wealth.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Sự giàu có.</font></i>""", "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Dedication.<br><i><font color="#059669">🇻🇳 VIE: Phương án B: Sự cống hiến.</font></i>""}
            },
            {
                "id": 2, "type": "Passage 1: Q2", "correct": "A",
                "raw_passage": "Continuous exposure to natural spoken English improves listening comprehension rapidly.",
                "passage_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Context: Continuous exposure to natural spoken English improves listening comprehension rapidly.<br><i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Tiếp xúc liên tục với tiếng Anh nói tự nhiên cải thiện khả năng nghe hiểu nhanh chóng.</font></i>""",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Question 2: What accelerates listening comprehension?<br><i><font color="#059669">🇻🇳 VIE: Câu hỏi 2: Điều gì đẩy nhanh khả năng nghe hiểu?</font></i>""",
                "options_html": {"A": """<b><font color="#1E3A8A">ENG:</font></b> A. Continuous exposure.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Sự tiếp xúc liên tục.</font></i>""", "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Memorizing vocabulary rules.<br><i><font color="#059669">🇻🇳 VIE: Phương án B: Ghi nhớ các quy tắc từ vựng.</font></i>""}
            }
        ]
    }

# ĐỒNG BỘ CÁC MÃ ĐỀ CHO PHẦN TỰ LUẬN TĨNH CÓ SƠ ĐỒ TƯ DUY
for name in VSTEP_DATABASE.keys():
    VSTEP_DATABASE[name]["3️⃣ VSTEP Viết"] = [
        {
            "id": 1, "type": "TASK 1",
            "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Tell Jane about An's personality.<br><i><font color="#059669">🇻🇳 VIE: Hãy kể cho Jane về tính cách của An.</font></i>""",
            "model_answer_raw": "An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.",
            "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.<br><small><font color="#4B5563">🎵 IPA: /æn ɪz ən ɪkˈsɛpʃənəli ˈfrɛndli ˈpɜːrsən.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Bài mẫu: An là một người cực kỳ thân thiện. Cô ấy thích đọc sách. Hiện tại, cô ấy đang học tập chăm chỉ ở trường đại học.</font></i>""",
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
        }
    ]
    VSTEP_DATABASE[name]["4️⃣ VSTEP Nói"] = [
        {
            "id": 1, "type": "Part 1",
            "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> What do you do in your free time?<br><i><font color="#059669">🇻🇳 VIE: Bạn làm gì vào thời gian rảnh?</font></i>""",
            "model_answer_raw": "In my free time, I prefer reading books because books widen my knowledge.",
            "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Response: In my free time, I prefer reading books because books widen my knowledge.<br><small><font color="#4B5563">🎵 IPA: /ɪn maɪ friː taɪm, aɪ prɪˈfɜːr riːdɪŋ bʊks.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Mẫu nói: Vào thời gian rảnh, tôi thích đọc sách hơn vì sách mở rộng kiến thức của tôi.</font></i>"""
        }
    ]

DE_LIST_KEYS = list(VSTEP_DATABASE.keys())

# Khởi tạo trạng thái bộ nhớ phẳng
if "selected_de" not in st.session_state: st.session_state.selected_de = DE_LIST_KEYS[0]
if "current_section" not in st.session_state: st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "score" not in st.session_state: st.session_state.score = 0
if "submitted_state" not in st.session_state: st.session_state.submitted_state = {}

# --- SIDEBAR THANH SƯỜN ĐIỀU HÀNH THỰC THI CHUẨN XÁC ---
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx, key="sb_de_master_final_v3")
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
c1, c2 = st.sidebar.columns(2)
with c1:
    if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True, key="btn_n_v3"):
        st.session_state.current_section = "1️⃣ VSTEP Nghe"; st.session_state.current_q_idx = 0; st.rerun()
with c2:
    if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True, key="btn_d_v3"):
        st.session_state.current_section = "2️⃣ VSTEP Đọc"; st.session_state.current_q_idx = 0; st.rerun()

c3, c4 = st.sidebar.columns(2)
with c3:
    if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True, key="btn_v_v3"):
        st.session_state.current_section = "3️⃣ VSTEP Viết"; st.session_state.current_q_idx = 0; st.rerun()
with c4:
    if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True, key="btn_no_v3"):
        st.session_state.current_section = "4️⃣ VSTEP Nói"; st.session_state.current_q_idx = 0; st.rerun()

questions_list = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

# SỬA LỖI ĐÓNG BĂNG ĐIỀU HƯỚNG CÂU HỎI BẰNG PHƯƠNG THỨC GỌI CONTAINER TRỰC TIẾP (KHÔNG DÙNG ST.SIDEBAR.BUTTON TRONG WITH)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")
cp, cn = st.sidebar.columns(2)
if cp.button("Anterior ⏮️ CÂU TRƯỚC", use_container_width=True, key="nav_prev_v3_fixed"):
    if st.session_state.current_q_idx > 0:
        st.session_state.current_q_idx -= 1
        st.rerun()
if cn.button("Siguiente ⏭️ CÂU TIẾP", use_container_width=True, key="nav_next_v3_fixed"):
    if st.session_state.current_q_idx < max_questions - 1:
        st.session_state.current_q_idx += 1
        st.rerun()

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_v3_{i}", use_container_width=True):
                st.session_state.current_q_idx = i; st.rerun()

# --- KHÔNG GIAN MAIN WORKSPACE CHÍNH DIỆN ---
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Trục vận hành phẳng chống lỗi đơ phím điều hướng | Mã đề: {st.session_state.selected_de}")
st.markdown("---")

current_de_pos = DE_LIST_KEYS.index(st.session_state.selected_de)
if current_de_pos < len(DE_LIST_KEYS) - 1:
    if st.button("🎉 THÀNH THẠO ĐỀ NÀY RỒI ── BẤM ĐỂ CHUYỂN SANG MÃ ĐỀ TIẾP THEO MỨC ĐỘ TIẾP THEO 🚀", use_container_width=True, key="btn_next_level_de_v3"):
        st.session_state.selected_de = DE_LIST_KEYS[current_de_pos + 1]
        st.session_state.current_q_idx = 0
        st.rerun()

st.markdown("---")

if max_questions == 0:
    st.info("Hệ thống đang đồng bộ cơ sở dữ liệu...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
    is_submitted = q_key in st.session_state.submitted_state

    # HIỂN THỊ PHẦN TỰ LUẬN TĨNH (VIẾT & NÓI)
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
        # HIỂN THỊ PHẦN TRẮC NGHIỆM ĐA CÂU HỎI (NGHE & ĐỌC)
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
        st.markdown(f"**Nội dung câu hỏi số {st.session_state.current_q_idx + 1}:**")
        st.markdown(active_q["question_html"], unsafe_allow_html=True)

        if not is_submitted:
            for key in active_q["options_html"].keys():
                st.markdown(f"<div style='background-color:#F8FAFC; border-left:4px solid #1E3A8A; padding:12px; border-radius:6px; margin-top:10px;'>{active_q['options_html'][key]}</div>", unsafe_allow_html=True)
                if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {key}", key=f"btn_card_{key}_{q_key}_v3_fix", use_container_width=True):
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
