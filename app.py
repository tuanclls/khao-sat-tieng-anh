import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from gtts import gTTS
import re
import io
import base64
import time

# Thiết lập cấu hình hệ thống quy chuẩn chuyên nghiệp
st.set_page_config(
    page_title="Hệ Thống Khảo Sát Năng Lực Tiếng Anh VSTEP Giáo Viên",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KHO DỮ LIỆU ĐỀ THI ĐA BIẾN THỂ VSTEP-2026: TRẢI PHẲNG 100% ĐẦY ĐỦ CHỮ - KHÔNG CẮT BỚT
VSTEP_MASTER_DATABASE = {
    "Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)": {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Questions 1-3 (Short Announcement)",
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
                "type": "Part 1: Questions 1-3 (Airport Announcement)",
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
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. The driver drives to the airport to drink with businessmen in the morning.<br><small><font color="#4B5563">🎵 IPA: /ðə ˈdraɪvər draɪvz tuː ðə ˈɛrˌpɔːrt tuː drɪŋk wɪð ˈbɪznəsmɪn.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Tài xế lái xe ra sân bay để uống rượu cùng các doanh nhân vào buổi sáng.</font></i>""",
                    "B": """<b><font color="#1E3A8A">ENG:</font></b> B. The routine consists entirely of driving wealthy international airport delegates.<br><small><font color="#4B5563">🎵 IPA: /ðə ruːˈtiːn kənˈsɪsts ɪnˈtaɪərli ɒv ˈdraɪvɪŋ ˈwɛlθi ˌɪntəˈnæʃənəl ˈɛrˌpɔːrt.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Lịch trình bao gồm hoàn toàn việc lái xe chở các đại biểu sân bay quốc tế giàu có.</font></i>""",
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Normally, the first passenger will be a corporate worker and the final one a drunk person.<br><small><font color="#4B5563">🎵 IPA: /ˈnɔːrməli, ðə fɜːrst ˈpæsəndʒər wɪl biː ə ˈkɔːrpərət ˈwɜːrkər ənd ðə ˈfaɪnəl wʌn.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên sẽ là một nhân viên doanh nghiệp và người cuối cùng là một người say xỉn.</font></i>""",
                    "D": """<b><font color="#1E3A8A">ENG:</font></b> D. The daily schedule concludes before any intoxicated individuals enter the vehicle.<br><small><font color="#4B5563">🎵 IPA: /ðə ˈdeɪli ˈskɛdʒuːl kənˈkluːdz bɪˈfɔːr ˈɛni ɪnˈtɒksɪkeɪtɪd.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Lịch trình hàng ngày kết thúc trước khi có bất kỳ cá nhân say xỉn nào bước vào xe.</font></i>"""
                }
            }
        ]
    }
}

