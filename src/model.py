import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
import statistics
warnings.filterwarnings("ignore")

class DataScraper:
    def __init__(self, company):
        self.company = company

    @staticmethod
    def scrap_data(company): # Static method to scrape data from webpage
        # Scrape data from web page
        url = f'https://www.screener.in/company/{company}/consolidated/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            return None

    @staticmethod
    def get_table(soup): # Static method to extract tables from BeautifulSoup object
        table = soup.find_all('table')
        return table

    def general_details(self):  # Method to extract general details about the company
        soup = self.scrap_data(self.company)
        company_ratios = soup.find(class_='company-ratios')
        search_inputs = company_ratios.find_all(class_='number')
        print(company_ratios.encode('utf-8'))
        # Initialize an empty list to store text from each element
        general_details = []
        # Iterate over each element in search_inputs
        for search_input in search_inputs:
            # Extract text from the current element and split it into lines
            text = search_input.text.strip()
            lines = text.split('\n')
            # Append non-empty lines to the general_details list
            general_details.extend([line for line in lines if line.strip()])
        print(general_details)

    def extract_table(self): # Method to extract various financial tables from the webpage
        soup = self.scrap_data(self.company)
        if soup:
            table = self.get_table(soup)
            if table:
                # Extracting each table data
                tables_data = []
                for t in table:
                    data = pd.read_html(str(t))
                    tables_data.append(pd.concat(data, axis=1))
                return tables_data
            else:
                return None
        else:
            return None
        
    def calculate_prev_pe(self):  
        general_details = self.general_details()
        table = self.extract_table()
        profit_loss_df = table[1]
        marketcap = general_details[0]
        marketcap = marketcap.replace(",", "")
        net_profit_23 = profit_loss_df.iloc[:, -1][9]
        prev_pe_ratio = round(int(marketcap)/int(net_profit_23),2)
        return prev_pe_ratio
    
    def roce_5_year_median(self): # Method to calculate the 5 year median RoCE
        table = self.extract_table()
        ratios_df = table[8]
        if table:
            if not pd.isnull(ratios_df.iloc[:, -1][5]):
                RoCE_5_year_median = statistics.median([int(ratios_df.iloc[:, -1][5].replace("%", "")), 
                                                        int(ratios_df.iloc[:, -2][5].replace("%", "")), 
                                                        int(ratios_df.iloc[:, -3][5].replace("%", "")), 
                                                        int(ratios_df.iloc[:, -4][5].replace("%", "")), 
                                                        int(ratios_df.iloc[:, -5][5].replace("%", ""))])        
            else:
                RoCE_5_year_median = statistics.median([int(ratios_df.iloc[:, -2][5].replace("%", "")), 
                                                    int(ratios_df.iloc[:, -3][5].replace("%", "")), 
                                                    int(ratios_df.iloc[:, -4][5].replace("%", "")), 
                                                    int(ratios_df.iloc[:, -5][5].replace("%", ""))])
            return RoCE_5_year_median
        else:
            return None

    
    def compound_sales_growth(self): # Method to calculate compound sales growth rates
        table = self.extract_table()
        compound_sales_growth_df = table[2]
        csg_ttm = compound_sales_growth_df['Compounded Sales Growth.1'][3]
        csg_3_year = compound_sales_growth_df['Compounded Sales Growth.1'][2]
        csg_5_year = compound_sales_growth_df['Compounded Sales Growth.1'][1]
        csg_10_year = compound_sales_growth_df['Compounded Sales Growth.1'][0]
        df_csg = pd.DataFrame({'TTM': [csg_ttm], '3 Year': [csg_3_year], '5 Year': [csg_5_year], '10 Year': [csg_10_year]})
        return df_csg
    
    def compound_profit_growth(self): # Method to calculate compound profit growth rates
        table = self.extract_table()
        compound_profit_growth_df = table[3]
        cpg_ttm = compound_profit_growth_df['Compounded Profit Growth.1'][3]
        cpg_3_year = compound_profit_growth_df['Compounded Profit Growth.1'][2]
        cpg_5_year = compound_profit_growth_df['Compounded Profit Growth.1'][1]
        cpg_10_year = compound_profit_growth_df['Compounded Profit Growth.1'][0]
        df_cpg = pd.DataFrame({'TTM': [cpg_ttm], '3 Year': [cpg_3_year], '5 Year': [cpg_5_year], '10 Year': [cpg_10_year]})
        return df_cpg
    
    def qoq_results(self):
        table = self.extract_table()
        qoq = table[0]
        qoq_df = pd.DataFrame(qoq.iloc[0:11, :]).T
        qoq_df = qoq_df.reset_index()
        qoq_df.columns = qoq_df.iloc[0]
        qoq_df = qoq_df[1:]
        qoq_df = qoq_df.rename(columns={qoq_df.columns[0]: 'Quarter'})
        return qoq_df
    
    def yoy_results(self):
        table = self.extract_table()
        yoy = table[1]
        yoy_df = pd.DataFrame(yoy.iloc[0:11, :]).T
        yoy_df = yoy_df.reset_index()
        yoy_df.columns = yoy_df.iloc[0]
        yoy_df = yoy_df[1:]
        yoy_df = yoy_df.rename(columns={yoy_df.columns[0]: 'Year'})
        return yoy_df

    def stock_price_cagr(self):
        table = self.extract_table()
        stock_price_cagr_df = table[4]
        stock_price_cagr_df.columns = ['Number of Years', 'Stock Price CAGR']
        return stock_price_cagr_df

    def roe(self):
        table = self.extract_table()
        roe_df = table[5]
        roe_df.columns = ['Number of Years', 'Return on Equity']
        return roe_df

    def balance_sheet(self):
        table = self.extract_table()
        balance_sheet = table[6]
        balance_sheet_df = pd.DataFrame(balance_sheet.iloc[0:13, :]).T
        balance_sheet_df = balance_sheet_df.reset_index()
        balance_sheet_df.columns = balance_sheet_df.iloc[0]
        balance_sheet_df = balance_sheet_df[1:]
        balance_sheet_df = balance_sheet_df.rename(columns={balance_sheet_df.columns[0]: 'Year'})
        return balance_sheet_df


    def cashflow(self):
        table = self.extract_table()
        cashflow = table[7]
        cashflow_df = pd.DataFrame(cashflow.iloc[0:4, :]).T
        cashflow_df = cashflow_df.reset_index()
        cashflow_df.columns = cashflow_df.iloc[0]
        cashflow_df = cashflow_df[1:]
        cashflow_df = cashflow_df.rename(columns={cashflow_df.columns[0]: 'Year'})
        return cashflow_df

    def ratios(self):
        table = self.extract_table()
        ratios = table[8]
        try:
            ratios_df = pd.DataFrame(ratios.iloc[0:6, :]).T
            ratios_df = ratios_df.reset_index()
            ratios_df.columns = ratios_df.iloc[0]
            ratios_df = ratios_df[1:]
            ratios_df = ratios_df.rename(columns={ratios_df.columns[0]: 'Year'})
            return ratios_df
        except:
            return
        
    def shareholding_pattern(self):
        table = self.extract_table()
        shareholding = table[9]
        shareholding_df = pd.DataFrame(shareholding.iloc[0:6, :]).T
        shareholding_df = shareholding_df.reset_index()
        shareholding_df.columns = shareholding_df.iloc[0]
        shareholding_df = shareholding_df[1:]
        shareholding_df = shareholding_df.rename(columns={shareholding_df.columns[0]: 'Year'})  
        return shareholding_df
        
    
