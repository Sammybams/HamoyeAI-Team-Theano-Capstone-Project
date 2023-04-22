import streamlit as st
import time
import numpy as np
from Crime_Forecast_App import load_data
import json

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

f = open('country_flags.json')
data = json.load(f) # returns JSON object as a dictionary

emoji = ""
for country in data:
    if country['name'] == option:
        emoji = country['emoji']

selected = crime.loc[crime['COUNTRY']==option]
max_fatality = selected.FATALITIES.max()
by_fatality = selected[selected['FATALITIES']==max_fatality]

st.write('You selected:', option)

deadliest = selected.loc[selected['FATALITIES']==selected['FATALITIES'].max()]

extra = ""
if deadliest.shape[0]>1:
	extra = "s"
st.header(f"Deadliest☠️ Crime{extra} Recorded in {option}{emoji}")

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
details = ["EVENT_DATE", "DISORDER_TYPE", "EVENT_TYPE", "SUB_EVENT_TYPE",
			"ACTOR1", "INTER1", "INTER2", "REGION", "COUNTRY", "ADMIN1",
			"LOCATION", "SOURCE", "NOTES", "FATALITIES"]

deadliest.reset_index(drop=True, inplace=True)
deadliest.index = deadliest.index + 1
deadliest = deadliest[details]
deadliest['EVENT_DATE'] = deadliest['EVENT_DATE'].apply(lambda x: x.strftime("%d %B, %Y"))
deadliest['INTER1'] = deadliest['INTER1'].map(description)
deadliest['INTER2'] = deadliest['INTER1'].map(description)
deadliest.columns = ['EVENT DATE', 'DISORDER TYPE', 'EVENT TYPE', 'SUB EVENT TYPE', 'MAIN ACTOR INVOLVED',
                      'MAIN ACTOR TYPE', 'SUBSIDIARY ACTOR TYPE', 'REGION', 'COUNTRY', 'LARGEST SUB-NATIONAL ADMINISTRATIVE REGION',
                      'LOCATION', 'SOURCE', 'NOTES', 'FATALITIES']

st.markdown(deadliest.T.to_markdown())


st.button("Re-run")