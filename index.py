import requests
from bs4 import BeautifulSoup
import csv

# Read data from CSV
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data_list = list(reader)

# Prepare the CSV writer for the results
with open('results4.csv', 'w', newline='') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['indexNumber', 'name', 'student_name', 'school_name', 'mean_grade', 'subject_grades'])

    # Loop through data
    for data in data_list:
        # Prepare data for the request
        request_data = {'indexNumber': data['indexNumber'], 'name': data['name']}
        headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "http://results.knec.ac.ke",
                    "Referer": "http://results.knec.ac.ke/",
                    "Upgrade-Insecure-Requests": "1"
                }

        # Send request to the form
        response = requests.post('http://results.knec.ac.ke/Home/CheckResults', data=request_data, headers=headers)

        # Print the status code and headers
        print('Status code:', response.status_code)
        print('Headers:', response.headers)

        # Parse response HTML
        soup = BeautifulSoup(response.text, 'html.parser')

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
        writer.writerow([data['indexNumber'], data['name'], student_name, school_name, mean_grade, grades])