import streamlit as st

st.set_page_config(page_title="Forecasting Toolkit", page_icon="🌍")

import pandas as pd
import numpy as np
import datetime
from Crime_Forecast_App import load_data
from pickle import load

# from dotenv import load_dotenv
# load_dotenv('bot_token.env')

st.markdown("# Forecasting Toolkit")
st.sidebar.header("Forecasting Toolkit")

st.subheader(
    """Forecast the occurence in a location based on observed disorder type and date."""
)

crime = load_data()
# DATA_URL_ENCODED = DATA_URL = os.environ.get('DATA_URL_ENCODED')
DATA_URL_ENCODED = st.secrets["DATA_URL_ENCODED"]


@st.experimental_memo
def load_data_encoded():

	data = pd.read_parquet(DATA_URL_ENCODED)

	return data

@st.experimental_memo
def load_models():
    scaler = load(open('scaler.pkl', 'rb'))
    pca = load(open('pca.pkl', 'rb'))
    model = load(open('model.pkl', 'rb')) 

    return scaler, pca, model

description = {
    0: "Others",
    1: "State Forces",
    2: "Rebel Groups",
    3: "Political Militias",
    4: "Identity Militias",
    5: "Rioters",
    6: "Protesters",
    7: "Civilians",
    8: "External/Other Forces"
}

encoded_set = load_data_encoded()
actor1_dict = dict(zip(crime.ACTOR1.unique(), encoded_set.ACTOR1_encode.unique()))
actor1_dict_reverse = dict(zip(encoded_set.ACTOR1_encode.unique(), crime.ACTOR1.unique()))

admin1_dict = dict(zip(crime.ADMIN1.unique(), encoded_set.ADMIN1_encode.unique()))
admin1_dict_reverse = dict(zip(encoded_set.ADMIN1_encode.unique(), crime.ADMIN1.unique()))

location_dict = dict(zip(crime.LOCATION.unique(), encoded_set.LOCATION_encode.unique()))
location_dict_reverse = dict(zip(encoded_set.LOCATION_encode.unique(), crime.LOCATION.unique()))


mapping_binned_reverse = {
    0: "101 TO 500",
    1: "11 TO 50",
    2: "1",
    3: "2 TO 10",
    4: "501 TO 1350",
    5: "51 TO 100",
    6: "0"
}

correct_order = {
    "101 TO 500": 5,
    "11 TO 50": 3,
    "1": 1,
    "2 TO 10": 2,
    "501 TO 1350" :6,
    "51 TO 100": 4,
    "0": 0 
}

correct_order_reverse = {
    5: "101 TO 500",
    3: "11 TO 50",
    1: "1",
    2: "2 TO 10",
    6: "501 TO 1350",
    4: "51 TO 100",
    0: "0"
}
date = st.date_input(
    "Choose expected date",
    value = datetime.datetime.today(),
    min_value=datetime.datetime(1997, 1, 1))

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
    'Select Largest Sub-national Administrative Region',
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
date_time_options = []
for event in updated.EVENT_TYPE.unique():
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
                    date_time_options.append(date)


test = pd.DataFrame(0, index=np.arange(len(event_options)), columns=encoded_set.columns.values)
record = pd.DataFrame()

test['EVENT_DATE'] = date_time_options
test['EVENT_DATE'] = pd.to_datetime(test.EVENT_DATE, format='%Y-%m-%d')
record['EVENT_DATE'] = date_time_options

test['DISORDER_TYPE'] = disorder_type_options
record['DISORDER_TYPE'] = disorder_type_options

test['REGION'] = region_options
record['REGION'] = region_options

test['COUNTRY'] = country_options
record['COUNTRY'] = country_options

test['ADMIN1'] = admin1_options
record['ADMIN1'] = admin1_options

test['LOCATION'] = location_options
record['LOCATION'] = location_options

test['EVENT_TYPE'] = event_options
record['EVENT_TYPE'] = event_options

