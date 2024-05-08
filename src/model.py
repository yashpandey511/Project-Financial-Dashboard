import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
import statistics
warnings.filterwarnings("ignore")

class DCF:
    def __init__(self, company):
        # Initialize instance attributes
        self.company = company

    @staticmethod
    def scrap_data(company): # Static method to scrape data from webpage
        # Scrape data from web page
        url = f'https://www.screener.in/company/{company}/'
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
        search_inputs = soup.find_all(class_='number')
        # Initialize an empty list to store text from each element
        general_details = []
        # Iterate over each element in search_inputs
        for search_input in search_inputs:
            # Extract text from the current element and split it into lines
            text = search_input.text.strip()
            lines = text.split('\n')
            # Append non-empty lines to the general_details list
            general_details.extend([line for line in lines if line.strip()])
        return general_details

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

    def calculate_pe(self): # Method to calculate the PE ratio of the company
        general_details = self.general_details()
        if general_details:
            # Current PE Ratio
            current_pe = general_details[4]
            return current_pe
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

    
    def calculate_compound_sales_growth(self): # Method to calculate compound sales growth rates
        table = self.extract_table()
        compound_sales_growth_df = table[2]
        csg_ttm = compound_sales_growth_df['Compounded Sales Growth.1'][3]
        csg_3_year = compound_sales_growth_df['Compounded Sales Growth.1'][2]
        csg_5_year = compound_sales_growth_df['Compounded Sales Growth.1'][1]
        csg_10_year = compound_sales_growth_df['Compounded Sales Growth.1'][0]
        return csg_ttm, csg_3_year, csg_5_year, csg_10_year
    
    def calculate_compound_profit_growth(self): # Method to calculate compound profit growth rates
        table = self.extract_table()
        compound_profit_growth_df = table[3]
        cpg_ttm = compound_profit_growth_df['Compounded Profit Growth.1'][3]
        cpg_3_year = compound_profit_growth_df['Compounded Profit Growth.1'][2]
        cpg_5_year = compound_profit_growth_df['Compounded Profit Growth.1'][1]
        cpg_10_year = compound_profit_growth_df['Compounded Profit Growth.1'][0]
        return cpg_ttm, cpg_3_year, cpg_5_year, cpg_10_year