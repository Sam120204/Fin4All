import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Fin4All.UI.fetch_data.fetch_data_from_ticker_statements import *
from Fin4All.Agent.Semantics.gpt_investment_analysis import *

# Page configuration
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Stock Dashboard")

@st.cache_data
def fetch_stock_data_from_db():
    db = get_database()
    if db is None:
        return {}

    collection_name = "TickersStatement"
    collection_news = "NewsSentiment"
    collection = db[collection_name]
    news_info = db[collection_news]
    stock_data = {}

    # Fetch all documents from the collection
    cursor = collection.find({})

    for document in cursor:
        ticker = document['ticker']
        
        # Fetch news articles and sentiment summary for the current ticker
        news_document = news_info.find_one({"ticker": ticker})

        if news_document:
            articles = news_document.get('articles', [])
            news = [{"title": article['headline'], "url": article['url']} for article in articles]
            sentiment_summary = news_document.get('sentiment_summary', '')
        else:
            news = []
            sentiment_summary = ''

        # Construct the stock data structure
        stock_data[ticker] = {
            'Current Price': document['price']['Current Price'],
            'Price Change (%)': document['price']['Price Change (%)'],
            '52-Week High': document['price']['52-Week High'],
            '52-Week Low': document['price']['52-Week Low'],
            'Volume': document['price']['Volume'],
            'Prices': document.get('Prices', []),
            'Open Price': document['price']['Open Price'],
            'Close Price': document['price']['Close Price'],
            'Balance Sheet': pd.DataFrame(document['balance_sheet']).transpose(),
            'Cash Flow': pd.DataFrame(document['cashflow']).transpose(),
            'Income Statement': pd.DataFrame(document['income_statement_quarter']).transpose(),
            'News': news,
            'Sentiment Summary': sentiment_summary
        }
    
    return stock_data

# Fetch stock data from the database
stock_data = fetch_stock_data_from_db()

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
                st.session_state['messages'] = []
                st.rerun()
            else:
                st.error("Invalid Credentials")
            

