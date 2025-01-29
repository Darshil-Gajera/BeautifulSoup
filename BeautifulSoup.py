import requests
from bs4 import BeautifulSoup
import pandas as pd  # Importing pandas for table formatting

# List of URLs to scrape
urls = [
    'https://groww.in/us-stocks/nke',
    'https://groww.in/us-stocks/ko',
    'https://groww.in/us-stocks/msft',
    'https://groww.in/us-stocks/v',
    'https://groww.in/us-stocks/amgn',
    'https://groww.in/us-stocks/jpm', 
    'https://groww.in/us-stocks/mcd',
    'https://groww.in/us-stocks/crm', 
    'https://groww.in/us-stocks/vz', 
    'https://groww.in/us-stocks/v', 
    'https://groww.in/us-stocks/wmt',  
    'https://groww.in/us-stocks/dis'
]

# List to store results
data = []

# Loop through each URL in the list
for url in urls:
    # Send GET request to fetch the content
    r = requests.get(url)
    
    # Convert the response content to a BeautifulSoup object, specifying the parser
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the stock name (heading) using the specified class 'usph14Head displaySmall'
    stock_name = soup.find(class_='usph14Head displaySmall')

    # Find the element with the specified class for price
    price_element = soup.find(class_='valign-wrapper vspace-between usph14PriceWrapper')

    # Try to find the element for 1-day performance with a negative class
    change_element_negative = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentNegative'})

    # Try to find the element for 1-day performance with a positive class (if negative isn't found)
    change_element_positive = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentPositive'})

    # Determine the change element to use (negative or positive)
    change_element = change_element_negative if change_element_negative else change_element_positive

    # If stock name is found, extract it
    if stock_name:
        stock_name_text = stock_name.text.strip()
    else:
        stock_name_text = 'Not Found'

    # Initialize the dictionary for storing stock information
    stock_data = {'Stock Name': stock_name_text}

    # Check if price_element is found and extract the price
    if price_element:
        price = price_element.text.strip().split('-')[0]  # Split by '-' to handle range if present
        price = price.strip().split('+')[0]  # Further split to remove any plus sign, leaving clean price
    else:
        price = 'Not Found'

    # Add the price to the stock data
    stock_data['Price'] = price

    # Check if change_element is found and extract the 1-day change
    if change_element:
        change_raw = change_element.text.strip()
        # Extract only the numeric change, removing any text like percentage or parentheses
        change_value = change_raw.split('(')[0].strip()  # Take only the part before '('
        stock_data['1 Day Change'] = change_value
    else:
        stock_data['1 Day Change'] = 'Element not found'

    # Append the stock data to the results list
    data.append(stock_data)

# Create a pandas DataFrame from the collected data
df = pd.DataFrame(data)

# Display the result in a table format
print(df)
