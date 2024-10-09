import pathlib
import pandas as pd
import streamlit as st

COMMISSION = 0.05

def initialize_dataset():
    if not 'datasets_dict' in st.session_state:
        py_cwd = pathlib.Path(__file__).parent
        datasets_cwd = py_cwd / 'datasets'

        #importing sales_dataset
        df_sales = pd.read_csv(datasets_cwd / 'vendas.csv' , sep= ';', index_col=0)
        df_sales.index = pd.to_datetime(df_sales.index)

        df_sales.columns = ['ID' , 'City' , 'Seller' , 'Product', 'Client Name', 'Client Gender', 'Payment Form' ]
        df_sales.rename_axis('Date', inplace= True)
        

        #importing filiais
        df_filiais = pd.read_csv(datasets_cwd / 'filiais.csv' , sep= ';', index_col=0)
        df_filiais.columns = ['State', 'City', 'Sellers']
        df_filiais.rename_axis('ID', inplace= True)
        df_filiais.index = df_filiais.index.astype('str')


        #importing products
        df_products = pd.read_csv(datasets_cwd / 'produtos.csv' , sep= ';', index_col=0)
        df_products.columns = ['Product', 'ID', 'Price']
        df_products.set_index('ID', inplace=True)
        df_products.index = df_products.index.astype('str')

        datasets = {
            'sales' : df_sales,
            'filiais' : df_filiais,
            'products' : df_products
        }

        st.session_state['path'] = datasets_cwd
        st.session_state['datasets_dict'] = datasets

def merge_dataset_sales(sales, products, filiais):
    #merge sales with products
    sales = sales.reset_index()

    sales = pd.merge(left= sales,
                     right= products,
                     on= 'Product',
                     how= 'left')

    sales.set_index('Date' , inplace= True)

    #merge new sales with filiais
    sales = sales.reset_index()

    sales = pd.merge(left= sales,
                     right= filiais[['State', 'City']],
                     on= 'City',
                     how='left')
    
    sales.set_index(keys='Date', inplace=True)

    sales.index = pd.to_datetime(sales.index)

    return sales