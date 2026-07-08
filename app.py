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

# KHO DỮ LIỆU ĐỀ THI ĐA BIẾN THỂ VSTEP-2026: TRẢI PHẲNG CHỮ 100% - TUYỆT ĐỐI KHÔNG VIẾT TẮT
VSTEP_MASTER_DATABASE = {
    "Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Questions 1-8 (Short Announcement)",
                "correct": "D",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1. How many languages are officially taught at Hanoi International Language School?<br>
<small><font color="#4B5563">🎵 IPA: /haʊ ˈmɛni ˈlæŋɡwɪdʒɪz ɑːr əˈfɪʃəli tɔːt æt hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu 1: Có bao nhiêu ngôn ngữ được giảng dạy chính thức tại Trường Ngôn ngữ Quốc tế Hà Nội?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Only one primary language is taught here.<br><small><font color="#4B5563">🎵 IPA: /ˈoʊnli wʌn ˈpraɪmɛri ˈlæŋɡwɪdʒ ɪz tɔːt hɪər/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Chỉ có một ngôn ngữ chính được giảng dạy ở đây.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. There are two languages available for students.<br><small><font color="#4B5563">🎵 IPA: /ðɛr ɑːr tuː ˈlæŋɡwɪdʒɪz əˈveɪləbəl fɔːr ˈstuːdənts/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Có hai ngôn ngữ sẵn có dành cho các học viên.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. The school offers exactly three distinct languages.<br><small><font color="#4B5563">🎵 IPA: /ðə skuːl ˈɔːfərz ɪɡˈzæktli θriː dɪˈstɪŋkt ˈlæŋɡwɪdʒɪz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Trường cung cấp chính xác ba ngôn ngữ riêng biệt.</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. A total of four languages are provided this term.<br><small><font color="#4B5563">🎵 IPA: /ə ˈtoʊtəl ɒv fɔːr ˈlæŋɡwɪdʒɪz ɑːr prəˈvaɪdɪd ðɪs tɜːrm/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Tổng cộng có bốn ngôn ngữ được cung cấp trong học kỳ này.</font></i>"""
                },
                "raw_script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.<br>
<small><font color="#4B5563">🎵 IPA: /ˈwɛlkəm tuː hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl. ðɪs sɪˈmɛstər, ˈaʊər ˌɪnstɪˈtuːʃən ɪz praʊd tuː ˈɔːfər əˈfɪʃəl ˌsɜːtɪfɪˈkeɪʃən ˈkɔːrsɪz ɪn fɔːr dɪˈstɪŋkt ˈlæŋɡwɪdʒɪz: ˈɪŋŋɡlɪʃ, frɛntʃ, ˌdʒæpəˈniːz, ənd kəˈriːən./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Chào mừng đến với Trường Ngôn ngữ Quốc tế Hà Nội. Học kỳ này, cơ sở của chúng tôi tự hào cung cấp các khóa học chứng chỉ chính thức bằng bốn ngôn ngữ riêng biệt: Tiếng Anh, Tiếng Pháp, Tiếng Nhật và Tiếng Hàn.</font></i>"""
            },
            {
                "id": 2,
                "type": "Part 1: Questions 1-8 (Airport Announcement)",
                "correct": "B",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 2. What is the updated boarding time of Flight VN178 to Ho Chi Minh City?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt ɪz ðə ˈʌpdeɪtɪd ˈbɔːrdɪŋ taɪm ɒv flaɪt viː ɛn wʌn ˈsɛvən eɪt tuː hoʊ tʃiː mɪn ˈsɪti/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu 2: Giờ lên máy bay được cập nhật mới của Chuyến bay VN178 đi Thành phố Hồ Chí Minh là mấy giờ?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. The plane will take off at exactly three thirty.<br><small><font color="#4B5563">🎵 IPA: /ðə pleɪn wɪl teɪk ɒf æt ɪɡˈzæktli θriː ˈθɜːrti/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Máy bay sẽ cất cánh vào lúc chính xác ba giờ ba mươi phút.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. The new adjusted schedule is set for three forty-five.<br><small><font color="#4B5563">🎵 IPA: /ðə nuː əˈdʒʌstɪd ˈskɛdʒuːl ɪz sɛt fɔːr θriː fɔːrti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Lịch trình điều chỉnh mới được ấn định vào lúc ba giờ bốn mươi lăm phút.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Boarding process will officially begin at four fifteen.<br><small><font color="#4B5563">🎵 IPA: /ˈbɔːrdɪŋ ˈproʊsɛs wɪl əˈfɪʃəli bɪˈɡɪn æt fɔːr fɪfˈtiːn/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Quy trình lên máy bay sẽ chính thức bắt đầu lúc bốn giờ mười lăm phút.</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. Passengers must enter the gate at four forty-five.<br><small><font color="#4B5563">🎵 IPA: /ˈpæsəndʒərz mʌst ˈɛntər ðə ɡeɪt æt fɔːr fɔːrti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Hành khách phải đi vào cửa khởi hành lúc bốn giờ bốn mươi lăm phút.</font></i>"""
                },
                "raw_script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.<br>
<small><font color="#4B5563">🎵 IPA: /əˈtɛnʃən ɔːl ˈpæsəndʒərz ˈtrævəlɪŋ ɒn flaɪt viː ɛn wʌn ˈsɛvən eɪt tuː hoʊ tʃiː mɪn ˈsɪti. duː tuː ðə leɪt əˈraɪvəl ɒv ðə ˈɪnˌkʌmɪŋ ˈɛrkræft.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Xin chú ý tất cả hành khách đi trên Chuyến bay VN178 đến Thành phố Hồ Chí Minh. Do máy bay đến muộn, giờ lên máy bay đã được thay đổi từ 3:30 sang 3:45.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "PASSAGE 1 - Urban Transportation Dynamics",
                "correct": "C",
                "raw_passage": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger. I do not mind drunk people because sometimes they are the better version of themselves.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: My day typically starts with a business person going to the airport, and nearly always ends with a drunk passenger. I do not mind drunk people because sometimes they are the better version of themselves.<br>
<small><font color="#4B5563">🎵 IPA: /maɪ deɪ ˈtɪpɪkli stɑːrts wɪð ə ˈbɪznəs ˈpɜːrsən ˈɡoʊɪŋ tuː ðə ˈɛrˌpɔːrt, ənd ˈnɪrli ˈɔːlweɪz ɛndz wɪð ə drʌŋk ˈpæsəndʒər./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Ngày của tôi thường bắt đầu với một doanh nhân đi ra sân bay, và gần như luôn kết thúc với một hành khách say xỉn. Tôi không phiền những người say vì đôi khi họ là phiên bản tốt hơn của chính mình.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What best paraphrases the routine sequence of the driver's working day?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt bɛst ˈpærəfreɪzɪz ðə ruːˈtiːn ˈsiːkwəns ɒv ðə ˈdraɪvərz ˈwɜːrkɪŋ deɪ/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Ý nào diễn đạt lại chính xác nhất trình tự lộ trình ngày làm việc thông thường của tài xế?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. The driver drives to the airport to drink with businessmen in the morning.<br><small><font color="#4B5563">🎵 IPA: /ðə ˈdraɪvər draɪvz tuː ðə ˈɛrˌpɔːrt tuː drɪŋk wɪð ˈbɪznəsmɪn ɪn ðə ˈmɔːrnɪŋ/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Tài xế lái xe ra sân bay để uống rượu cùng các doanh nhân vào buổi sáng.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. The routine consists entirely of driving wealthy international airport delegates.<br><small><font color="#4B5563">🎵 IPA: /ðə ruːˈtiːn kənˈsɪsts ɪnˈtaɪərli ɒv ˈdraɪvɪŋ ˈwɛlθi ˌɪntəˈnæʃənəl ˈɛrˌpɔːrt ˈdɛlɪɡəts/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Lịch trình bao gồm hoàn toàn việc lái xe chở các đại biểu sân bay quốc tế giàu có.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Normally, the first passenger will be a corporate worker and the final one a drunk person.<br><small><font color="#4B5563">🎵 IPA: /ˈnɔːrməli, ðə fɜːrst ˈpæsəndʒər wɪl biː ə ˈkɔːrpərət ˈwɜːrkər ənd ðə ˈfaɪnəl wʌn ə drʌŋk ˈpɜːrsən/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên sẽ là một nhân viên doanh nghiệp và người cuối cùng là một người say xỉn.</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. The daily schedule concludes before any intoxicated individuals enter the vehicle.<br><small><font color="#4B5563">🎵 IPA: /ðə ˈdeɪli ˈskɛdʒuːl kənˈkluːdz bɪˈfɔːr ˈɛni ɪnˈtɒksɪkeɪtɪd ˌɪndɪˈvɪdʒuəlz ˈɛntər ðə ˈviːɪkəl/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Lịch trình hàng ngày kết thúc trước khi có bất kỳ cá nhân say xỉn nào bước vào xe.</font></i>"""
                }
            }
        ]
    }
}

