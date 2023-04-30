import streamlit as st

st.set_page_config(page_title="Analysis Toolkit", page_icon="📈")

import time
import numpy as np
import pandas as pd
from Crime_Forecast_App import load_data
import json


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
st.header(f"Deadliest☠️ Crime{extra} Recorded in {option} {emoji}")

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
			"LOCATION", "SOURCE", "SOURCE_SCALE", "NOTES", "FATALITIES"]

deadliest.reset_index(drop=True, inplace=True)
deadliest.index = deadliest.index + 1
deadliest = deadliest[details]
deadliest['EVENT_DATE'] = deadliest['EVENT_DATE'].apply(lambda x: x.strftime("%d %B, %Y"))
deadliest['INTER1'] = deadliest['INTER1'].map(description)
deadliest['INTER2'] = deadliest['INTER2'].map(description)
deadliest.columns = ['EVENT DATE', 'DISORDER TYPE', 'EVENT TYPE', 'SUB EVENT TYPE', 'MAIN ACTOR INVOLVED',
                      'MAIN ACTOR TYPE', 'SUBSIDIARY ACTOR TYPE', 'REGION', 'COUNTRY', 'LARGEST SUB-NATIONAL ADMINISTRATIVE REGION',
                      'LOCATION', 'SOURCE', 'SOURCE SCALE', 'NOTES', 'FATALITIES']

st.markdown(deadliest.T.to_markdown())

st.markdown("<br>", unsafe_allow_html=True)

st.header(f"Analysis of Crime rate and Fatalities in {option}{emoji}")

tab1, tab2, tab3 = st.tabs(["Highest Record of Crime",
                            "Lowest Record of Crime",
                            "Highest Total Record of Fatalities"])

conflict_count = selected["ADMIN1"].value_counts()

fatalities = selected.groupby(["ADMIN1"])[["FATALITIES"]].sum().sort_values(by=["FATALITIES"], axis=0, ascending=False)

tab1.subheader("Sub-National Administrative Region with Highest Record of Crime")
tab1.bar_chart(conflict_count.head(3), height = 500)

tab2.subheader("Sub-National Administrative Regions with Lowest Record of Crime")
tab2.bar_chart(conflict_count.tail(3), height = 500)

tab3.subheader("Sub-National Administrative Regions with Highest Total Record of Fatalities")
tab3.bar_chart(fatalities.head(5), height = 500)
# st.button("Re-run")


st.markdown("<br>", unsafe_allow_html=True)
by_actor = selected.groupby(["ACTOR1"])[["FATALITIES"]].sum().sort_values(by=["FATALITIES"], axis=0, ascending=False).head(3)

extra1 = ""
if by_actor.shape[0]>1:
	extra1 = "s"

st.header(f"Top Crime Actor{extra1} in {option}{emoji}")
st.subheader("Between 1997 and 2023 March 31st")

group_of_actors = pd.DataFrame()

by_actor = selected.groupby(["ACTOR1"])[["FATALITIES"]].sum().sort_values(by=["FATALITIES"], axis=0, ascending=False).head(3)
group_of_actors["ACTOR"] = by_actor.index

no_of_crimes = []
for pos in range(0, by_actor.shape[0]):
    no_of_crimes.append(selected.loc[selected["ACTOR1"]==by_actor.index[pos]].shape[0])
group_of_actors["NUMBER OF CRIMES"] = no_of_crimes

group_of_actors["TOTAL FATALITIES"] = by_actor.FATALITIES.values
locations = []
events = []
sub_events = []
fatalites_of_biggest_crime = []
actors_crime_notes = []
for pos in range(0, by_actor.shape[0]):
    locations.append(", ".join(sorted(selected.loc[selected["ACTOR1"]==by_actor.index[pos]].ADMIN1.unique())))
    events.append(", ".join(sorted(selected.loc[selected["ACTOR1"]==by_actor.index[pos]].EVENT_TYPE.unique())))
    sub_events.append(", ".join(sorted(selected.loc[selected["ACTOR1"]==by_actor.index[pos]].SUB_EVENT_TYPE.unique())))

    # Getting Description of Biggest Crime in terms of Fatalities.
    actors_crimes = selected.loc[selected["ACTOR1"]==by_actor.index[pos]]
    fatalites_of_biggest_crime.append(actors_crimes.loc[actors_crimes["FATALITIES"]==actors_crimes["FATALITIES"].max()].head(1).FATALITIES.values[0])
    actors_crime_notes.append(actors_crimes.loc[actors_crimes["FATALITIES"]==actors_crimes["FATALITIES"].max()].head(1).NOTES.values[0])


group_of_actors["SUB-NATIONAL ADMINISTRATIVE REGIONS OPERATED"] = locations
group_of_actors["EVENT TYPES"] = events
group_of_actors["SUB-EVENT TYPES"] = sub_events
group_of_actors["NUMBER OF FATALITIES IN BIGGEST CRIME"] = fatalites_of_biggest_crime
group_of_actors["DESCRIPTION OF BIGGEST CRIME"] = actors_crime_notes

group_of_actors.reset_index(drop=True, inplace=True)
group_of_actors.index = group_of_actors.index + 1
st.markdown(group_of_actors.T.to_markdown())