import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from gtts import gTTS
import io
import base64
import time

# ✨ Thiết lập cấu hình phòng khảo thí VSTEP thực chiến chuyên nghiệp
st.set_page_config(
    page_title="Siêu Ứng Dụng Khảo Sát VSTEP Toàn Diện - Master Blueprint",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📁 CO SỞ DỮ LIỆU ĐỀ THI ĐA PHÂN HỆ CỐ ĐỊNH (CHỐNG LỖI MẤT NGỮ CẢNH VÀ ĐƠ CÂU HỎI)
VSTEP_EXAM_DB = {
    "1️⃣ VSTEP Nghe": [
        {
            "id": 1,
            "type": "Part 1: Thông báo ngắn (Short Announcement)",
            "question": "How many languages are taught at Hanoi International Language School?",
            "options": ["A. 1", "B. 2", "C. 3", "D. 4"],
            "correct": "D",
            "script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean."
        },
        {
            "id": 2,
            "type": "Part 1: Hướng dẫn bay (Airport Announcement)",
            "question": "What is the boarding time of Flight VN178?",
            "options": ["A. 3:30", "B. 3:45", "C. 4:15", "D. 4:45"],
            "correct": "B",
            "script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45. Please gather at Gate 4 immediately."
        },
        {
            "id": 3,
            "type": "Part 2: Hội thoại học thuật (Academic Conversation)",
            "question": "What will be happening in Lecture hall 4 next Monday?",
            "options": ["A. An art workshop", "B. An art exhibition", "C. A history lesson", "D. A talk about history of art"],
            "correct": "D",
            "script": "Please note that next Monday's history lesson has been moved. Instead, Lecture hall 4 will host a special talk about the history of art given by Professor Evans."
        },
        {
            "id": 4,
            "type": "Part 2: Thông báo nội bộ trường học (Staff Notice)",
            "question": "Where should the teachers park their vehicles tomorrow?",
            "options": ["A. In the main school yard", "B. Behind the science building", "C. At the public stadium", "D. Along the main road"],
            "correct": "B",
            "script": "Attention all staff members. Due to the construction work in the main school yard tomorrow, please park your vehicles behind the science building until further notice."
        }
    ],
    "2️⃣ VSTEP Đọc": [
        {
            "id": 1,
            "type": "Passage 1: Y học & Đời sống (Epidemics Analysis)",
            "passage": "Diseases are a natural part of life on Earth. If there were no diseases, the human population would grow too quickly, and there would not be enough food. The severe Marburg virus, discovered in 1967, has an extremely dangerous fatality rate of 70-80%.",
            "question": "According to Passage 1, what is the exact fatality rate of the Marburg virus?",
            "options": ["A. 19%", "B. 67%", "C. 70-80%", "D. Over 90%"],
            "correct": "C"
        },
        {
            "id": 2,
            "type": "Passage 1: Y học & Đời sống (Epidemics Analysis)",
            "passage": "Diseases are a natural part of life on Earth. If there were no diseases, the human population would grow too quickly, and there would not be enough food. The severe Marburg virus, discovered in 1967, has an extremely dangerous fatality rate of 70-80%.",
            "question": "What is the primary natural function of diseases mentioned in the text?",
            "options": ["A. To eliminate all food resources", "B. To act as a natural check on population growth", "C. To improve medical laboratory statistics", "D. To encourage urban migration"],
            "correct": "B"
        },
        {
            "id": 3,
            "type": "Passage 2: Văn hóa & Trang phục (Japanese Dress Culture)",
            "passage": "Kimonos came to Japan from China originally as an undergarment. It later evolved into a traditional T-shaped outer robe. This traditional clothing is securely fastened around the waist with a wide decorative sash known as the Obi belt.",
            "question": "Where did the Kimono dress originally come from before evolving in Japan?",
            "options": ["A. Japan", "B. China", "C. Korea", "D. Austria"],
            "correct": "B"
        },
        {
            "id": 4,
            "type": "Passage 2: Văn hóa & Trang phục (Japanese Dress Culture)",
            "passage": "Kimonos came to Japan from China originally as an undergarment. It later evolved into a traditional T-shaped outer robe. This traditional clothing is securely fastened around the waist with a wide decorative sash known as the Obi belt.",
            "question": "What is the primary mechanical function of the wide Obi belt?",
            "options": ["A. To keep the neck area warm", "B. To cover the wearer's head", "C. To securely fasten the T-shaped robe around the waist", "D. To serve exclusively as an inner garment"],
            "correct": "C"
        }
    ],
    "3️⃣ VSTEP Viết": [
        {
            "id": 1,
            "type": "Task 1: Viết thư hồi đáp công việc (Informal Email Interaction)",
            "prompt": "You received an email from Jane asking about your friend An, who is planning to take a short English summer course in London. Write a reply email to provide details about his accommodation arrangements and arrival schedule.",
            "template": "Dear Jane,\n\nI am writing to inform you that An has finalized his summer course plan...\n\nBest regards,\n[Your Name]"
        },
        {
            "id": 2,
            "type": "Task 2: Viết luận nghị luận xã hội (Academic Essay Writing)",
            "prompt": "Write an academic essay (at least 250 words) to discuss the positive and negative effects of modern international tourism on local communities.",
            "template": "Introduction: In modern society, international tourism has become...\nBody 1 (Benefits): On the one hand, tourism significantly boosts local economy...\nBody 2 (Drawbacks): On the other hand, it causes severe environmental pollution...\nConclusion: In conclusion, while tourism has clear economic advantages..."
        }
    ],
    "4️⃣ VSTEP Nói": [
        {
            "id": 1,
            "type": "Part 1: Tương tác xã hội phản xạ (Social Interaction)",
            "prompt": "Let's talk about your free time activities. What TV channels do you prefer to watch? Do you like reading books in your spare time? Why or why not?"
        },
        {
            "id": 2,
            "type": "Part 2: Thảo luận giải pháp tối ưu (Solution Discussion Matrix)",
            "prompt": "Situation: You want to move a group of students from Danang to Hanoi for an educational field trip. There are three options available: Train, Plane, or Coach. Discuss which option is the best choice."
        },
        {
            "id": 3,
            "type": "Part 3: Phát triển chủ đề chuyên sâu (Topic Development Lecture)",
            "prompt": "Topic: Reading habits should be actively encouraged among teenagers.\n- Branch 1: It expands general academic knowledge.\n- Branch 2: It effectively reduces daily mental stress.\n- Branch 3: It improves long-term memory retention."
        }
    ]
}

# 🧠 MASTER_PROMPT: CHỈ THỊ ÉP AI CHẤM ĐIỂM VÀ ĐỒNG BỘ 3 DÒNG INTERLINEAR TUYỆT ĐỐI
MASTER_PROMPT = """
# ROLE & PERSONALITY
You are the elite "VSTEP Master Trainer" specialized in rapid remediation for learners who lost their English roots (người mất gốc). You operate with 20+ years of high-stakes teacher proficiency assessment experience. Address the user respectfully as "thầy cô".

# UNIVERSAL COMPACT INTERLINEAR RULE (MANDATORY FOR ALL RESPONSES)
Every single English piece of text, sample sentence, correction text, or alternative suggestion that you output MUST strictly follow this 3-line interlinear layout with hard `<br>` break tags to eliminate line collapsing forever on the UI:
<b><font color="#1E3A8A">ENG:</font></b> [English Text]<br>
<small><font color="#4B5563">🎵 IPA: /[Standard International Phonetic Alphabet chunk pauses]/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: [Dịch Nghĩa Tiếng Việt Bình Dân Dễ Hiểu Nhất]</font></i>

# EXPANDER DIEN_GIAI PACKAGING PROTOCOL
You MUST bundle your entire feedback analytical breakdown strictly inside `[DIEN_GIAI_START]` and `[DIEN_GIAI_END]` tags. Inside, render this exact scannable structure:
<b>[🎯 ĐÁP ÁN ĐÚNG / ĐÁNH GIÁ CHUYÊN GIA]</b>: <Provide score alignment or grammatical evaluation in 1 clear sentence>

<b>[🎧 CỤM TỪ VÀNG CẦN CHÚ Ý - VSTEP KEYWORDS]</b>
• <b>[Keyword/Phrase]</b>: [Nghĩa Việt] -> [Concise neuro-linguistic anchoring explanation].

<b>[🧠 SƠ ĐỒ TƯ DUY CẤU TRÚC - MIND MAP]</b>
📌 CẤU TRÚC CÂU GỐC
├── 🔑 Từ khóa cốt lõi: [Từ] -> [Nghĩa]
└── 🧱 Thành phần ngữ pháp chính:
    ├── S (Chủ ngữ): [Từ]
    ├── V (Động từ): [Từ]
    └── O (Tân ngữ): [Từ]

<b>[⚠️ BẪY ĐỀ THI - MẤT GỐC CẦN TRÁNH]</b>: <Explain traps concisely using simple math formulas or rules>
<b>[⏳ TRA CỨU THÌ QUÁ KHỨ - GỐC TỪ]</b>: <Map past verbs to infinitive form: "• <b>past_verb</b> là quá khứ của <b>infinitive_verb</b> (nghĩa)">

# AUDIO REGENERATION TAGS
Duplicate the target clear English sample text between `[AUDIO_START]` and `[AUDIO_END]` tags at the very end of your response block to trigger the playback engine.
"""

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

MODEL_NAME = "gemini-2.5-flash"

# 💾 STATE MANAGEMENT PHÒNG THI KIÊN CỐ CHỐNG MẤT NGỮ CẢNH
if "current_section" not in st.session_state:
    st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0

# ⚙️ SIDEBAR ĐIỀU HÀNH PHÒNG THI CHUYÊN GIA
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("1. Nhập Gemini API Key:", type="password")

st.sidebar.markdown("### 📁 BỘ CHỌN MÃ ĐỀ LUYỆN THI")
selected_de = st.sidebar.selectbox(
    "Chọn Mã đề thi thực chiến:",
    ["Mã đề VSTEP-2026-A (Đề Minh Họa Chuẩn)", "Mã đề VSTEP-2026-B (Biến Thể Song Song)", "Mã đề VSTEP-2026-C (Nâng Cao Chuyên Sâu)"]
)

font_size = st.sidebar.slider("Kích thước chữ (Nút chữ T)", 14, 24, 16)
st.markdown(f"<style>.stMarkdown, p, li, .stChatMessage {{ font-size: {font_size}px !important; }}</style>", unsafe_allow_html=True)

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True):
        st.session_state.current_section = "1️⃣ VSTEP Nghe"
        st.session_state.current_q_idx = 0
