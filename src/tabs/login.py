"""
Login Page - Authentication gateway for the pricing dashboard
Final version with custom background image, scroll fixes, red tones, 
extended panel length, larger input boxes, and centered text alignment.
"""
import streamlit as st
import hashlib
import base64
from pathlib import Path


# Demo users (in production, this would be a database)
DEMO_USERS = {
    "maria": {"password": "demo123", "name": "Maria A.", "role": "Admin"},
    "john": {"password": "demo123", "name": "John D.", "role": "Analyst"},
    "sarah": {"password": "demo123", "name": "Sarah M.", "role": "Manager"},
    "demo": {"password": "demo", "name": "Demo User", "role": "Viewer"},
}


def hash_password(password: str) -> str:
    """Simple password hashing for demo purposes."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username: str, password: str) -> dict:
    """Verify login credentials."""
    username = username.lower().strip()
    if username in DEMO_USERS:
        if DEMO_USERS[username]["password"] == password:
            return {
                "valid": True,
                "name": DEMO_USERS[username]["name"],
                "role": DEMO_USERS[username]["role"],
                "username": username
            }
    return {"valid": False}


def get_background_image():
    """
    Load and encode the background image.
    Place your background image as 'background.png' in the same directory as this script.
    """
    # Try to load the background image
    image_path = Path(__file__).parent / "background.png"
    
    if image_path.exists():
        try:
            with open(image_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
        except:
            return None
    else:
        # Fallback to gradient if image not found
        return None


def render_login_page():
    """Render the login page with the two-column UI design, using red/maroon tones and background image."""
    
    # Get background image
    bg_image = get_background_image()
    
    # Determine background style for left panel
    if bg_image:
        left_panel_bg = f"""
            background-image: url('{bg_image}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        """
    else:
        # Fallback gradient
        left_panel_bg = """
            background: linear-gradient(135deg, #E57373 0%, #EF5350 25%, #F48FB1 50%, #E57373 75%, #EF5350 100%);
        """
    
    # -----------------------------------------------------------
    # 1. Custom CSS for Global Styles and Background
    # -----------------------------------------------------------
    st.markdown(f"""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Hide Streamlit header/footer/menu */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        
        /* Remove all default padding */
        .main {{
            padding: 0 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}
        
        .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}
        
        /* Full screen container */
        .login-container {{
            display: flex;
            height: 20vh;: 
            width: 100%;
            overflow: hidden;
        }}
        
        /* Left Panel - Background Image or Gradient */
        .login-left-panel {{
            flex: 1;
            {left_panel_bg}
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 80px 100px;
            position: relative;
        }}
        
        /* Overlay for better text readability on image */
        .login-left-panel::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.2) 100%);
            pointer-events: none;
        }}
        
        .login-left-content {{
            text-align: center;
            color: white;
            position: relative;
            z-index: 1;
        }}
        
        .login-left-content h3 {{
            color: white;
            margin: 0;
            font-size: 48px;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            line-height: 1.2;
        }}
        
        .login-left-content .subtitle {{
            color: #FFFFFF;
            opacity: 0.95;
            margin: 12px 0 0 0;
            font-size: 16px;
            font-weight: 500;
            text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
        }}
        
        .login-left-content h1 {{
            color: white;
            margin: 60px 0 0 0;
            font-size: 56px;
            font-weight: 800;
            line-height: 1.1;
            text-shadow: 0 2px 15px rgba(0, 0, 0, 0.3);
        }}
        
        /* Right Panel - White Form */
        .login-right-panel {{
            width: 750px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(250, 245, 245, 0.98) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px 20px;
            box-shadow: -10px 0 40px rgba(0, 0, 0, 0.2);
            overflow-y: auto;
        }}
        
        .form-container {{
            width: 100%;
            max-width: 420px;
        }}
        
        /* Input Field Overrides */
        .login-right-panel .stTextInput > div > div > input {{
            background: rgba(0, 0, 0, 0.85) !important;
            border: none !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            padding: 18px 22px !important;
            font-size: 16px !important;
            height: 58px !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }}
        
        .login-right-panel .stTextInput > div > div > input:focus {{
            box-shadow: 0 0 0 3px rgba(229, 115, 115, 0.3) !important;
            background: rgba(0, 0, 0, 0.9) !important;
        }}
        
        .login-right-panel .stTextInput > div > div > input::placeholder {{
            color: rgba(255, 255, 255, 0.4) !important;
        }}
        
        .login-right-panel .stTextInput label {{
            color: rgba(0, 0, 0, 0.7) !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-transform: none !important;
            font-family: 'Inter', sans-serif !important;
            margin-bottom: 8px !important;
        }}
        
        /* Checkbox styling */
        .login-right-panel .stCheckbox {{
            margin-top: 8px !important;
        }}
        
        .login-right-panel .stCheckbox > label {{
            color: rgba(0, 0, 0, 0.7) !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        /* Button Overrides */
        .login-right-panel .stButton > button {{
            background: linear-gradient(135deg, #E57373 0%, #EF5350 100%) !important;
            border: none !important;
            border-radius: 8px !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            padding: 14px 32px !important;
            height: 50px !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.3px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(229, 115, 115, 0.4) !important;
        }}
        
        .login-right-panel .stButton > button:hover {{
            background: linear-gradient(135deg, #EF5350 0%, #F44336 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(229, 115, 115, 0.5) !important;
        }}
        
        /* Sign Up Button (secondary) */
        .signup-button .stButton > button {{
            background: transparent !important;
            border: 2px solid rgba(229, 115, 115, 0.4) !important;
            color: #E57373 !important;
            box-shadow: none !important;
        }}
        
        .signup-button .stButton > button:hover {{
            background: rgba(229, 115, 115, 0.08) !important;
            border-color: rgba(229, 115, 115, 0.6) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Forgot password link */
        .forgot-link {{
            text-align: right;
            font-size: 13px;
            color: rgba(229, 115, 115, 0.9);
            margin-top: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: color 0.2s ease;
        }}
        
        .forgot-link:hover {{
            color: #E57373;
        }}
        
        /* Social links */
        .social-links {{
            text-align: center;
            padding-top: 40px;
            font-size: 12px;
            color: rgba(0, 0, 0, 0.4);
            font-weight: 500;
            letter-spacing: 2px;
        }}
        
        /* Divider */
        hr {{
            border: none;
            border-top: 1px solid rgba(0, 0, 0, 0.08);
            margin: 24px 0;
        }}
        
        /* Success/Error messages */
        .stSuccess, .stError, .stWarning {{
            margin-top: 16px !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        /* Hide form border */
        [data-testid="stForm"] {{
            background: transparent !important;
            border: none !important;
        }}
        
        /* Responsive */
        @media (max-width: 1024px) {{
            .login-left-panel {{
                padding: 60px 40px;
            }}
            
            .login-right-panel {{
                width: 450px;
                padding: 60px 40px;
            }}
            
            .login-left-content h3 {{
                font-size: 40px;
            }}
            
            .login-left-content h1 {{
                font-size: 48px;
            }}
        }}
        
        @media (max-width: 768px) {{
            .login-container {{
                flex-direction: column;
            }}
            
            .login-right-panel {{
                width: 100%;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # -----------------------------------------------------------
    # 2. Main Login Box Structure (Two Columns)
    # -----------------------------------------------------------
    
    # Use columns to create the split
    col_left, col_right = st.columns([1, 0.8])
    
    # --- LEFT PANEL (Background Image/Gradient) ---
    with col_left:
        st.markdown("""
            <div class="login-left-panel">
                <div class="login-left-content">
                    <h3>PricingIQ</h3>
                    <p class="subtitle">Price Right, Every Time</p>
                    <h1>Hello, welcome!</h1>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- RIGHT PANEL (White Form) ---
    with col_right:
        st.markdown('<div class="login-right-panel"><div class="form-container">', unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form"):
            # Username Field
            username = st.text_input(
                "User Name", 
                placeholder="User name",
                key="login_username"
            )
            
            # Password Field
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••••••",
                key="login_password"
            )
            
            # Checkbox and Forgot Password Link
            col_check, col_forgot = st.columns([1.5, 1])
            with col_check:
                st.checkbox("Remember me", value=False)
            with col_forgot:
                st.markdown('<div class="forgot-link">Forgot password?</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Login Button
            col_login, col_space = st.columns([1, 2])
            with col_login:
                submit = st.form_submit_button("Login", use_container_width=True)
            
            # Login Logic
            if submit:
                if username and password:
                    result = check_credentials(username, password)
                    if result["valid"]:
                        st.session_state.logged_in = True
                        st.session_state.user_name = result["name"]
                        st.session_state.user_role = result["role"]
                        st.session_state.username = result["username"]
                        st.success(f"Welcome back, {result['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

        # Sign Up Button (outside form)
        st.markdown('<div class="signup-button">', unsafe_allow_html=True)
        col_space1, col_signup, col_space2 = st.columns([1.5, 1, 1])
        with col_signup:
            if st.button("Sign Up", use_container_width=True, key="signup_button"):
                st.info("Sign up functionality coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)


    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)


def is_logged_in() -> bool:
    """Check if user is logged in."""
    return st.session_state.get("logged_in", False)


def get_current_user() -> dict:
    """Get current logged in user info."""
    return {
        "name": st.session_state.get("user_name", "Guest"),
        "role": st.session_state.get("user_role", "Viewer"),
        "username": st.session_state.get("username", "guest")
    }


def logout():
    """Log out the current user."""
    st.session_state.logged_in = False
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.username = None


# -----------------------------------------------------------
# Execution Block (for direct testing, ignored when imported)
# -----------------------------------------------------------
def main():
    if not is_logged_in():
        render_login_page()
    else:
        # Placeholder for what happens after login
        st.write(f"Logged in as {st.session_state.user_name} ({st.session_state.user_role}).")
        if st.button("Logout"):
            logout()
            st.rerun()


if __name__ == "__main__":
    main()