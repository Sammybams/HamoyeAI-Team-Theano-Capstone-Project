import streamlit as st
import time
import numpy as np
from Crime_Forecast_App import load_data

st.set_page_config(page_title="Analysis Toolkit", page_icon="📈")

st.markdown("# Analysis Toolkit")
st.sidebar.header("Analysis Toolkit")
st.subheader(
    """This page gives you access to analyse crime per country."""
)

crime = load_data()

countries_to_check = sorted(crime.COUNTRY.unique())

option = st.selectbox(
    'Select Country to Analyse',
    (countries_to_check))

selected = crime.loc[crime['COUNTRY']==option]
max_fatality = selected.FATALITIES.max()
by_fatality = selected[selected['FATALITIES']==max_fatality]

st.write('You selected:', option)


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")