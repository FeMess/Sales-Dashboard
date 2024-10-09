import pandas as pd
import streamlit as st
from utilities import initialize_dataset

st.set_page_config(
    page_title= 'Tables',
    layout='centered'
)

initialize_dataset()

df_sales = st.session_state['datasets_dict']['sales']
df_products = st.session_state['datasets_dict']['products']
df_filiais = st.session_state['datasets_dict']['filiais']

#creating sidebar
st.sidebar.markdown('## Table Selection')

db_table_selected = st.sidebar.selectbox('Select Dataset', 
                     ['Sales', 'Products', 'Subsidiaries'],help='Which dataset do you want to see?'
                     )

if db_table_selected == 'Products':
    st.dataframe(df_products)
elif db_table_selected == 'Subsidiaries':
    st.dataframe(df_filiais)
else:
    st.sidebar.divider()
    st.sidebar.markdown('## Filter Table')
    multi_columns_selected = st.sidebar.multiselect(
                'Select the columns that you want to see',
                list(df_sales.columns),
                list(df_sales.columns)
                )

    #creating double filters
    col_one, col_second = st.sidebar.columns(2)

    db_filter_column_selected = col_one.selectbox(
                    'Column Filter',
                    multi_columns_selected)
    
    db_uniques_column_selected = col_second.selectbox(
                    'Filter Value',
                    df_sales[db_filter_column_selected].unique())
    
    button_filter = col_one.button('Filter')
    button_clear = col_second.button('Clear')

    if button_filter:
        st.dataframe(df_sales[df_sales[db_filter_column_selected] == db_uniques_column_selected][multi_columns_selected], height=650)
    elif button_clear:
        st.dataframe(df_sales[multi_columns_selected],height=650)
    else:
        st.dataframe(df_sales[multi_columns_selected],height=650)

st.sidebar.divider()
st.sidebar.markdown('Developed by ***Felipe Mesquita***')
