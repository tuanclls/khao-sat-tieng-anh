import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import base64
import time      # ✨ "Thời gian là vàng bạc" - Kính chúc thầy cô và học viên luôn làm chủ mọi khoảnh khắc vàng ngọc.

# ✨ "Hiền tài là nguyên khí của quốc gia" - Thiết lập không gian khảo thí VSTEP chuẩn sư phạm.
st.set_page_config(
    page_title="Hệ Thống Khảo Sát VSTEP Tiếng Anh Cho Giáo Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🧠 BỘ NÃO AI VSTEP SIÊU THỰC CHIẾN - Tích hợp dữ liệu thính giác thông minh và kho đề mẫu chính thức.
MASTER_PROMPT = """
# ROLE & PERSONALITY
You are the official interactive "VSTEP Proficiency Assessment Application". Your absolute objective is to evaluate and train the teacher (addressed respectfully as "thầy cô") to master the VSTEP exam using Real-Time Adaptive Feedback.

# NUMERIC NAVIGATION SYSTEM (VSTEP STRUCTURE)
Route the exam sections immediately based on numeric inputs:
- Input `1`: SECTION 1: LISTENING (Based on official VSTEP sample text bank below)
- Input `2`: SECTION 2: READING (Based on official VSTEP sample text bank below)
- Input `3`: SECTION 3: WRITING (VSTEP Task 1 Email & Task 2 Essay)
- Input `4`: SECTION 4: SPEAKING (Social Interaction, Solution Discussion & Topic Development)

# SEQUENTIAL DELIVERY WORKFLOW
1. Present exam items ONE BY ONE strictly. Do not display multiple questions or mix sections.
2. Hide answer keys, comprehensive syntax breakdowns, and explanations until the user submits their option (A, B, C, D) or record text. Once submitted, reveal deep pedagogical feedback immediately.

# MANDATORY INTERLINEAR 3-LINE SEPARATE LAYOUT (STRICTLY ENFORCED)
Whenever you display ANY English material, sample answers, or sentences, you MUST print them in three strictly SEPARATE lines with clear structural markings:
Line 1: [📦 ENG] <English text>
Line 2: [🎵 IPA] <Standard IPA transcription with / for rhythmic pauses>
Line 3: [🇻🇳 VIE] <Contextual Vietnamese translation>

# SMART MICROPHONE AUDIO FILTRATION PROTOCOL (HEAR CLEARLY RULE)
When analyzing the raw spoken audio recorded by the user, act as an advanced audio-linguistic filter:
1. [SPEECH-TO-TEXT FILTRATION]: Predict and transcribe what the user said. Only write down words that are HEARD CLEARLY and intelligibly. If a word is mumbled, heavily masked by background noise, or whispered unreadably, do NOT write or include it in the transcription text at all.
2. [VISUAL ERROR GRAPHICS]: Render the clearly heard transcribed text using a clean custom HTML block. Compare it word-by-word against the standard target sentence:
   - Correctly pronounced words: Display in dark blue/black (`.txt-correct`).
   - Mispronounced or entirely skipped targeted words: You MUST color them in bright RED (`.txt-wrong`), and insert their standard correct IPA phonetics directly underneath (`.ipa-practice`) so they can practice targeted fixing.

# EMBEDDED OFFICIAL VSTEP MINH HOA MATERIAL BANK
Use this official syllabus text for text generation and assessment routing:
- SECTION 1: LISTENING 
  * Q1: "How many languages are taught at Hanoi International Language School?" (A. 1 | B. 2 | C. 3 | B. 4)
  * Q2: "What is the boarding time of Flight VN178?" (A. 3.30 | B. 3.45 | C. 4.15 | D. 4.45)
  * Q3: "What will be happening in Lecture hall 4 next Monday?" (A. An art workshop | B. An art exhibition | C. A history lesson | D. A talk about history of art)
- SECTION 2: READING
  * Passage 1: Nature's balance and pandemics. "Diseases are a natural part of life on Earth. If there were no diseases, the population would grow too quickly..." (Focus on Marburg virus vs 1918 flu statistics).
  * Passage 2: Japanese Dress Culture. "Kimonos came to Japan from China. They were worn underneath clothes as an undergarment. Kimono was the Japanese word for clothing..."
- SECTION 3: WRITING
  * Task 1: Email responding to Jane about friend An taking a course in London this summer.
  * Task 2: Essay evaluating the positive and negative effects of tourism on local communities or City vs Countryside living (At least 250 words).
- SECTION 4: SPEAKING
  * Part 1 (Social Interaction): Free time activities (TV channels, reading books) and neighborhood preferences.
  * Part 2 (Solution Discussion): Moving a group from Danang to Hanoi. Choices: Train, Plane, or Coach.
  * Part 3 (Topic Development): "Reading habit should be encouraged among teenagers." (Branches: increases knowledge, reduces stress, improves memory).

# AUDIO REGENERATION COMPLIANCE TAGS
For every turn of generation containing an English listening task or oral model answer, duplicate the pure target English sentence inside `[AUDIO_START] target text [AUDIO_END]` at the very end of your block. This is critical to maintain the functionality of the gTTS engine.
"""

# 💾 HỆ THỐNG LƯU TRỮ PHÒNG THI KIÊN CỐ - Chống đơ, chống bẫy lặp quay vòng dữ liệu.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ⚙️ BẢN ĐIỀU HƯỚNG PHÒNG THI SƯ PHẠM
st.sidebar.title("⚙️ ĐIỀU HÀNH THI VSTEP")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("1. Nhập Gemini API Key:", type="password")

font_size = st.sidebar.slider("2. KÍCH THƯỚC CHỮ (Nút chữ T)", 14, 24, 16)
st.markdown(f"<style>.stMarkdown, p, li, .stChatMessage {{ font-size: {font_size}px !important; }}</style>", unsafe_allow_html=True)

# 🔢 PHÍM TẮT CHUYỂN NHANH PHẦN THI THEO ĐỀ MẪU VSTEP
st.sidebar.markdown("### 🔢 PHẦN THI THEO ĐỀ MẪU")
col_s1, col_s2 = st.sidebar.columns(2)
nav_action = None
with col_s1:
    if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True): nav_action = "1"
    if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True): nav_action = "3"
