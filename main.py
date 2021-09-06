import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import numpy as np
import requests
import tweepy
import config
import streamlit.components.v1 as components

st.title("Kickstart Finance")
st.sidebar.title("DashBoard")

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

options = st.sidebar.selectbox("Single Out", ('Twitter', 'Stocktwit Picks', 'Charts', 'Forecasting'))

st.subheader(options)

if options == 'Twitter':
    
    list_of_users = st.sidebar.selectbox("User", (
    '@eWhispers',
    '@FromValue',
    '@theWalrusStreet',
    '@realwillmeade',
    '@Fxhedgers',
    '@WhiteHouse',
    '@PressSec',
    '@Tesla',
    '@business',
    '@Reuters',
    '@TheEconomist',
    '@JonahLupton',
    '@1228hassanali',
    '@elonmusk',
    '@chamath',
    '@CathieDWood',
    '@ARKInvest',
    '@BillAckman',
    '@Stocktwits'
    ))
    
    user = api.get_user(list_of_users)
    tweets = api.user_timeline(list_of_users)

    st.subheader(list_of_users)
    st.image(user.profile_image_url)
        
    for tweet in tweets:
        if '$' in tweet.text:
            words = tweet.text.split(' ')
            for word in words:
                if word.startswith('$') and word[1:].isalpha():
                    symbol = word[1:]
                    st.write(symbol)
                    st.write(tweet.text)
                    st.image(f"https://finviz.com/chart.ashx?t={symbol}")

if options == 'Stocktwit Picks':
    st.write("")
    
    symbol = st.sidebar.text_input("Ticker", value='AAPL')

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if options == 'Charts':
    
    components.html(
        """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
        <div id="tradingview_f16c9"></div>
        <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {
        "width": 2000,
        "height": 1000,
        "symbol": "NASDAQ:AAPL",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "withdateranges": true,
        "allow_symbol_change": true,
        "studies": [
            "MACD@tv-basicstudies",
            "MASimple@tv-basicstudies",
            "RSI@tv-basicstudies"
        ],
        "container_id": "tradingview_f16c9"
        }
        );
        </script>
        </div>
        <!-- TradingView Widget END -->
        """,
        height=1000,
        width=2000,
    )

if options == 'Forecasting':
    
    START = '2015-01-01'
    TODAY = date.today().strftime("%Y-%m-%d")

    stocks = st.sidebar.text_input("Ticker", value='AAPL')

    n_years = st.slider("Years of prediction:", 1, 4)
    period = n_years*365

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace = True)
        return data
    
    data_load_state = st.text("Load data...")
    data = load_data(stocks)
    data_load_state.text("Loading data...done!")


    st.subheader('Raw Data')
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y = data['Open'], name = 'stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'], name = 'stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    
    plot_raw_data()

    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader("Forecast Data")
    st.write(forecast.tail())

    st.subheader('Forecast Chart')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.subheader('Forecast Components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)