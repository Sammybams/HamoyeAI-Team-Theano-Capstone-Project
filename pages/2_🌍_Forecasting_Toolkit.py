import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime
from urllib.error import URLError
from Crime_Forecast_App import load_data

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Forecasting Toolkit")
st.sidebar.header("Forecasting Toolkit")

st.subheader(
    """Forecast the occurence in a location based on observed disorder type and date."""
)

# @st.experimental_memo
# def from_data_file(filename):
#     url = (
#         "http://raw.githubusercontent.com/streamlit/"
#         "example-data/master/hello/v1/%s" % filename
#     )
#     return pd.read_json(url)


crime = load_data()

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    date = st.date_input(
        "Choose expected date",
        datetime.datetime.today())

with col2:
    disorder_type = st.selectbox(
        'Select Disorder Type',
        (sorted(crime.DISORDER_TYPE.unique())))
    
with col3:
    region = st.selectbox(
        'Select Region',
        (sorted(crime.REGION.unique())))

with col4:
    country = st.selectbox(
        'Select Country',
        (sorted(crime.COUNTRY.unique())))
    
with col5:
    admin1 = st.selectbox(
        'Select Sub-national Admin Region',
        (sorted(crime.ADMIN1.unique())))
    
with col6:
    location = st.selectbox(
        'Select Location',
        (sorted(crime.LOCATION.unique())))