with col_s2:
    if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True):
        st.session_state.current_section = "2️⃣ VSTEP Đọc"
        st.session_state.current_q_idx = 0
col_s3, col_s4 = st.sidebar.columns(2)
with col_s3:
    if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True):
        st.session_state.current_section = "3️⃣ VSTEP Viết"
        st.session_state.current_q_idx = 0
with col_s4:
    if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True):
        st.session_state.current_section = "4️⃣ VSTEP Nói"
        st.session_state.current_q_idx = 0

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI (TIẾN LÙI TỰ DO)")

questions_list = VSTEP_EXAM_DB[st.session_state.current_section]
max_questions = len(questions_list)

col_prev, col_next = st.sidebar.columns(2)
with col_prev:
    if st.button("⏮️ CÂU TRƯỚC", use_container_width=True):
        st.session_state.current_q_idx = max(st.session_state.current_q_idx - 1, 0)
with col_next:
    if st.button("⏭️ CÂU TIẾP", use_container_width=True):
        st.session_state.current_q_idx = min(st.session_state.current_q_idx + 1, max_questions - 1)

if st.sidebar.button("🔄 KHỞI ĐỘNG LẠI PHÒNG THI", use_container_width=True):
    st.session_state.current_section = "1️⃣ VSTEP Nghe"
    st.session_state.current_q_idx = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.messages = []
    st.session_state.mic_key += 1
    if "scored_questions" in st.session_state:
        st.session_state.scored_questions.clear()
    st.rerun()

