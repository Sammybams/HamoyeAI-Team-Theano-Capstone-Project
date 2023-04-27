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

crime = load_data()

date = st.date_input(
    "Choose expected date",
    datetime.datetime.today())

disorder_type = st.selectbox(
    'Select Disorder Type',
    (sorted(crime.DISORDER_TYPE.unique())))

region = st.selectbox(
    'Select Region',
    (sorted(crime.REGION.unique())))

updated = crime.loc[crime['REGION']==region]
country = st.selectbox(
    'Select Country',
    (sorted(updated.COUNTRY.unique())))

updated = updated.loc[updated['COUNTRY']==country]
admin1 = st.selectbox(
    'Select Sub-national Administrative Region',
    (sorted(updated.ADMIN1.unique())))

updated = updated.loc[updated['ADMIN1']==admin1]
location = st.selectbox(
    'Select Location',
    (sorted(updated.LOCATION.unique())))



with st.button("Run"):
    pass