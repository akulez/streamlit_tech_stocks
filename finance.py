import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import requests
import datetime

st.header("Tech Stocks Live Analytics")

st.sidebar.header("Please select the Stock and the time frame here.")
stock_name = st.sidebar.radio('Which stock do you wish to analyze?', ['AAPL', 'AMZN', 'GOOGL', 'MSFT'], index=0)
interval = st.sidebar.radio("What interval do you wish to analyze?", ['3d', '1w','15d', '1mo', '45d'], index=0)
st.write("------")

def fetch_data(stock_name, interval):
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=7)  
    end_date = now

    if interval == '3d':
        start_date = now - datetime.timedelta(days=3)
    elif interval == '1w':
        start_date = now - datetime.timedelta(weeks=1)
    elif interval == '15d':
        start_date = now - datetime.timedelta(days=15)
    elif interval == '1mo':
        start_date = now - datetime.timedelta(days=30)
    elif interval == '45d':
        start_date = now - datetime.timedelta(days=45)

    stock = yf.Ticker(stock_name)
    df = stock.history(start=start_date, end=end_date, interval='1d')
    df.index = df.index.tz_convert("UTC")
    return df

def generate_graphs():
    df = fetch_data(stock_name, interval)
    df['DateTime'] = df.index  # Convert the index to a column

    highest_price = df['Close'].max()
    lowest_price = df['Close'].min()
    average_price = df['Close'].mean()

    st.subheader(f"Financial Metrics for {stock_name} stock")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"Highest Price in the past {interval}")
        st.write(f"{highest_price:.2f}")

    with col2:
        st.info(f"Lowest Price in the past {interval}")
        st.write(f"{lowest_price:.2f}")

    with col3:
        st.info(f"Average Price in the past {interval}")
        st.write(f"{average_price:.2f}")
    st.write("------")

    st.subheader(f"Closing Price Chart for {stock_name} stock")
    st.write("")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['DateTime'], y=df['Close'], mode='lines', name='Closing Price'))
    fig.update_layout(xaxis_title='Time Period', yaxis_title='Closing Price')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")  

    st.subheader(f"Candlestick Chart for {stock_name} stock")
    candlestick_fig = go.Figure()
    candlestick_fig.add_trace(go.Candlestick(x=df['DateTime'],
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'],
                                             increasing_line_color='green',
                                             decreasing_line_color='red'
                                             ))
    candlestick_fig.update_layout(xaxis_title='Time Period', yaxis_title='Prices')
    st.plotly_chart(candlestick_fig, use_container_width=True)
    st.write("---")

    st.markdown(f"## Latest upcoming news for the {stock_name} stock:")
    st.write("")
    st.write("")
    st.write("")
    stock_symbol = stock_name
    api_key = '6696f95f57c54e7e9006645dc39b56ad'
    url = f"https://newsapi.org/v2/everything?q={stock_symbol}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        articles = data['articles'][:10]
        for article in articles:
            st.write(f"**Title:** {article['title']}")
            st.write(f"**Source:** {article['source']['name']}")
            st.write(f"**URL:** {article['url']}")
            st.write(f"**Description:** {article['description']}")
            st.markdown("---")
    else:
        st.write("Error occurred while fetching news. Please try again.")

generate_graphs()