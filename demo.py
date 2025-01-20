"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

st.header("RASA'S DASHBOARD")

#reading excelfile
#from io import StringIO
#uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')

#skiprows
#df = xls.parse('Sheet1', skiprows=4, index_col=None, na_values=['NA'])
df= pd.read_excel('payout.xlsx',sheet_name='Order Level',skiprows=2)
st.write(df.head())