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
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if request_login(username, password):
                st.success("Login successful")
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid Credentials")
            

def display_stock_graphs():
    st.text("Trending Stocks")
    
def display_chatbot():    
    # Display a header for the chat
    st.header("Chat with the customized finance Bot")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display chat messages from history on app rerun
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Prompt user for input and handle input submission
    if user_input := st.chat_input("You:"):
        # Store user message in session state
        st.session_state['messages'].append({"role": "user", "content": user_input})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Simulate bot response
        # bot_response = generate_bot_response(user_input)
        bot_response = user_input
        st.session_state['messages'].append({"role": "bot", "content": bot_response})
        
        # Display bot response in chat message container
        with st.chat_message("bot"):
            st.markdown(bot_response)

def display_dashboard_page():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        st.markdown("<h2 style='text-align: center'>Dashboard</h2>", unsafe_allow_html=True)
        display_stock_graphs()
    else:
        display_login_page()

if __name__ == '__main__':
    st.markdown("<h1 style='text-align: center'>Welcome to Fin4All</h1>", unsafe_allow_html=True)

    mode = st.sidebar.radio('Select Page:', ['Chatbot', 'Dashboard'])
    if mode == 'Chatbot':
        display_chatbot()
    else:
        display_dashboard_page()