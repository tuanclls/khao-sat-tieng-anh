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

# KHO DỮ LIỆU ĐỀ THI ĐA BIẾN THỂ VSTEP-2026: ĐỒNG BỘ 4 MÃ ĐỀ (A, B, C, D) ĐẦY ĐỦ ĐÁP ÁN MẪU KHÓA TRƯỚC
VSTEP_MASTER_DATABASE = {
    "Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Questions 1-8 (Short Announcement)",
                "correct": "D",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> 1. How many languages are taught at Hanoi International Language School?<br>
<small><font color="#4B5563">🎵 IPA: /haʊ ˈmɛni ˈlæŋɡwɪdʒɪz ɑːr tɔːt æt hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu 1: Có bao nhiêu ngôn ngữ được giảng dạy tại Trường Ngôn ngữ Quốc tế Hà Nội?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 1<br><small><font color="#4B5563">🎵 IPA: /wʌn/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 1 ngôn ngữ</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 2<br><small><font color="#4B5563">🎵 IPA: /tuː/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 2 ngôn ngữ</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 3<br><small><font color="#4B5563">🎵 IPA: /θriː/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 3 ngôn ngữ</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 4<br><small><font color="#4B5563">🎵 IPA: /fɔːr/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 4 ngôn ngữ</font></i>"""
                },
                "raw_script": "Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Welcome to Hanoi International Language School. This semester, our institution is proud to offer official certification courses in four distinct languages: English, French, Japanese, and Korean.<br>
<small><font color="#4B5563">🎵 IPA: /ˈwɛlkəm tuː hæˈnɔɪ ˌɪntəˈnæʃənəl ˈlæŋɡwɪdʒ skuːl. ðɪs sɪˈmɛstər, ˈaʊər ˌɪnstɪˈtuːʃən ɪz praʊd tuː ˈɔːfər əˈfɪʃəl ˌsɜːtɪfɪˈkeɪʃən ˈkɔːrsɪz ɪn fɔːr dɪˈstɪŋkt ˈlæŋɡwɪdʒɪz: ˈɪŋɡlɪʃ, frɛntʃ, ˌdʒæpəˈniːz, ənd kəˈriːən./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Chào mừng đến với Trường Ngôn ngữ Quốc tế Hà Nội. Học kỳ này, cơ sở của chúng tôi tự hào cung cấp các khóa học chứng chỉ chính thức bằng bốn ngôn ngữ riêng biệt: Tiếng Anh, Tiếng Pháp, Tiếng Nhật và Tiếng Hàn.</font></i>"""
            },
            {
                "id": 2,
                "type": "Part 1: Questions 1-8 (Airport Announcement)",
                "correct": "B",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> 2. What is the boarding time of Flight VN178?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt ɪz ðə ˈbɔːrdɪŋ taɪm ɒv flaɪt viː ɛn wʌn ˈsɛvən eɪt/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu 2: Giờ lên máy bay của Chuyến bay VN178 là mấy giờ?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 3.30<br><small><font color="#4B5563">🎵 IPA: /θriː ˈθɜːti/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 3 giờ 30 phút</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 3.45<br><small><font color="#4B5563">🎵 IPA: /θriː fɔːrˈti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 3 giờ 45 phút</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 4.15<br><small><font color="#4B5563">🎵 IPA: /fɔːr fɪfˈtiːn/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 4 giờ 15 phút</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 4.45<br><small><font color="#4B5563">🎵 IPA: /fɔːr fɔːrˈti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 4 giờ 45 phút</font></i>"""
                },
                "raw_script": "Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Attention all passengers traveling on Flight VN178 to Ho Chi Minh City. Due to the late arrival of the incoming aircraft, the boarding time has been rescheduled from 3:30 to 3:45.<br>
<small><font color="#4B5563">🎵 IPA: /əˈtɛnʃən ɔːl ˈpæsɪndʒərz ˈtrævəlɪŋ ɒn flaɪt viː ɛn wʌn ˈsɛvən eɪt tuː hoʊ tʃiː mɪn ˈsɪti./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Xin chú ý tất cả hành khách đi trên Chuyến bay VN178 đến Thành phố Hồ Chí Minh. Do máy bay đến muộn, giờ lên máy bay đã được thay đổi từ 3:30 sang 3:45.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "PASSAGE 1 - Questions 1-10",
                "correct": "C",
                "raw_passage": "My day typically starts with a business person going to the airport, and nearly always ends with a drunk. I don't mind drunk people. Sometimes I think they're the better version of themselves.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: My day typically starts with a business person going to the airport, and nearly always ends with a drunk. I don't mind drunk people. Sometimes I think they're the better version of themselves.<br>
<small><font color="#4B5563">🎵 IPA: /maɪ deɪ ˈtɪpɪkli stɑːrts wɪð ə ˈbɪznəs ˈpɜːrsən ˈɡoʊɪŋ tuː ðə ˈɛrˌpɔːrt, ənd ˈnɪrli ˈɔːlweɪz ɛndz wɪð ə drʌŋk./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Ngày của tôi thường bắt đầu với một doanh nhân đi ra sân bay, và gần như luôn kết thúc với một người say xỉn. Tôi không phiền những người say. Đôi khi tôi nghĩ họ là phiên bản tốt hơn của chính mình.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What best paraphrases the sentence 'My day typically starts with a business person going to the airport, and nearly always ends with a drunk'?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt bɛst ˈpærəfreɪzɪz ðə ˈsɛntəns?/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Câu nào diễn đạt lại tốt nhất nhận định về lộ trình hàng ngày của nhân vật?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Normally, I will take a business person and a drunk at the airport.<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Thông thường, tôi đón doanh nhân và người say ở sân bay.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Normally, I will go to the airport in the morning and come back with a drunk.<br><small><font color="#4B5563">🎵 IPA: /.../ </font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Thông thường, tôi ra sân bay buổi sáng và về với người say.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Normally, my first passenger will be a businessman and my last one a drunk.<br><small><font color="#4B5563">🎵 IPA: /.../ </font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên là doanh nhân và người cuối cùng là người say.</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. Normally, I will drive a businessman to the airport and come back almost drunk.<br><small><font color="#4B5563">🎵 IPA: /.../ </font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Thông thường, tôi chở doanh nhân ra sân bay và quay về trong tình trạng gần như say.</font></i>"""
                }
            }
        ]
    },
    "Mã đề VSTEP-2026-B (Biến Thể Song Song 1)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Short Announcement",
                "correct": "C",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: How many science labs are available at the New Era Academy?<br>
