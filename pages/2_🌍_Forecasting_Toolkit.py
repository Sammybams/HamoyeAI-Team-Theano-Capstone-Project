import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime
from urllib.error import URLError

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


col1, col2, col3, col4, col5, col6 = st.columns(6)



with col1:
    d = st.date_input(
        "Expected Date",
        datetime.datetime.today())
    
