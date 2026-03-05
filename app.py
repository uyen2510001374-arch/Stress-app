import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Khảo sát Stress chuẩn hóa", page_icon="🧠", layout="centered")

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

# 3. GIAO DIỆN
st.title("📊 Khảo sát Mức độ Căng thẳng (Chuẩn hóa)")
st.markdown("""
**Quy tắc đánh giá:**
*   **0 điểm:** Trạng thái lý tưởng (Tốt nhất, không stress).
*   **10 điểm:** Trạng thái tồi tệ nhất (Stress cực độ).
""")

st.divider()

# 4. DANH SÁCH 20 CHỈ SỐ
st.subheader("📝 Vui lòng đánh giá từ 0 đến 10")

# Nhóm thuận: Càng cao càng stress (Giữ nguyên logic 0 tốt, 10 tệ)
st.markdown("#### 🧘 Tâm lý & Sinh lý")
anxiety_u = st.slider("1. Mức độ lo âu (0: Bình tĩnh, 10: Rất lo sợ)", 0, 10, 0)
depression_u = st.slider("2. Mức độ trầm cảm (0: Vui vẻ, 10: Tuyệt vọng)", 0, 10, 0)
headache_u = st.slider("3. Tần suất đau đầu (0: Không đau, 10: Đau liên tục)", 0, 10, 0)
bp_u = st.slider("4. Vấn đề huyết áp (0: Ổn định, 10: Rất bất thường)", 0, 10, 0)
breathing_u = st.slider("5. Khó khăn khi thở (0: Dễ thở, 10: Hay bị hụt hơi)", 0, 10, 0)

# Nhóm nghịch: Trong data gốc 10 là tốt, nhưng người dùng nhập 0 là tốt -> Phải lấy (10 - giá trị nhập)
self_esteem_u = st.slider("6. Sự thiếu tự tin (0: Rất tự tin, 10: Rất tự ti)", 0, 10, 0)
sleep_u = st.slider("7. Vấn đề giấc ngủ (0: Ngủ ngon, 10: Mất ngủ)", 0, 10, 0)
living_u = st.slider("8. Điều kiện sống tệ (0: Rất tốt, 10: Rất kém)", 0, 10, 0)
safety_u = st.slider("9. Cảm giác mất an toàn (0: Rất an toàn, 10: Rất nguy hiểm)", 0, 10, 0)
basic_needs_u = st.slider("10. Thiếu hụt nhu cầu cơ bản (0: Đầy đủ, 10: Rất thiếu thốn)", 0, 10, 0)
social_support_u = st.slider("11. Thiếu hỗ trợ xã hội (0: Được hỗ trợ tốt, 10: Cô độc)", 0, 10, 0)
academic_u = st.slider("12. Kết quả học tập kém (0: Học rất tốt, 10: Học rất tệ)", 0, 10, 0)
teacher_rel_u = st.slider("13. Quan hệ với thầy cô tệ (0: Rất tốt, 10: Rất xung đột)", 0, 10, 0)

# Nhóm thuận tiếp theo
st.markdown("#### 🌍 Môi trường & Áp lực")
noise_u = st.slider("14. Mức độ tiếng ồn xung quanh", 0, 10, 0)
peer_pressure_u = st.slider("15. Áp lực từ bạn bè", 0, 10, 0)
bullying_u = st.slider("16. Mức độ bị bắt nạt", 0, 10, 0)
study_load_u = st.slider("17. Khối lượng bài vở", 0, 10, 0)
future_career_u = st.slider("18. Lo lắng nghề nghiệp", 0, 10, 0)
extracurricular_u = st.slider("19. Áp lực từ hoạt động ngoại khóa", 0, 10, 0)
mental_history_u = st.radio("20. Có tiền sử sức khỏe tâm thần không?", ["Không", "Có"])

# 5. QUY ĐỔI LOGIC (QUAN TRỌNG)
# Với các biến nghịch, mô hình cần số cao để báo Stress thấp. 
# Nhưng người dùng nhập 0 (Tốt), nên ta lấy (10 - 0) * hệ số = số cao.

anxiety = anxiety_u * 2.1
depression = depression_u * 2.7
headache = headache_u * 0.5
bp = 1 + (bp_u * 0.2)
breathing = breathing_u * 0.5
noise = noise_u * 0.5
peer_pressure = peer_pressure_u * 0.5
study_load = study_load_u * 0.5
future_career = future_career_u * 0.5
bullying = bullying_u * 0.5
extra_act = extracurricular_u * 0.5
mental_history = 1 if mental_history_u == "Có" else 0

# ĐẢO NGƯỢC CHO NHÓM NGHỊCH (Để khớp với dữ liệu máy học)
self_esteem = (10 - self_esteem_u) * 3.0
sleep = (10 - sleep_u) * 0.5
living = (10 - living_u) * 0.5
safety = (10 - safety_u) * 0.5
basic_needs = (10 - basic_needs_u) * 0.5
social_support = (10 - social_support_u) * 0.3
academic = (10 - academic_u) * 0.5
teacher_rel = (10 - teacher_rel_u) * 0.5

# 6. DỰ BÁO
st.divider()
if st.button("🚀 XEM KẾT QUẢ DỰ BÁO"):
    features = [[
        anxiety, self_esteem, mental_history, depression, headache, bp, sleep,
        breathing, noise, living, safety, basic_needs, academic, study_load,
        teacher_rel, future_career, social_support, peer_pressure, extra_act, bullying
    ]]
    
    prediction = model.predict(features)[0]
    
    if prediction == 0:
        st.success("### Mức độ Stress: THẤP ✅")
        st.balloons()
    elif prediction == 1:
        st.warning("### Mức độ Stress: TRUNG BÌNH ⚠️")
    else:
        st.error("### Mức độ Stress: CAO 🚨")
