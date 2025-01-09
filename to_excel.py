import pandas as pd
import ast

# Read the text file
with open('extracted_details.txt', 'r') as file:
    lines = file.readlines()

# Initialize lists to store data
data = []
subjects = set()

# Parse the text file
for i in range(0, len(lines), 7):
    try:
        index_number = lines[i].split(': ')[1].strip()
        student_name = lines[i+1].split(': ')[1].strip()
        school_name = lines[i+2].split(': ')[1].strip()
        mean_grade = lines[i+3].split(': ')[1].strip()
        
        # Check if the line contains the expected delimiter
        if ': ' in lines[i+4]:
            subject_grades = ast.literal_eval(lines[i+4].split(': ', 1)[1].strip())
        else:
            subject_grades = {}

        # Add subjects to the set
        subjects.update(subject_grades.keys())

        # Append data to the list
        data.append({
            'Index Number': index_number,
            'Student Name': student_name,
            'School Name': school_name,
            'Mean Grade': mean_grade,
            **subject_grades
        })
    except IndexError:
        print(f"Skipping incomplete record starting at line {i}")

# Create a DataFrame
df = pd.DataFrame(data)

# Ensure all subjects are columns
subjects_list = list(subjects)
for subject in subjects_list:
    if subject not in df.columns:
        df[subject] = None

# Calculate mean grades for each subject and overall mean grade
subject_means = df[subjects_list].apply(lambda x: x.str.extract(r'(\d+)').astype(float).mean())
overall_mean = subject_means.mean()

# Append mean grades to the DataFrame
mean_row = {subject: f'{mean:.2f}' for subject, mean in subject_means.items()}
mean_row.update({
    'Index Number': 'Mean',
    'Student Name': '',
    'School Name': '',
    'Mean Grade': f'{overall_mean:.2f}'
})
df = df.append(mean_row, ignore_index=True)

# Save the DataFrame to an Excel file using the xlsxwriter engine
df.to_excel('results.xlsx', index=False, engine='xlsxwriter')