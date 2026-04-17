import streamlit as st
import cv2
from pathlib import Path
from core.database import add_student
from core.face_engine import train_model

st.set_page_config(page_title="Register Student", layout="wide")
st.title("📸 Register New Student")

with st.form("reg_form"):
    col1, col2 = st.columns(2)
    roll  = col1.text_input("Roll Number *")
    name  = col1.text_input("Full Name *")
    branch = col2.selectbox("Branch", ["CSE","ECE","ME","CE","EE","IT"])
    email = col2.text_input("Email")
    submitted = st.form_submit_button("Next → Capture Face")

if submitted:
    if not roll or not name:
        st.error("Roll number and name are required.")
    else:
        st.session_state["reg_roll"]  = roll
        st.session_state["reg_name"]  = name
        st.session_state["reg_branch"] = branch
        st.session_state["reg_email"] = email
        st.success(f"Details saved for {name}. Now capture face images below.")

# ---- Face Capture Section ----
if "reg_roll" in st.session_state:
    roll = st.session_state["reg_roll"]
    name = st.session_state["reg_name"]

    save_dir = Path(f"dataset/{roll}")
    save_dir.mkdir(parents=True, exist_ok=True)

    st.subheader(f"📷 Capture Face Images for {name} ({roll})")
    st.info("Capture at least **5 images** from different angles for best accuracy.")

    img_file = st.camera_input("Take a photo")

    existing = list(save_dir.glob("*.jpg"))
    st.write(f"Images captured so far: **{len(existing)}**")

    if img_file:
        import time
        img_path = save_dir / f"img_{int(time.time())}.jpg"
        img_path.write_bytes(img_file.getvalue())
        st.success(f"Image saved! ({len(existing)+1} total)")

    if len(existing) >= 5:
        if st.button("✅ Save Student & Train Model"):
            add_student(roll, name,
                        st.session_state["reg_branch"],
                        st.session_state["reg_email"])
            with st.spinner("Training model... this may take a minute."):
                count = train_model()
            st.success(f"🎉 {name} registered! Model trained on {count} encodings.")
            for k in ["reg_roll","reg_name","reg_branch","reg_email"]:
                del st.session_state[k]