<small><font color="#4B5563">🎵 IPA: /haʊ ˈmɛni ˈsaɪəns læbz ɑːr əˈveɪləbəl æt ðə nuː ˈɪərə əˈkædəmi/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Có bao nhiêu phòng thí nghiệm khoa học tại Học viện Kỷ nguyên Mới?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 1 lab<br><small><font color="#4B5563">🎵 IPA: /wʌn læb/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 1 phòng</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 2 labs<br><small><font color="#4B5563">🎵 IPA: /tuː læbz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 2 phòng</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 3 labs<br><small><font color="#4B5563">🎵 IPA: /θriː læbz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 3 phòng thí nghiệm</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 5 labs<br><small><font color="#4B5563">🎵 IPA: /faɪv læbz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 5 phòng</font></i>"""
                },
                "raw_script": "Attention students, our New Era Academy has built three fully equipped science labs this term for physics, chemistry, and biology research classes.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Attention students, our New Era Academy has built three fully equipped science labs this term for physics, chemistry, and biology research classes.<br>
<small><font color="#4B5563">🎵 IPA: /əˈtɛnʃən ˈstuːdənts, ˈaʊər nuː ˈɪərə əˈkædəmi hæz bɪlt θriː ˈfʊli ɪˈkwɪpt ˈsaɪəns læbz.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Xin chú ý các học sinh, Học viện Kỷ nguyên Mới của chúng ta đã xây dựng ba phòng thí nghiệm khoa học được trang bị đầy đủ trong học kỳ này cho các lớp nghiên cứu vật lý, hóa học và sinh học.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "Passage 1: Modern Workplaces",
                "correct": "A",
                "raw_passage": "My working shift always starts with a hot coffee, and almost certainly ends with answering infinite unread corporate emails from foreign partners.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: My working shift always starts with a hot coffee, and almost certainly ends with answering infinite unread corporate emails from foreign partners.<br>
<small><font color="#4B5563">🎵 IPA: /maɪ ˈwɜːrkɪŋ ʃɪft ˈɔːlweɪz stɑːrts wɪð ə hɒt ˈkɔːfi.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Ca làm việc của tôi luôn bắt đầu bằng một ly cà phê nóng, và gần như chắc chắn kết thúc bằng việc trả lời vô số email công ty chưa đọc từ các đối tác nước ngoài.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What is the main regular activity at the end of the author's shift?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt ɪz ðə meɪn ˈrɛɡjələr ækˈtɪvəti æt ðə ɛnd ɒv ðə ˈɔːθərz ʃɪft?/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Hoạt động thường xuyên chính vào cuối ca làm việc của tác giả là gì?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Handling email correspondence<br><small><font color="#4B5563">🎵 IPA: /ˈhændlɪŋ ˈiːmeɪl ˌkɒrɪˈspɒndəns/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Xử lý thư từ email công ty</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Drinking hot beverages<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Uống đồ uống nóng</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Meeting international clients<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Gặp gỡ khách hàng quốc tế</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. Leaving the workplace early<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Rời nơi làm việc sớm</font></i>"""
                }
            }
        ]
    },
    "Mã đề VSTEP-2026-C (Biến Thể Song Song 2)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Short Announcement",
                "correct": "B",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: Where should the international students pick up their temporary badges?<br>
