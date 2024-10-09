import pandas as pd
import streamlit as st
from utilities import initialize_dataset, COMMISSION

st.set_page_config(
    page_title= 'Dinamic View',
    layout= 'centered'
)


st.sidebar.markdown('Developed by ***Felipe Mesquita***')

initialize_dataset()

df_sales = st.session_state['datasets_dict']['sales']
df_products = st.session_state['datasets_dict']['products']
df_filiais = st.session_state['datasets_dict']['filiais']

#defining columns to analysis
INDEX_COLUMNS = ['City', 'Seller', 'Product', 'Client Gender', 'Payment Form']
VALUE_ANALYSIS = ['Price', 'Commission']
AGG_FUNCTIONS = ['Sum' , 'Count']

#merge and add commission
df_sales = df_sales.reset_index()

df_sales = pd.merge(left= df_sales,
                    right= df_products[['Product', 'Price']],
                    on='Product',
                    how='left')

df_sales.set_index('Date', inplace=True)
df_sales['Commission'] =  df_sales['Price'] * COMMISSION

#creating the filters
index_selected_analysis = st.sidebar.selectbox('Select the Index to Analysis',
                                              INDEX_COLUMNS,
                                              index= INDEX_COLUMNS.index('Seller'))

INDEX_COLUMNS_EXP = [x for x in INDEX_COLUMNS if not x == index_selected_analysis]

columns_selected_analysis = st.sidebar.selectbox('Select the column to Analysis',
                                                 INDEX_COLUMNS_EXP,
                                                 index = INDEX_COLUMNS_EXP.index('Product'))

value_analysis_selected = st.sidebar.selectbox('Select the Analysis Value',
                                               VALUE_ANALYSIS,
                                               index= VALUE_ANALYSIS.index('Price'))

agg_analysis_selected = st.sidebar.selectbox('Which is the Metric?',
                                             options= AGG_FUNCTIONS,
                                             index= AGG_FUNCTIONS.index('Count'))

if index_selected_analysis in INDEX_COLUMNS and columns_selected_analysis in INDEX_COLUMNS and value_analysis_selected in VALUE_ANALYSIS and agg_analysis_selected in AGG_FUNCTIONS:
    df_sales_pivot = pd.pivot_table(data= df_sales,
                                    index= index_selected_analysis,
                                    columns= columns_selected_analysis,
                                    values= value_analysis_selected,
                                    aggfunc= agg_analysis_selected.lower())
    df_sales_pivot['Total Column'] = df_sales_pivot.sum(axis=1)
    df_sales_pivot.loc['Total Row'] = df_sales_pivot.sum(axis=0).to_list()
    
    st.dataframe(df_sales_pivot)

else:
    st.dataframe(df_sales)

st.sidebar.divider()
st.sidebar.markdown('Developed by **Felipe Mesquita**')
