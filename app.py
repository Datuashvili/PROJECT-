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

st.title('IBM & TSCO PRICE MONTHLY')

# IBM prepare  data
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=(key)'
i = requests.get(url)
dj = pd.read_json(i.content, typ = 'series')

data_IBM = pd.DataFrame(dj['Monthly Adjusted Time Series']).T

data_IBM['4. close'] = pd.to_numeric(data_IBM['4. close'], errors='coerce')
data_IBM['1. open'] = pd.to_numeric(data_IBM['1. open'], errors='coerce')
data_IBM['5. adjusted close'] = pd.to_numeric(data_IBM['5. adjusted close'], errors='coerce')
# IBM1 for chart 
data_IBM1= data_IBM[['4. close']]
data_IBM1 = data_IBM1.reset_index()
data_IBM1 =data_IBM1.rename(columns = ({'4. close' : 'IBM','index': 'Date'}))
# IBM2 for select option
data_IBM2 = data_IBM[['4. close', '1. open','5. adjusted close']]
data_IBM2 = data_IBM2.reset_index()
data_IBM2 = data_IBM2.rename(columns = ({'4. close' : 'Closing_price_IBM', '1. open': 'opening_price_IBM', 
                                        '5. adjusted close': 'adjusted_close_price_IBM', 'index': 'Date' }))
# TSCO prepare  data
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=(key)'
t = requests.get(url)
df = pd.read_json(t.content, typ = 'series')
data_TSCO = pd.DataFrame(df['Monthly Adjusted Time Series']).T
data_TSCO['4. close'] = pd.to_numeric(data_TSCO['4. close'], errors='coerce')
data_TSCO['1. open'] = pd.to_numeric(data_TSCO['1. open'], errors='coerce')
data_TSCO['5. adjusted close'] = pd.to_numeric(data_TSCO['5. adjusted close'], errors='coerce')
# TSCO1 for chart
data_TSCO1 = data_TSCO[['4. close']]
data_TSCO1 = data_TSCO1.reset_index()
data_TSCO1 = data_TSCO1.rename(columns = ({'4. close' : 'TSCO', 'index': 'Date'}))

#TSCO2 for select option 
data_TSCO2 = data_TSCO[['4. close', '1. open','5. adjusted close']]
data_TSCO2 = data_TSCO2.reset_index()
data_TSCO2 = data_TSCO2.rename(columns = ({'4. close' : 'Closing_price_TSCO', '1. open': 'opening_price_TSCO', 
                                        '5. adjusted close': 'adjusted_close_price_TSCO', 'index': 'Date' }))

#merge IBM1 and TSCO2 data for chart 
data_all = data_TSCO1.merge(data_IBM1, on='Date')
new_data = data_all.melt('Date', var_name='symbol', value_name='price')
#set up selection 
input_dropdown = alt.binding_select(options=['ALL','IBM','TSCO'])
selection = alt.selection_single(fields=['symbol'], bind=input_dropdown, name='choose here ')
select = alt.condition(selection,
                    alt.Color('symbol:N', legend=None),
                    alt.value('lightgray'))

# set up chart 
c = alt.Chart(new_data).mark_line().encode(
  x='Date:T',
  y='price:Q',
  color= select, 
    tooltip='Name:N'
) .properties( title='Stock closing price data IBM and TSCO',
    width=700,
    height=400) .configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=20,
    cornerRadius=10,
    orient='top-right'
) .configure_title(
    fontSize=20,
    font='Courier',
    anchor='start',
    color='gray'
) .add_selection(
    selection
)

st.altair_chart(c)



# set uo select option for IBM
Dates = data_IBM2.Date.unique()  
date_selected = st.selectbox('Select Date to view IBM data', Dates)
df_for_display = data_IBM2[data_IBM2.Date.isin([date_selected])]
st.write(df_for_display)
#set up select option for TSCO
Dates = data_TSCO2.Date.unique()  
date_selected = st.selectbox('Select Date to view TSCO data', Dates)
df_for_display = data_TSCO2[data_TSCO2.Date.isin([date_selected])]
st.write(df_for_display)




