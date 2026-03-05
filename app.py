import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Khảo sát Căng thẳng", page_icon="🧠", layout="centered")

# 2. HUẤN LUYỆN MÔ HÌNH
@st.cache_resource
def train_model():
    df = pd.read_csv('StressLevelDataset.csv')
    X = df.drop('stress_level', axis=1)
    y = df['stress_level']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_model()

# 3. GIAO DIỆN CHÍNH
st.title("📊 Bảng Khảo sát & Dự báo Stress")
st.markdown("""
Chào mừng bạn đến với công cụ đánh giá tâm - sinh lý. 
Vui lòng đánh giá các chỉ số dưới đây theo thang điểm từ **0 đến 10**.
""")

# 4. BẢNG HƯỚNG DẪN MỨC ĐỘ
st.info("""
**📖 HƯỚNG DẪN ĐÁNH GIÁ (Thang điểm 0 - 10):**
*   **0 - 3 (Thấp/Tốt):** Trạng thái rất ổn định, không có vấn đề hoặc mức độ rất nhẹ.
*   **4 - 7 (Trung bình):** Bắt đầu có sự ảnh hưởng rõ rệt đến cuộc sống hàng ngày.
*   **8 - 10 (Cao/Nghiêm trọng):** Ảnh hưởng cực kỳ lớn, mức độ rất nặng hoặc diễn ra liên tục.
""")

st.divider()

# 5. DANH SÁCH 20 CHỈ SỐ KHẢO SÁT (Trên cùng 1 trang)
st.subheader("📝 Nội dung khảo sát")

# Hàm tạo slider 0-10 nhanh
def stress_slider(label, help_text):
    return st.slider(label, 0, 10, 5, help=help_text)

# Nhóm 1: Tâm lý
st.markdown("#### 🧘 Nhóm Tâm lý & Cảm xúc")
anxiety_u = stress_slider("1. Mức độ lo âu", "Cảm giác lo lắng, bồn chồn về các vấn đề trong cuộc sống.")
depression_u = stress_slider("2. Mức độ trầm cảm", "Cảm giác buồn bã, mất hứng thú hoặc tuyệt vọng.")
self_esteem_u = st.slider("3. Lòng tự trọng (0 là thấp, 10 là rất tự tin)", 0, 10, 5, help="Sự tự tin và đánh giá về giá trị bản thân.")
mental_history_u = st.radio("4. Bạn có tiền sử vấn đề sức khỏe tâm thần không?", ["Không", "Có"])

# Nhóm 2: Sinh lý
st.markdown("#### 🩺 Nhóm Sức khỏe Sinh lý")
sleep_u = st.slider("5. Chất lượng giấc ngủ (0 là rất tệ, 10 là cực tốt)", 0, 10, 5)
headache_u = stress_slider("6. Tần suất đau đầu", "Mức độ thường xuyên và cường độ đau đầu.")
bp_u = stress_slider("7. Chỉ số huyết áp", "Đánh giá mức độ bất thường của huyết áp.")
breathing_u = stress_slider("8. Vấn đề về hô hấp", "Khó thở hoặc nhịp thở không đều khi stress.")

# Nhóm 3: Môi trường & Xã hội
st.markdown("#### 🌍 Nhóm Môi trường & Xã hội")
noise_u = stress_slider("9. Mức độ ô nhiễm tiếng ồn", "Tiếng ồn nơi ở hoặc nơi làm việc/học tập.")
living_u = st.slider("10. Điều kiện sống (0 là tệ, 10 là rất tốt)", 0, 10, 5)
safety_u = st.slider("11. Cảm giác an toàn (0 là sợ hãi, 10 là rất an toàn)", 0, 10, 5)
basic_needs_u = st.slider("12. Đáp ứng nhu cầu cơ bản (Ăn, mặc, ở...)", 0, 10, 5)
social_support_u = st.slider("13. Sự hỗ trợ từ xã hội (Gia đình, bạn bè...)", 0, 10, 5)
peer_pressure_u = stress_slider("14. Áp lực từ bạn bè/đồng lứa", "Cảm giác phải chạy đua theo người khác.")
bullying_u = stress_slider("15. Tần suất bị bắt nạt/công kích", "Bị đe dọa hoặc làm phiền bởi người khác.")
extracurricular_u = st.slider("16. Hoạt động ngoại khóa (Giải trí, thể thao...)", 0, 10, 5)

# Nhóm 4: Học tập
st.markdown("#### 🏫 Nhóm Học tập & Sự nghiệp")
academic_u = st.slider("17. Kết quả học tập/Làm việc (0 là rất tệ, 10 là xuất sắc)", 0, 10, 5)
study_load_u = stress_slider("18. Khối lượng bài vở/Công việc", "Khối lượng công việc bạn phải gánh vác.")
teacher_rel_u = st.slider("19. Mối quan hệ với Thầy cô/Cấp trên (0 là tệ, 10 là tốt)", 0, 10, 5)
future_career_u = stress_slider("20. Lo lắng về nghề nghiệp tương lai", "Nỗi sợ hoặc băn khoăn về sự nghiệp.")

# 6. QUY ĐỔI THANG ĐIỂM (Mapping 0-10 về thang gốc của Dataset)
# Công thức: (giá trị_người_dùng / 10) * max_thang_gốc
anxiety = anxiety_u * 2.1
self_esteem = self_esteem_u * 3.0
mental_history = 1 if mental_history_u == "Có" else 0
depression = d
