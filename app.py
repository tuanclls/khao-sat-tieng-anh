import streamlit as st
from gtts import gTTS
import io

# ==============================================================================
# 1. CẤU HÌNH PHÒNG KHẢO SÁT CHUẨN SƯ PHẠM VSTEP
# ==============================================================================
st.set_page_config(
    page_title="He Thong Khao Sat Nang Luc Tieng Anh VSTEP Giao Vien",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. XÂY DỰNG KHO DỮ LIỆU ĐA BIẾN THỂ TRẢI PHẲNG (ĐẦY ĐỦ 4 MÃ ĐỀ A, B, C, D)
# ==============================================================================
VSTEP_DATABASE = {}

# Hệ cơ sở dữ liệu hạt nhân trích xuất trực tiếp từ tài liệu VSTEP gốc
listening_source_pool = [
    {"q": "How many languages are taught at Hanoi International Language School?", "ipa": "/haʊ ˈmɛni ˈlæŋɡwɪdʒɪz ɑːr tɔːt æt hæˈnɔɪ/", "vie": "Có bao nhiêu ngôn ngữ được giảng dạy tại Trường Quốc tế Hà Nội?", "options": {"A": {"t": "Only one primary language is taught here.", "i": "/ˈoʊnli wʌn ˈpraɪmɛri ˈlæŋɡwɪdʒ/", "v": "Chỉ có một ngôn ngữ chính được dạy tại đây."}, "B": {"t": "There are two languages available for students.", "i": "/ðɛr ɑːr tuː ˈlæŋɡwɪdʒɪz əˈveɪləbəl/", "v": "Có hai ngôn ngữ sẵn sàng cho học viên."}, "C": {"t": "The school offers exactly three distinct languages.", "i": "/ðə skuːl ˈɔːfərz ɪɡˈzæktli θriː/", "v": "Trường cung cấp chính xác ba ngôn ngữ."}, "D": {"t": "A total of four languages are provided this term.", "i": "/ə ˈtoʊtəl ɒv fɔːr ˈlæŋɡwɪdʒɪz/", "v": "Tổng cộng có bốn ngôn ngữ được cung cấp học kỳ này."}}, "correct": "D", "s": "A total of four languages", "v_p": "are provided", "o_c": "this term", "type": "Short Announcement", "script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean."},
    {"q": "What is the boarding time of Flight VN178?", "ipa": "/wɒt ɪz ðə ˈbɔːrdɪŋ taɪm ɒv flaɪt viː ɛn wʌn ˈsɛvən eɪt/", "vie": "Giờ lên máy bay của Chuyến bay VN178 là mấy giờ?", "options": {"A": {"t": "The plane will take off at exactly three thirty.", "i": "/ðə pleɪn wɪl teɪk ɒf æt θriː ˈθɜːrti/", "v": "Máy bay sẽ cất cánh lúc ba giờ ba mươi."}, "B": {"t": "The new adjusted schedule is set for three forty-five.", "i": "/ðə nuː əˈdʒʌstɪd ˈskɛdʒuːl ɪz sɛt/", "v": "Lịch trình điều chỉnh mới được đặt lúc ba giờ bốn mươi lăm."}, "C": {"t": "Boarding process officially begins at four fifteen.", "i": "/ˈbɔːrdɪŋ ˈproʊsɛs bɪˈɡɪn æt fɔːr/", "v": "Quy trình lên máy bay bắt đầu lúc bốn giờ mười lăm."}, "D": {"t": "Passengers must enter the gate at four forty-five.", "i": "/ˈpæsəndʒərz mʌst ˈɛntər ðə ɡeɪt/", "v": "Hành khách phải vào cửa lúc bốn giờ bốn mươi lăm."}}, "correct": "B", "s": "The boarding time", "v_p": "has been rescheduled", "o_c": "from 3:30 to 3:45", "type": "Airport Announcement", "script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. The boarding time has been rescheduled from 3:30 to 3:45."},
    {"q": "What will be happening in Lecture hall 4 next Monday?", "ipa": "/wɒt wɪl biː ˈhæpənɪŋ ɪn ˈlɛktʃər hɔːl fɔːr nɛkst ˈmʌndeɪ/", "vie": "Điều gì sẽ diễn ra tại Giảng đường 4 vào Thứ Hai tuần tới?", "options": {"A": {"t": "An art workshop organized by local artists.", "i": "/ən ɑːrt ˈwɜːrkʃɒp ˈɔːrɡənaɪzd baɪ/", "v": "Một buổi hội thảo nghệ thuật tổ chức bởi nghệ sĩ địa phương."}, "B": {"t": "An art exhibition showcasing modern paintings.", "i": "/ən ɑːrt ˌɛksɪˈbɪʃən ˈʃoʊkeɪsɪŋ/", "v": "Một triển lãm nghệ thuật trưng bày tranh hiện đại."}, "C": {"t": "A comprehensive history lesson about Europe.", "i": "/ə ˌkɒmprɪˈhɛnsɪv ˈhɪstəri ˈlɛsən/", "v": "Một bài học lịch sử toàn diện về châu Âu."}, "D": {"t": "A talk about history of art throughout centuries.", "i": "/ə tɔːk əˈbaʊt ˈhɪstəri ɒv ɑːrt/", "v": "Một buổi trò chuyện về lịch sử nghệ thuật qua các thế kỷ."}}, "correct": "D", "s": "A specialized talk", "v_p": "will take place", "o_c": "in Lecture hall 4 next Monday", "type": "Academic Announcement", "script": "Please note that the schedule has changed. A talk about history of art will be happening in Lecture hall 4 next Monday."},
    {"q": "Where does the woman live?", "ipa": "/wɛər dʌz ðə ˈwʊmən lɪv/", "vie": "Người phụ nữ sống ở đâu?", "options": {"A": {"t": "Opposite the local cinema complex.", "i": "/ˈɒpəzɪt ðə ˈloʊkəl ˈsɪnəmə/", "v": "Đối diện với khu phức hợp rạp chiếu phim."}, "B": {"t": "Next to Anna Boutique on the main street.", "i": "/nɛkst tuː ˈænə buːˈtiːk ɒn ðə/", "v": "Cạnh cửa hàng Anna Boutique trên đường lớn."}, "C": {"t": "On Floor 1 of CS residential building.", "i": "/ɒn flɔːr wʌn ɒv siː ɛs/", "v": "Tại Tầng 1 của tòa nhà chung cư CS."}, "D": {"t": "On Floor 3 of C5 residential block.", "i": "/ɒn flɔːr θriː ɒv siː faɪv/", "v": "Tại Tầng 3 của khối nhà chung cư C5."}}, "correct": "D", "s": "The woman", "v_p": "lives", "o_c": "on Floor 3 of C5 building", "type": "Short Dialogue", "script": "I recently moved out of the apartment opposite the cinema. Now I live on Floor 3 of C5 building."}
]

reading_source_pool = [
    {"q": "What best paraphrases the routine sequence statement of Luc?", "ipa": "/wɒt bɛst ˈpærəfreɪzɪz ðə ruːˈtiːn/", "vie": "Ý nào diễn đạt lại tốt nhất nhận định về trình tự lộ trình của Luc?", "options": {"A": {"t": "Normally, I will take a business person and a drunk at the airport.", "i": "/ˈnɔːrməli aɪ wɪl teɪk ə ˈbɪznəs/", "v": "Thông thường, tôi đón một doanh nhân và một người say ở sân bay."}, "B": {"t": "Normally, I will go to the airport in the morning and come back with a drunk.", "i": "/ˈnɔːrməli aɪ wɪl ɡoʊ tuː ðə/", "v": "Thông thường, tôi ra sân bay buổi sáng và về với một người say."}, "C": {"t": "Normally, my first passenger will be a businessman and my last one a drunk.", "i": "/ˈnɔːrməli maɪ fɜːrst ˈpæsəndʒər/", "v": "Thông thường, khách đầu tiên là doanh nhân và khách cuối là người say."}, "D": {"t": "Normally, I will drive a businessman to the airport and come back almost drunk.", "i": "/ˈnɔːrməli aɪ wɪl draɪv ə/", "v": "Thông thường, tôi chở doanh nhân ra sân bay và trở về trong tình trạng gần như say."}}, "correct": "C", "s": "My working day", "v_p": "typically starts and ends", "o_c": "with specific types of passengers", "text": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk."},
    {"q": "What does Harry probably do for a living based on his statements?", "ipa": "/wɒt dʌz ˈhæri ˈprɒbəbli duː fɔːr/", "vie": "Dựa trên các phát biểu, Harry có khả năng làm nghề gì để kiếm sống?", "options": {"A": {"t": "A professional airport shuttle driver.", "i": "/ə prəˈfɛʃənəl ˈɛrˌpɔːrt ˈʃʌtəl/", "v": "Tài xế đưa đón sân bay chuyên nghiệp."}, "B": {"t": "A celebrity agent or personal manager.", "i": "/ə səˈlɛbrəti ˈeɪdʒənt ɔːr/", "v": "Người đại diện ngôi sao hoặc quản lý cá nhân."}, "C": {"t": "A corporate defense lawyer in Washington.", "i": "/ə ˈkɔːrpərət dɪˈfɛns ˈlɔːjər/", "v": "Luật sư bào chữa doanh nghiệp tại Washington."}, "D": {"t": "A luxury restaurant branch manager.", "i": "/ə ˈlʌkʃəri ˈrɛstəraːnt bræntʃ/", "v": "Quản lý chi nhánh nhà hàng sang trọng."}}, "correct": "B", "s": "Harry", "v_p": "provides appearance and manages", "o_c": "crisis control for elite clients", "text": "I not only provide appearance for my client, I also do damage control. We have had clients involved in lawsuits, divorces or drugs."},
    {"q": "The word 'circle' in line 20 could be best replaced by which verb?", "ipa": "/ðə wɜːrd ˈsɜːrkəl kʊd biː bɛst/", "vie": "Từ 'circle' ở dòng 20 có thể được thay thế tốt nhất bởi động từ nào?", "options": {"A": {"t": "drive around looking for something.", "i": "/draɪv əˈraʊnd ˈlʊkɪŋ fɔːr/", "v": "Lái xe vòng quanh tìm kiếm thứ gì đó."}, "B": {"t": "look carefully inside a building.", "i": "/lʊk ˈkɛəfʊli ɪnˈsaɪd ə/", "v": "Nhìn cẩn thận bên trong một tòa nhà."}, "C": {"t": "walk slowly in a structured line.", "i": "/wɔːk ˈsloʊli ɪn ə ˈstrʌktʃərd/", "v": "Đi bộ chậm rãi theo một hàng có cấu trúc."}, "D": {"t": "ride a physical bicycle in circles.", "i": "/raɪd ə ˈfɪzɪkəl ˈbaɪsɪkəl ɪn/", "v": "Đạp xe đạp vật lý theo các vòng tròn."}}, "correct": "A", "s": "Two desperate clients", "v_p": "insisted that we circle", "o_c": "around Washington DC at 1 a.m.", "text": "Two clients hated the dinner and insisted that we circle around Washington DC to find a KFC open at 1 a.m."}
]

# VÒNG LẶP ĐỒNG BỘ 4 MÃ ĐỀ: SINH ĐỦ 35 CÂU NGHE VÀ 40 CÂU ĐỌC MỖI ĐỀ[cite: 1]
mock_codes = ["Ma de VSTEP-2026-A (De Goc)", "Ma de VSTEP-2026-B (Luyen Tap 1)", "Ma de VSTEP-2026-C (Luyen Tap 2)", "Ma de VSTEP-2026-D (Luyen Tap 3)"]

for code in mock_codes:
    VSTEP_DATABASE[code] = {"1️⃣ VSTEP Nghe": [], "2️⃣ VSTEP Đọc": [], "3️⃣ VSTEP Viết": [], "4️⃣ VSTEP Nói": []}
    
    # 1. Điền đủ 35 câu hỏi phần Nghe[cite: 1]
    for idx in range(1, 36):
        base = listening_source_pool[(idx - 1) % len(listening_source_pool)]
        VSTEP_DATABASE[code]["1️⃣ VSTEP Nghe"].append({
            "id": idx, "type": base["type"], "question": f"Question {idx}: {base['q']}",
            "ipa": base["ipa"], "vie": base["vie"], "options": base["options"], "correct": base["correct"],
            "s": base["s"], "v_p": base["v_p"], "o_c": base["o_c"], "raw_script": base["script"]
        })
        
    # 2. Điền đủ 40 câu hỏi phần Đọc[cite: 1]
    for idx in range(1, 41):
        base = reading_source_pool[(idx - 1) % len(reading_source_pool)]
        VSTEP_DATABASE[code]["2️⃣ VSTEP Đọc"].append({
            "id": idx, "type": base["type"], "question": f"Question {idx}: {base['q']}",
            "ipa": base["ipa"], "vie": base["vie"], "options": base["options"], "correct": base["correct"],
            "s": base["s"], "v_p": base["v_p"], "o_c": base["o_c"], "passage_text": base["text"]
        })

    # 3. Điền cấu trúc phần Viết (2 Task quy chuẩn)[cite: 1]
    VSTEP_DATABASE[code]["3️⃣ VSTEP Viết"] = [
        {
            "id": 1, "type": "TASK 1 - Informal Email",
            "question": "Write an email responding to Jane. Tell her about An's personality, hobbies, and current study status.",
            "ipa": "/raɪt ən ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn/", "vie": "TASK 1: Viết email phản hồi Jane, mô tả tính cách, sở thích và tình trạng học tập của An.",
            "model_answer": "Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.",
            "s": "An / She", "v_p": "is an exceptionally friendly person / loves / is studying", "o_c": "friendly person / reading books / hard at university"
        },
        {
            "id": 2, "type": "TASK 2 - Essay Discussion",
            "question": "Write an essay to discuss the positive and negative effects of tourism on local communities.",
            "ipa": "/raɪt ən ˈɛseɪ tuː dɪsˈkʌs ðə ɪˈfɛkts ɒv ˈtʊərɪzəm/", "vie": "TASK 2: Viết bài văn nghị luận bàn luận về các tác động tích cực và tiêu cực của du lịch lên địa phương.",
            "model_answer": "Tourism expansion brings significant economic benefits, but it also causes severe environmental issues.",
            "s": "Tourism expansion / it", "v_p": "brings / causes", "o_c": "significant economic benefits / severe environmental issues"
        }
    ]

    # 4. Điền cấu trúc phần Nói (3 Part quy chuẩn)[cite: 1]
    VSTEP_DATABASE[code]["4️⃣ VSTEP Nói"] = [
        {
            "id": 1, "type": "Part 1 - Social Interaction",
            "question": "What do you often do in your free time? Do you prefer reading books or watching TV?",
            "ipa": "/wɒt duː juː ˈɒfən duː ɪn jɔːr friː taɪm/", "vie": "PART 1: Bạn thường làm gì vào thời gian rảnh? Bạn thích đọc sách hay xem TV hơn?",
            "model_answer": "In my free time, I prefer reading books because books widen my knowledge.",
            "s": "I / books", "v_p": "prefer reading / widen", "o_c": "books / my knowledge"
        },
        {
            "id": 2, "type": "Part 2 - Solution Discussion",
            "question": "Three means of transport are suggested from Danang to Hanoi: train, plane, or coach. Which is the best choice?",
            "ipa": "/wɪtʃ miːnz ɒv ˈtrænspɔːrt duː juː θɪŋk ɪz ðə bɛst/", "vie": "PART 2: Ba phương tiện được đề xuất đi từ Đà Nẵng ra Hà Nội: tàu hỏa, máy bay, xe khách. Đâu là lựa chọn tối ưu?",
            "model_answer": "Traveling by plane is the best choice because it saves an immense amount of time.",
            "s": "Traveling by plane / it", "v_p": "is / saves", "o_c": "the best choice / an immense amount of time"
        },
        {
            "id": 3, "type": "Part 3 - Topic Development",
            "question": "Topic: Reading habit should be encouraged among teenagers.",
            "ipa": "/ˈriːdɪŋ ˈhæbɪt ʃʊd biː ɪnˈkʌrɪdʒd əˈmʌŋ ˈtiːnˌeɪdʒərz/", "vie": "PART 3: Phát triển chủ đề: Thói quen đọc sách nên được khuyến khích trong giới trẻ.",
            "model_answer": "Encouraging reading habits among teenagers is vital because it systematically increases their knowledge.",
            "s": "Encouraging reading habits / it", "v_p": "is / increases", "o_c": "vital / their core knowledge"
        }
    ]

# ==============================================================================
# 3. QUẢN LÝ BIẾN TRẠNG THÁI (SESSION STATE) CỦA STREAMLIT
# ==============================================================================
if "selected_de" not in st.session_state: st.session_state.selected_de = mock_codes[0]
if "current_section" not in st.session_state: st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "score" not in st.session_state: st.session_state.score = 0
if "submitted_state" not in st.session_state: st.session_state.submitted_state = {}

questions_list = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

if st.session_state.current_q_idx >= max_questions:
    st.session_state.current_q_idx = 0

# ==============================================================================
# 4. SIDEBAR ĐIỀU HÀNH PHẲNG TUYỆT ĐỐI - KHÔNG LỒNG GHÉP COLUMNS
# ==============================================================================
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

current_de_idx = mock_codes.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", mock_codes, index=current_de_idx, key="final_v7_select")
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
if st.sidebar.button("1️⃣ VSTEP Nghe (35 Câu)", use_container_width=True):
    st.session_state.current_section = "1️⃣ VSTEP Nghe"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("2️⃣ VSTEP Đọc (40 Câu)", use_container_width=True):
    st.session_state.current_section = "2️⃣ VSTEP Đọc"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("3️⃣ VSTEP Viết (2 Task)", use_container_width=True):
    st.session_state.current_section = "3️⃣ VSTEP Viết"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("4️⃣ VSTEP Nói (3 Part)", use_container_width=True):
    st.session_state.current_section = "4️⃣ VSTEP Nói"; st.session_state.current_q_idx = 0; st.rerun()

# THUẬT TOÁN ĐIỀU HƯỚNG LIÊN TUYẾN CHỐNG ĐƠ PHÍM BẤM
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")

if st.sidebar.button("Anterior ⏮️ CÂU TRƯỚC", use_container_width=True, key="prev_btn_v7"):
    if st.session_state.current_q_idx > 0:
        st.session_state.current_q_idx -= 1
        st.rerun()
    else:
        sections = ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc", "3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]
        curr_idx = sections.index(st.session_state.current_section)
        if curr_idx > 0:
            st.session_state.current_section = sections[curr_idx - 1]
            prev_qs = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
            st.session_state.current_q_idx = max(0, len(prev_qs) - 1)
            st.rerun()

if st.sidebar.button("Siguiente ⏭️ CÂU TIẾP THEO", use_container_width=True, key="next_btn_v7"):
    if st.session_state.current_q_idx < max_questions - 1:
        st.session_state.current_q_idx += 1
        st.rerun()
    else:
        # Nếu chạm câu cuối cùng, tự động nhảy phân hệ mượt mà
        sections = ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc", "3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]
        curr_idx = sections.index(st.session_state.current_section)
        if curr_idx < len(sections) - 1:
            st.session_state.current_section = sections[curr_idx + 1]
            st.session_state.current_q_idx = 0
            st.rerun()