<small><font color="#4B5563">🎵 IPA: /wɛr ʃʊd ðə ˌɪntəˈnæʃənəl ˈstuːdənts pɪk ʌp ðɛr ˈtɛmpərəri ˈbædʒɪz/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Sinh viên quốc tế nên nhận thẻ tạm thời của họ ở đâu?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. At the main library entrance<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Tại lối vào thư viện chính</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. At the security desk near Gate A<br><small><font color="#4B5563">🎵 IPA: /æt ðə sɪˈkjʊərəti dɛsk nɪər ɡeɪt eɪ/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Tại bàn an ninh gần Cổng A</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. In the dean's office room<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Trong phòng văn phòng trưởng khoa</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. From their tour guides directly<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Trực tiếp từ hướng dẫn viên du lịch</font></i>"""
                },
                "raw_script": "Welcome exchange students. Please obtain your temporary entry badges at the security desk near Gate A before entering the dynamic laboratory area.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Welcome exchange students. Please obtain your temporary entry badges at the security desk near Gate A before entering the dynamic laboratory area.<br>
<small><font color="#4B5563">🎵 IPA: /ˈwɛlkəm ɪksˈtʃeɪndʒ ˈstuːdənts. pliːz əbˈteɪn jɔːr ˈtɛmpərəri ˈbædʒɪz.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Chào mừng các sinh viên trao đổi. Vui lòng nhận thẻ vào cửa tạm thời tại bàn an ninh gần Cổng A trước khi vào khu vực phòng thí nghiệm.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "Passage 1: Daily Administrative Duties",
                "correct": "B",
                "raw_passage": "The secretary's schedule usually opens with organizing files on the database server, and regularly concludes with filing financial records.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: The secretary's schedule usually opens with organizing files on the database server, and regularly concludes with filing financial records.<br>
<small><font color="#4B5563">🎵 IPA: /ðə ˈsɛkrətəriz ˈskɛdʒuːl ˈjuːʒuəli ˈoʊpənz wɪð ˈɔːrɡənaɪzɪŋ faɪlz.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Lịch trình của thư ký thường mở đầu bằng việc sắp xếp các tệp tin trên máy chủ cơ sở dữ liệu, và thường kết thúc bằng việc lưu trữ hồ sơ tài chính.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What task officially concludes the secretary's daily office workload?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt tɑːsk əˈfɪʃəli kənˈkluːdz ðə ˈsɛkrətəriz ˈdeɪli ˈɔːfɪs ˈwɜːrkleʊd?/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Nhiệm vụ nào kết thúc một cách chính thức khối lượng công việc văn phòng hàng ngày của thư ký?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Organizing files on database server<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Sắp xếp các tệp trên máy chủ dữ liệu</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Filing financial paperwork records<br><small><font color="#4B5563">🎵 IPA: /ˈfaɪlɪŋ faɪˈnænʃəl ˈpeɪpərwɜːrk ˈrɛkɔːrdz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Lưu trữ hồ sơ giấy tờ tài chính</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Cleaning the computer infrastructure<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Vệ sinh hạ tầng máy tính</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. Calling foreign academic delegates<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Gọi điện cho các đại biểu học thuật nước ngoài</font></i>"""
                }
            }
        ]
    },
    "Mã đề VSTEP-2026-D (Biến Thể Song Song 3)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Short Announcement",
                "correct": "A",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What is the updated departure time of Flight AA250?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt ɪz ðə ˈʌpdeɪtɪd dɪˈpɑːrtʃər taɪm ɒv flaɪt eɪ eɪ tuː faɪv oʊ/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Giờ khởi hành đã cập nhật của Chuyến bay AA250 là mấy giờ?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. 5.15<br><small><font color="#4B5563">🎵 IPA: /faɪv fɪfˈtiːn/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: 5 giờ 15 phút</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. 5.30<br><small><font color="#4B5563">🎵 IPA: /faɪv ˈθɜːrti/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: 5 giờ 30 phút</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. 6.00<br><small><font color="#4B5563">🎵 IPA: /sɪks oʊ klɒk/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: 6 giờ đúng</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. 6.45<br><small><font color="#4B5563">🎵 IPA: /sɪks fɔːrˈti-faɪv/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: 6 giờ 45 phút</font></i>"""
                },
                "raw_script": "Attention airport passengers, Flight AA250 to London has changed its departure schedule from 5:30 to 5:15 due to rapid custom clearing procedures.",
                "script_html": """<b><font color="#1E3A8A">ENG:</font></b> Attention airport passengers, Flight AA250 to London has changed its departure schedule from 5:30 to 5:15 due to rapid custom clearing procedures.<br>
