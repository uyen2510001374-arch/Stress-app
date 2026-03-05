import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Cấu hình trang
st.set_page_config(page_title="Phân tích Stress Toàn diện", page_icon="🧠", layout="wide")

# Load dữ liệu và huấn luyện mô hình
@st.cache_resource
def train_model():
    df = pd.read_csv('StressLevelDataset.csv')
    X = df.drop('stress_level', axis=1)
    y = df['stress_level']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, X.columns

model, feature_names = train_model()

st.title("🧠 Công cụ Dự báo & Phân tích Mức độ Căng thẳng")
st.markdown("Hệ thống sẽ phân tích dựa trên **20 chỉ số tâm - sinh lý** của bạn.")

# Tạo 4 cột để chia nhóm các chỉ số
st.header("📋 Nhập thông tin chi tiết")
tab1, tab2, tab3, tab4 = st.tabs(["🧘 Tâm lý", "🩺 Sinh lý", "🌍 Môi trường & Xã hội", "🏫 Học tập"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        anxiety = st.slider("Mức độ lo âu (0-21)", 0, 21, 10)
        depression = st.slider("Mức độ trầm cảm (0-27)", 0, 27, 10)
    with col2:
        self_esteem = st.slider("Lòng tự trọng (0-30)", 0, 30, 20)
        mental_history = st.selectbox("Tiền sử sức khỏe tâm thần", [0, 1], format_func=lambda x: "Có" if x==1 else "Không")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("Chất lượng giấc ngủ (0-5)", 0, 5, 3)
        headache = st.slider("Tần suất đau đầu (0-5)", 0, 5, 1)
    with col2:
        bp = st.slider("Chỉ số huyết áp (1-3)", 1, 3, 2)
        breathing = st.slider("Vấn đề hô hấp (0-5)", 0, 5, 1)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        noise = st.slider("Mức độ tiếng ồn (0-5)", 0, 5, 2)
        living = st.slider("Điều kiện sống (0-5)", 0, 5, 3)
        safety = st.slider("Cảm giác an toàn (0-5)", 0, 5, 4)
        basic_needs = st.slider("Đáp ứng nhu cầu cơ bản (0-5)", 0, 5, 3)
    with col2:
        social_support = st.slider("Hỗ trợ xã hội (0-3)", 0, 3, 2)
        peer_pressure = st.slider("Áp lực từ bạn bè (0-5)", 0, 5, 2)
        bullying = st.slider("Mức độ bị bắt nạt (0-5)", 0, 5, 0)
        extracurricular = st.slider("Hoạt động ngoại khóa (0-5)", 0, 5, 2)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        academic = st.slider("Kết quả học tập (0-5)", 0, 5, 3)
        study_load = st.slider("Khối lượng học tập (0-5)", 0, 5, 2)
    with col2:
        teacher_rel = st.slider("Mối quan hệ với giáo viên (0-5)", 0, 5, 3)
        future_career = st.slider("Lo lắng nghề nghiệp tương lai (0-5)", 0, 5, 2)

# Gom tất cả input vào 1 mảng theo đúng thứ tự của file CSV
user_input = [
    anxiety, self_esteem, mental_history, depression, headache, bp, sleep,
    breathing, noise, living, safety, basic_needs, academic, study_load,
    teacher_rel, future_career, social_support, peer_pressure, extracurricular, bullying
]

st.divider()

if st.button("🚀 BẮT ĐẦU DỰ BÁO", use_container_width=True):
    prediction = model.predict([user_input])[0]
    prob = model.predict_proba([user_input])
    
    levels = {0: "THẤP (An toàn) ✅", 1: "TRUNG BÌNH (Cần chú ý) ⚠️", 2: "CAO (Nguy hiểm) 🚨"}
    
    # Hiển thị kết quả nổi bật
    st.markdown(f"<h1 style='text-align: center;'>Mức độ Stress: {levels[prediction]}</h1>", unsafe_allow_html=True)
    
    # Đưa ra lời khuyên chi tiết
    st.subheader("💡 Lời khuyên dựa trên các chỉ số của bạn:")
    if prediction == 2:
        st.error("- Bạn nên ưu tiên nghỉ ngơi và tìm kiếm sự hỗ trợ từ chuyên gia tâm lý hoặc người thân ngay lập tức.")
    elif prediction == 1:
        st.warning("- Hãy cân bằng lại thời gian học tập và nghỉ ngơi. Tham gia các hoạt động ngoại khóa để giải tỏa căng thẳng.")
    else:
        st.success("- Bạn đang duy trì trạng thái tâm lý rất tốt. Hãy tiếp tục lối sống lành mạnh này!")

    if sleep < 3:
        st.info("👉 Gợi ý: Chất lượng giấc ngủ của bạn hơi thấp. Hãy thử cải thiện môi trường ngủ và ngủ đủ giấc hơn.")
