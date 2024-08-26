# Auction House Data Scraper

This script is designed to scrape property data from an auction house website and store it in a pandas DataFrame. It utilizes the `requests` library to make HTTP requests and the `multiprocessing.pool.ThreadPool` for concurrent data fetching.

## Features

- **Concurrent Data Fetching**: Uses threading to fetch multiple property data simultaneously, improving efficiency.
- **Data Storage**: Stores the scraped data in a pandas DataFrame for easy manipulation and analysis.
- **Customizable Start Point**: Allows users to specify the starting lot number for data scraping.
- **HTTP Headers Management**: Manages HTTP headers to mimic browser requests and avoid blocking.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `multiprocessing` library

You can install the required libraries using pip:

```sh
pip install requests pandas 
```

## Usage

### Class: `AuctionHouse`
This class is responsible for managing the data scraping process.

#### Methods

- **`__init__(self)`**: Initializes the `AuctionHouse` object. It sets up an empty DataFrame, a set for unique properties, and headers for HTTP requests.

- **`get_headers(self)`**: Returns a dictionary of HTTP headers used for making requests to the auction house website.

- **`get_properties(self, start_lot=12, get_total_count=False)`**: Fetches property data starting from a specified lot number. The `start_lot` parameter specifies the starting lot number, and the `get_total_count` parameter determines whether to fetch the total count of properties.

### Example

```python
from auction_house import AuctionHouse

# Create an instance of AuctionHouse
auction_house = AuctionHouse()

# Fetch properties starting from lot number 12
auction_house.get_properties(start_lot=12)

# Access the DataFrame containing the property data
df = auction_house.df

# Display the DataFrame
print(df)
```


## Contact

For any questions or inquiries, please contact [abinatmail@gmail.com](mailto:abinatmail@gmail.com)

---
