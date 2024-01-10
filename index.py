import requests
from bs4 import BeautifulSoup
import csv

# Read data from CSV
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data_list = list(reader)

# Loop through data
for data in data_list:
    # Send request to the form
    response = requests.post('form_url', data=data)

    # Parse response HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant information
    result_data = soup.find('div', class_='result').text

    # Save results to CSV or Excel
    with open('results.csv', 'a') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([data['column1'], data['column2'], result_data])
