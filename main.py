import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy

st.title("Kickstart Finance")
st.sidebar.title("DashBoard")

options = st.sidebar.selectbox("Single Out", ('Twitter', 'WSB', 'Stocktwit Picks', 'Charts', 'Patterns'))

st.subheader(options)

if options == 'Twitter':
    st.write('hi')

if options == 'WSB':
    st.write('hey')

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
    st.write('yo')

if options == 'Patterns':
    st.write('no')
