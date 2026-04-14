import streamlit as st
from core.database import init_db

st.set_page_config(
    page_title="Face Attendance System",
    page_icon="🎓",
    layout="wide"
)

init_db()

st.title("🎓 Face Recognition Attendance System")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.page_link("pages/1_📸_Register.py",    label="📸 Register Student",  icon="➕")
col2.page_link("pages/2_📷_Attendance.py",  label="📷 Take Attendance",   icon="✅")
col3.page_link("pages/3_📊_Dashboard.py",   label="📊 Dashboard",         icon="📈")
col4.page_link("pages/4_📁_Reports.py",     label="📁 Reports",           icon="📥")

st.info("Use the sidebar or buttons above to navigate.")