# 🏛️ KHÔNG GIAN KHẢO THÍ SỐ HÓA VSTEP
st.title("🎓 SIÊU ỨNG DỤNG KHẢO SÁT TIẾNG ANH VSTEP")
st.caption(f"Cơ sở hạ tầng Master Blueprint hoàn thiện | Đang vận hành: {selected_de}")
st.markdown("---")

# 📊 ĐỒNG HỒ ĐẾM NGƯỢC VÀ THANH TIẾN ĐỘ THỰC TẾ TRÊN GIAO DIỆN
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(50 * 60 - elapsed_time, 0)
mins, secs = divmod(int(remaining_time), 60)

dash_col1, dash_col2, dash_col3 = st.columns(3)
with dash_col1:
    st.markdown(f"**📊 PHẦN THI HIỆN TẠI: {st.session_state.current_section}**")
    st.progress((st.session_state.current_q_idx + 1) / max_questions)
    st.caption(f"Tiến độ: Câu {st.session_state.current_q_idx + 1} trên tổng số {max_questions} mục tiêu.")
with dash_col2:
    st.metric(label="💯 Điểm Số Phòng Thi Hiện Tại", value=f"{st.session_state.score} Điểm")
with dash_col3:
    st.metric(label="⏳ Đồng Hồ Đếm Ngược", value=f"{mins:02d}:{secs:02d} Phút")

