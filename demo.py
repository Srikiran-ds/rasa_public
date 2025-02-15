"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd


st.title("RASA'S DASHBOARD")

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


#def creds_entered():
#    if st.session_state["user"].strip() == "rasa" and st.session_state["passwd"].strip()=="key2success" :
#        st.session_state["authenticated"] = True
#    else:
#        st.session_state["authenticated"] = False
#        if not st.session_state["passwd"]:
#            st.warning("Please enter password.")
#        elif not st.session_state["user"]:
#            st.warning("Please enter username.")
#        else:
#            st.error("Invalid username or password")


#def authenticate_user():
#    if "authenticated" not in st.session_state:
#        st.text_input(label="Username:", value="", key="user", on_change=creds_entered)
#        st.text_input(label="Password", value="", key="passwd", type="password", on_change=creds_entered)
#        return False
#    else:
#        if st.session_state["authenticated"]:
#            return True
#        else:
#            st.text_input(label="Username:", value="", key="user", on_change=creds_entered)
#            st.text_input(label="Password : ", value="", key="passwd", type="password", on_change=creds_entered)
#            return False


#if st.session_state["authenticated"]:

#if authenticate_user():
if True:

#@st.cache_data

# Creating tabs

    main_dashboard,input_files,costing,item_wise_payout,discount=st.tabs(["Executive Dashboard","Input Files","Costing","Item Wise Analysis","Coupon Analysis"])

    #placeholder = main_dashboard.empty()
    uploaded_file_annexure = input_files.file_uploader("Choose a annexure file", type = 'xlsx',accept_multiple_files=True)
    uploaded_file_orders = input_files.file_uploader("Choose a orders file", type = 'xlsx')
    uploaded_file_costing = input_files.file_uploader("Choose a costing file", type = 'xlsx')



    @st.cache_data 
    def load_data(uploaded_file_annexure):
        if uploaded_file_annexure is None:
            df = pd.read_excel('invoice_Annexure_980384_22012025_1737568230083.xlsx', sheet_name='Order Level') 
        else:
            #for uploaded_file in uploaded_file_annexure:
            df = pd.read_excel(uploaded_file, sheet_name='Order Level')
        return df
    #if len(uploaded_file_annexure) > 0:
    #    df = pd.read_excel('invoice_Annexure_980384_22012025_1737568230083.xlsx', sheet_name='Order Level')
    #else:
    #    for i in uploaded_file_annexure:
    #        df = pd.read_excel(i, sheet_name='Order Level')
    #        st.write(df.head())

    
    if uploaded_file_annexure:
        for file in uploaded_file_annexure:
            file.seek(0)
        uploaded_data_read = [pd.read_excel(file, sheet_name='Order Level') for file in uploaded_file_annexure]
        df = pd.concat(uploaded_data_read)
    else:
        df=pd.read_excel('invoice_Annexure_980384_22012025_1737568230083.xlsx', sheet_name='Order Level') 
    @st.cache_data
    def load_data2(uploaded_file_orders):
        
        if uploaded_file_orders is None:
            df = pd.read_excel('reports_past_orders_980384_2c0c3fca-b18d-4093-81e5-ea3e551d5c26_2025-01-12_2025-01-18.xlsx')
        else:
            df = pd.read_excel(uploaded_file_orders,skiprows=5)
        return df
    df_1 = load_data2(uploaded_file_orders) 
    @st.cache_data
    def load_data3(uploaded_file_costing):
        if uploaded_file_costing is None:
            df = pd.read_excel('costing.xlsx')
        else:
            df = pd.read_excel(uploaded_file_costing)
        return df
    df_costing = load_data3(uploaded_file_costing) 
    #@st.cache_data
    #df_1 = pd.read_excel('reports_past_orders_980384_2c0c3fca-b18d-4093-81e5-ea3e551d5c26_2025-01-12_2025-01-18.xlsx')
    #@st.cache_data
    #df_costing = pd.read_excel('costing.xlsx')



    costing.header("Costing")
    #costing.dataframe(df_costing.sort_values('Costing', ascending=False))
    #df_costing=
    df_costing=costing.data_editor(df_costing.sort_values('Costing', ascending=False))
    #costing.dataframe(df_costing)

    #main_dashboard.dataframe(df)
    df = df.iloc[1:]

    df.columns = df.iloc[0]
    df = df[1:]


    #Cancelled order %
    Cancelled_perc = len(df_1[df_1['Order-status'] == 'cancelled'])/len(df_1[df_1['Order-status'] == 'delivered'])

    df = df[df['Order Status'] == 'delivered']
    #main_dashboard.dataframe(df)
    #main_dashboard.dataframe(df_1)
    df_1 = df_1[df_1['Order-status'] == 'delivered']
    #main_dashboard
    df['Order Date']=pd.to_datetime(df['Order Date'])
    df['Order Date']=df['Order Date'].dt.date
    col11, col12 = main_dashboard.columns(2)
    #min_date=col11.date_input("start date",value=str(df['Order Date'].min()))
    #max_date=col12.date_input("end date",value=str(df['Order Date'].max()))
    min_date=col11.date_input("start date",value=str(df['Order Date'].min()),min_value=str(df['Order Date'].min()),max_value=str(df['Order Date'].max()))
    max_date=col12.date_input("end date",value=str(df['Order Date'].max()),min_value=str(df['Order Date'].min()),max_value=str(df['Order Date'].max()))
    #main_dashboard.write(min_date)
    #main_dashboard.write(max_date)
    df=df[(df['Order Date']>=min_date) & (df['Order Date']<=max_date)]  

    #main_dashboard.dataframe(df.groupby('Order Date').size())

    #Metrics
    main_dashboard.subheader("Orders Summary")
    col1, col2,col1_3,col1_4 = main_dashboard.columns(4)
    col1.metric("Orders", len(df))
    col2.metric("Sale", round(df['Item Total'].sum(),2))
    col1_3.metric("Cancelled Orders(%)", round(Cancelled_perc*100,2))
    main_dashboard.subheader("Payouts")
    col3,col8 = main_dashboard.columns(2)
    col3.metric("Payout", round(df['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum()))
    col8.metric("Payout %", round((df['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum()/df['Item Total'].sum())*100,2))




    df['payout ratio'] = df['Net Payout for Order (after taxes)\n[A-B-C-D]']/df['Item Total']
    ######Order slot analysis######
    #removing empty datetime rows

    df_ordercleaned = df_1[df_1['Order-acceptance-time <placed_time>'].notna()]

    # Define the timeslots
    timeslots = [
        ('Lunch', '12:00', '16:00'),
        ('Evening', '16:00', '19:00'),
        ('Dinner', '19:00', '23:00'),
        ('Late Dinner1', '23:00', '23:59'),
        ('Late Dinner2', '00:00', '03:00')
    ]

    # Function to count datetime entries in each timeslot
    def count_by_timeslot(df, timeslots):
        counts = {slot[0]: 0 for slot in timeslots}
    
        for index, row in df.iterrows():
            time = row['Order-acceptance-time <placed_time>'].time()
        
            for slot in timeslots:
                start_time = pd.to_datetime(slot[1]).time()
                end_time = pd.to_datetime(slot[2]).time()
            
                if start_time <= time < end_time:
                    counts[slot[0]] += 1
        return counts

    # Get the counts
    counts = count_by_timeslot(df_ordercleaned, timeslots)

    #Combining Late night dinner orders
    counts['Late Dinner'] = counts['Late Dinner1'] + counts['Late Dinner2']
    del counts['Late Dinner1']
    del counts['Late Dinner2']

    #main_dashboard.write("counts")
    #main_dashboard.write(counts)
    

    # Calculate the total number of orders
    total_orders = sum(counts.values())

    # Calculate the percentage of each timeslot
    percentages = {timeslot: (count / total_orders) * 100 for timeslot, count in counts.items()}

    # Print the percentages
    main_dashboard.subheader("Slot-Wise Split")
    #main_dashboard.write(percentages)
    for timeslot, percentage in percentages.items():
        main_dashboard.write(f"{timeslot}: {percentage:.2f}%")


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
    
    #Item order ratio
    item_order_ratio = len(df_melted)/len(df_1)
    col1_4.metric("Items to Order", round(item_order_ratio,2))
    #col1_4.print(item_order_ratio)

    
    df_melted[['Item_name','temp','Qty','Price']] = df_melted['Item'].str.split("_",expand=True)
    #df_melted[['Price','Type','addon']] = df_melted['Price'].str.split("+",expand=True)
    #df_melted['Type'] = df_melted['Type'].fillna(value="")
    df_melted['Item_final_name'] = df_melted['Item_name']
    #df_melted['Item_final_name'] = df_melted['Item_name']+"_"+df_melted['Qty']+"_"+df_melted['Type']
    df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')
    df_melted['Qty'] = pd.to_numeric(df_melted['Qty'], errors='coerce')


    def if_price(df):
        if (df['addon'] == 'Gulab Jamun'):
            return df['Price'] - df['Qty']*10
        elif (df['addon'] == 'Chicken Dum Piece'):
            return df['Price'] - df['Qty']*80
        else:
            return df['Price'] - 20 - df['Qty']*10
        
    #df_melted['Price_final'] = df_melted.apply(if_price, axis = 1)
    df_melted['Price_final'] =df_melted['Price'] 
    df_temp = df[['Order ID','payout ratio']]
    df_temp['payout ratio'] = pd.to_numeric(df_temp['payout ratio'], errors='coerce')


    df_temp['Order ID'] = df_temp['Order ID'].astype(str)
    df_melted['Order ID'] = df_melted['Order ID'].astype(str)

    df_melted = pd.merge(df_melted, df_temp, on='Order ID')

    df_melted['payout'] = df_melted['Price_final']*df_melted['payout ratio']
    #Top Items analysis
    #unique_items = df_melted['Item_final_name'].unique()
    item_counts = df_melted['Item_final_name'].value_counts()
    df_melted = pd.merge(df_melted, df_costing, how='left',on='Item_final_name')
    number = costing.number_input(
    "Default Costing", value=50, placeholder="Type a number..."
)
    df_melted['Costing']=df_melted['Costing'].fillna(number)

    df_melted['avg_payout'] = df_melted['payout'] - df_melted['Costing']


    average_payout = df_melted.groupby('Item_final_name')['avg_payout'].mean().reset_index()
    count = df_melted.groupby('Item_final_name')['avg_payout'].count().reset_index()

    df_final = pd.merge(average_payout, count, on='Item_final_name')
    avg_payout=round(df_final['avg_payout_x']*df_final['avg_payout_y']).sum()/sum(df_final['avg_payout_y'])
    main_dashboard.subheader("Average Payout and Orders")
    col4, col5 = main_dashboard.columns(2)
    col4.metric("Avg Payout Per Item", round(avg_payout))
    col5.metric("Avg Orders Per Day",round(df.groupby('Order Date').size().mean()))
    main_dashboard.subheader("Targets")
    col6, col7 = main_dashboard.columns(2)
    number_cost = col6.number_input("Fixed Costs",value=300000)
    offline = col6.number_input("Offline",value=50000)
    
    col7.metric("Target Orders Per Day",round((number_cost-offline)/30/item_order_ratio/avg_payout))

    #df.groupby('Order Date').size().mean()*avg_payout/round(number/30/1.25/avg_payout)

    main_dashboard.header("Orders Trend")
    main_dashboard.bar_chart(df.groupby('Order Date').size().reset_index(),x='Order Date')
    #main_dashboard.write(locale.currency(df['Item Total'].sum(), grouping=True))

    main_dashboard.header("Sales Trend")
    main_dashboard.bar_chart(df.groupby('Order Date')['Item Total'].sum().reset_index(),x='Order Date')
    #item_counts
    item_wise_payout.header("Top Items By Orders")
    item_wise_payout.dataframe(item_counts)
    item_wise_payout.header("Item Wise Payout")
    item_wise_payout.dataframe(average_payout.sort_values('avg_payout', ascending=False))
    #main_dashboard.write(average_payout)

    ###################Coupon Analysis#################################
    
    df_1['Order ID'] = pd.to_numeric(df_1['Order ID'], errors='coerce')
    df['Order ID'] = pd.to_numeric(df['Order ID'], errors='coerce')
    discount.dataframe(df.head())
    discount.dataframe(df_1.head())
    df_coupon = pd.merge(df, df_1, on='Order ID')
    #pd.DataFrame(df_coupon).to_csv('master_swiggy.csv')

    #couponwise avg payout
    coupon_avgpayout = df_coupon.groupby('Coupon type applied by customer')['payout ratio'].mean().reset_index()
    coupon_avgpayout['payout'] = df_coupon.groupby('Coupon type applied by customer')['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum().reset_index()['Net Payout for Order (after taxes)\n[A-B-C-D]']
    coupon_avgpayout['avg_order_value'] = df_coupon.groupby('Coupon type applied by customer')['Item Total'].mean().reset_index()['Item Total']
    coupon_avgpayout.sort_values(by=['payout ratio'], inplace= True)

    #low payout coupons
    low_coupons = coupon_avgpayout[(coupon_avgpayout['payout ratio']<0.5) & (coupon_avgpayout['payout']>1000)]
    discount.subheader("Low performing coupons")
    discount.dataframe(low_coupons)

    #high payout coupons
    high_coupons = coupon_avgpayout[(coupon_avgpayout['payout ratio']>0.5) & (coupon_avgpayout['payout']>1000)]
    discount.subheader("High performing coupons")
    discount.dataframe(high_coupons)

    ####Swiggyone impact####
    #% Swiggy one % orders
    Swiggy_one_perc = len(df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']>0])/len(df_coupon)
    discount.subheader("Swiggy One Share")
    discount.write(round(Swiggy_one_perc*100,2))
    #print(round(Swiggy_one_perc*100,2))
    
    #% Swiggy one vs Non-swiggy one
    swiggyone_payout = df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']>0]['payout ratio'].mean()
    non_swiggyone_payout = df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']==0]['payout ratio'].mean()
    
    diff_payout_swiggyone = non_swiggyone_payout - swiggyone_payout
    discount.subheader("Swiggy One Additional Discount %")
    discount.write(round(diff_payout_swiggyone*100,2))
    #print(round(diff_payout_swiggyone*100,2))
    
    #Swiggyone_payout lost profit
    df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']>0]['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum()*diff_payout_swiggyone
    discount.subheader("Swiggy One Additional Discount")
    discount.write(df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']>0]['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum())
    #print(df_coupon[df_coupon['Swiggy One \nExclusive Offer Discount']>0]['Net Payout for Order (after taxes)\n[A-B-C-D]'].sum())
    ####################################################################################################################################
