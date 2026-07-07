import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
import base64
import time      # ✨ "Thời gian là vàng bạc" - Chúc thầy cô và học trò luôn trân quý từng phút giây mài giũa tri thức!

# ✨ "Hiền tài là nguyên khí của quốc gia." - Giáo dục là nền tảng chắp cánh cho mọi ước mơ sư phạm đại tài.
st.set_page_config(
    page_title="Hệ Thống Khảo Sát Tiếng Anh Cho Giáo Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🧠 "Muốn biết phải hỏi, muốn giỏi phải học." - Bộ não cốt lõi luôn đồng hành cùng thầy cô khám phá tri thức mới.
MASTER_PROMPT = """
# ROLE & PERSONALITY
You are the official interactive "English Proficiency Assessment Application for Teachers", inheriting 20+ years of expertise in Applied Linguistics, Language Pedagogy, and Cognitive Psychology. Your absolute objective is to train the teacher (addressed respectfully as "thầy cô") to effortlessly pass their 4-skill standardized exam using Reverse Engineering and Real-Time Feedback.

# NUMERIC NAVIGATION SYSTEM
You must listen to numeric inputs from the user or system to route the exam sections immediately:
- Input `1`: SECTION 1: LISTENING (12 Questions total)
- Input `2`: SECTION 2: READING (12 Questions total)
- Input `3`: SECTION 3: WRITING (Opinion Paragraph)
- Input `4`: SECTION 4: SPEAKING (Opinion Presentation)

# SEQUENTIAL QUESTION DELIVERY & INTERACTIVE ANSWER WORKFLOW
1. Present the exam questions ONE BY ONE strictly based on the current question index provided.
2. For the active question, display ONLY the question text using the 3-LINE INTERLINEAR FORMAT below. Do not show the explanation or syntax anatomy yet.
3. Once the user enters an answer (e.g., A, B, C, D) or submits a paragraph/speech, IMMEDIATELY reveal:
   - Whether it is Correct/Incorrect.
   - The full [🧬 GIẢI PHẪU NGỮ PHÁP CÚ PHÁP] breakdown in Vietnamese explaining why this choice is correct and how it fits Level 4 (B2) criteria.

# MANDATORY INTERLINEAR 3-LINE LAYOUT (STRICTLY ENFORCED)
Whenever you introduce ANY English text (reading passages, listening text, active questions, or speech templates), you MUST format it strictly line-by-line using this exact 3-line parallel structure:
- Dòng 1: [📦 ENG] <Chữ tiếng Anh nguyên bản>
- Dòng 2: [🎵 IPA] <Phiên âm quốc tế chuẩn, phân tách các cụm nghĩa bằng dấu / để ngắt nghỉ rhythmic>
- Dòng 3: [🇻🇳 VIE] <Bản dịch nghĩa tiếng Việt bám sát ngữ cảnh sư phạm>

Example layout format:
[📦 ENG] Education is the key to success.
[🎵 IPA] /ˌedʒuˈkeɪʃn/ /ɪz/ /ðə/ /kiː/ /tə/ /səkˈses/
[🇻🇳 VIE] Giáo dục là chìa khóa dẫn tới thành công.

# RAW AUDIO PROCESSING & SPEECH-TO-TEXT PROTOCOL
When you receive raw audio data input from the microphone, you MUST execute these steps in absolute order to prevent text-masking bugs:
1. Display a prominent heading: `### [🗣️ TEXT ĐÃ NGHE ĐƯỢC TỪ MICROPHONE]`
2. Output the exact English words transcribed from the teacher's speech.
3. Apply the 3-LINE INTERLINEAR LAYOUT (ENG -> IPA -> VIE) directly onto that transcribed speech text.
4. Provide [🎯 CHẤM ĐIỂM PHÁT ÂM] and [💼 ỨNG DỤNG THỰC CHIẾN] based on their voice input.

# AUDIO SYNCHRONIZATION TAGS
Wrap English text segments meant for listening practice between [AUDIO_START] and [AUDIO_END] tags. Do not autoplay.
"""

# 💾 "Trẻ vui học hỏi, già thích suy tư." - Khởi tạo cấu trúc bộ nhớ lưu trữ bền vững để theo dõi tiến độ phòng thi.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ⚙️ "Muốn sang thì bắc cầu Kiều, muốn con hay chữ thì yêu lấy thầy." - Bản điều hướng trợ thủ đắc lực nâng bước thầy cô.
st.sidebar.title("⚙️ BẢN ĐIỀU HƯỚNG PHÒNG THI")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("1. Nhập Gemini API Key:", type="password")

font_size = st.sidebar.slider("2. NÚT CHỮ T (Kích thước chữ)", 14, 24, 16)

# 🔤 "Học hải vô biên, cần cần vi lộ." - Giao diện tối ưu hóa hiển thị, trân trọng và bảo vệ đôi mắt ngọc ngà của thầy cô.
st.markdown(f"<style>.stMarkdown, p, li, .stChatMessage {{ font-size: {font_size}px !important; }}</style>", unsafe_allow_html=True)

# 🔢 "Đi một ngày đàng, học một sàng khôn." - Lối tắt chọn phần thi bằng chữ số hành chính tối giản.
st.sidebar.markdown("### 🔢 CHỌN NHANH PHẦN THI")
col_s1, col_s2 = st.sidebar.columns(2)
nav_action = None
with col_s1:
    if st.sidebar.button("1️⃣ Phần Nghe", use_container_width=True): nav_action = "1"
    if st.sidebar.button("3️⃣ Phần Viết", use_container_width=True): nav_action = "3"
with col_s2:
    if st.sidebar.button("2️⃣ Phần Đọc", use_container_width=True): nav_action = "2"
    if st.sidebar.button("4️⃣ Phần Nói", use_container_width=True): nav_action = "4"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI LẦN LƯỢT")

# ⏭️ "Có công mài sắt, có ngày nên kim." - Nút chuyển câu tiếp theo, hiển thị đề bài một cách tuần tự khoa học.
if st.sidebar.button("⏭️ CÂU TIẾP THEO", use_container_width=True):
    st.session_state.current_q = min(st.session_state.current_q + 1, 12)
    st.session_state.score = min(st.session_state.score + 5, 100)
    nav_action = f"Hãy đưa ra câu hỏi số {st.session_state.current_q} theo đúng lộ trình và áp dụng cấu trúc 3 dòng interlinear."

# 🔄 "Học nhi thời tập chi, bất diệc duyệt hồ." - Làm lại từ đầu, ôn cũ biết mới, khơi nguồn động lực rực rỡ.
if st.sidebar.button("🔄 LÀM LẠI TỪ ĐẦU", use_container_width=True):
    st.session_state.current_q = 1
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    nav_action = "VỀ MENU CHÍNH"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎤 PHẦN THI NÓI - THU ÂM")
audio_data = st.sidebar.audio_input("Bấm nút tròn để ghi âm bài làm trực tiếp:")

# 🏛 "Vì lợi ích mười năm thì phải trồng cây, vì lợi ích trăm năm thì phải trồng người." - Giảng đường số hóa hiện đại.
st.title("🎓 ỨNG DỤNG KHẢO SÁT TIẾNG ANH CHO GIÁO VIÊN")
st.caption("Giao diện tối ưu Cloud Run & Win.exe - Cấu trúc 3 dòng Interlinear song song & Phản hồi đáp án thông minh")
st.markdown("---")

# 📊 "Ngọc kia chuốt mới nên đồ, người ta học mới biết cơ biết điều." - Bảng tiến độ, thời gian đếm ngược trực quan.
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(60 * 60 - elapsed_time, 0)
mins, secs = divmod(int(remaining_time), 60)

dash_col1, dash_col2, dash_col3 = st.columns(3)
with dash_col1:
    st.metric(label="📈 Tiến Độ Bài Làm", value=f"Câu {st.session_state.current_q} / 12")
    st.progress(st.session_state.current_q / 12)
with dash_col2:
    st.metric(label="💯 Thang Điểm Hiện Tại", value=f"{st.session_state.score} / 100 Điểm")
with dash_col3:
    st.metric(label="⏳ Thời Gian Còn Lại", value=f"{mins:02d}:{secs:02d} Phút")

st.markdown("---")

# 🌟 "Vạn sự khởi đầu nan." - Tự động kích hoạt hệ thống lời chào mở màn từ bộ não siêu trí tuệ nhân tạo.
if "initialized" not in st.session_state and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=MASTER_PROMPT)
        init_res = model.generate_content("START_APPLICATION")
        st.session_state.messages.append({"role": "assistant", "content": init_res.text})
        st.session_state.initialized = True
    except Exception as e:
        st.sidebar.error(f"Lỗi kết nối hệ thống: {e}")

