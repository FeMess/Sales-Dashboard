import streamlit as st

st.set_page_config(
    layout= 'centered',
    page_title= 'Home'
    )

st.sidebar.markdown('Developed by ***Felipe Mesquita***')

st.header('Welcome to Sales Dashboard')
st.divider()
st.markdown('''
           I'm utilizing **three key libraries** in this development. There are:
           - `Pandas`: to extract, load and transform (ETL) the dataset.
           - `Streamlit`: to create a web dashboard in Python for analysis.
           - `Plotly`: to create an attractive charts.
            
           Thank you.
            
           You can contact me on Linkedin [Felipe Mesquita](https://www.linkedin.com/in/felipemesquita19).
           ''')
