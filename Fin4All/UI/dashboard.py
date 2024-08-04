import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Importing fetch_stock_data_from_db from DB.fetch_data package
from fetch_data.fetch_data_from_ticker_statements import fetch_stock_data_from_db

# Fetch stock data from the database
stock_data = fetch_stock_data_from_db()

# Page configuration
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("Stock Dashboard")

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
