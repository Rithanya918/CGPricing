"""
CG Pricing Dashboard - Main Streamlit App
Updated with #8c1a12 background color
"""
import streamlit as st

# Import tab modules
from tabs import insights, alerts, pricing_engine, approvals
import tabs.login as login

# Page configuration
st.set_page_config(
    page_title="PricingIQ",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check if user is logged in
if not login.is_logged_in():
    login.render_login_page()
    st.stop()

# Get current user info
current_user = login.get_current_user()


# Custom CSS with #8c1a12 background
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background - #911717 */
    .main {
        background: #911717;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        padding: 0 !important;
        min-height: 100vh;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Custom Header Styling */
    .custom-header {
        background: #911717;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    /* Logo - PIQ with red P and white IQ */
    .company-logo {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
        width: 80px;
        height: 56px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: -1px;
        box-shadow: 0 8px 24px rgba(229, 115, 115, 0.4);
        font-family: 'Inter', sans-serif;
    }
    
    /* PIQ styling */
    .logo-p {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    .logo-iq {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    /* Company title */
    .company-info h1 {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
        line-height: 1.2;
    }
    
    /* Subtitle */
    .company-info p {
        color: #F48FB1;
        font-size: 15px;
        margin: 4px 0 0 0;
        font-weight: 400;
        letter-spacing: 0.2px;
    }
    
    .header-right {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    /* Header icons */
    .header-icon {
        background: rgba(255, 255, 255, 0.1);
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.7);
    }
    
    .header-icon svg {
        stroke: rgba(255, 255, 255, 0.7);
    }
    
    .header-icon:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        color: #F48FB1;
    }
    
    .header-icon:hover svg {
        stroke: #F48FB1;
    }
    
    /* User icon - Pink gradient */
    .header-icon.user-icon {
        background: linear-gradient(135deg, #F48FB1 0%, #F06292 100%);
        border: none;
        box-shadow: 0 4px 14px rgba(244, 143, 177, 0.3);
    }
    
    .header-icon.user-icon svg {
        stroke: rgba(255, 255, 255, 1);
    }
    
    /* Navigation Tabs */
    .stTabs {
        background: transparent;
        padding: 0 40px;
        margin-top: 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        padding: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: rgba(255, 255, 255, 0.6);
        border: none;
        border-bottom: 3px solid transparent;
        padding: 18px 32px;
        font-weight: 600;
        font-size: 17px;
        transition: all 0.2s;
        letter-spacing: 0.3px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #F48FB1;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* Active tab - Coral underline */
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #E57373 !important;
    }
    
    /* Main content area */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 32px 40px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #c21f13;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric Icons */
    .metric-icon {
        width: 56px;
        height: 56px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        font-size: 26px;
        color: white;
    }
    
    .metric-icon.green {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
        box-shadow: 0 8px 24px rgba(229, 115, 115, 0.35);
    }
    
    .metric-icon.pink {
        background: linear-gradient(135deg, #F48FB1 0%, #F06292 100%);
        box-shadow: 0 8px 24px rgba(244, 143, 177, 0.35);
    }
    
    .metric-icon.magenta {
        background: linear-gradient(135deg, #F8BBD0 0%, #F48FB1 100%);
        box-shadow: 0 8px 24px rgba(248, 187, 208, 0.35);
    }
    
    .metric-icon.gold {
        background: linear-gradient(135deg, #EF5350 0%, #E57373 100%);
        box-shadow: 0 8px 24px rgba(239, 83, 80, 0.35);
    }
    
    /* Metric Labels and Values */
    .metric-label {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 8px;
        line-height: 1;
    }
    
    .metric-change {
        font-size: 13px;
        color: #F48FB1;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .metric-change svg {
        color: #E57373;
    }
    
    /* Chart Cards */
    .chart-card {
        background: #c21f13;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    
    .chart-title {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #E57373 0%, #EF5350 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(229, 115, 115, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #EF5350 0%, #F44336 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 115, 115, 0.4);
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }
    
    /* Date Input */
    .stDateInput > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    
    .stDateInput input {
        color: #FFFFFF !important;
    }
    
    /* Section headers */
    .section-header {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 40px 0 20px 0;
        letter-spacing: -0.5px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #E57373 0%, #F48FB1 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #EF5350 0%, #F06292 100%);
    }
    
    /* Markdown */
    .stMarkdown {
        color: #FFFFFF;
    }
    
    .stMarkdown h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .stDataFrame thead tr {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stDataFrame thead th {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        font-size: 15px;
        border-radius: 8px;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus {
        border-color: #E57373;
        box-shadow: 0 0 0 2px rgba(229, 115, 115, 0.2);
    }
    
    /* Labels */
    label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    
    /* Alert badge on tab */
    .alert-badge {
        background: #EF5350;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 6px;
        display: inline-block;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 8px;
    }
    
    .stRadio > div > label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #E57373 0%, #F48FB1 100%) !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .metric-card {
            padding: 16px;
        }
        
        .metric-value {
            font-size: 24px;
        }
        
        .metric-icon {
            width: 48px;
            height: 48px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown("""
<div class="custom-header">
    <div class="header-left">
        <div class="company-logo">
            <span class="logo-p">P</span><span class="logo-iq">IQ</span>
        </div>
        <div class="company-info">
            <h1>PricingIQ</h1>
            <p>AI-Driven Dynamic Pricing Engine</p>
        </div>
    </div>
    <div class="header-right">
        <div class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
        </div>
        <div class="header-icon notification-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
        </div>
        <div class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M12 1v6m0 6v6m5.2-13.2l-4.2 4.2m0 6l4.2 4.2M23 12h-6m-6 0H5m13.2 5.2l-4.2-4.2m0-6l-4.2-4.2"></path>
            </svg>
        </div>
        <div class="header-icon user-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'time_range' not in st.session_state:
    st.session_state.time_range = '6m'

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Insights",
    "Pricing Engine", 
    "Approvals",
    "Alerts"
])

# Add SVG icons to tabs
st.markdown("""
<style>
    /* Insights icon */
    .stTabs [data-baseweb="tab"]:nth-child(1)::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.6)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='20' x2='18' y2='10'%3E%3C/line%3E%3Cline x1='12' y1='20' x2='12' y2='4'%3E%3C/line%3E%3Cline x1='6' y1='20' x2='6' y2='14'%3E%3C/line%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        vertical-align: middle;
    }
    
    /* Pricing Engine icon */
    .stTabs [data-baseweb="tab"]:nth-child(2)::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.6)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='12' y1='1' x2='12' y2='23'%3E%3C/line%3E%3Cpath d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'%3E%3C/path%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        vertical-align: middle;
    }
    
    /* Approvals icon */
    .stTabs [data-baseweb="tab"]:nth-child(3)::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.6)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        vertical-align: middle;
    }
    
    /* Alerts icon */
    .stTabs [data-baseweb="tab"]:nth-child(4)::before {
        content: "";
        display: inline-block;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.6)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'%3E%3C/path%3E%3Cline x1='12' y1='9' x2='12' y2='13'%3E%3C/line%3E%3Cline x1='12' y1='17' x2='12.01' y2='17'%3E%3C/line%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        vertical-align: middle;
    }
    
    /* Active tab icon */
    .stTabs [aria-selected="true"]::before {
        filter: brightness(1.5);
    }
    
    /* Alerts badge */
    .stTabs [data-baseweb="tab"]:nth-child(4)::after {
        content: "3";
        background: #EF5350;
        color: white;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 8px;
        display: inline-block;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# Render each tab
with tab1:
    insights.render()

with tab2:
    pricing_engine.render()

with tab3:
    approvals.render()

with tab4:
    alerts.render()