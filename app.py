import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    try:
        df = pd.read_csv("C:\Users\jonesp\Documents\TripleTen_project\vehicles_us.csv")
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

st.title('Vehicle Data Explorer')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"], accept_multiple_files=False)

if uploaded_file is not None:
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    df = load_data(file_path)

    if df is not None:
        st.header('Data viewer')

        show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
        if not show_manuf_1k_ads:
            df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

        st.dataframe(df)

        st.header('Vehicle types by manufacturer')
        st.write(px.histogram(df, x='manufacturer', color='type'))

        st.header('Histogram of `condition` vs `model_year`')
        st.write(px.histogram(df, x='model_year', color='condition'))

        st.header('Compare price distribution between manufacturers')
        manufac_list = sorted(df['manufacturer'].unique())
        manufacturer_1 = st.selectbox('Select manufacturer 1', manufac_list, index=manufac_list.index('chevrolet'))
        manufacturer_2 = st.selectbox('Select manufacturer 2', manufac_list, index=manufac_list.index('hyundai'))

        mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
        df_filtered = df[mask_filter]

        normalize = st.checkbox('Normalize histogram', value=True)
        if normalize:
            histnorm = 'percent'
        else:
            histnorm = None

        st.write(px.histogram(df_filtered,
                            x='price',
                            nbins=30,
                            color='manufacturer',
                            histnorm=histnorm,
                            barmode='overlay'))
else:
    st.warning("Please upload a CSV file.")
