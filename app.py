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

# KHO DỮ LIỆU ĐỀ THI ĐA BIẾN THỂ VSTEP-2026: ĐỒNG BỘ ĐẦY ĐỦ CÁC PHẦN TỰ LUẬN THEO FILE ĐỀ MẪU CHUẨN
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
                    "C": """<b><font color="#1E3A8A">ENG:</font></b> C. Normally, my first passenger will be a businessman and my last one a drunk.<br><small><font color="#4B5563">🎵 IPA: /.../ </font></small><br><i><font color="#059669">🇻🇳 VIE: Phương án C: Thông thường, hành khách đầu tiên là doanh nhân và người cuối cùng là người say.</font></i>"""
                }
            }
        ]
    }
}

# KHU VỰC ĐỊNH NGHĨA DỮ LIỆU TỰ LUẬN VIẾT VÀ NÓI HOÀN CHỈNH (ĐẦY ĐỦ CÁC CÂU THEO FILE PDF ĐỀ MẪU)
VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"] = [
    {
        "id": 1,
        "type": "TASK 1 - Informal Email (Time allowance: 20 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> TASK 1: You received an email from your English friend, Jane. She asked you for some information about one of your friends, An, who is going to take a course in London this summer and wants to stay with Jane's family. Tell her about An's personality, hobbies, interests, and current work or study.<br>
<small><font color="#4B5563">🎵 IPA: /raɪt ən ɪnˈfɔːrməl ˈiːmeɪl rɪˈspɒndɪŋ tuː dʒeɪn. juː ʃʊd raɪt æt liːst wʌn ˈhʌndrəd ənd ˈtwɛnti wɜːrdz./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI TASK 1: Bạn nhận được email từ Jane hỏi thông tin về bạn của bạn tên là An - người sắp tham gia khóa học ở Luân Đôn hè này và muốn ở cùng gia đình Jane. Hãy viết email kể về tính cách, sở thích và tình trạng học tập/làm việc của An.</font></i>""",
        "model_answer_raw": "Dear Jane, I am writing to respond to your email about my close friend, An. She is an exceptionally friendly, open-minded, and highly responsible person. In her free time, she is really keen on reading English novels and cooking traditional Vietnamese dishes, which your family will definitely find fascinating. Currently, she is studying diligently as a final-year student at university. I am fully confident that she will easily adapt and fit in with your family perfectly. Warmest regards.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: Dear Jane, I am writing to respond to your email about my close friend, An. She is an exceptionally friendly, open-minded, and highly responsible person. In her free time, she is really keen on reading English novels and cooking traditional Vietnamese dishes, which your family will definitely find fascinating. Currently, she is studying diligently as a final-year student at university. I am fully confident that she will easily adapt and fit in with your family perfectly. Warmest regards.<br>
<small><font color="#4B5563">🎵 IPA: /dɪər dʒeɪn, maɪ frɛnd æn ɪz ən ɪkˈsɛpʃənəli ˈfrɛndli ˈpɜːrsən.../ </font></small><br>
<i><font color="#059669">🇻🇳 VIE: Bài viết mẫu học thuộc: Jane thân mến, tôi viết thư này để trả lời email của bạn về An, người bạn thân của tôi. Cô ấy là một người cực kỳ thân thiện, cởi mở và có trách nhiệm cao. Khi rảnh rỗi, cô ấy rất thích đọc tiểu thuyết tiếng Anh và nấu các món ăn truyền thống của Việt Nam, điều mà gia đình bạn chắc chắn sẽ thấy thú vị. Hiện tại, cô ấy đang học tập chăm chỉ với tư cách là sinh viên năm cuối đại học. Tôi hoàn toàn tự tin rằng cô ấy sẽ dễ dàng thích nghi và hòa nhập hoàn hảo với gia đình bạn. Thân ái.</font></i>""",
        "analysis_html": """<b>[🧠 PHÂN TÍCH NGỮ PHÁP & CẤU TRÚC VIẾT]:</b><br>
• Cấu trúc nhấn mạnh tính từ: <i>"exceptionally friendly, open-minded, and highly responsible"</i> -> Sử dụng các trạng từ nâng cao (exceptionally, highly) giúp nâng điểm tiêu chí Lexical Resource.<br>
• Cấu trúc mệnh đề quan hệ không giới hạn: <i>", which your family will definitely find fascinating"</i> -> Thay thế cho cấu trúc chuyển ý đơn điệu, giúp tạo câu phức đạt chuẩn VSTEP bậc 4 và bậc 5."""
    },
    {
        "id": 2,
        "type": "TASK 2 - Essay Discussion (Time allowance: 40 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> TASK 2: Tourism has become one of the fastest growing industries in the world. Some people argue that the development of tourism has had negative effects on local communities; others think that its influences are positive. Discuss the effects of tourism on local communities.<br>
<small><font color="#4B5563">🎵 IPA: /raɪt ən ˈɛseɪ tuː ən ˈɛdʒʊkeɪtɪd ˈriːdər tuː dɪsˈkʌs ðə ɪˈfɛkts ɒv ˈtʊərɪzəm./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI TASK 2: Du lịch đã trở thành một trong những ngành phát triển nhanh nhất thế giới. Một số người cho rằng du lịch gây ảnh hưởng tiêu cực đến cộng đồng địa phương; số khác nghĩ nó mang lại tác động tích cực. Hãy viết bài văn nghị luận thảo luận về các tác động của du lịch đối với cộng đồng.</font></i>""",
        "model_answer_raw": "It is widely believed that tourism expansion brings significant benefits, while others voice concerns over its adverse impacts on local residents. On the positive side, tourism acts as a powerful economic catalyst. It generates employment opportunities in hospitality and retail, boosting household incomes. Furthermore, it fosters cultural exchange, encouraging authorities to preserve historical landmarks. On the negative side, mass tourism often triggers environmental degradation and overcrowding. Rising prices of goods and housing can also place an immense financial burden on local inhabitants. In conclusion, while tourism poses certain challenges, its economic and cultural advantages are undeniable if managed sustainably.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Model Answer: It is widely believed that tourism expansion brings significant benefits, while others voice concerns over its adverse impacts on local residents...<br>
<small><font color="#4B5563">🎵 IPA: /ɪt ɪz ˈwaɪdli bɪˈliːvd ðæt ˈtʊərɪzəm ɪkˈspænʃən brɪŋz sɪɡˈnɪfɪkənt ˈbɛnɪfɪts.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Bài mẫu học thuộc: Người ta tin rằng sự mở rộng du lịch mang lại lợi ích lớn, trong khi số khác lo ngại về tác động tiêu cực đối với cư dân. Về mặt tích cực, du lịch là chất xúc tác kinh tế mạnh mẽ. Nó tạo ra việc làm trong ngành dịch vụ và bán lẻ, nâng cao thu nhập. Hơn nữa, nó thúc đẩy giao lưu văn hóa, khuyến khích bảo tồn di tích. Về mặt tiêu cực, du lịch đại chúng gây suy thoái môi trường và quá tải. Giá cả hàng hóa và nhà ở tăng cao cũng đặt gánh nặng tài chính lên người dân. Kết luận, dù du lịch đặt ra thách thức, lợi ích kinh tế và văn hóa là không thể phủ nhận nếu được quản lý bền vững.</font></i>""",
        "analysis_html": """<b>[🧠 PHÂN TÍCH NGỮ PHÁP & CẤU TRÚC NGHỊ LUẬN]:</b><br>
• Cấu trúc câu bị động khách quan mở bài: <i>"It is widely believed that..."</i> -> Thường dùng để dẫn dắt vấn đề một cách khách quan, trang trọng.<br>
• Từ nối chuyển ý tương phản cao cấp: <i>"acts as a powerful economic catalyst"</i> (đóng vai trò là chất xúc tác kinh tế mạnh mẽ), <i>"triggers environmental degradation"</i> (gây ra sự suy thoái môi trường)."""
    }
]

VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"] = [
    {
        "id": 1,
        "type": "Part 1: Social Interaction (Time: 3 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Part 1: Let's talk about your free time activities. What do you often do in your free time? Do you watch TV or read books? Why? Let's talk about your neighborhood. Can you tell me something about it?<br>
<small><font color="#4B5563">🎵 IPA: /lɛts tɔːk əˈbaʊt jɔːr friː taɪm ækˈtɪvətiz.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI NÓI PHẦN 1: Hãy trò chuyện về các hoạt động lúc rảnh rỗi của bạn. Bạn thường làm gì? Bạn thích xem TV hay đọc sách hơn? Tại sao? Tiếp theo, hãy giới thiệu đôi nét về khu phố nơi bạn đang sinh sống.</font></i>""",
        "model_answer_raw": "In my free time, I honestly prefer reading books to watching television. The main reason is that reading books helps widen my practical knowledge and effectively reduces stress after long hours of hard working. Regarding my neighborhood, it is a very peaceful and friendly place located in the suburban area. What I like most about it is the strong sense of community, where neighbors always support each other.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Speaking Response: In my free time, I honestly prefer reading books to watching television. The main reason is that reading books helps widen my practical knowledge and effectively reduces stress after long hours of hard working. Regarding my neighborhood, it is a very peaceful and friendly place located in the suburban area. What I like most about it is the strong sense of community, where neighbors always support each other.<br>
<small><font color="#4B5563">🎵 IPA: /ɪn maɪ friː taɪm, aɪ ˈɒnɪstli prɪˈfɜːr riːdɪŋ bʊks tuː ˈwɒtʃɪŋ ˈtɛlɪˌvɪʒən.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu trả lời mẫu học thuộc: Vào thời gian rảnh, tôi thực sự thích đọc sách hơn xem ti vi. Lý do chính là đọc sách giúp tôi mở rộng kiến thức thực tế và giảm căng thẳng hiệu quả sau những giờ làm việc vất vả. Về khu phố của tôi, đó là một nơi rất yên bình và thân thiện nằm ở vùng ngoại ô. Điều tôi thích nhất ở đây là tinh thần cộng đồng mạnh mẽ, nơi những người hàng xóm luôn sẵn sàng giúp đỡ lẫn nhau.</font></i>"""
    },
    {
        "id": 2,
        "type": "Part 2: Solution Discussion (Time: 4 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Part 2: Situation: A group of people is planning a trip from Danang to Hanoi. Three means of transport are suggested: by train, by plane, and by coach. Which means of transport do you think is the best choice?<br>
<small><font color="#4B5563">🎵 IPA: /θriː miːnz ɒv ˈtrænspɔːrt ɑːr səˈdʒɛstɪd: baɪ treɪn, baɪ pleɪn, ənd baɪ koʊtʃ./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI NÓI PHẦN 2: Tình huống: Một nhóm người đang lập kế hoạch đi du lịch từ Đà Nẵng ra Hà Nội. Ba phương tiện được đề xuất bao gồm: tàu hỏa, máy bay, và xe khách. Bạn nghĩ phương tiện nào là sự lựa chọn tối ưu nhất?</font></i>""",
        "model_answer_raw": "In my opinion, traveling by plane is the best choice among the three options. First and foremost, flying is extremely time-saving, taking only about one hour compared to half a day by train or coach. This allows the group to maximize their sightseeing time in Hanoi. Although plane tickets are more expensive, the comfort and speed it offers outweigh the financial cost. Therefore, I highly recommend going by plane.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Speaking Response: In my opinion, traveling by plane is the best choice among the three options. First and foremost, flying is extremely time-saving, taking only about one hour...<br>
<small><font color="#4B5563">🎵 IPA: /ɪn maɪ əˈpɪnjən, ˈtrævəlɪŋ baɪ pleɪn ɪz ðə bɛst tʃɔɪs.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu trả lời mẫu học thuộc: Theo tôi, đi du lịch bằng máy bay là lựa chọn tốt nhất trong ba phương án. Trước hết, việc bay cực kỳ tiết kiệm thời gian, chỉ mất khoảng một giờ so với nửa ngày nếu đi bằng tàu hỏa hoặc xe khách. Điều này cho phép nhóm tối đa hóa thời gian tham quan tại Hà Nội. Mặc dù vé máy bay đắt hơn, nhưng sự thoải mái và tốc độ mà nó mang lại vượt trội hơn chi phí tài chính. Vì vậy, tôi khuyên nên đi bằng máy bay.</font></i>"""
    },
    {
        "id": 3,
        "type": "Part 3: Topic Development (Time: 5 minutes)",
        "prompt_html": """<b><font color="#1E3A8A">ENG:</font></b> Part 3: Topic: Reading habit should be encouraged among teenagers. Ideas: Increases knowledge, reduces stress, improves memory. Follow-up: What is the difference between kinds of books read by your parents' generation and yours?<br>
<small><font color="#4B5563">🎵 IPA: /ˈriːdɪŋ ˈhæbɪt ʃʊd biː ɪnˈkʌrɪdʒd əˈmʌŋ ˈtiːnˌeɪdʒərz./</font></small><br>
<i><font color="#059669">🇻🇳 VIE: ĐỀ BÀI NÓI PHẦN 3: Chủ đề: Thói quen đọc sách nên được khuyến khích trong giới trẻ. Các ý gợi ý: Tăng kiến thức, giảm căng thẳng, cải thiện trí nhớ. Câu hỏi mở rộng: Sự khác biệt giữa các loại sách mà thế hệ cha mẹ bạn đọc và thế hệ của bạn đọc là gì?</font></i>""",
        "model_answer_raw": "I firmly believe that developing a reading habit is crucial for teenagers for several reasons. Firstly, it substantially increases their academic and life knowledge. Secondly, immersing oneself in a good book effectively reduces mental stress. Lastly, reading stimulates brain activities, which directly improves memory. Regarding the generation gap, my parents mostly read historical novels and hard-copy books, while my generation prefers digital ebooks, comic books, and self-development materials online.",
        "model_answer_html": """<b><font color="#1E3A8A">ENG:</font></b> Speaking Response: I firmly believe that developing a reading habit is crucial for teenagers for several reasons. Firstly, it substantially increases their knowledge...<br>
<small><font color="#4B5563">🎵 IPA: /aɪ ˈfɜːrmli bɪˈliːv ðæt dɪˈvɛləpɪŋ ə ˈriːdɪŋ ˈhæbɪt ɪz ˈkruːʃəl.../</font></small><br>
<i><font color="#059669">🇻🇳 VIE: Câu trả lời mẫu học thuộc: Tôi tin chắc rằng việc phát triển thói quen đọc sách là vô cùng quan trọng đối với thanh thiếu niên vì một vài lý do. Thứ nhất, nó làm tăng đáng kể kiến thức học tập và đời sống của họ. Thứ hai, đắm mình vào một cuốn sách hay giúp giảm căng thẳng tinh thần hiệu quả. Cuối cùng, việc đọc kích thích các hoạt động của não bộ, giúp cải thiện trực tiếp trí nhớ. Về khoảng cách thế hệ, cha mẹ tôi hầu như đọc tiểu thuyết lịch sử và sách in giấy, trong khi thế hệ của tôi ưa chuộng sách điện tử kỹ thuật số, truyện tranh và các tài liệu phát triển bản thân trực tuyến.</font></i>"""
    }
]

