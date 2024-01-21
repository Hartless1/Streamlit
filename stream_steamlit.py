import time
import numpy as np 
import pandas as pd 
import plotly.express as px 
import streamlit as st 
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile

api = KaggleApi()
api.authenticate()
api.dataset_download_files('lsind18/euro-exchange-daily-rates-19992020')

zf = ZipFile('euro-exchange-daily-rates-19992020.zip')
#extracted data is saved in the same directory as notebook
zf.extractall() 
zf.close()

#@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv('euro-daily-hist_1999_2022.csv')

df = get_data()

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

# Get most recent values for KPI comparisons
currentDollar = float(df.loc[0]["[US dollar ]"])
currentPound = float(df.loc[0]["[UK pound sterling ]"])
currentYen = float(df.loc[0]["[Japanese yen ]"])

# top-level filters
date_filter = st.selectbox("Select the Date Period", pd.unique(df[r"Period\Unit:"]))

# dataframe filter
df = df[df[r"Period\Unit:"] == date_filter]

# create three columns
kpi1, kpi2, kpi3 = st.columns(3, gap="small")

#variance to current dollar
selectedDollar = float(df.iloc[0]["[US dollar ]"])
kpi1.metric(
    label="US Dollar $",
    value=selectedDollar,
    delta=round(selectedDollar-currentDollar,2)
)

#variance to current British Pound
selectedPound = float(df.iloc[0]["[UK pound sterling ]"])
kpi2.metric(
    label="UK Pound Sterling £",
    value=selectedPound,
    delta=round(selectedPound-currentPound,2)
)

#variance to current Japanese Yen
selectedYen = float(df.iloc[0]["[Japanese yen ]"])
kpi3.metric(
    label="Japanese Yen ¥",
    value=selectedYen,
    delta=round(selectedYen-currentYen,2)
)

st.markdown("### Detailed Data View")
st.dataframe(df)