# 🎵 "Thánh thót như tiếng đàn cầm." - Nút phát âm thanh tinh tế, tắt chế độ tự động chạy (Autoplay=False) giúp người học làm chủ.
def play_audio_safely(text_content):
    if "[AUDIO_START]" in text_content:
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
                audio_html = f'<audio controls src="data:audio/mp3;base64,{b64_audio}" style="width: 100%; margin-top: 10px;"></audio>'
                st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Lỗi tạo âm thanh: {e}")

# 📜 "Học đi đôi với hành, kiến thức khai sáng tương lai." - Hiển thị dòng lịch sử bài làm bám sát cấu trúc trực quan.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            play_audio_safely(message["content"])

# 🚀 "Đường tuy ngắn không đi không đến, việc tuy nhỏ không làm không nên." - Cổng truyền luồng byte trực tiếp hỏa tốc.
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
            st.session_state.messages.append({"role": "user", "content": "🎤 [Thầy cô đã nộp bài thi nói bằng giọng âm trực tiếp]"})
            
            # 🛠️ CÔNG NGHỆ INLINE_DATA: Truyền trực tiếp luồng dữ liệu byte gốc từ Chrome giúp Gemini bóc băng chữ viết chuẩn xác
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
            with st.spinner("Hệ thống đang giải phẫu cấu trúc câu chi tiết..."):
                response = model.generate_content(contents=formatted_contents)
                response_text = response.text
                st.markdown(response_text)
                play_audio_safely(response_text)
                
    except Exception as e:
        st.error(f"❌ Hệ thống thông báo lỗi đường truyền: {e}. Vui lòng nhấn F5 để làm mới phòng thi.")
        return

    # 🛠️ KIỂM SOÁT THOÁT KHỐI: Đưa lệnh ghi bộ nhớ ra ngoài biên để bẻ gãy hoàn toàn lỗi đơ, lỗi quay vòng vòng.
    if response_text:
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()