# CHỒNG HỆ THỐNG TỰ LUẬN TĨNH: PHÂN TÍCH TOÀN DIỆN SƠ ĐỒ NGỮ PHÁP CHO NGƯỜI MẤT GỐC
VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"] = [
    {
        "id": 1,
        "type": "TASK 1 - Informal Email (Time allowance: 20 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> TASK 1: You received an email from your English friend, Jane. She asked you for some information about one of your friends, An, who is going to take a course in London this summer. Tell her about An's personality, hobbies, and study status.<br>
<small><font color="#4B5563">🎵 IPA: /raɪt ən ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI TASK 1: Bạn nhận được email từ Jane hỏi thông tin về bạn của bạn tên là An. Hãy viết email trả lời kể về tính cách, sở thích và tình trạng học tập của An.</font></i>""",
        "model_answer_raw": "Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: Dear Jane, An is an exceptionally friendly person. She loves reading books. Currently, she is studying hard at university.<br>
<small><font color="#4B5563">🎵 IPA: /dɪər dʒeɪn, æn ɪz ən ɪkˈsɛpʃənəli ˈfrɛndli ˈpɜːrsən. ʃiː lʌvz ˈriːdɪŋ bʊks. ˈkʌrəntli, ʃiː ɪz ˈstʌdiɪŋ hɑːrd æt ˌjuːnɪˈvɜːrsəti./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Bài viết mẫu học thuộc: Jane thân mến, An là một người cực kỳ thân thiện. Cô ấy thích đọc sách. Hiện tại, cô ấy đang học tập chăm chỉ ở trường đại học.</font></i>""",
        "analysis_html": """### 🧠 SƠ ĐỒ TƯ DUY NGỮ PHÁP PHÂN TÍCH CÂU (MIND MAP)

#### 📌 CÂU 1: "An is an exceptionally friendly person."
*   **Mô hình cây cấu trúc đặt câu:**