<small><font color="#4B5563">🎵 IPA: /əˈtɛnʃən ˈɛrˌpɔːrt ˈpæsɪndʒərz, flaɪt eɪ eɪ tuː faɪv oʊ tuː ˈlʌndən.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Xin chú ý các hành khách tại sân bay, Chuyến bay AA250 đến Luân Đôn đã thay đổi lịch khởi hành từ 5:30 thành 5:15 do thủ tục thông quan nhanh chóng.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "Passage 1: Medical Officer Shift Routine",
                "correct": "D",
                "raw_passage": "The nurse's morning routine typically starts with checking clinical vital signs, and predictably finishes with completing final ward medical logs.",
                "passage_html": """<b><font color="#1E3A8A">ENG:</font></b> Context: The nurse's morning routine typically starts with checking clinical vital signs, and predictably finishes with completing final ward medical logs.<br>
<small><font color="#4B5563">🎵 IPA: /ðə ˈnɜːrsɪz ˈmɔːrnɪŋ ruːˈtiːn ˈtɪpɪkli stɑːrts wɪð ˈtʃɛkɪŋ ˈklɪnɪkəl ˈvaɪtl saɪnz... /</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Lộ trình buổi sáng của điều dưỡng thường bắt đầu bằng việc kiểm tra các dấu hiệu sinh tồn lâm sàng, và kết thúc một cách có thể đoán trước bằng việc hoàn thành các nhật ký y tế của khoa.</font></i>""",
                "question_html": """<b><font color="#1E3A8A">ENG:</font></b> Question 1: What process concludes the diagnostic workload of the medical nurse shift?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt ˈproʊsɛs kənˈkluːdz ðə ˌdaɪəɡˈnɒstɪk ˈwɜːrkleʊd ɒv ðə ˈmɛdɪkəl nɜːrs ʃɪft?/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Quy trình nào kết thúc khối lượng công việc chẩn đoán của ca trực điều dưỡng y tế?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Checking clinical vital signs<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Kiểm tra dấu hiệu sinh tồn lâm sàng</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. Buying medicine from pharmacy stores<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Mua thuốc từ các cửa hàng dược phẩm</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Training junior medical students<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Đào tạo các sinh viên y khoa cấp dưới</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. Completing ward medical logs<br><small><font color="#4B5563">🎵 IPA: /kəmˈpliːtɪŋ wɔːrd ˈmɛdɪkəl lɒɡz/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Hoàn thành nhật ký y tế của bệnh phòng</font></i>"""
                }
            }
        ]
    }
}

