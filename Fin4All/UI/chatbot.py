import streamlit as st

# Streamlit app title
st.title("Chatbot with Streamlit")

# Sidebar with a radio button to switch between chat and other functionalities
mode = st.sidebar.radio('Choose Mode:', ['Chatbot', 'Other'])

if mode == 'Chatbot':
    st.sidebar.write("### Chatbot Interface")
    
    # Display a header for the chat
    st.header("Chat with the Bot")

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
        bot_response = f"Bot: {user_input}"  # Echo user's input
        st.session_state['messages'].append({"role": "bot", "content": bot_response})
        
        # Display bot response in chat message container
        with st.chat_message("bot"):
            st.markdown(bot_response)

else:
    st.sidebar.write("### Other Options")
    st.write("This section can contain other functionality.")

# Main content
st.write("This is the main content area of the Streamlit app.")
