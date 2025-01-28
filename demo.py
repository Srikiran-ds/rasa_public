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
#df= pd.read_excel('payout.xlsx',sheet_name='Order Level',skiprows=2)
#st.write(df.head())
# -*- coding: utf-8 -*-
"""

"""


import pandas as pd
import numpy as np

df = pd.read_excel('invoice_Annexure_980384_22012025_1737568230083.xlsx', sheet_name='Order Level') 

df_1 = pd.read_excel('reports_past_orders_980384_2c0c3fca-b18d-4093-81e5-ea3e551d5c26_2025-01-12_2025-01-18.xlsx')

df_costing = pd.read_excel('costing.xlsx')

main_dashboard,costing=st.tabs(["Executive Dashboard","Costing"])

costing.dataframe(df_costing.sort_values('Costing', ascending=False))

df = df.iloc[1:]

df.columns = df.iloc[0]
df = df[1:]

#Metrics
col1, col2, col3 = main_dashboard.columns(3)
col1.metric("Orders", "70 °F", "1.2 °F")
col2.metric("Sale", "9 mph", "-8%")
col3.metric("Payout", "86%", "4%")

df = df[df['Order Status'] == 'delivered']
df_1 = df_1[df_1['Order-status'] == 'delivered']

df['payout ratio'] = df['Net Payout for Order (after taxes)\n[A-B-C-D]']/df['Item Total']

df_1.rename(columns={ df_1.columns[30]: "item1" }, inplace = True)
df_1.rename(columns={ df_1.columns[31]: "item2" }, inplace = True)
df_1.rename(columns={ df_1.columns[32]: "item3" }, inplace = True)
df_1.rename(columns={ df_1.columns[33]: "item4" }, inplace = True)
df_1.rename(columns={ df_1.columns[34]: "item5" }, inplace = True)
df_1.rename(columns={ df_1.columns[35]: "item6" }, inplace = True)

# Reshape the data using melt
df_melted = df_1.melt(id_vars='Order ID', value_vars=['item1', 'item2', 'item3','item4', 'item5', 'item6'], 
                    var_name='Item_Column', value_name='Item')

# Filter out empty rows
df_melted = df_melted.dropna()
df_melted[['Item_name','temp','Qty','Price']] = df_melted['Item'].str.split("_",expand=True)
df_melted[['Price','Type','addon']] = df_melted['Price'].str.split("+",expand=True)
df_melted['Type'] = df_melted['Type'].fillna(value="")

df_melted['Item_final_name'] = df_melted['Item_name']+"_"+df_melted['Qty']+"_"+df_melted['Type']
df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')
df_melted['Qty'] = pd.to_numeric(df_melted['Qty'], errors='coerce')


def if_price(df):
    if (df['addon'] == None):
        return df['Price'] - df['Qty']*10
    else:
        return df['Price'] - 20 - df['Qty']*10
    
df_melted['Price_final'] = df_melted.apply(if_price, axis = 1)

df_temp = df[['Order ID','payout ratio']]
df_temp['payout ratio'] = pd.to_numeric(df_temp['payout ratio'], errors='coerce')


df_temp['Order ID'] = df_temp['Order ID'].astype(str)
df_melted['Order ID'] = df_melted['Order ID'].astype(str)

df_melted = pd.merge(df_melted, df_temp, on='Order ID')

df_melted['payout'] = df_melted['Price_final']*df_melted['payout ratio']

df_melted = pd.merge(df_melted, df_costing, on='Item_final_name')

df_melted['avg_payout'] = df_melted['payout'] - df_melted['Costing']


average_payout = df_melted.groupby('Item_final_name')['avg_payout'].mean().reset_index()
count = df_melted.groupby('Item_final_name')['avg_payout'].count().reset_index()

df_final = pd.merge(average_payout, count, on='Item_final_name')

(df_final['avg_payout_x']*df_final['avg_payout_y']).sum()/sum(df_final['avg_payout_y'])


#main_dashboard.write(average_payout)
