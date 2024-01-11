from flask import Flask, request, send_file, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

        # Extract relevant information
        name_and_grade = soup.find_all('th', style='border: transparent; padding-left: 0%; padding-top: 2px; padding-bottom: 2px;')
        if name_and_grade:
            student_name = name_and_grade[0].text
            school_name = name_and_grade[1].text
            mean_grade = name_and_grade[2].text.split(':')[-1].strip()
        else:
            student_name = school_name = mean_grade = 'No result found'

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
        else:
            grades = {'No result found': ''}

        # Save results to CSV
        # writer.writerow([data['indexNumber'], data['name'], student_name, school_name, mean_grade, grades])
        # Add the scraped data to the DataFrame
        df.loc[index, 'student_name'] = student_name
        df.loc[index, 'school_name'] = school_name
        df.loc[index, 'mean_grade'] = mean_grade
        df.loc[index, 'subject_grades'] = str(grades)


    # Save the DataFrame to an Excel file in memory
    # Save the DataFrame to an Excel file on disk
    df.to_excel('results.xlsx')

    # Send the Excel file as a response
    return send_file('results.xlsx', as_attachment=True, download_name='results.xlsx')
if __name__ == '__main__':
    app.run(debug=True)