# CHỒNG BỔ SUNG CÁC PHÂN HỆ TỰ LUẬN CHỨA ĐÁP ÁN MẪU TĨNH - HIỂN THỊ NGAY KHÔNG CẦN CHỜ NỘP BÀI
for de_name in VSTEP_MASTER_DATABASE.keys():
    VSTEP_MASTER_DATABASE[de_name]["3️⃣ VSTEP Viết"] = [
        {
            "id": 1,
            "type": "Task 1: Informal Email Reply (120 words)",
            "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Prompt: Write an informal email responding to Jane. Tell her about your friend An (personality, hobbies, current study or work status) to check if she fits in with Jane's family in London.<br>
<small><font color="#4B5563">🎵 IPA: /raɪt ân ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Đề bài: Viết một email thân mật trả lời Jane. Hãy kể cho cô ấy nghe về người bạn tên An (tính cách, sở thích, tình trạng học tập hoặc làm việc hiện tại) để xem cô ấy có phù hợp ở cùng gia đình Jane tại Luân Đôn không.</font></i>""",
            "model_answer_raw": "Dear Jane, I am writing to tell you that An is a wonderful person. She is extremely friendly, helpful, and highly responsible. In her free time, she loves reading books and cooking Vietnamese traditional food, which your family will definitely enjoy. Currently, she is studying hard as a final-year student at university. I am sure she will be a great fit for your home. Best, Nguyen.",
            "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: Dear Jane, I am writing to tell you that An is a wonderful person. She is extremely friendly, helpful, and highly responsible. In her free time, she loves reading books and cooking Vietnamese traditional food, which your family will definitely enjoy. Currently, she is studying hard as a final-year student at university. I am sure she will be a great fit for your home. Best, Nguyen.<br>
<small><font color="#4B5563">🎵 IPA: /dɪər dʒeɪn, maɪ frɛnd æn ɪz ə ˈwʌndərfʊl ˈpɜːrsən. ʃiː ɪz ɪksˈtriːmli ˈfrɛndli.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Bài mẫu học thuộc: Jane thân mến, tôi viết thư này để kể với bạn rằng An là một người tuyệt vời. Cô ấy cực kỳ thân thiện, hay giúp đỡ và có trách nhiệm cao. Khi rảnh rỗi, cô ấy thích đọc sách và nấu các món ăn truyền thống Việt Nam, điều mà gia đình bạn chắc chắn sẽ thích. Hiện tại, cô ấy đang học tập chăm chỉ với tư cách là sinh viên năm cuối đại học. Tôi chắc chắn cô ấy sẽ rất phù hợp với ngôi nhà của bạn. Thân ái, Nguyễn.</font></i>""",
            "analysis_html": """<b>[🎯 PHÂN TÍCH NGỮ CẢNH CẤU TRÚC CÂU & NGỮ PHÁP]:</b><br>
1. <b>Cấu trúc mô tả tính cách song hành:</b> Cụm <i>"She is extremely friendly, helpful, and highly responsible"</i> ứng dụng trạng từ bổ nghĩa cấp độ cao (extremely, highly) đi kèm tính từ cốt lõi, giúp ghi điểm tuyệt đối tiêu chí Từ vựng (Vocabulary).<br>
2. <b>Mệnh đề quan hệ không hạn định:</b> Sử dụng cụm <i>", which your family will definitely enjoy"</i> bổ nghĩa cho toàn bộ hành động phía trước, tạo câu phức chuẩn mực cấu trúc VSTEP bậc 4.<br>
3. <b>Cách dùng thì Hiện tại tiếp diễn biểu đạt trạng thái:</b> <i>"she is studying hard as a..."</i> nhấn mạnh tính liên tục của hành động học tập hiện tại."""
        }
    ]
    VSTEP_MASTER_DATABASE[de_name]["4️⃣ VSTEP Nói"] = [
        {
            "id": 1,
            "type": "Part 1: Social Interaction (Free Time)",
            "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Prompt: What do you often do in your free time? Do you prefer reading books or watching TV?<br>
<small><font color="#4B5563">🎵 IPA: /wɒt duː juː ˈɒfən duː ɪn jɔːr friː taɪm.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Đề bài: Bạn thường làm gì vào thời gian rảnh? Bạn thích đọc sách hay xem TV hơn?</font></i>""",
            "model_answer_raw": "In my free time, I often read books and listen to English music. Personally speaking, I prefer reading books to watching television because books help widen my knowledge and reduce stress after hard working hours.",
            "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Speaking Response: In my free time, I often read books and listen to English music. Personally speaking, I prefer reading books to watching television because books help widen my knowledge and reduce stress after hard working hours.<br>
<small><font color="#4B5563">🎵 IPA: /ɪn maɪ friː taɪm, maɪ ˈɒfən riːd bʊks ənd ˈlɪsən tuː ˈɪŋɡlɪʃ ˈmjuːzɪk. ˈpɜːrsənəli ˈspiːkɪŋ.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu trả lời mẫu thuộc lòng: Vào thời gian rảnh, tôi thường đọc sách và nghe nhạc tiếng Anh. Đối với cá nhân tôi, tôi thích đọc sách hơn xem ti vi vì sách giúp mở rộng kiến thức và giảm căng thẳng sau những giờ làm việc vất vả.</font></i>"""
        }
    ]

