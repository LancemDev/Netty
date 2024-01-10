from flask import Flask, request, send_file
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded', 400

    # Read the Excel file
    file = request.files['file']
    df = pd.read_excel(file)

    # Your headers and URL
    URL = "http://results.knec.ac.ke/Home/CheckResults"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://results.knec.ac.ke",
        "Referer": "http://results.knec.ac.ke/",
        "Upgrade-Insecure-Requests": "1"
    }

    # Loop through the rows of the DataFrame and scrape data for each one
    for index, row in df.iterrows():
        data = {'indexNumber': row['indexNumber'], 'name': row['name']}  # replace with your actual column names

        # Send the request
        r = requests.post(URL, headers=headers, data=data)

        # Parse the response
        soup = BeautifulSoup(r.content, 'html5lib')

        # Your scraping logic here...
        # Add the scraped data to the DataFrame

    # Save the DataFrame to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer)

    # Send the Excel file as a response
    output.seek(0)
    return send_file(output, attachment_filename='results.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)