"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
#import locale

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
import warnings
warnings.filterwarnings('ignore')

#@st.cache_data
@st.cache_data 
def load_data():
    uploaded_file = st.file_uploader("Choose a annexure file", type = 'xlsx')
    if uploaded_file is not None:
        df = pd.read_excel('invoice_Annexure_980384_22012025_1737568230083.xlsx', sheet_name='Order Level') 
    else:
        df = pd.read_excel(uploaded_file, sheet_name='Order Level')
    return df
df = load_data() 
@st.cache_data
def load_data2():
    df = pd.read_excel('reports_past_orders_980384_2c0c3fca-b18d-4093-81e5-ea3e551d5c26_2025-01-12_2025-01-18.xlsx')
    return df
df_1 = load_data2() 
@st.cache_data
def load_data3():
    df = pd.read_excel('costing.xlsx')
    return df
df_costing = load_data3() 
#@st.cache_data
#df_1 = pd.read_excel('reports_past_orders_980384_2c0c3fca-b18d-4093-81e5-ea3e551d5c26_2025-01-12_2025-01-18.xlsx')
#@st.cache_data
#df_costing = pd.read_excel('costing.xlsx')

main_dashboard,costing,item_wise_payout=st.tabs(["Executive Dashboard","Costing","Item Wise Payout"])

costing.header("Costing")
costing.dataframe(df_costing.sort_values('Costing', ascending=False))

df = df.iloc[1:]

df.columns = df.iloc[0]
df = df[1:]



df = df[df['Order Status'] == 'delivered']
df_1 = df_1[df_1['Order-status'] == 'delivered']

df['Order Date']=pd.to_datetime(df['Order Date'])
df['Order Date']=df['Order Date'].dt.date

#main_dashboard.dataframe(df.groupby('Order Date').size())

#Metrics
col1, col2, col3,col8 = main_dashboard.columns(4)
col1.metric("Orders", len(df))
col2.metric("Sale", df['Item Total'].sum())
col3.metric("Payout", round(df['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum()))
col8.metric("Payout %", round((df['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum()/df['Item Total'].sum())*100,2))




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
avg_payout=round(df_final['avg_payout_x']*df_final['avg_payout_y']).sum()/sum(df_final['avg_payout_y'])

col4, col5 = main_dashboard.columns(2)
col4.metric("Avg Payout Per Item", round(avg_payout))
col5.metric("Avg Orders Per Day",round(df.groupby('Order Date').size().mean()))

col6, col7 = main_dashboard.columns(2)
number = col6.number_input("Fixed Costs",value=300000)

col7.metric("Target Orders Per Day",round(number/30/1.25/avg_payout))

#df.groupby('Order Date').size().mean()*avg_payout/round(number/30/1.25/avg_payout)

main_dashboard.header("Orders Trend")
main_dashboard.bar_chart(df.groupby('Order Date').size().reset_index(),x='Order Date')
#main_dashboard.write(locale.currency(df['Item Total'].sum(), grouping=True))

main_dashboard.header("Sales Trend")
main_dashboard.bar_chart(df.groupby('Order Date')['Item Total'].sum().reset_index(),x='Order Date')

item_wise_payout.header("Item Wise Payout")
item_wise_payout.dataframe(average_payout.sort_values('avg_payout', ascending=False))
#main_dashboard.write(average_payout)