st.markdown("---")

# 📥 TRÍCH XUẤT ĐỐI TƯỢNG ĐỀ BÀI HIỆN TẠI TỪ PYTHON DATABASE (ĐẢM BẢO LUÔN HIỂN THỊ)
active_q = questions_list[st.session_state.current_q_idx]

# Thuật toán hoán đổi dữ liệu động để tạo biến thể song song khi chọn mã đề B hoặc C
display_question = active_q['question']
display_options = list(active_q['options'])
display_script = active_q.get('script', "")
display_passage = active_q.get('passage', "")
display_prompt = active_q.get('prompt', "")

if "Mã đề VSTEP-2026-B" in selected_de or "Mã đề VSTEP-2026-C" in selected_de:
    display_question = display_question.replace("Hanoi", "Saigon").replace("Marburg", "Ebola").replace("VN178", "VN256")
    display_options = [opt.replace("4", "5").replace("3:45", "4:15").replace("70-80%", "80-90%").replace("China", "Korea") for opt in display_options]
    if display_script:
        display_script = display_script.replace("Hanoi", "Saigon").replace("four", "five").replace("VN178", "VN256").replace("3:30 to 3:45", "4:00 to 4:15")
    if display_passage:
        display_passage = display_passage.replace("Marburg", "Ebola").replace("70-80%", "80-90%").replace("China", "Korea")
    if display_prompt:
        display_prompt = display_prompt.replace("London", "New York").replace("Danang to Hanoi", "Nha Trang to Saigon")

st.markdown(f"### 📝 {active_q['type']} - Câu hỏi số {active_q['id']}")

# Luồng hiển thị trực quan cho từng kỹ năng cụ thể
if st.session_state.current_section == "1️⃣ VSTEP Nghe":
    st.info("🎧 **Học viên nghe băng ghi âm chủ động dưới đây và chọn đáp án chính xác (Văn bản kịch bản đã được giấu tự động để chống bẫy thị giác):**")
    tts = gTTS(text=display_script, lang='en', tld='com')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format="audio/mp3")
    
    st.markdown(f"**Question:** {display_question}")
    user_choice = st.radio("Chọn phương án trả lời:", display_options, key=f"listen_radio_{active_q['id']}_{selected_de}")

elif st.session_state.current_section == "2️⃣ VSTEP Đọc":
    st.success("=== ĐOẠN VĂN NỀN ĐỌC HIỂU HOÀN CHỈNH (PASSAGE CONTEXT) ===")
    st.markdown(f"> {display_passage}")
    st.markdown("=========================================================")
    st.markdown(f"**Question:** {display_question}")
    user_choice = st.radio("Chọn phương án trả lời:", display_options, key=f"read_radio_{active_q['id']}_{selected_de}")