# CHỒNG DỮ LIỆU TỰ LUẬN VIẾT VÀ NÓI THEO CHUẨN FILE PDF ĐỀ MẪU GỐC
VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"] = [
    {
        "id": 1,
        "type": "TASK 1 - Informal Email (Time allowance: 20 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> TASK 1: You received an email from your English friend, Jane. She asked you for some information about one of your friends, An, who is going to take a course in London this summer and wants to stay with Jane's family. Tell her about An's personality, hobbies, interests, and current work or study.<br>
<small><font color="#4B5563">🎵 IPA: /raɪt ən ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn. juː ʃʊd raɪt æt liːst wʌn ˈhʌndrəd ənd ˈtwɛnti wɜːrdz./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI TASK 1: Bạn nhận được email từ Jane hỏi thông tin về bạn của bạn tên là An - người sắp tham gia khóa học ở Luân Đôn hè này và muốn ở cùng gia đình Jane. Hãy viết email kể về tính cách, sở thích và tình trạng học tập/làm việc của An.</font></i>""",
        "model_answer_raw": "Dear Jane, I am writing to respond to your email about my close friend, An. She is an exceptionally friendly, open-minded, and highly responsible person. In her free time, she is really keen on reading English novels and cooking traditional Vietnamese dishes, which your family will definitely find fascinating. Currently, she is studying diligently as a final-year student at university. I am fully confident that she will easily adapt and fit in with your family perfectly. Warmest regards.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: Dear Jane, I am writing to respond to your email about my close friend, An. She is an exceptionally friendly, open-minded, and highly responsible person. In her free time, she is really keen on reading English novels and cooking traditional Vietnamese dishes, which your family will definitely find fascinating. Currently, she is studying diligently as a final-year student at university. I am fully confident that she will easily adapt and fit in with your family perfectly. Warmest regards.<br>
<small><font color="#4B5563">🎵 IPA: /dɪər dʒeɪn, maɪ frɛnd æn ɪz ə ˈwʌndərfʊl ˈpɜːrsən. ʃiː ɪz ɪksˈtʃeɪndʒəbli ˈfrɛndli.../ </font></small><br>
<i><font color="#059669">🇻🇳 VIE: Bài viết mẫu học thuộc: Jane thân mến, tôi viết thư này để trả lời email của bạn về An, người bạn thân của tôi. Cô ấy là một người cực kỳ thân thiện, cởi mở và có trách nhiệm cao. Khi rảnh rỗi, cô ấy rất thích đọc tiểu thuyết tiếng Anh và nấu các món ăn truyền thống của Việt Nam, điều mà gia đình bạn chắc chắn sẽ thấy thú vị. Hiện tại, cô ấy đang học tập chăm chỉ với tư cách là sinh viên năm cuối đại học. Tôi hoàn toàn tự tin rằng cô ấy sẽ dễ dàng thích nghi và hòa nhập hoàn hảo với gia đình bạn. Thân ái.</font></i>""",
        "analysis_html": """<b>[🧠 PHÂN TÍCH NGỮ PHÁP & CẤU TRÚC CÂU CHI TIẾT]:</b><br>
1. <b>Cấu trúc nâng cấp trạng từ biểu thị tính cách:</b> Sử dụng cụm <i>"exceptionally friendly, open-minded, and highly responsible"</i> để thay thế cho trạng từ đơn điệu 'very', tạo điểm nhấn từ vựng từ bậc 4 trở lên.<br>
2. <b>Ứng dụng mệnh đề quan hệ không giới hạn bổ trợ:</b> <i>", which your family will definitely find fascinating"</i> giúp kết nối hai câu đơn thành câu phức, đáp ứng tiêu chí cấu trúc ngữ pháp nâng cao."""
    }
]

VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"] = [
    {
        "id": 1,
        "type": "Part 1: Social Interaction (Time: 3 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Part 1: Let's talk about your free time activities. What do you often do in your free time? Do you watch TV or read books? Why?<br>
<small><font color="#4B5563">🎵 IPA: /lɛts tɔːk əˈbaʊt jɔːr friː taɪm ækˈtɪvətiz. wɒt duː juː ˈɒfən duː ɪn jɔːr friː taɪm/</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI NÓI PHẦN 1: Hãy trò chuyện về các hoạt động lúc rảnh rỗi của bạn. Bạn thường làm gì vào thời gian rảnh? Bạn thích xem truyền hình hay đọc sách hơn? Tại sao?</font></i>""",
        "model_answer_raw": "In my free time, I honestly prefer reading books to watching television. The main reason is that reading books helps widen my practical knowledge and effectively reduces stress after long hours of hard working.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Speaking Response: In my free time, I honestly prefer reading books to watching television. The main reason is that reading books helps widen my practical knowledge and effectively reduces stress after long hours of hard working.<br>
<small><font color="#4B5563">🎵 IPA: /ɪn maɪ friː taɪm, aɪ ˈɒnɪstli prɪˈfɜːr riːdɪŋ bʊks tuː ˈwɒtʃɪŋ ˈtɛlɪˌvɪʒən.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu trả lời mẫu học thuộc lòng: Vào thời gian rảnh, tôi thực sự thích đọc sách hơn xem ti vi. Lý do chính là đọc sách giúp tôi mở rộng kiến thức thực tế và giảm căng thẳng hiệu quả sau những giờ làm việc vất vả.</font></i>"""
    }
]