MASTER_PROMPT = """
# ROLE & PERSONALITY
You are the elite "VSTEP Master Trainer" specialized in rapid remediation for learners who lost their English roots (người mất gốc). Address the user respectfully as "thầy cô".

# UNIVERSAL COMPACT INTERLINEAR RULE
Every piece of English text output MUST strictly follow this 3-line interlinear layout with hard `<br>` breaks:
<b><font color="#1E3A8A">ENG:</font></b> [English Text]<br>
<small><font color="#4B5563">🎵 IPA: /[Phonetic Transcription]/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: [Dịch Nghĩa Tiếng Việt]</font></i>
"""

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

MODEL_NAME = "gemini-2.5-flash"
DE_LIST_KEYS = list(VSTEP_MASTER_DATABASE.keys())

# Quản lý trạng thái cốt lõi
if "selected_de" not in st.session_state:
    st.session_state.selected_de = DE_LIST_KEYS[0]
if "current_section" not in st.session_state:
    st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# --- SIDEBAR ĐIỀU HÀNH PHẲNG TUYỆT ĐỐI ---
st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập mã truy cập hệ thống:", type="password")

st.sidebar.markdown("### 📁 BỘ CHỌN MÃ ĐỀ THI")
current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx, key="sb_de_master_direct")
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

font_size = st.sidebar.slider("Kích thước chữ", 14, 24, 16)
st.markdown(f"<style>.stMarkdown, p, li {{ font-size: {font_size}px !important; }}</style>", unsafe_allow_html=True)

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
c1, c2 = st.sidebar.columns(2)
with c1:
    if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True, key="sd_n"):
        st.session_state.current_section = "1️⃣ VSTEP Nghe"
        st.session_state.current_q_idx = 0
        st.rerun()
with c2:
    if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True, key="sd_d"):
        st.session_state.current_section = "2️⃣ VSTEP Đọc"
        st.session_state.current_q_idx = 0
        st.rerun()

c3, c4 = st.sidebar.columns(2)
with c3:
    if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True, key="sd_v"):
        st.session_state.current_section = "3️⃣ VSTEP Viết"
        st.session_state.current_q_idx = 0
        st.rerun()
with c4:
    if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True, key="sd_no"):
        st.session_state.current_section = "4️⃣ VSTEP Nói"
        st.session_state.current_q_idx = 0
        st.rerun()

questions_list = VSTEP_MASTER_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")
cp, cn = st.sidebar.columns(2)
with cp:
    if st.sidebar.button("⏮️ CÂU TRƯỚC", use_container_width=True, key="nav_p"):
        if st.session_state.current_q_idx > 0:
            st.session_state.current_q_idx -= 1
            st.rerun()
with cn:
    if st.sidebar.button("⏭️ CÂU TIẾP", use_container_width=True, key="nav_n"):
        if st.session_state.current_q_idx < max_questions - 1:
            st.session_state.current_q_idx += 1
            st.rerun()

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_{i}", use_container_width=True):
                st.session_state.current_q_idx = i
                st.rerun()

# --- KHÔNG GIAN MAIN WORKSPACE CHÍNH DIỆN ---
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Đang vận hành: {st.session_state.selected_de}")
st.markdown("---")

# NÚT BẤM THÔNG MINH CHUYỂN ĐỀ CHIẾN LƯỢC THEO YÊU CẦU BỔ SUNG
current_de_pos = DE_LIST_KEYS.index(st.session_state.selected_de)
if current_de_pos < len(DE_LIST_KEYS) - 1:
    if st.button("🎉 THÀNH THẠO ĐỀ NÀY RỒI ── BẤM ĐỂ CHUYỂN SANG MÃ ĐỀ TIẾP THEO MỨC ĐỘ TIẾP THEO 🚀", use_container_width=True):
        st.session_state.selected_de = DE_LIST_KEYS[current_de_pos + 1]
        st.session_state.current_q_idx = 0
        st.rerun()

st.markdown("---")

