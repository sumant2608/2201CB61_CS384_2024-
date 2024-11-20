import pandas as pd
import numpy as np
# from google.colab import files

# Step 1: Upload the file
print("Please upload your Excel file.")
uploaded = files.upload()

# Extract the uploaded file name
file_name = next(iter(uploaded))

# Step 2: Load the uploaded file
df = pd.read_excel(file_name, header=None)  # Load without a header for flexible column identification

# Step 3: Extract the assessment components, max marks, and weightage
assessment_columns = df.iloc[0, 2:].values  # Assuming first row has column names like MidSem, Endsem, etc.
max_marks = df.iloc[1, 2:].values  # The second row contains max marks
weightage = df.iloc[2, 2:].values  # The third row contains weightage

# Step 4: Prepare the dataframe containing student details (excluding first 3 rows)
student_data = df.iloc[3:, :].reset_index(drop=True)

# Step 5: Assign column names to the student data (Roll, Name, and Assessment Columns)
student_data.columns = ['Roll', 'Name'] + list(assessment_columns)

# Step 6: Convert numeric columns (assessments) to float for calculations
for col in assessment_columns:
    student_data[col] = pd.to_numeric(student_data[col], errors='coerce')

# Step 7: Dynamically calculate scaled marks based on weightage and max marks
for idx, component in enumerate(assessment_columns):
    max_mark = max_marks[idx]  # Max mark for the component
    weight = weightage[idx]    # Weightage for the component
    student_data[f'Scaled_{component}'] = (student_data[component] / max_mark) * weight

# Step 8: Calculate Grand Total (scaled sum)
student_data['Grand Total'] = student_data[[f'Scaled_{component}' for component in assessment_columns]].sum(axis=1)

# Step 9: Function to assign grades dynamically based on sorted total scores
def assign_grades(df):
    total_students = len(df)
    sorted_df = df.sort_values(by='Grand Total', ascending=False).reset_index(drop=True)

    # Calculate the number of students per grade dynamically based on the total number of students
    GRADE_QUOTA = {
        "AA": 5,  # Top 5% get AA
        "AB": 10,
        "BB": 20,
        "BC": 25,
        "CC": 20,
        "CD": 10,
        "DD": 10
    }

    grade_counts = {grade: round(total_students * (percent / 100)) for grade, percent in GRADE_QUOTA.items()}

    grades = []
    for grade, count in grade_counts.items():
        grades.extend([grade] * count)

    grades = grades[:total_students] + ['F'] * (total_students - len(grades))  # Fill the remaining with F

    sorted_df['Grade'] = grades
    return sorted_df

# Step 10: Apply grading and create output DataFrames sorted by grade and roll number
graded_df = assign_grades(student_data)
graded_df_roll_sorted = graded_df.sort_values(by='Roll', ascending=True)

# Step 11: Save results to an Excel file with two sheets
output_file = "graded_output.xlsx"
with pd.ExcelWriter(output_file) as writer:
    graded_df.to_excel(writer, sheet_name="Sorted by Grade", index=False)
    graded_df_roll_sorted.to_excel(writer, sheet_name="Sorted by Roll Number", index=False)

# Step 12: Display a preview of the graded DataFrame
print("Grading completed. Here is a preview of the graded data:")
print(graded_df[['Roll', 'Name', 'Grand Total', 'Grade']].head())

# Step 13: Download the output file
files.download(output_file)