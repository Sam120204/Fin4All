import streamlit as st
import requests

def request_login(username, password):
    headers = {'Content-Type': 'application/json'}
    res = requests.post('http://localhost:8000/login', json={"username": username, "password": password}, headers=headers)
    return res.status_code == 200

def display_login_page():
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if request_login(email, password):
                st.success("Login successful")
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
            

def display_stock_graphs():
    st.text("Stock Graphs")
    

def display_dashboard_page():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.markdown("<h1 style='text-align: center'>Dashboard</h1>", unsafe_allow_html=True)
        display_stock_graphs()
    else:
        display_login_page()

if __name__ == '__main__':
    display_dashboard_page()