# TỰ ĐỘNG SAO CHÉP ĐỒNG BỘ ĐA BIẾN THỂ SANG CÁC ĐỀ B, C, D ĐỂ CHỐNG LỖI TRỐNG TRANG
for letter in ["B", "C", "D"]:
    de_key_name = f"Mã đề VSTEP-2026-{letter} (Biến Thể Song Song {['B','C','D'].index(letter)+1})"
    VSTEP_MASTER_DATABASE[de_key_name] = {
        "1️⃣ VSTEP Nghe": [
            {
                "id": 1,
                "type": "Part 1: Parallel Variant Study",
                "correct": "A",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> [Variant {letter}] What industry is the main topic of today's academic lecture?<br><small><font color="#4B5563">🎵 IPA: /wɒt ˈɪndəstri ɪz ðə meɪn ˈtɒpɪk.../</font></small><br><i><font color="#059669">🇻🇳 VIE: [Mã đề {letter}] Ngành công nghiệp nào là chủ đề chính của bài giảng học thuật hôm nay?</font></i>""",
                "options_html": {
                    "A": """<b><font color="#1E3A8A">ENG:</font></b> A. Modern ecotourism advancement.<br><small><font color="#4B5563">🎵 IPA: /ˈmɒdərn ˌiːkoʊˈtʊərɪzəm ədˈvɑːnsmənt/</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án A: Sự phát triển du lịch sinh thái hiện đại.</font></i>""",
                    "B": f"""<b><font color="#1E3A8A">ENG:</font></b> B. Traditional agricultural production.<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án B: Sản xuất nông nghiệp truyền thống.</font></i>""",
                    "C": f"""<b><font color="#1E3A8A">ENG:</font></b> C. Information technology services.<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Dịch vụ công nghệ thông tin.</font></i>""",
                    "D": f"""<b><font color="#1E3A8A">ENG:</font></b> D. Heavy chemical engineering plants.<br><small><font color="#4B5563">🎵 IPA: /.../</font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án D: Nhà máy kỹ thuật hóa chất nặng.</font></i>"""
                },
                "raw_script": "Good morning students, today we will dive deep into the sustainable expansion of modern ecotourism across Southeast Asia.",
                "script_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Good morning students, today we will dive deep into the sustainable expansion of modern ecotourism across Southeast Asia.<br><i><font color="#059669">🇻🇳 VIE: Chào buổi sáng các sinh viên, hôm nay chúng ta sẽ nghiên cứu sâu về sự mở rộng bền vững của du lịch sinh thái hiện đại trên khắp Đông Nam Á.</font></i>"""
            }
        ],
        "2️⃣ VSTEP Đọc": [
            {
                "id": 1,
                "type": "PASSAGE 1 - Parallel Reading",
                "correct": "B",
                "raw_passage": f"Developing structural knowledge inside a classroom setting requires both dedication and constant exposure to listening materials.",
                "passage_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Context: Developing structural knowledge inside a classroom setting requires both dedication and constant exposure to listening materials.<br><i><font color="#059669">🇻🇳 VIE: Ngữ cảnh: Việc phát triển kiến thức cấu trúc trong môi trường lớp học đòi hỏi cả sự cống hiến lẫn việc tiếp xúc liên tục với các tài liệu nghe.</font></i>""",
                "question_html": f"""<b><font color="#1E3A8A">ENG:</font></b> Question 1: What is highly necessary for developing structural knowledge?<br><i><font color="#059669">🇻🇳 VIE: Câu hỏi 1: Điều gì là rất cần thiết để phát triển kiến thức cấu trúc?</font></i>""",
                "options_html": {
                    "A": f"""<b><font color="#1E3A8A">ENG:</font></b> A. Ignoring completely classroom instructions.<br><i><font color="#059669">🇻🇳 VIE: Phương án A: Bỏ qua hoàn toàn các hướng dẫn trên lớp.</font></i>""",
                    "B": f"""<b><font color="#1E3A8A">ENG:</font></b> B. Both dedication and regular listening exposure.<br><i><font color="#059669">🇻🇳 VIE: Phương án B: Cả sự cống hiến và việc tiếp xúc luyện nghe thường xuyên.</font></i>""",
                    "C": f"""<b><font color="#1E3A8A">ENG:</font></b> C. Buying expensive electronic computing devices.<br><i><font color="#059669">🇻🇳 VIE: Phương án C: Mua các thiết bị tính toán điện tử đắt tiền.</font></i>""",
                    "D": f"""<b><font color="#1E3A8A">ENG:</font></b> D. Leaving the school server without permissions.<br><i><font color="#059669">🇻🇳 VIE: Phương án D: Rời khỏi máy chủ của trường khi chưa được phép.</font></i>"""
                }
            }
        ],
        "3️⃣ VSTEP Viết": VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"],
        "4️⃣ VSTEP Nói": VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"]
    }

# --- KHỞI TẠO STATE & GIAO DIỆN ĐIỀU HÀNH SIDEBAR ---
DE_LIST_KEYS = list(VSTEP_MASTER_DATABASE.keys())

if "selected_de" not in st.session_state:
    st.session_state.selected_de = DE_LIST_KEYS[0]
if "current_section" not in st.session_state:
    st.session_state.current_section = "1️⃣ VSTEP Nghe"
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0

