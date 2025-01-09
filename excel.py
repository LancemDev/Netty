import pandas as pd
import re

# Function to process grades into numerical values for mean calculation
def process_grade(grade):
    grade_map = {
        'A': 12, 'A-': 11,
        'B+': 10, 'B': 9, 'B-': 8,
        'C+': 7, 'C': 6, 'C-': 5,
        'D+': 4, 'D': 3, 'D-': 2,
        'E': 1
    }
    grade = grade.split("(")[0].strip()  # Remove extras like (PLUS), (MINUS)
    return grade_map.get(grade, None)

# Read data from text file
def read_data(file_path):
    with open(file_path, "r") as file:
        data = file.read()

    student_records = data.split("\n\n")  # Split records by empty lines
    students = []
    
    for record in student_records:
        # Extract data using regex
        index_match = re.search(r"Index Number: (\d+)", record)
        name_match = re.search(r"Student Name: (.+)", record)
        grades_match = re.search(r"Subject Grades: (\{.+\})", record)

        if not (index_match and name_match and grades_match):
            print(f"Skipping record due to missing fields: {record[:50]}...")
            continue

        index_number = index_match.group(1)
        student_name = name_match.group(1).split(" - ")[1]
        subject_grades = eval(grades_match.group(1))  # Use eval safely for trusted input

        students.append({"Index Number": index_number, "Student Name": student_name, **subject_grades})

    return students

# Write to CSV
def write_to_csv(students, output_file):
    df = pd.DataFrame(students)

    # Add mean calculation column
    subject_columns = df.columns.difference(["Index Number", "Student Name"])

    def calculate_mean(row):
        grades = [process_grade(row[subject]) for subject in subject_columns if pd.notna(row[subject])]
        return sum(grades) / len(grades) if grades else None

    df["Mean"] = df.apply(calculate_mean, axis=1)

    # Calculate average for each subject and overall mean
    subject_averages = {
        subject: df[subject].dropna().apply(process_grade).mean()
        for subject in subject_columns
    }
    overall_mean = df["Mean"].mean()

    # Add subject averages and overall mean to the DataFrame
    averages_row = {"Index Number": "", "Student Name": "Averages", **subject_averages, "Mean": overall_mean}
    df = pd.concat([df, pd.DataFrame([averages_row])], ignore_index=True)

    # Write to CSV
    df.to_csv(output_file, index=False)

# Main script
input_file = "extracted_details.txt"  # Replace with your text file path
output_file = "kitonyini101.csv"

students = read_data(input_file)
write_to_csv(students, output_file)

print(f"CSV file has been created: {output_file}")
