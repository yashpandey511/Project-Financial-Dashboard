import pandas as pd
import plotly.graph_objs as go
import streamlit as st # type: ignore
from streamlit_option_menu import option_menu
from model import DataScraper
import warnings
warnings.filterwarnings("ignore")


def main():
    # settings
    pd.options.plotting.backend = "plotly"

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
        if st.button('Visualize QoQ Results'):
            qoq_df = data_scraper.qoq_results()

            #Area Plot for QoQ Results - Sales, Expenses, Net Profit
             # Create traces
            trace1 = go.Scatter(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 1],
                mode='lines',
                fill='tozeroy',
                name='Sales'
            )
            trace2 = go.Scatter(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 2],
                mode='lines',
                fill='tozeroy',
                name='Expenses'
            )
            trace3 = go.Scatter(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 10],
                mode='lines',
                fill='tozeroy',
                name='Net Profit'
            )

            data = [trace1, trace2, trace3]

            # Layout
            layout = go.Layout(
                title='QoQ Results - Sales, Expenses & Net Profit',
                xaxis=dict(title='Quarter'),
                yaxis=dict(title='Amount (in Crs.)'),
                legend=dict(x=0, y=1)
            )

            # Plot
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig)

            #Line Plot for QoQ Results - Net Profit, EPS
            # Create traces
            trace1 = go.Scatter(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 10],
                mode='lines',
                name='Net Profit'
            )
            trace2 = go.Scatter(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 11],
                mode='lines',
                name='EPS',
                yaxis='y2'
            )
            data = [trace1, trace2]

            # Layout
            layout = go.Layout(
                title='QoQ Results - Net Profit & EPS',
                xaxis=dict(title='Quarter'),
                yaxis=dict(title='Net Profit (in Crs.)', showgrid=False),
                yaxis2=dict(title='EPS', overlaying='y', side='right', showgrid=False),
                legend=dict(x=0, y=1)
            )

            # Plot
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig)

            # Create stacked bar chart traces
            trace1 = go.Bar(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 3],
                name='Operating Profit'
            )
            trace2 = go.Bar(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 5],
                name='Other Income'
            )
            trace3 = go.Bar(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 6],
                name='Interest'
            )
            trace4 = go.Bar(
                x=qoq_df['Quarter'],
                y=qoq_df.iloc[:, 7],
                name='Depreciation'
            )

            data = [trace1, trace2, trace3, trace4]

            # Layout
            layout = go.Layout(
                title='Breakdown of Profit before Tax',
                xaxis=dict(title='Quarter'),
                yaxis=dict(title='Amount (in Crs.)'),
                barmode='stack'  # Stacked bar chart
            )

            # Plot
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig)

        
    elif selected_option == 'YoY Results':
        a = 1
        

if __name__ == '__main__':
    main()
