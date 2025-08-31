import streamlit as st

# CSS styles including button hover, titles, boxes etc.
custom_css = """
<style>
.main-title {
    color: #2368A2;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 30px;
    letter-spacing: 1px;
}
.form-label {
    font-size: 1.1rem;
    color: #2368A2;
    font-weight: 500;
}
.stButton > button {
    background: linear-gradient(90deg,#2368A2 30%, #17a2b8 100%);
    color: white;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    padding: 0.4em 1.5em;
    margin-top: 1em;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(90deg,#17a2b8 30%, #2368A2 100%);
    color: #fff;
    box-shadow: 0 0 12px #2368A2aa;
}
.registered-users-box {
    background: #f0f8ff;
    border-radius: 10px;
    padding: 1em;
    margin-top: 2em;
}
.success-box {
    border-left: 8px solid #23d160;
    background: #eaffea;
    padding: 1em;
    border-radius: 8px;
    margin-top: 1em;
}

/* Background Image Styling */
[data-testid="stAppViewContainer"] {
    background-image: url("C:\Users\fitbe\OneDrive\Documents\Streamlit\top-view-frame-with-plane-sweets.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}


[data-testid="stHeader"] {
    background: rgba(0,0,0,0.4);
}

[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.5);
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)




if "users" not in st.session_state:
    st.session_state.users = []
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

#Toggle: Show signup or login
mode = st.sidebar.radio("Choose page:", ["Sign Up", "Log In"])

st.title("User Authentication")

if mode == "Sign Up":
    st.subheader("Create a New Account")
    with st.form("signup_form", clear_on_submit=True):
        email = st.text_input("Email", key="signup_email")
        username = st.text_input("Username", key="signup_username")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        signup_btn = st.form_submit_button("Sign Up")
        
        if signup_btn:
            errors = []
            if not email or not username or not password or not confirm:
                errors.append("All fields are required.")
            if password != confirm:
                errors.append("Passwords do not match.")
            if username in [u["username"] for u in st.session_state.users]:
                errors.append("Username already exists.")
            if errors:
                st.error("\n".join(errors))
            else:
                st.session_state.users.append({"email": email, "username": username, "password": password})
                st.success(f"Account created! Please log in, {username}.")
                st.balloons()

if mode == "Log In":
    st.subheader("Login to Your Account")
    with st.form("login_form"):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pw")
        login_btn = st.form_submit_button("Log In")
        if login_btn:
            user = next((u for u in st.session_state.users if u["username"] == username and u["password"] == password), None)
            if user:
                st.session_state.auth_user = user
                st.success(f"Welcome back, {username}!")
                st.balloons()
            else:
                st.error("Incorrect username or password.")
    
    if st.session_state.auth_user:
        st.info(f"You are logged in as {st.session_state.auth_user['username']}.")
        if st.button("Log Out"):
            st.session_state.auth_user = None
            st.success("Logged out successfully.")

# Demo: Show registered users (remove in production)
if st.session_state.users:
    st.caption("Registered users (for demo):")
    st.write(st.session_state.users)
