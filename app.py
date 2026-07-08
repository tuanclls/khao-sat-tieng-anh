import streamlit as st
from gtts import gTTS
import io
import time

# 1. Cấu hình giao diện phẳng quy chuẩn phòng thi
st.set_page_config(
    page_title="Hệ Thống Khảo Sát Năng Lực Tiếng Anh VSTEP Giáo Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Kho dữ liệu VSTEP cốt lõi trải phẳng 100% chữ nghĩa - Không viết tắt, không dấu ba chấm
VSTEP_DATABASE = {
    "Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Questions 1-8 (Short Announcement)",
                "correct": "D",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 1. How many languages are officially taught at Hanoi International Language School?<br><small><font color='#4B5563'>🎵 IPA: /haʊ ˈmɛni ˈlæŋɡwɪdʒɪz ɑːr əˈfɪʃəli tɔːt æt hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Câu 1: Có bao nhiêu ngôn ngữ được giảng dạy chính thức tại Trường Ngôn ngữ Quốc tế Hà Nội?</font></i>""",
                "options_html": {
                    "A": """<b><font color='#1E3A8A'>ENG:</font></b> A. Only one primary language is taught here.<br><small><font color='#4B5563'>🎵 IPA: /ˈoʊnli wʌn ˈpraɪmɛri ˈlæŋɡwɪdʒ ɪz tɔːt hɪər/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Chỉ có một ngôn ngữ chính được giảng dạy ở đây.</font></i>""",
                    "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. There are two languages available for students.<br><small><font color='#4B5563'>🎵 IPA: /ðɛr ɑːr tuː ˈlæŋɡwɪdʒɪz əˈveɪləbəl fɔːr ˈstuːdənts/</font></small><br><i><font color='#059669">🇻🇳 VIE: Phương án B: Có hai ngôn ngữ sẵn có dành cho các học viên.</font></i>""",
                    "C": """<b><font color='#1E3A8A'>ENG:</font></b> C. The school offers exactly three distinct languages.<br><small><font color='#4B5563'>🎵 IPA: /ðə skuːl ˈɔːfərz ɪɡˈzæktli θriː dɪˈstɪŋkt ˈlæŋɡwɪdʒɪz/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án C: Trường cung cấp chính xác ba ngôn ngữ riêng biệt.</font></i>""",
                    "D": """<b><font color='#1E3A8A'>ENG:</font></b> D. A total of four languages are provided this term.<br><small><font color='#4B5563'>🎵 IPA: /ə ˈtoʊtəl ɒv fɔːr ˈlæŋɡwɪdʒɪz ɑːr prəˈvaɪdɪd ðɪs tɜːrm/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án D: Tổng cộng có bốn ngôn ngữ được cung cấp trong học kỳ này.</font></i>"""
                },
                "raw_script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.",
                "script_html": """<b><font color='#1E3A8A'>ENG:</font></b> Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.<br><small><font color='#4B5563'>🎵 IPA: /ˈwɛlkəm tuː hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl. ðɪs sɪˈmɛstər, ˈaʊər ˌɪnstɪˈtuːʃən ɪz praʊd tuː ˈɔːfər əˈfɪʃəl ˌsɜːtɪfɪˈkeɪʃən ˈkɔːrsɪz ɪn fɔːr dɪˈstɪŋkt ˈlæŋɡwɪdʒɪz: ˈɪŋŋɡlɪʃ, frɛntʃ, ˌdʒæpəˈniːz, ənd kəˈriːən./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Chào mừng đến với Trường Ngôn ngữ Quốc tế Hà Nội. Học kỳ này, cơ sở của chúng tôi tự hào cung cấp các khóa học chứng chỉ chính thức bằng bốn ngôn ngữ riêng biệt: Tiếng Anh, Tiếng Pháp, Tiếng Nhật và Tiếng Hàn.</font></i>"""
            },
            {
                "id": 2,
                "type": "Part 1: Questions 1-8 (Airport Announcement)",
                "correct": "B",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 2. What is the updated boarding time of Flight VN178 to Ho Chi Minh City?<br><small><font color='#4B5563'>🎵 IPA: /wɒt ɪz ðə ˈʌpdeɪtɪd ˈbɔːrdɪŋ taɪm ɒv flaɪt viː ɛn wʌn ˈsɛvən eɪt tuː hoʊ tʃiː mɪn ˈsɪti/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Câu 2: Giờ lên máy bay được cập nhật mới của Chuyến bay VN178 đi Thành phố Hồ Chí Minh là mấy giờ?</font></i>""",
                "options_html": {
                    "A": """<b><font color='#1E3A8A'>ENG:</font></b> A. The plane will take off at exactly three thirty.<br><small><font color='#4B5563'>🎵 IPA: /ðə pleɪn wɪl teɪk ɒf æt ɪɡˈzæktli θriː ˈθɜːrti/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Máy bay sẽ cất cánh vào lúc chính xác ba giờ ba mươi phút.</font></i>""",
                    "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. The new adjusted schedule is set for three forty-five.<br><small><font color='#4B5563'>🎵 IPA: /ðə nuː əˈdʒʌstɪd ˈskɛdʒuːl ɪz sɛt fɔːr θriː fɔːrti-faɪv/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Lịch trình điều chỉnh mới được ấn định vào lúc ba giờ bốn mươi lăm phút.</font></i>""",
                    "C": """<b><font color='#1E3A8A'>ENG:</font></b> C. Boarding process will officially begin at four fifteen.<br><small><font color='#4B5563'>🎵 IPA: /ˈbɔːrdɪŋ ˈproʊsɛs wɪl əˈfɪʃəli bɪˈɡɪn æt fɔːr fɪfˈtiːn/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án C: Quy trình lên máy bay sẽ chính thức bắt đầu lúc bốn giờ mười lăm phút.</font></i>""",
                    "D": """<b><font color='#1E3A8A'>ENG:</font></b> D. Passengers must enter the gate at four forty-five.<br><small><font color='#4B5563'>🎵 IPA: /ˈpæsəndʒərz mʌst ˈɛntər ðə ɡeɪt æt fɔːr fɔːrti-faɪv/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án D: Hành khách phải đi vào cửa khởi hành lúc bốn giờ bốn mươi lăm phút.</font></i>"""
                },
                "raw_script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.",
                "script_html": """<b><font color='#1E3A8A'>ENG:</font></b> Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.<br><small><font color='#4B5563'>🎵 IPA: /əˈtɛnʃən ɔːl ˈpæsəndʒərz ˈtrævəlɪŋ ɒn flaɪt viː ɛn wʌn ˈsɛvən eɪt tuː hoʊ tʃiː mɪn ˈsɪti./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Xin chú ý tất cả hành khách đi trên Chuyến bay VN178 đến Thành phố Hồ Chí Minh. Do máy bay đến muộn, giờ lên máy bay đã được thay đổi từ 3:30 sang 3:45.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "PASSAGE 1 - Urban Transportation Dynamics",
                "correct": "C",
                "raw_passage": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger.",
                "passage_html": """<b><font color='#1E3A8A'>ENG:</font></b> Context: My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger.<br><small><font color='#4B5563'>🎵 IPA: /maɪ deɪ ˈtɪpɪkli stɑːrts wɪð ə ˈbɪznəs ˈpɜːrsən ˈɡoʊɪŋ tuː ðə ˈɛrˌpɔːrt, ənd ˈnɪrli ˈɔːlweɪz ɛndz wɪð ə drʌŋk ˈpæsəndʒər./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Ngữ cảnh: Ngày của tôi thường bắt đầu với một doanh nhân đi ra sân bay, và gần như luôn kết thúc với một hành khách say xỉn.</font></i>""",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 1: What best paraphrases the routine sequence of the driver's working day?<br><small><font color='#4B5563'>🎵 IPA: /wɒt bɛst ˈpærəfreɪzɪz ðə ruːˈtiːn ˈsiːkwəns ɒv ðə ˈdraɪvərz ˈwɜːrkɪŋ deɪ/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Câu hỏi 1: Ý nào diễn đạt lại chính xác nhất trình tự lộ trình ngày làm việc thông thường của tài xế?</font></i>""",
                "options_html": {
                    "A": """<b><font color='#1E3A8A'>ENG:</font></b> A. The driver drives to the airport to drink with businessmen in the morning.<br><small><font color='#4B5563'>🎵 IPA: /ðə ˈdraɪvər draɪvz tuː ðə ˈɛrˌpɔːrt tuː drɪŋk wɪð ˈbɪznəsmɪn ɪn ðə ˈmɔːrnɪŋ/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Tài xế lái xe ra sân bay để uống rượu cùng các doanh nhân vào buổi sáng.</font></i>""",
                    "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. The routine consists entirely of driving wealthy international airport delegates.<br><small><font color='#4B5563'>🎵 IPA: /ðə ruːˈtiːn kənˈsɪsts ɪnˈtaɪərli ɒv ˈdraɪvɪŋ ˈwɛlθi ˌɪntəˈnæʃənəl ˈɛrˌpɔːrt ˈdɛlɪɡəts/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Lịch trình bao gồm hoàn toàn việc lái xe chở các đại biểu sân bay quốc tế giàu có.</font></i>""",
                    "C": """<b><font color='#1E3A8A'>ENG:</font></b> C. Normally, the first passenger will be a corporate worker and the final one a drunk person.<br><small><font color='#4B5563'>🎵 IPA: /ˈnɔːrməli, ðə fɜːrst ˈpæsəndʒər wɪl biː ə ˈkɔːrpərət ˈwɜːrkər ənd ðə ˈfaɪnəl wʌn ə drʌŋk ˈpɜːrsən/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên sẽ là một nhân viên doanh nghiệp và người cuối cùng là một người say xỉn.</font></i>""",
                    "D": """<b><font color='#1E3A8A'>ENG:</font></b> D. The daily schedule concludes before any intoxicated individuals enter the vehicle.<br><small><font color='#4B5563'>🎵 IPA: /ðə ˈdeɪli ˈskɛdʒuːl kənˈkluːdz bɪˈfɔːr ˈɛni ɪnˈtɒksɪkeɪtɪd ˌɪndɪˈvɪdʒuəlz ˈɛntər ðə ˈviːɪkəl/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án D: Lịch trình hàng ngày kết thúc trước khi có bất kỳ cá nhân say xỉn nào bước vào xe.</font></i>"""
                }
            },
            {
                "id": 2,
                "type": "PASSAGE 2 - Judicial Psychology",
                "correct": "B",
                "raw_passage": "Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.",
                "passage_html": """<b><font color='#1E3A8A'>ENG:</font></b> Context: Behind closed doors most judges, even very experienced ones, are much more anxious about their work than most people might think.<br><small><font color='#4B5563'>🎵 IPA: /bɪˈhaɪnd kloʊzd dɔːrz moʊst ˈdʒʌdʒɪz, ˈiːvən ˈvɛri ɪkˈspɪəriənst wʌnz, ɑːr mʌtʃ mɔːr ˈæŋkʃəs əˈbaʊt ðɛr wɜːrk ðæn moʊst ˈpiːpəl maɪt θɪŋk./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Ngữ cảnh: Đằng sau những cánh cửa đóng kín, hầu hết các thẩm phán, ngay cả những người rất giàu kinh nghiệm, đều lo lắng về công việc của họ nhiều hơn mọi người nghĩ.</font></i>""",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 2: How do judges actually feel inside about their professional judicial workloads?<br><small><font color='#4B5563'>🎵 IPA: /haʊ duː ˈdʒʌdʒɪz ˈæktʃuəli fiːl ɪnˈsaɪd əˈbaʊt ðɛr prəˈfɛʃənəl dʒuːˈdɪʃəl ˈwɜːrkloʊdz/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Câu hỏi 2: Các thẩm phán thực sự cảm thấy thế nào bên trong nội tâm về khối lượng công việc xét xử chuyên nghiệp của họ?</font></i>""",
                "options_html": {
                    "A": """<b><font color='#1E3A8A'>ENG:</font></b> A. They feel entirely confident and completely relaxed all the time.<br><small><font color='#4B5563'>🎵 IPA: /ðeɪ fiːl ɪnˈtaɪərli ˈkɒnfɪdənt ənd kəmˈpliːtli rɪˈlækst ɔːl ðə taɪm/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Họ luôn cảm thấy hoàn toàn tự tin và thư giãn mọi lúc mọi nơi.</font></i>""",
                    "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. They are significantly more anxious and worried than public perception indicates.<br><small><font color='#4B5563'>🎵 IPA: /ðeɪ ɑːr sɪɡˈnɪfɪkəntli mɔːr ˈæŋkʃəs ənd ˈwʌrid ðæn ˈpʌblɪk pərˈsɛpʃən ˈɪndɪkeɪts/</font></small><br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Họ lo lắng và băn khoăn nhiều hơn đáng kể so với những gì công chúng nhận định.</font></i>"""
                }
            }
        ]
    }
}