if max_questions == 0:
    st.info("Đang nạp dữ liệu phân hệ...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
    if "submitted_state" not in st.session_state:
        st.session_state.submitted_state = {}
    is_submitted = q_key in st.session_state.submitted_state

    # PHÂN PHỐI LUỒNG HIỂN THỊ TỰ LUẬN TĨNH KHÔNG CẦN CHỜ BẤM NỘP
    if st.session_state.current_section in ["3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]:
        st.warning("📊 **Yêu cầu phân hệ khảo sát tự luận mẫu quy chuẩn:**")
        st.markdown(active_q["prompt_html"], unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🏆 ĐÁP ÁN MẪU KHUYÊN DÙNG ĐỂ HỌC THUỘC LÒNG THỰC CHIẾN:")
        st.markdown(active_q["model_answer_html"], unsafe_allow_html=True)
        
        # TÍCH HỢP THANH PHÁT ÂM AUDIO CHO BÀI MẪU TỰ LUẬN
        st.info("🎵 **Nút phát âm mẫu bài thi tự luận - Bấm để luyện nghe ngữ điệu chuẩn hóa:**")
        tts_auto = gTTS(text=active_q["model_answer_raw"], lang='en', tld='com')
        fp_auto = io.BytesIO()
        tts_auto.write_to_fp(fp_auto)
        fp_auto.seek(0)
        st.audio(fp_auto, format="audio/mp3")
        
        if st.session_state.current_section == "3️⃣ VSTEP Viết" and "analysis_html" in active_q:
            st.markdown("---")
            st.markdown(active_q["analysis_html"], unsafe_allow_html=True)

    else:
        # HIỂN THỊ CHO PHÂN HỆ TRẮC NGHIỆM (NGHE/ĐỌC)
        if st.session_state.current_section == "1️⃣ VSTEP Nghe":
            st.info("🎧 **Nội dung nghe ghi âm mẫu chuyên nghiệp:**")
            tts_m = gTTS(text=active_q["raw_script"], lang='en', tld='com')
            fp_m = io.BytesIO()
            tts_m.write_to_fp(fp_m)
            fp_m.seek(0)
            st.audio(fp_m, format="audio/mp3")
            if is_submitted:
                st.markdown(active_q["script_html"], unsafe_allow_html=True)

        elif st.session_state.current_section == "2️⃣ VSTEP Đọc":
            st.success("=== ĐOẠN VĂN NỀN ĐỌC HIỂU HOÀN CHỈNH ===")
            st.markdown(active_q["passage_html"], unsafe_allow_html=True)
            st.info("🎵 **Thành phần phát âm hỗ trợ luyện đọc:**")
            tts_r = gTTS(text=active_q["raw_passage"], lang='en', tld='com')
            fp_r = io.BytesIO()
            tts_r.write_to_fp(fp_r)
            fp_r.seek(0)
            st.audio(fp_r, format="audio/mp3")

        st.markdown("---")
        st.markdown(active_q["question_html"], unsafe_allow_html=True)

        # CARD ACTION TĨNH CHỐNG LỖI TRỐNG CHỮ 
        if not is_submitted:
            for key in active_q["options_html"].keys():
                st.markdown(f"<div style='background-color:#F8FAFC; border-left:4px solid #1E3A8A; padding:12px; border-radius:6px; margin-top:10px;'>{active_q['options_html'][key]}</div>", unsafe_allow_html=True)
                if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {key}", key=f"btn_{key}_{q_key}", use_container_width=True):
                    st.session_state.submitted_state[q_key] = key
                    if key == active_q["correct"]:
                        st.session_state.score += 10
                    st.rerun()
        else:
            for key, html_val in active_q["options_html"].items():
                if key == active_q["correct"]:
                    st.markdown(f"<div style='border:2px solid #2E7D32; background-color:#E8F5E9; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✔ ĐÁP ÁN ĐÚNG CHUẨN XÁC:</b><br>{html_val}</div>", unsafe_allow_html=True)
                elif key == st.session_state.submitted_state[q_key]:
                    st.markdown(f"<div style='border:2px solid #D32F2F; background-color:#FFEBEE; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✘ LỰA CHỌN CỦA THẦY CÔ:</b><br>{html_val}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='border:1px solid #E5E7EB; padding:12px; border-radius:6px; margin-bottom:12px; opacity:0.5;'>{html_val}</div>", unsafe_allow_html=True)