# TỰ ĐỘNG CHÂN PHƯƠNG HÓA SANG CÁC MÃ ĐỀ B, C, D ĐỂ ĐẢM BẢO ĐỒNG BỘ 4 MÃ ĐỀ KHÔNG BỊ KHUYẾT TẬP DỮ LIỆU
for letter in ["B", "C", "D"]:
    de_key_name = f"Mã đề VSTEP-2026-{letter} (Biến Thể Song Song {['B','C','D'].index(letter)+1})"
    if de_key_name in VSTEP_MASTER_DATABASE:
        VSTEP_MASTER_DATABASE[de_key_name]["3️⃣ VSTEP Viết"] = VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["3️⃣ VSTEP Viết"]
        VSTEP_MASTER_DATABASE[de_key_name]["4️⃣ VSTEP Nói"] = VSTEP_MASTER_DATABASE["Mã đề VSTEP-2026-A (Đề Minh Họa Gốc)"]["4️⃣ VSTEP Nói"]

# --- KHỞI CHẠY GIAO DIỆN PHÒNG THI SỐ HÓA ---
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
current_de_idx = DE_LIST_KEYS.index(st.session_state.selected_de)
chosen_de = st.sidebar.selectbox("Chọn Đề thi thực chiến:", DE_LIST_KEYS, index=current_de_idx)
if chosen_de != st.session_state.selected_de:
    st.session_state.selected_de = chosen_de
    st.session_state.current_q_idx = 0
    st.rerun()

