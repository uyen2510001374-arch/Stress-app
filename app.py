import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Cấu hình trang
st.set_page_config(page_title="Dự báo Stress", page_icon="🧠")

# Load dữ liệu và huấn luyện mô hình
@st.cache_resource
def train_model():
    df = pd.read_csv('StressLevelDataset.csv')
    X = df.drop('stress_level', axis=1)
    y = df['stress_level']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_model()

st.title("🧠 Công cụ Dự báo Mức độ Căng thẳng")
st.write("Nhập các chỉ số bên dưới để xem kết quả dự báo.")

# Giao diện nhập liệu
col1, col2 = st.columns(2)
with col1:
    anxiety = st.number_input("Mức độ lo âu (0-21)", 0, 21, 10)
    depression = st.number_input("Mức độ trầm cảm (0-27)", 0, 27, 10)
    sleep = st.slider("Chất lượng giấc ngủ (0-5)", 0, 5, 3)
with col2:
    self_esteem = st.number_input("Lòng tự trọng (0-30)", 0, 30, 20)
    headache = st.slider("Tần suất đau đầu (0-5)", 0, 5, 1)
    academic = st.slider("Kết quả học tập (0-5)", 0, 5, 3)

if st.button("Dự báo kết quả"):
    # Tạo mảng input (các giá trị khác để mặc định trung bình 2)
    features = [[anxiety, self_esteem, 0, depression, headache, 2, sleep, 2, 2, 3, 3, 3, academic, 2, 3, 3, 2, 2, 2, 1]]
    pred = model.predict(features)[0]
    
    levels = {0: "THẤP (An toàn) ✅", 1: "TRUNG BÌNH (Cần chú ý) ⚠️", 2: "CAO (Nguy hiểm) 🚨"}
    st.subheader(f"Kết quả: {levels[pred]}")