from flask import Flask, request, send_file, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import logging
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Check if a file was uploaded
    if 'file' not in request.files:
        logging.error('No file uploaded')
        return 'No file uploaded', 400

    # Read the Excel file
    file = request.files['file']
    df = pd.read_excel(file)
    logging.info('Excel file read successfully')

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

    def process_row(index, row):
        data = {'indexNumber': row['INDEX'], 'name': row['CANDIDATE NAME']}  # replace with your actual column names
        logging.info(f'Sending request for index number: {data["indexNumber"]}')

        # Retry logic
        while True:
            r = requests.post(URL, headers=headers, data=data)
            if r.status_code == 200:
                logging.info(f'Successful response for index number: {data["indexNumber"]}')
                break
            else:
                logging.warning(f'Failed response for index number: {data["indexNumber"]}, retrying...')
                time.sleep(5)  # Wait for 5 seconds before retrying

        # Parse the response
        soup = BeautifulSoup(r.content, 'html.parser')

        # Extract relevant information
        name_and_grade = soup.find_all('th', style='border: transparent; padding-left: 0%; padding-top: 2px; padding-bottom: 2px;')
        if name_and_grade:
            student_name = name_and_grade[0].text
            school_name = name_and_grade[1].text
            mean_grade = name_and_grade[2].text.split(':')[-1].strip()
            logging.info(f'Extracted data for index number: {data["indexNumber"]}')
        else:
            student_name = school_name = mean_grade = 'No result found'
            logging.warning(f'No result found for index number: {data["indexNumber"]}')

        # Extract grades for each subject
        grades_table = soup.find('table', id='grid')
        if grades_table:
            rows = grades_table.find_all('tr')
            grades = {}
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                subject = cols[2].text
                grade = cols[3].text
                grades[subject] = grade
            logging.info(f'Extracted grades for index number: {data["indexNumber"]}')
        else:
            grades = {'No result found': ''}
            logging.warning(f'No grades found for index number: {data["indexNumber"]}')

        # Add the scraped data to the DataFrame
        df.loc[index, 'student_name'] = student_name
        df.loc[index, 'school_name'] = school_name
        df.loc[index, 'mean_grade'] = mean_grade
        df.loc[index, 'subject_grades'] = str(grades)

        # Write the extracted details to a text file
        with open('extracted_details.txt', 'a') as f:
            f.write(f"Index Number: {data['indexNumber']}\n")
            f.write(f"Student Name: {student_name}\n")
            f.write(f"School Name: {school_name}\n")
            f.write(f"Mean Grade: {mean_grade}\n")
            f.write(f"Subject Grades: {grades}\n")
            f.write("\n")

    # Use ThreadPoolExecutor to process rows in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_row, index, row) for index, row in df.iterrows()]
        for future in futures:
            future.result()  # Wait for all threads to complete

    # Save the DataFrame to an Excel file in memory
    df.to_excel('results.xlsx')
    logging.info('Results saved to results.xlsx')

    # Send the Excel file as a response
    return send_file('results.xlsx', as_attachment=True, download_name='results.xlsx')

if __name__ == '__main__':
    app.run(debug=True)