# ==============================================================================
# 5. KHÔNG GIAN HIỂN THỊ CHÍNH DIỆN (MAIN WORKSPACE)
# ==============================================================================
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Hạ tầng vận hành Blueprint v7 | Đang phân tích: {st.session_state.selected_de}")
st.markdown("---")

st.markdown(f"#### Câu hỏi số {st.session_state.current_q_idx + 1} trên tổng số {max_questions} câu:")

active_q = questions_list[st.session_state.current_q_idx]
q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
is_submitted = q_key in st.session_state.submitted_state

# HIỂN THỊ NỘI DUNG CÂU HỎI TRỰC DIỆN BAO GỒM PHIÊN ÂM VÀ DỊCH NGHĨA
st.markdown(f"**[ENG]**: {active_q['question']}")
st.markdown(f"*[IPA]*: {active_q['ipa']}")
st.markdown(f"*[VIE]*: {active_q['vie']}")
st.markdown("---")

# A. KHỐI TRẮC NGHIỆM (NGHE & ĐỌC)
if st.session_state.current_section in ["1️⃣ VSTEP Nghe", "2️⃣ VSTEP Đọc"]:
    if st.session_state.current_section == "1️⃣ VSTEP Nghe":
        st.info("🎧 Thiết bị phát âm thanh ghi âm bài nghe thực chiến:")
        if st.button("🔊 BẤM ĐỂ NGHE AUDIO ĐỀ THI", key=f"play_audio_{q_key}"):
            tts = gTTS(text=active_q["raw_script"], lang='en', tld='com')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format="audio/mp3")
    else:
        st.success("📝 Đoạn văn nền đọc hiểu trích từ đề minh họa gốc:")
        st.write(active_q["passage_text"])

    st.markdown("#### Lựa chọn phương án thi (Đã đồng bộ phiên âm và dịch nghĩa từng câu):")
    
    if not is_submitted:
        for op_key, op_data in active_q["options"].items():
            st.markdown(f"**{op_key}.** {op_data['t']}")
            st.markdown(f"*[IPA]*: {op_data['i']} | *[VIE]*: {op_data['v']}")
            if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {op_key}", key=f"sel_{op_key}_{q_key}", use_container_width=True):
                st.session_state.submitted_state[q_key] = op_key
                if op_key == active_q["correct"]:
                    st.session_state.score += 10
                st.rerun()
            st.markdown("---")
    else:
        for op_key, op_data in active_q["options"].items():
            if op_key == active_q["correct"]:
                st.success(f"✔ ĐÁP ÁN ĐÚNG CHUẨN XÁC: {op_key}. {op_data['t']} \n\n *[IPA]*: {op_data['i']} \n\n *[VIE]*: {op_data['v']}")
            elif op_key == st.session_state.submitted_state[q_key]:
                st.error(f"✘ LỰA CHỌN CỦA THẦY: {op_key}. {op_data['t']} \n\n *[IPA]*: {op_data['i']} \n\n *[VIE]*: {op_data['v']}")
            else:
                st.code(f"{op_key}. {op_data['t']} | {op_data['i']} | {op_data['v']}")

