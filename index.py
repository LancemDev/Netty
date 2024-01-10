import requests
from bs4 import BeautifulSoup
import csv

# Read data from CSV
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data_list = list(reader)

# Prepare the CSV writer for the results
with open('results2.csv', 'w', newline='') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['indexNumber', 'name', 'student_name', 'school_name', 'mean_grade', 'subject_grades'])

    # Loop through data
    for data in data_list:
        # Prepare data for the request
        request_data = {'indexNumber': data['indexNumber'], 'name': data['name']}
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Send request to the form
        response = requests.post('http://results.knec.ac.ke', data=request_data, headers=headers)

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