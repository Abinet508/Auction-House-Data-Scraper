import requests
import pandas as pd
from multiprocessing.pool import ThreadPool

class AuctionHouse:
    def __init__(self):
        self.df = pd.DataFrame()
        self.unique_properties = set()
        self.headers = self.get_headers()
    
    def get_headers(self):
        """
        Get headers for the request

        Returns:
            dict: headers
        """
        return {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.auctionhouse.co.uk',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

    def get_properties(self, start_lot=12,get_total_count=False):
        """
        Get properties from auction house website

        Args:
            start_lot (int, optional): The start lot to scrape. Defaults to 12.
            get_total_count (bool, optional): To get the total count of properties. Defaults to False.
        Returns:
            _type_: _description_
        """
        json_data = {
            'filters': {
                'max_price': 0,
                'bed_rooms': '',
                'address': '',
                'formatted_address': '',
                'postcode': '',
                'latitude': 0,
                'longitude': 0,
                'radius': 0,
                'type': [],
                'propertyTypeCategories': [],
                'saleStatusData': [],
                'featuresData': [],
                'yieldData': [],
                'saleTypeData': [],
                'tenureData': [],
            },
            'orderBy': 'auction_first',
            'viewType': 'Grid',
            'isNationalTimedAuction': False,
            'startLot': start_lot,
            'lotLimit': 100,
            'action': 'getCurrentLots',
            'withAuth': False,
        }
        while True:
            try:
                response = requests.post('https://api.auctionhouse.co.uk/api/v1/getCurrentProperties', headers=self.headers, json=json_data)
                if response.status_code == 200:
                    print(f"Scraping page {start_lot//100}")
                    if get_total_count:
                        return response.json()['totalCount']
                    data = response.json()['data']
                    return data
            except Exception as e:
                print(f"An error occurred: {e}")
                break
            return []

    def main(self):
        """
        Main function to scrape the auction house website
        """
        while True:
            try:
                totalCount  = self.get_properties(start_lot=12,get_total_count=True)
                #slice the total count into max 100
                slices = [100]* (totalCount//100) + [totalCount%100]
                #add the previous slices to the next slices make sure the last slice is equal to the total count
                slices = [sum(slices[:i+1]) for i in range(len(slices))]
                final_scraped_data = [] 
                with ThreadPool(5) as pool:
                    results = pool.map(self.get_properties, slices)
                    for result in results:
                        final_scraped_data.extend(result)
                if not final_scraped_data:
                    break
                self.df = pd.json_normalize(final_scraped_data)
                self.df.columns = self.df.columns.str.upper()
                self.df.to_excel("auction_house.xlsx",index=False)
                print(f"Total properties found: {len(self.df)}")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
            
if __name__ == '__main__':
    AuctionHouse().main()
    