# NÚT CHUYỂN ĐỀ THÔNG MINH
current_de_pos = DE_LIST_KEYS.index(st.session_state.selected_de)
if current_de_pos < len(DE_LIST_KEYS) - 1:
    if st.button("🎉 THÀNH THẠO ĐỀ NÀY RỒI ── BẤM ĐỂ CHUYỂN SANG MÃ ĐỀ TIẾP THEO MỨC ĐỘ TIẾP THEO 🚀", use_container_width=True):
        st.session_state.selected_de = DE_LIST_KEYS[current_de_pos + 1]
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

if max_questions > 0:
    st.sidebar.markdown("### 🎯 PHÍM CHỌN CÂU NHANH")
    slots = st.sidebar.columns(max_questions)
    for i in range(max_questions):
        with slots[i]:
            lbl = f"*{i+1}*" if i == st.session_state.current_q_idx else f"{i+1}"
            if st.button(lbl, key=f"qk_nav_{i}", use_container_width=True):
                st.session_state.current_q_idx = i; st.rerun()

st.title("🎓 HỆ THỐNG KHẢO SÁT NĂNG LỰC TIẾNG ANH VSTEP CHUẨN SƯ PHẠM")
st.caption(f"Đang vận hành mã đề: {st.session_state.selected_de}")
st.markdown("---")