def render_dashboard():
    # Sidebar with search bar
    st.sidebar.subheader("Search Stock Ticker")
    all_tickers = list(stock_data.keys())
    selected_ticker = st.sidebar.selectbox("Select Ticker", all_tickers)

    # Check if the selected ticker is valid
    if selected_ticker and selected_ticker in stock_data:
        details = stock_data[selected_ticker]
        
        # Stock Performance Overview
        st.subheader(f"{selected_ticker} Stock Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("**Current Price**", f"${details['Current Price']:.2f}", f"{details['Price Change (%)']:.2f}%",
                    delta_color="inverse")
        with col2:
            st.write("**Price position within 52-Week Range**")
            st.progress((details['Current Price'] - details['52-Week Low']) / (details['52-Week High'] - details['52-Week Low']))
        with col3:
            st.metric("**Shares traded in the past month**", f"{details['Volume']:,}")

        # Daily Market Summary with Improved UI
        st.subheader("Daily Market Summary")
        summary_style = """
            display: flex; 
            justify-content: space-between; 
            background-color: #f9f9f9; 
            border-radius: 8px; 
            padding: 16px; 
            border: 1px solid #ddd;
            margin-bottom: 20px;
        """
        
        with st.container():
            st.markdown(
                f"""
                <div style="{summary_style}">
                    <div style="text-align: center; flex: 1;">
                        <strong>Open Price</strong>
                        <div>${details['Open Price']:.2f}</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <strong>Close Price</strong>
                        <div>${details['Close Price']:.2f}</div>
                    </div>
                    <div style="text-align: center; color: {'green' if details['Close Price'] > details['Open Price'] else 'red'}; flex: 1;">
                        <strong>Status</strong>
                        <div>{'CLOSED ABOVE' if details['Close Price'] > details['Open Price'] else 'CLOSED BELOW'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Financial Data
        st.subheader("Financial Data")
        with st.expander("**Balance Sheet**"):
            st.dataframe(details['Balance Sheet'].style.format("{:.2f}"))
        with st.expander("**Cash Flow Statement**"):
            st.dataframe(details['Cash Flow'].style.format("{:.2f}"))
        with st.expander("**Income Statement**"):
            st.dataframe(details['Income Statement'].style.format("{:.2f}"))

        # Enhanced Historical Price Chart using Matplotlib
        st.subheader("Historical Price Chart")
        if 'Prices' in details and len(details['Prices']) > 0:
            # Convert the list of prices to a DataFrame
            historical_prices = pd.DataFrame(details['Prices'])

            # Ensure the Date column is in datetime format for proper plotting
            historical_prices['Date'] = pd.to_datetime(historical_prices['Date'])

            # Set the Date column as the index for the DataFrame
            historical_prices.set_index('Date', inplace=True)

            # Plot using the actual historical prices
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(historical_prices.index, historical_prices['Close'], marker='o', linestyle='-', color='b', label='Close Price')
            ax.fill_between(historical_prices.index, historical_prices['Close'].min(), historical_prices['Close'], alpha=0.1, color='blue')
            ax.set_title(f'{selected_ticker} Historical Price Chart')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price ($)')
            ax.grid(True, linestyle='--', alpha=0.6)
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
        else:
            st.warning("No historical price data available for this ticker.")
            
    # Latest News with clickable links and sentiment summary
    st.subheader("Latest News")
    news_style = """
        border-radius: 8px; 
        padding: 10px; 
        margin: 10px 0;
        background-color: #f8f9fa; 
        border: 1px solid #ddd;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 0.95em;
    """

    news_link_style = """
        text-decoration: none; 
        font-weight: bold; 
        font-size: 1.1em; 
        color: #007bff;
    """

    # Display news articles
    for article in details['News']:
        st.markdown(
            f"""
            <div style="{news_style}">
                <a href="{article['url']}" target="_blank" style="{news_link_style}">
                    {article['title']}
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Display sentiment summary with enhanced styling
    if 'Sentiment Summary' in details and details['Sentiment Summary']:
        sentiment_style = """
            background-color: #e9f7f9; 
            border-left: 5px solid #17a2b8; 
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        """
        st.subheader("Sentiment Summary")
        st.markdown(
            f"""
            <div style="{sentiment_style}">
                {details['Sentiment Summary']}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Footer
    footer_style = """
        <style>
            .footer {
                background-color: #f1f1f1;
                padding: 15px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #555;
                font-size: 1em;
                font-weight: 600;
                margin-top: 30px;
            }
            .footer a {
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }
            .footer a:hover {
                text-decoration: underline;
                color: #0056b3;
            }
        </style>
        <div class="footer">
            Built by <a href="https://github.com/Sam120204/Fin4All" target="_blank">Fin4ALL TEAM</a> | © 2024 All Rights Reserved
        </div>
    """

    st.markdown(footer_style, unsafe_allow_html=True)

def generate_response(username, question, history):
    headers = {'Content-Type': 'application/json'}
    res = requests.post('http://localhost:8000/generate_response', 
                        json={"username": username,
                              "question": question,
                              "history": history}, headers=headers)
    return res.text
    
def display_chatbot():
    st.header("Chat with the customized finance Bot")

    # chat history
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("You:"):
        st.session_state['messages'].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # gen response
        bot_response = generate_response(st.session_state.get("username", "guest"), user_input, st.session_state['messages'])
        st.session_state['messages'].append({"role": "bot", "content": bot_response})

        with st.chat_message("bot"):
            st.markdown(bot_response)


def get_user_profile(username):
    db = get_database()
    collection = db['portfolio']
    return collection.find_one({"username": st.session_state.get('username', 'guest')})

def display_profile():
    if "experience" not in st.session_state:
        st.session_state["experience"] = "None"
    if "preference" not in st.session_state:
        st.session_state["preference"] = "None"
    if "balance" not in st.session_state:
        st.session_state["balance"] = "None"
    if "report" not in st.session_state:
        st.session_state["report"] = "None"

    st.header("User Profile")
    st.write(f"Username: {st.session_state.get('username', 'guest')}")

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = "guest"
        st.session_state['messages'] = []
        st.success("Logged out successfully")

    col1, col2, col3, col4, col5 = st.columns(5)

    if st.session_state['experience'] == 'None' or st.session_state['preference'] == 'None' or st.session_state['balance'] == 'None' or st.session_state['report'] == 'None':
        cur_user_portfolio = get_user_profile(st.session_state.get('username', 'guest'))
        st.session_state['experience'] = cur_user_portfolio['experience'] if cur_user_portfolio else 'None'
        st.session_state['preference'] = cur_user_portfolio['preference']['stock'] if cur_user_portfolio else 'None'
        st.session_state['balance'] = cur_user_portfolio['balance'] if cur_user_portfolio else 'None'

    resubmit_flag = False

    with col1:
        experience = st.text_input('Experience', value=st.session_state['experience'])
    with col2:
        preference = st.text_input('Preference/Strategy', value=st.session_state['preference'] if st.session_state['preference'] else 'None')
    with col3:
        balance = st.text_input('Balance', value=st.session_state['balance'])
    with col4:
        subject = st.text_input('Ticker/Sector')

    # Create a button to submit the inputs
    with col5:
        if st.button('Submit'):
            # Prepare the update document
            update_doc = {
                "$set": {
                    "experience": experience,
                    "preference.stock": preference,  # Assuming 'preference' is a subdocument
                    "balance": balance
                }
            }
            st.session_state['experience'] = experience
            st.session_state['preference'] = preference
            st.session_state['balance'] = balance

            # Update the document in MongoDB
            collection = get_database()['portfolio']
            collection.update_one({"username": st.session_state['username']}, update_doc)
            resubmit_flag = True
            st.success("Submit successful")

    st.write("Enter 'renew' for Renewable Engergy Sector, 'tech' for Technology Sector, 'pharma' for Pharmaceutical Sector, or ticker symbol for a specific stock.")

    if resubmit_flag:
        display_text = "You have successfully updated your profile. Please check your profile in a few minutes for a new report."
        recommendation_collection = get_database()['recommendation']
        recommendation_collection.update_one({"username": st.session_state.get('username', 'guest')}, {"$set": {"stock_suggestion": display_text}})
    else:
        display_text = st.session_state['report']
        if st.session_state['report'] == 'None' or 'report' not in st.session_state:
            recommendation = get_database()['recommendation'].find_one({"username": st.session_state.get('username', 'guest')})
            if recommendation:
                display_text = recommendation.get('stock_suggestion', 'None')
            else:
                display_text = 'None'

    st.subheader("Stock Suggestion")
    st.write(display_text)
    if resubmit_flag:
        if subject == 'renew' or subject == 'tech' or subject == 'pharma':
            store_gpt_recommendation_in_db(st.session_state.get('username', 'guest'), experience, preference, balance, None, subject)
        else:
            store_gpt_recommendation_in_db(st.session_state.get('username', 'guest'), experience, preference, balance, subject, None)


def display_dashboard_page():
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        # st.markdown("<h2 style='text-align: center'>Dashboard</h2>", unsafe_allow_html=True)
        render_dashboard()
    else:
        display_login_page()

if __name__ == '__main__':

    # st.markdown("<h1 style='text-align: center'>Welcome to Fin4All</h1>", unsafe_allow_html=True)

    mode = st.sidebar.radio('Select Page:', ['Chatbot', 'Dashboard', 'Profile'])
    if mode == 'Chatbot':
        display_chatbot()
    elif mode == 'Dashboard':
        display_dashboard_page()
    else:
        display_profile()