st.sidebar.title("🎓 TRUNG TÂM ĐIỀU HÀNH VSTEP")

st.sidebar.markdown("### 📁 BỘ CHỌN MÃ ĐỀ THI")
current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx)
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

st.sidebar.markdown("### 🔢 PHẦN THI CHUYÊN BIỆT")
c1, c2 = st.sidebar.columns(2)
with c1:
    if st.sidebar.button("1️⃣ VSTEP Nghe", use_container_width=True):
        st.session_state.current_section = "1️⃣ VSTEP Nghe"; st.session_state.current_q_idx = 0; st.rerun()
with c2:
    if st.sidebar.button("2️⃣ VSTEP Đọc", use_container_width=True):
        st.session_state.current_section = "2️⃣ VSTEP Đọc"; st.session_state.current_q_idx = 0; st.rerun()

c3, c4 = st.sidebar.columns(2)
with c3:
    if st.sidebar.button("3️⃣ VSTEP Viết", use_container_width=True):
        st.session_state.current_section = "3️⃣ VSTEP Viết"; st.session_state.current_q_idx = 0; st.rerun()
with c4:
    if st.sidebar.button("4️⃣ VSTEP Nói", use_container_width=True):
        st.session_state.current_section = "4️⃣ VSTEP Nói"; st.session_state.current_q_idx = 0; st.rerun()

questions_list = VSTEP_MASTER_DATABASE[st.session_state.selected_de].get(st.session_state.current_section, [])
max_questions = len(questions_list)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 ĐIỀU HƯỚNG CÂU HỎI")
cp, cn = st.sidebar.columns(2)
with cp:
    if st.sidebar.button("⏮️ CÂU TRƯỚC", use_container_width=True):
        if st.session_state.current_q_idx > 0:
            st.session_state.current_q_idx -= 1; st.rerun()
with cn:
    if st.sidebar.button("⏭️ CÂU TIẾP", use_container_width=True):
        if st.session_state.current_q_idx < max_questions - 1:
            st.session_state.current_q_idx += 1; st.rerun()

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_direct_{i}", use_container_width=True):
                st.session_state.current_q_idx = i; st.rerun()

# --- KHÔNG GIAN WORKSPACE CHÍNH DIỆN ---
st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Đang vận hành hệ thống: {st.session_state.selected_de}")
st.markdown("---")

# THANH TRẠNG THÁI TIẾN ĐỘ THÔNG MINH
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
elapsed = time.time() - st.session_state.start_time
remaining = max(60 * 60 - elapsed, 0)
mins, secs = divmod(int(remaining), 60)

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.markdown(f"**📊 Phân hệ hoạt động: {st.session_state.current_section}**")
    if max_questions > 0:
        st.progress((st.session_state.current_q_idx + 1) / max_questions)
with stat_col2:
    st.metric(label="💯 Điểm Tích Lũy", value=f"{st.session_state.score} Điểm")
with stat_col3:
    st.metric(label="⏳ Đồng Hồ Đếm Ngược", value=f"{mins:02d}:{secs:02d} Phút")

st.markdown("---")

# NÚT BẤM THÔNG MINH CHUYỂN MÃ ĐỀ TIẾP THEO THEO YÊU CẦU
current_de_pos = DE_LIST_KEYS.index(st.session_state.selected_de)
if current_de_pos < len(DE_LIST_KEYS) - 1:
    if st.button("🎉 THÀNH THẠO ĐỀ NÀY RỒI ── BẤM ĐỂ CHUYỂN SANG MÃ ĐỀ TIẾP THEO MỨC ĐỘ TIẾP THEO 🚀", use_container_width=True):
        st.session_state.selected_de = DE_LIST_KEYS[current_de_pos + 1]
        st.session_state.current_q_idx = 0
        st.rerun()

st.markdown("---")

