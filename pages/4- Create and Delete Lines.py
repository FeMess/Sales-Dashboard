import pandas as pd
import streamlit as st
import datetime
from utilities import initialize_dataset

st.set_page_config(
    page_title='Create and Delete',
    layout= 'centered'
)

initialize_dataset()

df_sales = st.session_state['datasets_dict']['sales']
df_products = st.session_state['datasets_dict']['products']
df_filiais = st.session_state['datasets_dict']['filiais']

#concat column in df_filiais
df_filiais['City/State'] = df_filiais['City'] + '/' + df_filiais['State']

# creating filters
st.sidebar.markdown('## Add Sales')
cityUF_selected = st.sidebar.selectbox('Select the City',
                                            df_filiais['City/State'].unique().tolist())

sellers = df_filiais[df_filiais['City/State'] == cityUF_selected]['Sellers'].iloc[0]
sellers = str(sellers)
sellers = sellers.strip('[]').strip("'").split("', '")

sellers_selected = st.sidebar.selectbox('Select the Seller',
                                        sellers)

product_selected = st.sidebar.selectbox('Select the Product',
                                        df_products['Product'].to_list())

client_name = st.sidebar.text_input('What is the client name?')

client_gender_selected = st.sidebar.selectbox('Client Gender',
                                     ['Male', 'Female'])

paymentform_selected = st.sidebar.selectbox('Payment Form',
                                     ['Credit', 'Debit'])

bt_add = st.sidebar.button('Add')

if bt_add:
    list_to_add = [
        df_sales['ID'].max() + 1,
        cityUF_selected.split('/')[0],
        sellers_selected,
        product_selected,
        client_name,
        client_gender_selected,
        paymentform_selected
    ]

    index_now = datetime.datetime.now()
    df_sales.loc[index_now] = list_to_add
    st.session_state['datasets_dict']['sales'] = df_sales

#creating remove sale
st.sidebar.divider()
st.sidebar.markdown('## Remove Sales')
id_remove = st.sidebar.number_input('What is the Sale ID?',
                                    min_value= 0,
                                    max_value= max(df_sales['ID'].to_list()))

bt_remove = st.sidebar.button('Remove')

if bt_remove:
    df_sales = df_sales[df_sales['ID'] != id_remove]
    st.session_state['datasets_dict']['sales'] = df_sales

st.dataframe(df_sales, height= 650)

st.sidebar.markdown('Developed by ***Felipe Mesquita***')