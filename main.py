import streamlit as st
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

options = st.sidebar.selectbox("Single Out", ('Twitter', 'Stocktwit Picks', 'Charts', 'Patterns'))

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
        "width": 900,
        "height": 610,
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
        height=610,
        width=900,
    )

if options == 'Patterns':
    print(12)