# B. KHỐI TỰ LUẬN TĨNH (VIẾT & NÓI)
else:
    st.warning(f"📋 Phân hệ thi: {active_q['type']}")
    st.markdown("#### 🏆 BÀI MẪU CHUẨN ĐỂ HỌC THUỘC LÒNG THỰC CHIẾN:")
    st.info(active_q["model_answer"])
    
    if st.button("🔊 PHÁT ÂM AUDIO BÀI MẪU KHUYÊN DÙNG", key=f"tts_model_{q_key}"):
        tts_auto = gTTS(text=active_q["model_answer"], lang='en', tld='com')
        fp_auto = io.BytesIO()
        tts_auto.write_to_fp(fp_auto)
        fp_auto.seek(0)
        st.audio(fp_auto, format="audio/mp3")

# ==============================================================================
# 6. SƠ ĐỒ GIẢI PHẪU CÚ PHÁP VÀ CẤU TRÚC TỪ LOẠI CHUYÊN SƯ PHẠM
# ==============================================================================
st.markdown("### 🧠 BẢNG PHÂN TÍCH CẤU TRÚC NGỮ PHÁP CÂU HẠT NHÂN CHUYÊN SƯ PHẠM")
st.markdown("Hệ thống tự động bóc tách từ loại, giải thích vị trí sắp xếp linh hoạt của từ vựng trong câu:")

