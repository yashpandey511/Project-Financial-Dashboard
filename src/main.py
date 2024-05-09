import pandas as pd
import plotly.express as px
import streamlit as st # type: ignore
from streamlit_option_menu import option_menu
from model import DataScraper
import warnings
warnings.filterwarnings("ignore")


def main():
    with st.sidebar:
        selected_option = option_menu(
            menu_title='Main Menu',
            options=['Raw Data', 'QoQ Results', 'YoY Results'],
            default_index=0,
        )

    
    if selected_option == 'Raw Data':
        st.title('Company Data Scraper')
        company = st.text_input('Enter the Ticker:')
        data_scraper = DataScraper(company)
        if st.button('Scrape Data'):
            st.write("Income Statement - QoQ Results")
            st.write(data_scraper.qoq_results())
            st.write("Profit and Loss - YoY Results")
            st.write(data_scraper.yoy_results())
            st.write("Compound Sales Growth Rate")
            st.write(data_scraper.compound_sales_growth())
            st.write("Compound Profit Growth Rate")
            st.write(data_scraper.compound_profit_growth()) 
            st.write("Stock Price CAGR")
            st.write(data_scraper.stock_price_cagr())
            st.write("Return on Equity")
            st.write(data_scraper.roe())
            st.write("Balance Sheet")
            st.write(data_scraper.balance_sheet())
            st.write("Cashflow")
            st.write(data_scraper.cashflow())
            if data_scraper.ratios() is not None:
                st.write("Ratios")
                st.write(data_scraper.ratios())
            st.write("Share Holding Pattern")
            st.write(data_scraper.shareholding_pattern())

    elif selected_option == 'QoQ Results':
        st.title('Company Data Scraper')
        company = st.text_input('Enter the Ticker:')
        data_scraper = DataScraper(company)
        if st.button('Scrape Data'):
            st.write("Income Statement - QoQ Results")
            qoq_df = data_scraper.qoq_results()
            st.line_chart()
        
    elif selected_option == 'YoY Results':
        a = 1
        

if __name__ == '__main__':
    main()
