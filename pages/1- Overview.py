import pandas as pd
import streamlit as st
import datetime
import plotly.express as px

from utilities import initialize_dataset, COMMISSION, merge_dataset_sales

st.set_page_config(
    page_title= 'Overview',
    layout= 'wide',
    initial_sidebar_state='auto'
)

st.markdown('# Sales Dashboard')

initialize_dataset()

df_sales = st.session_state['datasets_dict']['sales']
df_products = st.session_state['datasets_dict']['products']
df_filiais = st.session_state['datasets_dict']['filiais']

df_sales = merge_dataset_sales(df_sales , df_products, df_filiais)
df_sales['Commission'] = df_sales['Price'] * COMMISSION

#creating the filters
date_end_default_limit = df_sales.index.date.max()
date_start_limit = df_sales.index.date.min()
date_start_default = datetime.date(year= date_end_default_limit.year, month= date_end_default_limit.month-1, day= 1)

dt_start = st.sidebar.date_input('Start Date',
                                 max_value= date_end_default_limit,
                                 min_value= date_start_limit,
                                 value= date_start_default)

dt_end = st.sidebar.date_input('End Date',
                                max_value= date_end_default_limit,
                                min_value= date_start_limit,
                                value= date_end_default_limit)

analysis_selected = st.sidebar.selectbox('Select Analysis',
                                 options= ['City', 'Product', 'Client Gender', 'Payment Form'])

#creating columns and metrics
col1,col2,col3,col4 = st.columns(4)

df_sales_metric_date = df_sales[(df_sales.index.date <= dt_end) & (df_sales.index.date >= dt_start)]
key_subsidiarie = df_sales_metric_date['City'].value_counts().index[0]
key_seller = df_sales_metric_date['Seller'].value_counts().index[0]

col1.metric('Total Sales',
            value= f"R$ {df_sales_metric_date['Price'].sum():.2f}")

col2.metric('Quantity Sales',
            value= df_sales_metric_date['ID'].count())

col3.metric('Key Subsidiarie',
            value= key_subsidiarie)

col4.metric('Key Subsidiarie',
            value= key_seller)

st.divider()

#creating charts
col_below_1, col_below_2 = st.columns(2)

df_sales_metric_date['Sale Day'] = df_sales_metric_date.index.date
group_sales = df_sales_metric_date.groupby('Sale Day')[['Price']].sum()

col_below_1.markdown('**Price by Sale Day**')

fig_1 = px.line(data_frame=group_sales, markers=True)
col_below_1.plotly_chart(fig_1)

txt_title_chart_pie = analysis_selected + ' Participation'

col_below_2.markdown(f'**{txt_title_chart_pie}**')
fig = px.pie(data_frame= df_sales_metric_date,
              names= analysis_selected,
              values= 'Price')

col_below_2.plotly_chart(fig)

st.divider()

st.sidebar.markdown('Developed by ***Felipe Mesquita***')