with col_s2:
    if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True): nav_action = "2"
    if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True): nav_action = "4"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG THI TUẦN TỰ")

if st.sidebar.button("⏭️ CÂU TIẾP THEO", use_container_width=True):
    st.session_state.current_q = min(st.session_state.current_q + 1, 12)
    st.session_state.score = min(st.session_state.score + 5, 100)
    nav_action = f"Hãy đưa ra câu hỏi VSTEP tiếp theo số {st.session_state.current_q} và tuân thủ tuyệt đối quy tắc 3 dòng phân tách biệt lập."

if st.sidebar.button("🔄 LÀM LẠI TỪ ĐẦU", use_container_width=True):
    st.session_state.current_q = 1
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    nav_action = "VỀ MENU CHÍNH"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎤 THI NÓI VSTEP VÀ PHÁT ÂM")
audio_data = st.sidebar.audio_input("Bấm nút tròn để tiến hành thu âm trực tiếp:")

# 🏛️ KHÔNG GIAN KHẢO THÍ SỐ HÓA THỰC CHIẾN VSTEP
st.title("🎓 ỨNG DỤNG KHẢO SÁT TIẾNG ANH VSTEP")
st.caption("Phiên bản Đề Minh Họa Gốc - Cấu trúc 3 dòng biệt lập biệt li - Bộ lọc thính giác thông minh nghe rõ mới ghi chữ")
st.markdown("---")

# 📊 BẢNG THEO DÕI TIẾN ĐỘ THỜI GIAN VÀ ĐIỂM SỐ SƯ PHẠM
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(50 * 60 - elapsed_time, 0) # Khung thời gian VSTEP quy đổi tổng thể
mins, secs = divmod(int(remaining_time), 60)

dash_col1, dash_col2, dash_col3 = st.columns(3)
with dash_col1:
    st.metric(label="📈 Tiến Độ Đề Thi", value=f"Câu {st.session_state.current_q} / 12")
    st.progress(st.session_state.current_q / 12)
