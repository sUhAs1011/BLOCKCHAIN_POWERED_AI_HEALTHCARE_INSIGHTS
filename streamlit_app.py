import streamlit as st
import requests
import json

# API Base URL
BACKEND_URL = "http://127.0.0.1:5000"

# Enhanced page configuration
st.set_page_config(
    page_title="Healthcare AI Doctor Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1f77b4, #1565c0);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: white !important;
        font-size: 1.2rem;
        margin: 0;
        opacity: 0.95;
    }
    .section-header {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header h2 {
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    
    .section-header p {
        color: #333333;
        margin: 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Form styling for better visibility */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25) !important;
    }
    
    .stButton > button {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background-color: #1565c0 !important;
    }
    
    /* Better text contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1f77b4 !important;
    }
    
    p, label, span {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Healthcare AI Doctor Portal</h1>
    <p>Advanced AI-powered prescription analysis and patient risk assessment</p>
</div>
""", unsafe_allow_html=True)

# Session Management
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "doctor_id" not in st.session_state:
    st.session_state.doctor_id = None

# Enhanced Sidebar Navigation
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("---")

# Show login status
if st.session_state.access_token:
    st.sidebar.success("✅ **Logged In**")
    st.sidebar.info(f"👨‍⚕️ Doctor ID: {st.session_state.doctor_id}")
else:
    st.sidebar.warning("⚠️ **Not Logged In**")

page = st.sidebar.radio("Select Page:", [
    "🔐 Login", 
    "📤 Upload Prescription", 
    "📄 View Reports", 
    "📊 Dashboard", 
    "⚠️ Patient Risk Profile"
])

st.sidebar.markdown("---")

# 🔐 Login Page
if page == "🔐 Login":
    st.markdown("""
    <div class="section-header">
        <h2>🔐 Doctor Authentication</h2>
        <p>Please enter your credentials to access the healthcare portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("### Login Form")
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            if st.button("🚀 Login", type="primary", use_container_width=True):
                if username and password:
                    with st.spinner("🔐 Authenticating..."):
                        response = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.access_token = data["access_token"]
                            st.session_state.doctor_id = data["doctor_id"]
                            st.success("✅ **Login Successful!** Welcome to the Healthcare AI Portal.")
                            st.balloons()
                        else:
                            st.error("❌ **Authentication Failed!** Please check your credentials.")
                else:
                    st.warning("⚠️ Please fill in all fields.")

# 📤 Upload Prescription
elif page == "📤 Upload Prescription":
    if not st.session_state.access_token:
        st.warning("⚠️ **Authentication Required!** Please log in first to access this feature.")
    else:
        st.markdown("""
        <div class="section-header">
            <h2>📤 Prescription Upload & Analysis</h2>
            <p>Upload patient prescriptions for AI-powered analysis and DDI detection</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Upload Details")
            uploaded_file = st.file_uploader(
                "📄 Choose Prescription File", 
                type=["pdf", "png", "jpg", "jpeg"],
                help="Supported formats: PDF, PNG, JPG, JPEG"
            )
            patient_id = st.text_input("🆔 Patient ID", placeholder="Enter patient identifier")
            timestamp = st.text_input("🕒 Timestamp", placeholder="YYYY-MM-DD HH:MM:SS")
            
            if st.button("🚀 Submit for Analysis", type="primary", use_container_width=True):
                if uploaded_file and patient_id:
                    with st.spinner("🔍 Analyzing prescription..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                        data = {"patient_id": patient_id.strip(), "timestamp": timestamp}
                        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                        
                        response = requests.post(f"{BACKEND_URL}/upload_prescription", files=files, data=data, headers=headers)
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ **Prescription Analysis Complete!**")
                            
                            with col2:
                                st.markdown("### 📊 Analysis Results")
                                
                                # Extracted Text
                                st.markdown("**📝 Extracted Text:**")
                                st.text_area("", value=result.get('Extracted_Text', 'No text extracted'), height=150, disabled=True)
                                
                                # DDI Analysis
                                st.markdown("**⚠️ DDI Analysis:**")
                                st.text_area("", value=result.get("DDI Analysis", 'No DDI analysis available'), height=150, disabled=True)
                        else:
                            st.error("❌ **Analysis Failed!** Please try again or contact support.")
                else:
                    st.warning("⚠️ Please upload a file and enter patient ID.")

# 📄 View Reports
elif page == "📄 View Reports":
    if not st.session_state.access_token:
        st.warning("⚠️ **Authentication Required!** Please log in first to access this feature.")
    else:
        st.markdown("""
        <div class="section-header">
            <h2>📄 Patient Reports & History</h2>
            <p>Access comprehensive patient reports and prescription history</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### 🔍 Search")
            patient_id = st.text_input("🆔 Patient ID", placeholder="Enter patient ID")
            if st.button("📋 Get Reports", type="primary", use_container_width=True) and patient_id:
                with st.spinner("🔍 Fetching reports..."):
                    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                    response = requests.get(f"{BACKEND_URL}/get_prescriptions/{patient_id}", headers=headers)
                    
                    if response.status_code == 200:
                        reports = response.json().get("result", [])
                        if reports:
                            st.success(f"✅ Found {len(reports)} report(s)")
                            
                            with col2:
                                st.markdown("### 📊 Report Details")
                                for i, report in enumerate(reports, 1):
                                    data = json.loads(bytes.fromhex(report["data"]).decode())
                                    
                                    with st.expander(f"📋 Report #{i} - {data.get('timestamp', 'Unknown')}"):
                                        st.markdown(f"**🕒 Timestamp:** {data.get('timestamp', 'N/A')}")
                                        st.markdown(f"**🔗 IPFS Link:** [View on IPFS](https://ipfs.io/ipfs/{data.get('cid', 'N/A')})")
                                        st.markdown(f"**⚠️ DDI Analysis:** {data.get('ddi_analysis', 'N/A')}")
                        else:
                            st.info("ℹ️ No reports found for this patient.")
                    else:
                        st.error("❌ **Failed to fetch reports!** Please try again.")
            else:
                with col2:
                    st.info("🔍 Enter a Patient ID and click 'Get Reports' to view patient history.")

# 📊 Dashboard Page
elif page == "📊 Dashboard":
    if not st.session_state.access_token:
        st.warning("⚠️ **Authentication Required!** Please log in first to access this feature.")
    else:
        st.markdown("""
        <div class="section-header">
            <h2>📊 Doctor's Dashboard</h2>
            <p>Comprehensive overview of your prescription uploads and activities</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("📊 Loading dashboard data..."):
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            response = requests.get(f"{BACKEND_URL}/dashboard", headers=headers)
            
            if response.status_code == 200:
                uploads = response.json().get("uploads", [])
                
                # Dashboard Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📤 Total Uploads", len(uploads))
                with col2:
                    st.metric("👥 Patients", len(set(upload.get('Patient_ID', '') for upload in uploads)) if uploads else 0)
                with col3:
                    st.metric("📅 Active Sessions", "1" if st.session_state.access_token else "0")
                
                if not uploads:
                    st.info("ℹ️ **No uploads found.** Start by uploading your first prescription!")
                else:
                    st.markdown("### 📋 Recent Prescriptions")
                    for i, upload in enumerate(uploads):
                        with st.container():
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>📄 Prescription #{i+1}</h4>
                                <p><strong>👤 Patient ID:</strong> <code>{upload['Patient_ID']}</code></p>
                                <p><strong>🔗 File:</strong> <a href="https://ipfs.io/ipfs/{upload['CID']}" target="_blank">View on IPFS</a></p>
                                <p><strong>🕒 Uploaded:</strong> {upload['Timestamp']}</p>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.error("❌ **Failed to fetch dashboard data!** Please try again or contact support.")

# ⚠️ Patient Risk Profile
elif page == "⚠️ Patient Risk Profile":
    if not st.session_state.access_token:
        st.warning("⚠️ **Authentication Required!** Please log in first to access this feature.")
    else:
        st.markdown("""
        <div class="section-header">
            <h2>⚠️ Patient Risk Assessment</h2>
            <p>Generate comprehensive risk profiles for patients based on prescription history</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### 🔍 Risk Assessment")
            patient_id = st.text_input("🆔 Patient ID", placeholder="Enter patient ID")
            if st.button("⚠️ Generate Risk Profile", type="primary", use_container_width=True) and patient_id:
                with st.spinner("🔍 Analyzing patient risk..."):
                    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                    response = requests.get(f"{BACKEND_URL}/generate_patient_risk_profile/{patient_id}", headers=headers)
                    
                    if response.status_code == 200:
                        risk_profile = response.json().get("risk_profile")
                        st.success("✅ **Risk Profile Generated Successfully!**")
                        
                        with col2:
                            st.markdown("### 📊 Risk Assessment Results")
                            st.markdown(f"""
                            <div class="info-box">
                                <h4>⚠️ Patient Risk Profile</h4>
                                <p>{risk_profile}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("❌ **Failed to generate risk profile!** Please try again.")
            else:
                with col2:
                    st.info("🔍 Enter a Patient ID and click 'Generate Risk Profile' to assess patient risk factors.")

# Logout Button
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    if st.session_state.access_token:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        requests.post(f"{BACKEND_URL}/logout", headers=headers)
        st.session_state.access_token = None
        st.session_state.doctor_id = None
        st.success("✅ **Logged out successfully!** Redirecting to login...")
        st.rerun()
    else:
        st.warning("⚠️ You are not currently logged in.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏥 <strong>Healthcare AI Doctor Portal</strong> | Powered by Blockchain & AI Technology</p>
    <p>© 2024 Hash Bros Healthcare Solutions</p>
</div>
""", unsafe_allow_html=True)

