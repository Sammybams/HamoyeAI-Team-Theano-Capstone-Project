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
DATA_URL_ENCODED = "/Users/samuelbamgbola/Downloads/Crime-HamoyeAI-Capstone-Project/africa_crime_cleaned.parquet"

@st.experimental_memo
def load_data_encoded():

	data = pd.read_parquet(DATA_URL_ENCODED)

	return data

encoded_set = load_data_encoded()
actor1_dict = dict(zip(crime.ACTOR1.unique(), encoded_set.ACTOR1_encode.unique()))
actor1_dict_reverse = dict(zip(encoded_set.ACTOR1_encode.unique(), crime.ACTOR1.unique()))

admin1_dict = dict(zip(crime.ADMIN1.unique(), encoded_set.ADMIN1_encode.unique()))
admin1_dict_reverse = dict(zip(encoded_set.ADMIN1_encode.unique(), crime.ADMIN1.unique()))

location_dict = dict(zip(crime.LOCATION.unique(), encoded_set.LOCATION_encode.unique()))
location_dict_reverse = dict(zip(encoded_set.LOCATION_encode.unique(), crime.LOCATION.unique()))

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

updated = updated.loc[updated['LOCATION']==location]

disorder_type_options = []
region_options = []
country_options = []
admin1_options = []
location_options = []

event_options = []
sub_event_options = []
actor1_options = []
inter_1_options = []
inter2_options = []
interactions_options = []

for event in updated:
    updated =  updated.loc[updated["EVENT_TYPE"]==event]
    for sub_event in updated.SUB_EVENT_TYPE.unique():
        updated_2 = updated.loc[updated["SUB_EVENT_TYPE"]==sub_event]
        for actor in updated_2.ACTOR1.unique():
            updated_3 = updated_2.loc[updated_2["ACTOR1"]==actor]
            for inter_1 in updated_3.INTER1.unique():
                updated_4 = updated_3.loc[updated_3["INTER1"]==inter_1]
                for i in range(0,9):
                    event_options.append(event)
                    sub_event_options.append(sub_event)
                    actor1_options.append(actor)
                    inter_1_options.append(inter_1)
                    inter2_options.append(i)
                    interactions_options.append(inter_1*10 + i)
                    disorder_type_options.append(disorder_type)
                    region_options.append(region)
                    country_options.append(country)
                    admin1_options.append(admin1)
                    location_options.append(location)

test = pd.DataFrame()
test['DISORDER_TYPE'] = disorder_type_options
test['REGION'] = region_options
test['COUNTRY'] = country_options
test['ADMIN1'] = admin1_options
test['LOCATION'] = location_options
test['EVENT_TYPE'] = event_options
test['SUB_EVENT_TYPE'] = sub_event_options
test['ACTOR1'] = actor1_options
test['INTER1'] = inter_1_options
test['INTER2'] = inter2_options
test['INTERACTION'] = interactions_options



with st.button("Run"):


    pass