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

st.title('IBM CLOOSE PRICE MONTHLY')
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=(key)'
i = requests.get(url)
dj = pd.read_json(i.content, typ = 'series')

data_IBM = pd.DataFrame(dj['Monthly Adjusted Time Series']).T
data_IBM['4. close'] = pd.to_numeric(data_IBM['4. close'], errors='coerce')
data_IBM = pd.DataFrame(data_IBM['4. close'])
data_IBM = data_IBM.reset_index()
data_IBM = data_IBM.rename(columns = ({'4. close' : 'Closing price IBM', 'index': 'Date'}))

c = alt.Chart(data_IBM).mark_line().encode(alt.X('Date', scale=alt.Scale(zero=False)),
                                           alt.Y('Closing price IBM'))
st.altair_chart(c, use_container_width=True)
Dates = data_IBM.Date.unique()  
date_selected = st.selectbox('Select Date to view', Dates)
df_for_display = data_IBM[data_IBM.Date.isin([date_selected])]
st.write(df_for_display)
