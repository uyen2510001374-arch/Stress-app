import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Khảo sát & Tư vấn Stress", page_icon="🧠", layout="centered")

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
st.title("📊 Khảo sát & Tư vấn Mức độ Stress")
st.markdown("""
**Hướng dẫn:** Đánh giá từ **0** (Tốt nhất) đến **10** (Tệ nhất).
Hệ thống sẽ dựa trên 20 chỉ số để đưa ra dự báo và lời khuyên phù hợp.
""")

st.divider()

# 4. DANH SÁCH 20 CHỈ SỐ KHẢO SÁT
st.subheader("📝 Nội dung khảo sát")

# --- NHÓM 1: Tâm lý & Sinh lý ---
st.markdown("#### 🧘 Nhóm Tâm lý & Sinh lý")
anxiety_u = st.slider("1. Mức độ lo âu (0: Bình tĩnh, 10: Rất lo sợ)", 0, 10, 0)
depression_u = st.slider("2. Mức độ trầm cảm (0: Vui vẻ, 10: Tuyệt vọng)", 0, 10, 0)
headache_u = st.slider("3. Tần suất đau đầu (0: Không đau, 10: Đau liên tục)", 0, 10, 0)
bp_u = st.slider("4. Vấn đề huyết áp (0: Ổn định, 10: Rất bất thường)", 0, 10, 0)
breathing_u = st.slider("5. Khó khăn khi thở (0: Dễ thở, 10: Hay bị hụt hơi)", 0, 10, 0)

# --- NHÓM 2: Sức khỏe & Niềm tin (Nghịch đảo logic cho AI) ---
self_esteem_u = st.slider("6. Sự thiếu tự tin (0: Rất tự tin, 10: Rất tự ti)", 0, 10, 0)
sleep_u = st.slider("7. Vấn đề giấc ngủ (0: Ngủ ngon, 10: Mất ngủ)", 0, 10, 0)
living_u = st.slider("8. Điều kiện sống tệ (0: Rất tốt, 10: Rất kém)", 0, 10, 0)
safety_u = st.slider("9. Cảm giác mất an toàn (0: Rất an toàn, 10: Rất nguy hiểm)", 0, 10, 0)
basic_needs_u = st.slider("10. Thiếu hụt nhu cầu cơ bản (0: Đầy đủ, 10: Rất thiếu thốn)", 0, 10, 0)
social_support_u = st.slider("11. Thiếu hỗ trợ xã hội (0: Được hỗ trợ tốt, 10: Cô độc)", 0, 10, 0)
academic_u = st.slider("12. Kết quả học tập kém (0: Học rất tốt, 10: Học rất tệ)", 0, 10, 0)
teacher_rel_u = st.slider("13. Quan hệ với thầy cô tệ (0: Rất tốt, 10: Rất xung đột)", 0, 10, 0)

# --- NHÓM 3: Môi trường & Áp lực xã hội ---
st.markdown("#### 🌍 Môi trường & Áp lực xã hội")
noise_u = st.slider("14. Mức độ tiếng ồn (0: Yên tĩnh, 10: Quá ồn ào)", 0, 10, 0)
peer_pressure_u = st.slider("15. Áp lực từ bạn bè (0: Không có, 10: Rất áp lực)", 0, 10, 0)
bullying_u = st.slider("16. Mức độ bị bắt nạt (0: Không bị, 10: Thường xuyên bị)", 0, 10, 0)
study_load_u = st.slider("17. Khối lượng bài vở (0: Nhẹ nhàng, 10: Quá tải)", 0, 10, 0)
future_career_u = st.slider("18. Lo lắng nghề nghiệp (0: Tự tin, 10: Rất mông lung)", 0, 10, 0)
extracurricular_u = st.slider("19. Áp lực ngoại khóa (0: Thoải mái, 10: Kiệt sức)", 0, 10, 0)
mental_history_u = st.radio("20. Có tiền sử vấn đề tâm lý không?", ["Không", "Có"])

# 5. QUY ĐỔI LOGIC CHO MÔ HÌNH
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

# Nhóm nghịch đảo (Vì 0 bạn nhập là Tốt, nên máy phải nhận 10 là Tốt)
self_esteem = (10 - self_esteem_u) * 3.0
sleep = (10 - sleep_u) * 0.5
living = (10 - living_u) * 0.5
safety = (10 - safety_u) * 0.5
basic_needs = (10 - basic_needs_u) * 0.5
social_support = (10 - social_support_u) * 0.3
academic = (10 - academic_u) * 0.5
teacher_rel = (10 - teacher_rel_u) * 0.5

# 6. DỰ BÁO VÀ LỜI KHUYÊN
st.divider()
if st.button("🚀 XEM KẾT QUẢ & LỜI KHUYÊN", use_container_width=True):
    features = [[
        anxiety, self_esteem, mental_history, depression, headache, bp, sleep,
        breathing, noise, living, safety, basic_needs, academic, study_load,
        teacher_rel, future_career, social_support, peer_pressure, extra_act, bullying
    ]]
    
    pred = model.predict(features)[0]
    
    # --- PHẦN 1: KẾT QUẢ CHUNG ---
    st.subheader("🔍 Kết quả dự báo:")
    if pred == 0:
        st.success("### Mức độ Stress: THẤP ✅")
        st.write("**Trạng thái tâm lý của bạn rất tốt!** Hãy tiếp tục duy trì lối sống lành mạnh này.")
        st.balloons()
    elif pred == 1:
        st.warning("### Mức độ Stress: TRUNG BÌNH ⚠️")
        st.write("**Hãy chú ý cân bằng giữa học tập và nghỉ ngơi.** Bạn đang có dấu hiệu mệt mỏi.")
    else:
        st.error("### Mức độ Stress: CAO 🚨")
        st.write("**Bạn nên nghỉ ngơi và tham vấn ý kiến chuyên gia ngay lập tức.** Sức khỏe của bạn đang ở ngưỡng báo động.")

    # --- PHẦN 2: LỜI KHUYÊN CHI TIẾT THEO CHỈ SỐ ---
    st.subheader("💡 Lời khuyên dành riêng cho bạn:")
    
    # Kiểm tra từng nhóm chỉ số để đưa ra lời khuyên (nếu người dùng nhập điểm > 7)
    has_advice = False
    
    if sleep_u > 7:
        st.info("🌙 **Giấc ngủ:** Bạn đang gặp vấn đề về giấc ngủ. Hãy thử tắt điện thoại trước khi ngủ 30 phút và ngâm chân nước ấm nhé.")
        has_advice = True
        
    if anxiety_u > 7 or depression_u > 7:
        st.info("🧘 **Tâm lý:** Cảm xúc lo âu/trầm cảm của bạn khá cao. Hãy thử các bài tập hít thở sâu hoặc tâm sự với người bạn tin tưởng nhất.")
        has_advice = True
        
    if study_load_u > 7 or academic_u > 7:
        st.info("📚 **Học tập:** Áp lực bài vở đang quá tải. Hãy chia nhỏ mục tiêu theo phương pháp Pomodoro để giảm áp lực nhé.")
        has_advice = True

    if bullying_u > 5:
        st.info("🤝 **Mối quan hệ:** Có vẻ bạn đang gặp vấn đề với người xung quanh. Đừng im lặng, hãy tìm kiếm sự bảo vệ từ người thân hoặc thầy cô.")
        has_advice = True

    if not has_advice and pred == 0:
        st.write("Mọi chỉ số của bạn đều đang ở mức lý tưởng. Tuyệt vời!")
