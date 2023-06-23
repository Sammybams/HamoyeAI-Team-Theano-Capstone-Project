import streamlit as st
st.set_page_config(page_title="Crime Forecast App", page_icon="📊")

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import folium
from folium import plugins
from streamlit_folium import st_folium, folium_static

#from dotenv import load_dotenv
#load_dotenv('bot_token.env')

st.title('Analysing and Forecasting Crime in Africa')

#DATA_URL = os.environ.get('DATA_URL')
DATA_URL = st.secrets["DATA_URL"]

@st.experimental_memo
def load_data():

	data = pd.read_parquet(DATA_URL)

	return data

# Load 10,000 rows of data into the dataframe.
crime = load_data()

st.header("Hotspots of crimes recorded in Africa")
st.subheader("From 1997 till 2023 March 31st")

years_to_check = [i for i in range(1997, 2024)]

option = st.selectbox(
	'Filter by Year',
	(years_to_check))

st.write('You selected:', option)

map_df = crime[(crime['YEAR']==option)] 

crime_locations = list(zip(map_df.LATITUDE, map_df.LONGITUDE))

base_map = folium.Map(location=[2.318462, 19.56871], zoom_start=3)
heat_map = plugins.HeatMap(crime_locations, radius=6, blur=2)
base_map.add_child(heat_map)

folium_static(base_map, width=700)

st.header("Analysis of Crime rate and Fatalities")

conflict_count = crime["COUNTRY"].value_counts()

fatalities = crime.groupby(["COUNTRY"])[["FATALITIES"]].sum().sort_values(by=["FATALITIES"], axis=0, ascending=False)

per_region = crime.groupby(["REGION"])[["FATALITIES"]].sum()


tab1, tab2, tab3, tab4 = st.tabs(["Highest Record of Crime", "Least Record of Crime", "Most Number of Fatalities","Record of Fatalities Per Region"])

tab1.subheader("Countries with most number of crimes recorded")
tab1.bar_chart(conflict_count.head(6), height = 500)

tab2.subheader("Countries with least number of crimes recorded")
tab2.bar_chart(conflict_count.tail(6), height = 500)

tab3.subheader("Top 5 Countries with most number of fatalities recorded")
tab3.bar_chart(fatalities.head(5), height = 500)

tab4.subheader("Total Record of Fatalities Per Region")
tab4.bar_chart(per_region, height = 500)

deadliest = crime.loc[crime['FATALITIES']==crime['FATALITIES'].max()]

extra = ""
if deadliest.shape[0]>1:
	extra = "s"
st.header(f"Deadliest☠️ Crime{extra} Recorded in Africa🌍")

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
deadliest['INTER2'] = deadliest['INTER2'].map(description)
deadliest.columns = ['EVENT DATE', 'DISORDER TYPE', 'EVENT TYPE', 'SUB EVENT TYPE', 'MAIN ACTOR INVOLVED',
                      'MAIN ACTOR TYPE', 'SUBSIDIARY ACTOR TYPE', 'REGION', 'COUNTRY', 'LARGEST SUB-NATIONAL ADMINISTRATIVE REGION',
                      'LOCATION', 'SOURCE', 'NOTES', 'FATALITIES']

st.markdown(deadliest.T.to_markdown())

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("Built by Team Theano led by [Samuel Bamgbola](https://www.linkedin.com/in/bamgbola-samuel-29baa91a3/)", unsafe_allow_html=True)