if max_questions == 0:
    st.info("Đang nạp dữ liệu phân hệ...")
else:
    active_q = questions_list[st.session_state.current_q_idx]
    q_key = f"{st.session_state.selected_de}_{st.session_state.current_section}_{active_q['id']}"

    # LẬP TRÌNH ĐỒNG BỘ HIỂN THỊ PHẦN TỰ LUẬN TĨNH HOÀN TOÀN
    if st.session_state.current_section in ["3️⃣ VSTEP Viết", "4️⃣ VSTEP Nói"]:
        st.warning(f"📊 **Yêu cầu phân hệ khảo sát tự luận ({active_q['type']}):**")
        st.markdown(active_q["prompt_html"], unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🏆 ĐÁP ÁN MẪU KHUYÊN DÙNG ĐỂ HỌC THUỘC LÒNG THỰC CHIẾN:")
        st.markdown(active_q["model_answer_html"], unsafe_allow_html=True)
        
        st.info("🎵 **Nút phát âm mẫu bài thi tự luận - Bấm để luyện nghe ngữ điệu chuẩn hóa:**")
        tts_auto = gTTS(text=active_q["model_answer_raw"], lang='en', tld='com')
        fp_auto = io.BytesIO()
        tts_auto.write_to_fp(fp_auto)
        fp_auto.seek(0)
        st.audio(fp_auto, format="audio/mp3")
        
        if "analysis_html" in active_q:
            st.markdown("---")
            st.markdown(active_q["analysis_html"], unsafe_allow_html=True)
    else:
        # LUỒNG TRẮC NGHIỆM ĐỒNG BỘ
        if st.session_state.current_section == "1️⃣ VSTEP Nghe":
            st.info("🎧 **Nội dung nghe ghi âm mẫu chuyên nghiệp:**")
            tts_m = gTTS(text=active_q["raw_script"], lang='en', tld='com')
            fp_m = io.BytesIO()
            tts_m.write_to_fp(fp_m)
            fp_m.seek(0)
            st.audio(fp_m, format="audio/mp3")
        st.markdown(active_q["question_html"], unsafe_allow_html=True)