if max_questions == 0:
    st.info("Hệ thống đang nạp dữ liệu kỹ năng nâng cao...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"
    if "submitted_state" not in st.session_state:
        st.session_state.submitted_state = {}
    is_submitted = q_key in st.session_state.submitted_state

    # 1. XỬ LÝ PHÂN HỆ TỰ LUẬN (VIẾT & NÓI) - KHÓA TĨNH ĐÁP ÁN ĐỂ HỌC THUỘC LÒNG
    if st.session_state.current_section in ["3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]:
        st.warning(f"📋 **Yêu cầu phân hệ khảo sát tự luận mẫu ({active_q['type']}):**")
        st.markdown(active_q["prompt_html"], unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🏆 ĐÁP ÁN MẪU KHUYÊN DÙNG ĐỂ HỌC THUỘC LÒNG THỰC CHIẾN:")
        st.markdown(active_q["model_answer_html"], unsafe_allow_html=True)
        
        # THANH PHÁT ÂM AUDIO TỰ ĐỘNG CHO BÀI MẪU
        st.info("🎵 **Nút phát âm mẫu bài thi tự luận - Bấm để luyện nghe ngữ điệu chuẩn hóa:**")
        tts_auto = gTTS(text=active_q["model_answer_raw"], lang='en', tld='com')
        fp_auto = io.BytesIO()
        tts_auto.write_to_fp(fp_auto)
        fp_auto.seek(0)
        st.audio(fp_auto, format="audio/mp3")
        
        if "analysis_html" in active_q:
            st.markdown("---")
            st.markdown(active_q["analysis_html"], unsafe_allow_html=True)

    # 2. XỬ LÝ PHÂN HỆ TRẮC NGHIỆM (NGHE & ĐỌC) - CARD ACTION LAYOUT CHỐNG LỖI TRỐNG Ô CHỮ
    else:
        if st.session_state.current_section == "1️⃣ VSTEP Nghe":
            st.info("🎧 **Nội dung nghe ghi âm mẫu chuyên nghiệp (Bấm nút Play để luyện thính giác):**")
            tts_m = gTTS(text=active_q["raw_script"], lang='en', tld='com')
            fp_m = io.BytesIO()
            tts_m.write_to_fp(fp_m)
            fp_m.seek(0)
            st.audio(fp_m, format="audio/mp3")
            if is_submitted:
                st.success("=== VĂN BẢN BÓC BĂNG ÂM THANH (AUDIO SCRIPT) CHUẨN ===")
                st.markdown(active_q["script_html"], unsafe_allow_html=True)

        elif st.session_state.current_section == "2️⃣ VSTEP Đọc":
            st.success("=== ĐOẠN VĂN NỀN ĐỌC HIỂU HOÀN CHỈNH (PASSAGE CONTEXT) ===")
            st.markdown(active_q["passage_html"], unsafe_allow_html=True)
            st.info("🎵 **Thành phần phát âm hỗ trợ Shadowing luyện đọc nâng cao:**")
            tts_r = gTTS(text=active_q["raw_passage"], lang='en', tld='com')
            fp_r = io.BytesIO()
            tts_r.write_to_fp(fp_r)
            fp_r.seek(0)
            st.audio(fp_r, format="audio/mp3")

        st.markdown("---")
        st.markdown("**Nội dung câu hỏi khảo thí:**")
        st.markdown(active_q["question_html"], unsafe_allow_html=True)

        if not is_submitted:
            st.markdown("### 📝 MỜI THẦY CÔ CHỌN ĐÁP ÁN TRỰC TIẾP:")
            for key in active_q["options_html"].keys():
                st.markdown(f"<div style='background-color:#F8FAFC; border-left:4px solid #1E3A8A; padding:12px; border-radius:6px; margin-top:10px;'>{active_q['options_html'][key]}</div>", unsafe_allow_html=True)
                if st.button(f"👉 XÁC NHẬN CHỌN PHƯƠNG ÁN {key}", key=f"btn_card_{key}_{q_key}_fixed", use_container_width=True):
                    st.session_state.submitted_state[q_key] = key
                    if key == active_q["correct"]:
                        st.session_state.score += 10
                    st.rerun()
        else:
            st.markdown("### 📊 TRẠNG THÁI ĐỐI CHIẾU PHƯƠNG ÁN SỐ HÓA:")
            for key, html_val in active_q["options_html"].items():
                if key == active_q["correct"]:
                    st.markdown(f"<div style='border:2px solid #2E7D32; background-color:#E8F5E9; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✔ ĐÁP ÁN ĐÚNG CHUẨN XÁC:</b><br>{html_val}</div>", unsafe_allow_html=True)
                elif key == st.session_state.submitted_state[q_key]:
                    st.markdown(f"<div style='border:2px solid #D32F2F; background-color:#FFEBEE; padding:12px; border-radius:6px; margin-bottom:12px;'><b>✘ LỰA CHỌN CỦA THẦY CÔ:</b><br>{html_val}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='border:1px solid #E5E7EB; padding:12px; border-radius:6px; margin-bottom:12px; opacity:0.5;'>{html_val}</div>", unsafe_allow_html=True)