with dash_col2:
    st.metric(label="💯 Điểm Số Ước Tính", value=f"{st.session_state.score} / 100 Điểm")
with dash_col3:
    st.metric(label="⏳ Thời Gian Còn Lại", value=f"{mins:02d}:{secs:02d} Phút")

st.markdown("---")

# 🌟 KHỞI TẠO LỜI CHÀO PHÒNG THI TỰ ĐỘNG
if "initialized" not in st.session_state and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=MASTER_PROMPT)
        init_res = model.generate_content("START_APPLICATION")
        st.session_state.messages.append({"role": "assistant", "content": init_res.text})
        st.session_state.initialized = True
    except Exception as e:
        st.sidebar.error(f"Lỗi liên kết hệ thống: {e}")

# 🎵 TÁI SINH NÚT PHÁT ÂM THANH CHỦ ĐỘNG (AUTOPLAY=FALSE GIÚP THẦY CÔ LÀM CHỦ)
def play_audio_safely(text_content):
    if "[AUDIO_START]" in text_content and "[AUDIO_END]" in text_content:
        try:
            start_idx = text_content.find("[AUDIO_START]") + len("[AUDIO_START]")
            end_idx = text_content.find("[AUDIO_END]")
            audio_text = text_content[start_idx:end_idx].strip()
            if audio_text:
                tts = gTTS(text=audio_text, lang='en', tld='com')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                b64_audio = base64.b64encode(fp.read()).decode()
                audio_html = f'<audio controls src="data:audio/mp3;base64,{b64_audio}" style="width: 100%; margin-top: 12px; margin-bottom: 12px;"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi tạo thanh phát âm thanh: {e}")

# 📜 HIỂN THỊ DÒNG LỊCH SỬ KHẢO THÍ CHUẨN ĐỒ HỌA SƯ PHẠM
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
        if message["role"] == "assistant":
            play_audio_safely(message["content"])

# 🚀 CỔNG TRUYỀN DỮ LIỆU ĐƯỜNG TRUYỀN HỎA TỐC BIÊN NGOÀI
def send_exam_data(prompt_text, audio_file=None, is_nav=False):
    if not api_key:
        st.sidebar.warning("Thầy/cô vui lòng điền mã API Key ở góc trái để bắt đầu kích hoạt bài thi!")
        return
        
    response_text = ""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=MASTER_PROMPT)
        
        if is_nav:
            st.session_state.messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"][-1:]
        
        formatted_contents = []
        for msg in st.session_state.messages[-4:]:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append({"role": role, "parts": [msg["content"]]})
        
        if audio_file is not None:
            st.session_state.messages.append({"role": "user", "content": "🎤 [Hệ thống nhận tệp âm thanh trực tiếp từ Microphone]"})
            formatted_contents.append({
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": audio_file.type,
                            "data": audio_file.getvalue()
                        }
                    },
                    prompt_text
                ]
            })
        else:
            st.session_state.messages.append({"role": "user", "content": prompt_text})
            formatted_contents.append({"role": "user", "parts": [prompt_text]})
        
        with st.chat_message("assistant"):
            with st.spinner("Hệ thống VSTEP đang phân tích sóng âm và bóc tách dữ liệu câu..."):
                response = model.generate_content(contents=formatted_contents)
                response_text = response.text
                st.markdown(response_text, unsafe_allow_html=True)
                play_audio_safely(response_text)
                
    except Exception as e:
        st.error(f"❌ Hệ thống thông báo lỗi đường truyền: {e}. Vui lòng kiểm tra lại thiết bị thu âm hoặc API.")
        return

    # KÍCH HOẠT BIÊN NGOÀI KHỐI - Bẻ gãy hoàn toàn bẫy lỗi treo đơ giao diện
    if response_text:
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()

# Kích hoạt luồng điều hướng nút hành chính phụ trợ
if nav_action:
    send_exam_data(nav_action, is_nav=True)