test['SUB_EVENT_TYPE'] = sub_event_options
record['SUB_EVENT_TYPE'] = sub_event_options

test['ACTOR1'] = actor1_options
record['ACTOR1'] = actor1_options

test['INTER1'] = inter_1_options
record['INTER1'] = test['INTER1'].map(description)

test['INTER2'] = inter2_options
record['INTER2'] = test['INTER2'].map(description)

test['INTERACTION'] = interactions_options


test['ADMIN1_encode'] = test['ADMIN1'].map(admin1_dict)
test['LOCATION_encode'] = test['LOCATION'].map(location_dict)
test['ACTOR1_encode'] = test['ACTOR1'].map(actor1_dict)

one_hot_sample = pd.get_dummies(test, columns = ['DISORDER_TYPE', 'REGION', 'COUNTRY', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'INTER1', 'INTER2'])

for col in one_hot_sample.columns.values:
    if col in encoded_set.columns.values:
        test[col] = one_hot_sample[col].values

test['day_of_year'] = test.EVENT_DATE.dt.day_of_year
test['month'] = test.EVENT_DATE.dt.month
test['year'] = test.EVENT_DATE.dt.year

test.drop(['ADMIN1', 'LOCATION', 'ACTOR1', 'EVENT_DATE', 'fatalites-binned',
           'fatalities-binned-encoded', 'DISORDER_TYPE', 'REGION', 'COUNTRY',
           'EVENT_TYPE', 'SUB_EVENT_TYPE', 'INTER1', 'INTER2'], axis=1, inplace=True)

# st.write(test)

if st.button("Run"):
    st.header("Predictions")

    scaler, pca, model = load_models()

    test_scaled = scaler.transform(test.values)
    test_scaled_pca = pca.transform(test_scaled)
    predictions = model.predict(test_scaled_pca)

    # #st.write(predictions)

    record['PREDICTED FATALITIES'] = predictions
    record['PREDICTED FATALITIES'] = record['PREDICTED FATALITIES'].map(mapping_binned_reverse)


    record.columns = ['EVENT DATE', 'DISORDER TYPE','REGION', 'COUNTRY',
                      'LARGEST SUB-NATIONAL ADMINISTRATIVE REGION',
                      'LOCATION', 'EVENT TYPE', 'SUB EVENT TYPE', 'MAIN ACTOR INVOLVED',
                      'MAIN ACTOR TYPE', 'SUBSIDIARY ACTOR TYPE', 'PREDICTED FATALITIES']
    
    record['PREDICTED FATALITIES'] = record['PREDICTED FATALITIES'].map(correct_order)
    record = record.sort_values(by=['PREDICTED FATALITIES'], ascending=False)

    record['PREDICTED FATALITIES'] = record['PREDICTED FATALITIES'].map(correct_order_reverse)
    
    # record = record.sort_values(by=['CORRECT ORDER'], ascending=False)

    # st.write(record)

    record.reset_index(drop=True, inplace=True)
    record.index = record.index + 1

    # record.drop(['CORRECT ORDER'], axis=1, inplace=True)

    top_2 = record.head(2)
    # Reset index and add 1 to index to start at 1
    top_2.reset_index(drop=True, inplace=True)
    top_2.index = top_2.index + 1

    bottom_2 = record.tail(2)
    # Reset index and add 1 to index to start at 1
    bottom_2.reset_index(drop=True, inplace=True)
    bottom_2.index = bottom_2.index + 1

    extra_s1 = ""
    extra_s2 = ""
    if len(top_2) > 1:
        extra_s1 = "s"
    if len(bottom_2) > 1:
        extra_s2 = "s"

    tab1, tab2 = st.tabs([f"Worst Case Scenario{extra_s1}", f"Best Case Scenario{extra_s1}"])

    tab1.subheader("Highest Predicted Fatalities")
    tab1.markdown(top_2.T.to_markdown())
     
    tab2.subheader("Lowest Predicted Fatalities")
    tab2.markdown(bottom_2.T.to_markdown())