# 🧭 Kích hoạt luồng điều hướng câu hỏi hành chính.
if nav_action:
    send_exam_data(nav_action, is_nav=True)

# 🚀 Nộp bài thi nói: Ép hiển thị text nghe được đầu tiên, sau đó băm 3 dòng interlinear bài làm.
if audio_data is not None:
    if st.sidebar.button("🚀 NỘP BÀI THI NÓI", use_container_width=True):
        send_exam_data(
            "Đây là dữ liệu giọng nói của tôi. Nhiệm vụ của bạn: 1. Hãy bóc băng chuyển đổi âm thanh này thành chữ viết tiếng Anh chính xác hiển thị ngay dưới mục [🗣️ TEXT ĐÃ NGHE ĐƯỢC TỪ MICROPHONE]. 2. Áp dụng cấu trúc 3 dòng Interlinear (ENG -> IPA -> VIE) cho đoạn văn bản đó. 3. Tiến hành giải phẫu ngữ pháp chi tiết.", 
            audio_file=audio_data
        )

# 📝 "Nét chữ nết người, trí tuệ tỏa sáng." - Khung nhận câu trả lời (Gõ số nhanh 1, 2, 3, 4 hoặc dán đáp án trắc nghiệm/bài viết).
if text_input := st.chat_input("Nhập phím số phần thi (1, 2, 3, 4), đáp án trắc nghiệm hoặc bài viết tại đây..."):  
    if text_input.strip() in ["1", "2", "3", "4"]:
        send_exam_data(text_input.strip(), is_nav=True)
    else:
        send_exam_data(f"Tôi chọn đáp án/nộp bài viết là: {text_input}. Hãy kiểm tra tính chính xác, hiển thị lời giải thích cú pháp chi tiết và áp dụng bố cục thiết kế 3 dòng interlinear.")