# 🚀 NỘP BÀI THI NÓI VSTEP - Thuật toán lọc âm thanh thông minh và thiết lập đồ họa màu đỏ sửa sai
if audio_data is not None:
    if st.sidebar.button("🚀 NỘP BÀI THI NÓI VSTEP", use_container_width=True):
        vstep_speech_command = """
        Đây là dữ liệu giọng nói của tôi từ micro. Hãy xử lý nghiêm ngặt theo các bước sau:
        
        1. [DỰ ĐOÁN VÀ BÓC BĂNG PHÁN ĐOÁN AI]: Hãy đóng vai trò bộ lọc thính giác thông minh. Hãy chỉ ghi ra chữ (transcribe) những từ ngữ được tôi phát âm RÕ ÂM, rõ từ và nghe rõ ràng mạch lạc. Nếu từ nào thều thào, nói lắp, phát âm quá nhỏ hoặc bị tiếng ồn môi trường che khuất, tuyệt đối KHÔNG ĐƯỢC GHI RA.
        
        2. [MÃ HTML ĐỒ HỌA SO SÁNH PHÁT ÂM]: So sánh đoạn từ nghe rõ được với câu chuẩn của đề thi VSTEP. Trả về một khối mã HTML duy nhất (không bọc trong ký tự dấu nháy ```html) áp dụng CSS sau:
           <style>
              .word-group { display: inline-block; text-align: center; margin-right: 14px; margin-bottom: 18px; vertical-align: top; }
              .txt-correct { font-size: 19px; color: #2e7d32; font-weight: bold; }
              .txt-wrong { font-size: 19px; color: #d32f2f; font-weight: bold; }
              .ipa-practice { font-size: 13px; color: #c62828; font-family: monospace; display: block; margin-top: 5px; }
           </style>
           - Từ phát âm CHUẨN: bọc trong <div class='word-group'><span class='txt-correct'>Từ_Gốc</span></div>
           - Từ phát âm SAI hoặc BỊ BỎ QUA trong câu mẫu: Nhuộm màu ĐỎ rực rỡ bằng cách bọc trong <div class='word-group'><span class='txt-wrong'>Từ_Gốc</span><span class='ipa-practice'>/Phiên_Âm_Chuẩn/</span></div>
        
        3. [BIỂU DIỄN 3 DÒNG BIỆT LẬP TUYỆT ĐỐI]: Ngay bên dưới khối HTML sửa lỗi, hãy trình bày bài mẫu chuẩn, lời giải thích ngữ pháp chi tiết theo đúng thiết kế 3 dòng tách biệt biệt li:
           Dòng 1: [📦 ENG] <Câu Anh mẫu tiếng>
           Dòng 2: [🎵 IPA] <Phiên chuẩn quốc tế âm>
           Dòng 3: [🇻🇳 VIE] <Bản Việt bám dịch họa minh nghĩa sát tiếng đề>
           
        4. [TÁI SINH NÚT PHÁT ÂM THANH]: Đảm bảo sao chép lại câu tiếng Anh chuẩn bọc trong cặp thẻ [AUDIO_START] Câu tiếng Anh chuẩn [AUDIO_END] đặt ở cuối thông điệp để dựng lại nút phát thanh cho người học.
        """
        send_exam_data(vstep_speech_command, audio_file=audio_data)

# 📝 KHUNG TIẾP NHẬN BÀI LÀM TRẮC NGHIỆM VÀ BÀI VIẾT TỰ LUẬN VSTEP
if text_input := st.chat_input("Nhập đáp án trắc nghiệm (A,B,C,D), số phân hệ (1,2,3,4) hoặc nội dung bài viết luận tại đây..."):  
    if text_input.strip() in ["1", "2", "3", "4"]:
        send_exam_data(text_input.strip(), is_nav=True)
    else:
        send_exam_data(f"Tôi nộp đáp án/bài làm tự luận VSTEP là: {text_input}. Hãy thẩm định chuyên môn, phân tích sâu cấu trúc câu và trình bày kết quả theo đúng thiết kế bố cục 3 dòng biệt lập hoàn toàn (Dòng 1: Tiếng Anh, Dòng 2: Phiên âm IPA, Dòng 3: Dịch nghĩa). Đừng quên nhúng mã [AUDIO_START] nội dung tiếng Anh chuẩn [AUDIO_END] ở cuối cùng để hiển thị lại nút bấm phát âm thanh chủ động.")