# 3. Phân hệ tự luận học thuộc lòng tĩnh tích hợp sơ đồ tư duy phân rã câu cho người mất gốc
VSTEP_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"] = [
    {
        "id": 1,
        "type": "TASK 1 - Informal Email (Time allowance: 20 minutes)",
        "prompt_html": """<b><font color='#1E3A8A'>ENG:</font></b> TASK 1: You received an email from your English friend, Jane. She asked you for some information about one of your friends, An, who is going to take a course in London this summer. Tell her about An's personality, hobbies, and study status.<br><small><font color='#4B5563'>🎵 IPA: /raɪt ən ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn./</font></small><br><i><font color='#059669'>🇻🇳 VIE: ĐỀ BÀI TASK 1: Bạn nhận được email từ Jane hỏi thông tin về bạn của bạn tên là An. Hãy viết email trả lời kể về tính cách, sở thích và tình trạng học tập của An.</font></i>""",
        "model_answer_raw": "Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.",
        "model_answer_html": """<b><font color='#1E3A8A'>ENG:</font></b> Model Answer: Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.<br><small><font color='#4B5563'>🎵 IPA: /dɪər dʒeɪn, æn ɪz ən ɪkˈsɛpʃənəli ˈfrɛndli ˈpɜːrsən. ʃiː lʌvz ˈriːdɪŋ bʊks. ˈkʌrəntli, ʃiː ɪz ˈstʌdiɪŋ hɑːrd æt ˌjuːnɪˈvɜːrsəti./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Bài viết mẫu học thuộc: Jane thân mến, An là một người cực kỳ thân thiện. Cô ấy thích đọc sách. Hiện tại, cô ấy đang học tập chăm chỉ ở trường đại học.</font></i>""",
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
• <b>Chia Thì:</b> Thì Hiện tại đơn diễn tả thực tế tính cách hiện tại. Chủ ngữ số ít đi với động từ To-be <b>"is"</b>.<br><br>

<b>📌 CÂU 2: "She loves reading books."</b><br>
• Cấu trúc đặt câu:<br>
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
Chủ ngữ (S): She (Đại từ nhân xưng thay thế cho An)
├── Động từ chỉ sở thích (V): loves (Động từ thường hành động)
└── Tân ngữ trực tiếp (O): reading books (Danh động từ V-ing làm nhiệm vụ danh từ)
</pre>
• <b>Chia Thì:</b> Thì Hiện tại đơn nêu lên sở thích lâu dài. Vì chủ ngữ là "She" (số ít), động từ "love" thêm đuôi "s" thành <b>"loves"</b>. Sau động từ yêu thích (love/like), động từ sau dạng <b>V-ing (reading)</b>.<br><br>

<b>📌 CÂU 3: "Currently, she is studying hard at university."</b><br>
• Cấu trúc đặt câu:<br>
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
Trạng ngữ thời gian: Currently (Hành động diễn ra lúc nói)
├── Chủ ngữ (S): she 
├── Trợ động từ To-be: is
├── Động từ hành động chính (V-ing): studying 
├── Trạng từ cách thức (Adv): hard -> Đứng sau động từ thường để bổ nghĩa cách học
└── Trạng ngữ nơi chốn: at university (Giới từ + Danh từ)
</pre>
• <b>Chia Thì:</b> Dùng <b>Thì Hiện tại tiếp diễn (Present Progressive)</b> vì có trạng từ nhận biết <b>"Currently" (Hiện tại)</b>, diễn tả hành động đang xảy ra chưa chấm dứt. Cấu trúc: S + am/is/are + V-ing -> <b>"is studying"</b>."""
    }
]

VSTEP_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"] = [
    {
        "id": 1,
        "type": "Part 1: Social Interaction (Free Time)",
        "prompt_html": """<b><font color='#1E3A8A'>ENG:</font></b> Part 1: What do you often do in your free time? Do you prefer reading books or watching TV?<br><small><font color='#4B5563'>🎵 IPA: /wɒt duː juː ˈɒfən duː ɪn jɔːr friː taɪm/</font></small><br><i><font color='#059669'>🇻🇳 VIE: ĐỀ BÀI NÓI PHẦN 1: Bạn thường làm gì vào thời gian rảnh? Bạn thích đọc sách hay xem TV hơn?</font></i>""",
        "model_answer_raw": "In my free time, I prefer reading books because books widen my knowledge.",
        "model_answer_html": """<b><font color='#1E3A8A'>ENG:</font></b> Speaking Response: In my free time, I prefer reading books because books widen my knowledge.<br><small><font color='#4B5563'>🎵 IPA: /ɪn maɪ friː taɪm, aɪ prɪˈfɜːr riːdɪŋ bʊks bɪˈkɒz bʊks ˈwaɪdən maɪ ˈnɒlɪdʒ./</font></small><br><i><font color='#059669'>🇻🇳 VIE: Câu trả lời mẫu học thuộc: Vào thời gian rảnh, tôi thích đọc sách hơn vì sách mở rộng kiến thức của tôi.</font></i>""",
        "analysis_html": """### 🧠 SƠ ĐỒ TƯ DUY NGỮ PHÁP PHÂN TÍCH CÂU NÓI PHẢN XẠ
<pre style='background-color: #F8FAFC; padding: 12px; border-left: 4px solid #1E3A8A; border-radius: 4px; font-family: monospace;'>
[Cấu trúc câu ghép nguyên nhân]
├── Trạng ngữ nền: In my free time (Cụm giới từ chỉ thời gian)
├── Mệnh đề kết quả (Chính): I prefer reading books
│   ├── Chủ ngữ (S): I
│   ├── Động từ hành động (V): prefer (Thì hiện tại đơn chỉ xu hướng)
│   └── Tân ngữ (O): reading books (Dạng V-ing sau prefer)
└── Liên từ nối (Conjunction): because (Báo hiệu mệnh đề chỉ nguyên nhân)
    └── Mệnh đề nguyên nhân: books widen my knowledge
        ├── Chủ ngữ số nhiều (S): books
        ├── Động từ thường (V): widen (Để nguyên thể không chia vì danh từ số nhiều)
        └── Tân ngữ sở hữu (O): my knowledge
</pre>
• <b>Chia Thì:</b> Dùng <b>Thì Hiện tại đơn (Present Simple)</b> chỉ xu hướng ổn định. Động từ <b>"widen"</b> giữ nguyên thể do đứng sau chủ ngữ số nhiều <b>"books"</b>."""
    }
]

# 4. Nhân bản đồng bộ đa câu hỏi sang các mã đề B, C, D để tránh lỗi chạm trần chỉ số mảng
for letter in ["B", "C", "D"]:
    name = "Mã đề VSTEP-2026-" + letter + " (Biến Thể Song Song)"
    VSTEP_DATABASE[name] = {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1, "type": "Part 1: Q1", "correct": "A",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> 1. Which sector is discussed today?<br><i><font color='#059669'>🇻🇳 VIE: Câu 1: Ngành công nghiệp nào được thảo luận hôm nay?</font></i>""",
                "options_html": {"A": """<b><font color='#1E3A8A'>ENG:</font></b> A. Ecotourism development.<br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Phát triển du lịch sinh thái.</font></i>""", "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. Heavy chemical manufacturing.<br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Sản xuất hóa chất nặng.</font></i>"""},
                "raw_script": "Today we will focus our attention directly on the ecotourism expansion.",
                "script_html": """<b><font color='#1E3A8A'>ENG:</font></b> Today we will focus our attention directly on the ecotourism expansion.<br><i><font color='#059669'>🇻🇳 VIE: Hôm nay chúng ta sẽ tập trung sự chú ý trực tiếp vào sự phát triển du lịch sinh thái.</font></i>"""
            },
            {
                "id": 2, "type": "Part 1: Q2", "correct": "B",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> 2. What time does the workshop begin?<br><i><font color='#059669'>🇻🇳 VIE: Câu 2: Hội thảo bắt đầu lúc mấy giờ?</font></i>""",
                "options_html": {"A": """<b><font color='#1E3A8A'>ENG:</font></b> A. At 8.00 AM sharp.<br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Vào đúng 8 giờ sáng.</font></i>""", "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. At 9.00 AM sharp.<br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Vào đúng 9 giờ sáng.</font></i>"""},
                "raw_script": "Please note that the specialized training workshop will begin at 9:00 AM sharp.",
                "script_html": """<b><font color='#1E3A8A'>ENG:</font></b> Please note that the specialized training workshop will begin at 9:00 AM sharp.<br><i><font color='#059669'>🇻🇳 VIE: Vui lòng lưu ý rằng hội thảo tập huấn chuyên sâu sẽ bắt đầu vào đúng 9 giờ sáng.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1, "type": "Passage 1: Q1", "correct": "B",
                "raw_passage": "Developing systematic knowledge inside classroom settings requires dedication.",
                "passage_html": """<b><font color='#1E3A8A'>ENG:</font></b> Context: Developing systematic knowledge inside classroom settings requires dedication.<br><i><font color='#059669'>🇻🇳 VIE: Ngữ cảnh: Việc phát triển kiến thức có hệ thống trong môi trường lớp học đòi hỏi sự cống hiến.</font></i>""",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 1: What does developing knowledge require?<br><i><font color='#059669'>🇻🇳 VIE: Câu hỏi 1: Việc phát triển kiến thức đòi hỏi điều gì?</font></i>""",
                "options_html": {"A": """<b><font color='#1E3A8A'>ENG:</font></b> A. Wealth power.<br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Quyền lực tiền bạc.</font></i>""", "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. Dedication attitude.<br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Thái độ cống hiến.</font></i>""}
            },
            {
                "id": 2, "type": "Passage 1: Q2", "correct": "A",
                "raw_passage": "Continuous exposure to natural spoken English improves listening comprehension rapidly.",
                "passage_html": """<b><font color='#1E3A8A'>ENG:</font></b> Context: Continuous exposure to natural spoken English improves listening comprehension rapidly.<br><i><font color='#059669'>🇻🇳 VIE: Ngữ cảnh: Tiếp xúc liên tục với tiếng Anh nói tự nhiên cải thiện khả năng nghe hiểu nhanh chóng.</font></i>""",
                "question_html": """<b><font color='#1E3A8A'>ENG:</font></b> Question 2: What accelerates listening comprehension?<br><i><font color='#059669'>🇻🇳 VIE: Câu hỏi 2: Điều gì đẩy nhanh khả năng nghe hiểu?</font></i>""",
                "options_html": {"A": """<b><font color='#1E3A8A'>ENG:</font></b> A. Continuous exposure.<br><i><font color='#059669'>🇻🇳 VIE: Phương án A: Sự tiếp xúc liên tục.</font></i>""", "B": """<b><font color='#1E3A8A'>ENG:</font></b> B. Rule memorizing.<br><i><font color='#059669'>🇻🇳 VIE: Phương án B: Việc ghi nhớ quy tắc.</font></i>""}
            }
        ],
        "3️⃣ VSTEP Viết": VSTEP_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"],
        "4️⃣ VSTEP Nói": VSTEP_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"]
    }

DE_LIST_KEYS = list(VSTEP_DATABASE.keys())

# 5. Khởi tạo trạng thái vòng đời dữ liệu
if "selected_de" not in st.session_state: st.session_state.selected_de = DE_LIST_KEYS[0]
if "current_section" not in st.session_state: st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state: st.session_state.current_q_idx = 0
if "score" not in st.session_state: st.session_state.score = 0
if "submitted_state" not in st.session_state: st.session_state.submitted_state = {}

# --- SIDEBAR THANH SƯỜN ĐIỀU HÀNH PHẲNG ---
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx, key="sb_de_final_fixed")
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True, key="btn_n_final"):
    st.session_state.current_section = "1️⃣ VSTEP Nghe"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True, key="btn_d_final"):
    st.session_state.current_section = "2️⃣ VSTEP Đọc"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True, key="btn_v_final"):
    st.session_state.current_section = "3️⃣ VSTEP Viết"; st.session_state.current_q_idx = 0; st.rerun()
if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True, key="btn_no_final"):
    st.session_state.current_section = "4️⃣ VSTEP Nói"; st.session_state.current_q_idx = 0; st.rerun()

questions_list = VSTEP_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

# TRIỆT TIÊU LỖI ĐƠ PHÍM: Đưa nút chuyển câu ra độc lập bên ngoài thanh sườn, không lồng cột phức tạp
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")

if st.sidebar.button("⏮️ CÂU TRƯỚC", use_container_width=True, key="nav_prev_sidebar_fixed"):
    if st.session_state.current_q_idx > 0:
        st.session_state.current_q_idx -= 1
        st.rerun()

if st.sidebar.button("⏭️ CÂU TIẾP", use_container_width=True, key="nav_next_sidebar_fixed"):
    if st.session_state.current_q_idx < max_questions - 1:
        st.session_state.current_q_idx += 1
        st.rerun()

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_fixed_{i}", use_container_width=True):
                st.session_state.current_q_idx = i; st.rerun()

# --- KHÔNG GIAN WORKSPACE CHÍNH DIỆN ---
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Hạ tầng sửa đổi an toàn tuyệt đối | Đang chạy mã đề: {st.session_state.selected_de}")
st.markdown("---")

current_de_pos = DE_LIST_KEYS.index(st.session_state.selected_de)
if current_de_pos < len(DE_LIST_KEYS) - 1:
    if st.button("🎉 THÀNH THẠO ĐỀ NÀY RỒI ── BẤM ĐỂ CHUYỂN SANG MÃ ĐỀ TIẾP THEO MỨC ĐỘ TIẾP THEO 🚀", use_container_width=True, key="btn_next_level_de_fixed"):
        st.session_state.selected_de = DE_LIST_KEYS[current_de_pos + 1]
        st.session_state.current_q_idx = 0
        st.rerun()

st.markdown("---")

# THANH TRẠNG THÁI TIẾN ĐỘ THÔNG MINH
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
elapsed = time.time() - st.session_state.start_time
remaining = max(60 * 60 - elapsed, 0)
mins, secs = divmod(int(remaining), 60)

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.markdown(f"**📊 Phân hệ hiện tại: {st.session_state.current_section}**")
    if max_questions > 0:
        st.progress((st.session_state.current_q_idx + 1) / max_questions)
with stat_col2:
    st.metric(label="💯 Điểm Tích Lũy", value=f"{st.session_state.score} Điểm")
with stat_col3:
    st.metric(label="⏳ Đồng Hồ Đếm Ngược", value=f"{mins:02d}:{secs:02d} Phút")

st.markdown("---")

if max_questions == 0:
    st.info("Hệ thống đang đồng bộ cơ sở dữ liệu...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
    is_submitted = q_key in st.session_state.submitted_state

    # A. Phân hệ hiển thị tự luận tĩnh (Viết & Nói)
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
        # B. Phân hệ hiển thị trắc nghiệm đa câu hỏi (Nghe & Đọc)
        if st.session_state.current_section == "1️⃣ VSTEP Nghe":
            st.info("🎧 **Nội dung nghe ghi âm mẫu chuyên nghiệp (Bấm Play để luyện tai):**")
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
                if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {key}", key=f"btn_card_{key}_{q_key}_final_fixed", use_container_width=True):
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