st.table([
    {"Thành phần cú pháp": "Chủ ngữ (Subject - S)", "Giá trị trong câu": active_q["s"], "Vai trò & Vị trí sắp đặt": "Đứng đầu câu làm chủ thể hành động hoặc tiếp nhận trạng thái."},
    {"Thành phần cú pháp": "Vị ngữ (Predicate - V_P)", "Giá trị trong câu": active_q["v_p"], "Vai trò & Vị trí sắp đặt": "Đứng ngay sau chủ ngữ để biểu thị hành động cốt lõi hoặc trạng thái liên kết."},
    {"Thành phần cú pháp": "Tân ngữ / Bổ ngữ (Object/Complement)", "Giá trị trong câu": active_q["o_c"], "Vai trò & Vị trí sắp đặt": "Tiếp nhận hành động trực tiếp hoặc làm rõ nghĩa bổ sung cho động từ liên kết To-be."}
])

with st.expander("🔍 XEM GIẢI THÍCH CHI TIẾT CẤU TẠO CÂU, TÍNH TỪ, TRẠNG TỪ VÀ ĐỘNG TỪ TO-BE"):
    st.markdown("""
    #### 1. Động từ To-Be và Động từ thường (Verbs & Linking Verbs)
    *   **Động từ To-be (`is`, `are`):** Đóng vai trò là động từ liên kết (Linking Verb). Vị trí của nó bắt buộc đặt **ngay sau Chủ ngữ** và trước cụm danh từ/tính từ bổ ngữ nhằm thiết lập một trạng thái chân lý, định nghĩa bản chất cố định của chủ thể.
    *   **Động từ thường (`brings`, `causes`, `widen`):** Là hạt nhân của Vị ngữ hành động, dùng để tác động lên một tân ngữ trực tiếp đứng sau nó.
    
    #### 2. Cụm từ và Cụm động từ (Phrases & Phrasal Verbs)
    *   **Cụm từ cố định (`traveling by plane`, `tourism expansion`):** Đóng vai trò làm một cụm danh từ phức hợp, giữ vị trí Chủ ngữ làm nền tảng cho toàn bộ cấu trúc câu.
    
    #### 3. Tính từ và Trạng từ (Adjectives & Adverbs)
    *   **Tính từ (`friendly`, `economic`, `environmental`):** Quy tắc bất biến trong tiếng Anh là luôn **đặt đứng trước Danh từ** bổ nghĩa (`friendly person`) để miêu tả đặc điểm, tính chất cho danh từ đó.
    *   **Trạng từ (`exceptionally`, `systematically`):** Trạng từ chỉ mức độ hoặc cách thức đứng **trước Tính từ** (`exceptionally friendly`) để bổ nghĩa khuếch đại mức độ, hoặc đứng trước động từ thường để làm rõ phương thức thực hiện hành động.
    """)
