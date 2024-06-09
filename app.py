import streamlit as st
import pandas as pd
import plotly_express as px
import requests
from io import StringIO

# Define the raw URL of your CSV file on GitHub
CSV_URL = 'https://raw.githubusercontent.com/plj2k2002/TripleTen_project/main/vehicles_us.csv'

# Fetch the CSV content from the URL and load it into a DataFrame
response = requests.get(CSV_URL)
if response.status_code == 200:
    csv_content = response.text
    df = pd.read_csv(StringIO(csv_content))
else:
    st.error(f"Failed to fetch data from {CSV_URL}. Status code: {response.status_code}")

# Now you can use df as your DataFrame
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Data viewer')
show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

st.dataframe(df)
st.header('Vehicle types by manufacturer')
st.write(px.histogram(df, x='manufacturer', color='type'))
st.header('Histogram of `condition` vs `model_year`')

st.write(px.histogram(df, x='model_year', color='condition'))

st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))
