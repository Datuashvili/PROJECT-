import streamlit as st
import os
import numpy as np
import pandas as pd
import json
import requests
import altair as alt
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('key')

st.title('IBM CLOOSING PRICE MONTHLY')
# prepare IBM data
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=(key)'
i = requests.get(url)
dj = pd.read_json(i.content, typ = 'series')

data_IBM = pd.DataFrame(dj['Monthly Adjusted Time Series']).T

data_IBM['4. close'] = pd.to_numeric(data_IBM['4. close'], errors='coerce')
data_IBM['1. open'] = pd.to_numeric(data_IBM['1. open'], errors='coerce')
data_IBM['5. adjusted close'] = pd.to_numeric(data_IBM['5. adjusted close'], errors='coerce')
data_IBM1= pd.DataFrame(data_IBM['4. close'])
# datafame with 4 columns open price, close price and adjusted close price and set DATE as column 
data_IBM2 = pd.DataFrame([data_IBM['4. close'], data_IBM['1. open'], data_IBM['5. adjusted close']]).T
data_IBM2 = data_IBM2.reset_index()
data_IBM2 = data_IBM2.rename(columns = ({'4. close' : 'Closing_price_IBM', '1. open': 'opening_price_IBM', 
                                        '5. adjusted close': 'adjusted_close_price', 'index': 'Date'  }))
# set up chart 
c = alt.Chart(data_IBM2).mark_line().encode(alt.X('Date', scale=alt.Scale(zero=False)),
                                           alt.Y('Closing_price_IBM' ))
st.altair_chart(c, use_container_width=True)

# set uo select option 
Dates = data_IBM2.Date.unique()  
date_selected = st.selectbox('Select Date to view', Dates)
df_for_display = data_IBM2[data_IBM2.Date.isin([date_selected])]
st.write(df_for_display)