elif st.session_state.current_section == "3️⃣ VSTEP Viết":
    st.warning("✍️ **ĐỀ BÀI LUẬN / THƯ TỰ LUẬN CHUẨN HÓA (WRITING TASK):**")
    st.markdown(f"📢 **Yêu cầu:** {display_prompt}")
    with st.expander("💡 Bấm vào đây để xem Khung xương cá từ vựng gợi ý (Sentence Scaffolding Templates)"):
        st.code(active_q.get("template", ""), language="markdown")
    user_essay = st.text_area("Nhập nội dung bài viết tự luận của thầy cô tại đây (Hệ thống sẽ chuyển cho AI chấm điểm chuyên sâu):", height=250, key=f"write_area_{active_q['id']}")

elif st.session_state.current_section == "4️⃣ VSTEP Nói":
    st.error("🎤 **ĐỀ THI NÓI THỰC CHIẾN (SPEAKING PROMPT):**")
    st.markdown(f"🗣️ **Yêu cầu phản xạ:** {display_prompt}")
    st.info("Thầy cô hãy bật nút Ghi âm ở thanh Micro bên dưới thanh điều hướng Sidebar để thu âm câu trả lời.")

st.markdown("---")

# 🏛️ HÀM GIAO TIẾP VỚI BỘ NÃO AI GEMINI ĐỂ THẨM ĐỊNH LỜI GIẢI VÀ ĐÓNG GÓI NÚT DIỄN GIẢI
def get_model():
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME, system_instruction=MASTER_PROMPT, safety_settings=SAFETY_SETTINGS)

def extract_text_safely(response):
    try:
        if not response.candidates:
            return None, "⚠️ Bộ lọc an toàn của API đã từ chối xử lý âm thanh nhiễu. Thầy/cô vui lòng thu âm to, rõ ràng hơn."
        candidate = response.candidates[0]
        parts_text = [part.text for part in candidate.content.parts if hasattr(part, "text") and part.text]
        return "".join(parts_text).strip(), None
    except Exception as e:
        return None, f"⚠️ Lỗi đọc luồng dữ liệu AI candidate: {e}"

def render_custom_vstep_message(content):
    clean_content = content
    dien_giai_text = ""
    if "[DIEN_GIAI_START]" in content and "[DIEN_GIAI_END]" in content:
        start_dg = content.find("[DIEN_GIAI_START]")
        end_dg = content.find("[DIEN_GIAI_END]")
        dien_giai_text = content[start_dg + len("[DIEN_GIAI_START]"):end_dg].strip()
        clean_content = content.replace(content[start_dg:end_dg + len("[DIEN_GIAI_END]")], "")
    
    visible_content = clean_content.replace("[SCORE_UP]", "")
    st.markdown(visible_content, unsafe_allow_html=True)
    if dien_giai_text:
        with st.expander("=== BẤM VÀO ĐÂY ĐỂ BUNG SƠ ĐỒ TƯ DUY, CỤM TỪ VÀNG & TRA CỨU QUÁ KHỨ ==="):
            st.markdown(dien_giai_text, unsafe_allow_html=True)

# 🚀 NÚT BẤM NỘP BÀI THỰC CHIẾN DÀNH CHO TRẮC NGHIỆM VÀ ĐOẠN VĂN VIẾT
if st.session_state.current_section in ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc", "3️⃣ VSTEP Viết"]:
    if st.button("🚀 NỘP BÀI THỰC CHIẾN", use_container_width=True):
        if not api_key:
            st.sidebar.error("Vui lòng nhập API Key để kích hoạt bộ não thẩm định AI.")
        else:
            if st.session_state.current_section in ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc"]:
                student_answer = user_choice[0]
                is_correct = (student_answer == active_q["correct"])
                score_tag = "[SCORE_UP]" if is_correct else ""
                
                eval_prompt = f"""
                Học viên đang làm đề {selected_de}, kỹ năng {st.session_state.current_section}, câu hỏi: '{display_question}'.
                Đáp án đúng của hệ thống là: {active_q['correct']}. Học viên chọn phương án: {student_answer}.
                Hãy xuất ra kết quả chấm điểm. Nếu đúng chèn thẻ {score_tag}.
                Sau đó áp dụng quy tắc cưỡng bách 3 dòng interlinear để biểu diễn câu hỏi và phương án đúng chuẩn mực.
                Cuối cùng đóng gói phần bóc tách sơ đồ tư duy, từ khóa vàng định vị thính giác vào cặp thẻ [DIEN_GIAI_START] và [DIEN_GIAI_END].
                """
            else:
                eval_prompt = f"""
                Học viên nộp bài tự luận viết cho đề bài: '{display_prompt}'.
                Nội dung văn bản học viên viết:
                \"\"\"{user_essay}\"\"\"
                Hãy đóng vai trò chuyên gia khảo thí, sửa sai ngữ pháp, nhuộm đỏ từ dùng lỗi, cung cấp bản viết lại chuẩn hóa theo cấu trúc interlinear 3 dòng ngắt hàng bằng thẻ <br>.
                Đóng gói phần chấm điểm, mẹo huấn luyện cấu trúc câu xương cá vào bên trong cặp thẻ [DIEN_GIAI_START] và [DIEN_GIAI_END].
                """
            
            with st.spinner("Hệ thống chuyên gia đang phân tích dữ liệu..."):
                try:
                    model = get_model()
                    response = model.generate_content(eval_prompt)
                    res_text, err = extract_text_safely(response)
                    final_payload = res_text if res_text else err
                    
                    if res_text and "[SCORE_UP]" in res_text:
                        q_key = f"{selected_de}_{st.session_state.current_section}_{active_q['id']}"
                        if "scored_questions" not in st.session_state:
                            st.session_state.scored_questions = set()
                        if q_key not in st.session_state.scored_questions:
                            st.session_state.score += 10
                            st.session_state.scored_questions.add(q_key)
                    
                    st.session_state.messages.append({"role": "assistant", "content": final_payload})
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi hệ thống truyền tải: {e}")

# 🚀 NÚT BẤM NỘP BÀI THI NÓI (XỬ LÝ FILE NHỊ PHÂN TỪ SIDEBAR AUDIO_INPUT)
audio_data = st.sidebar.audio_input(
    "Bấm nút tròn bên dưới để thu âm bài nói trực tiếp:",
    key=f"mic_widget_{st.session_state.mic_key}"
)

if audio_data is not None:
    if st.sidebar.button("🚀 NỘP BÀI THI NÓI VSTEP", use_container_width=True):
        if not api_key:
            st.sidebar.error("Vui lòng điền mã API Key để thẩm định giọng nói.")
        else:
            vstep_speech_command = f"""
            Đây là file ghi âm bài nói micro của tôi tại câu số {active_q['id']} phần {st.session_state.current_section} mã đề {selected_de}. Đề bài yêu cầu: '{display_prompt}'.
            Hãy thực hiện bóc băng âm thanh, chỉ viết ra text những từ nghe rõ tự tin, so sánh với câu mẫu chuẩn. Nhuộm đỏ từ phát âm lệch chuẩn.
            Toàn bộ câu mẫu và sửa lỗi bắt buộc trình bày 3 dòng interlinear ngắt hàng bằng thẻ <br>.
            Gói toàn bộ sơ đồ cấu trúc câu Mind Map phân nhánh vào cặp thẻ [DIEN_GIAI_START] và [DIEN_GIAI_END].
            """
            with st.spinner("Hệ thống AI NLP đang xử lý và phân tách thính giác..."):
                try:
                    model = get_model()
                    contents = [{
                        "mime_type": audio_data.type or "audio/wav",
                        "data": audio_data.getvalue()
                    }, vstep_speech_command]
                    
                    response = model.generate_content(contents=contents)
                    res_text, err = extract_text_safely(response)
                    final_payload = res_text if res_text else err
                    
                    st.session_state.messages.append({"role": "assistant", "content": final_payload})
                    st.session_state.mic_key += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi phân tích tệp micro: {e}")

# 📜 KHÔNG GIAN BẢNG TIN CHAT HIỂN THỊ KẾT QUẢ VÀ HỘP CÔNG CỤ DIỄN GIẢI
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 🔔 KẾT QUẢ THẨM ĐỊNH VÀ SỬA LỖI TỪ AI CHUYÊN GIA:")
    for message in st.session_state.messages[-1:]:
        with st.chat_message(message["role"]):
            render_custom_vstep_message(message["content"])
