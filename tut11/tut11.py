import streamlit as st
import pandas as pd
import io

def calculate_total_marks(df, marks_columns, max_marks, weightage):
    def calculate(row):
        total = 0
        for i, col in enumerate(marks_columns, start=2):
            if pd.notnull(row[col]) and pd.notnull(max_marks[i]) and pd.notnull(weightage[i]):
                scaled_mark = (row[col] / max_marks[i]) * weightage[i]
                total += scaled_mark
        return total
    return df.apply(calculate, axis=1)

def assign_grades(df, total_students, schema):
    grade_boundaries = {}
    boundary = 0
    for grade, percentage in schema.items():
        count_for_grade = (percentage / 100) * total_students
        grade_boundaries[grade] = (boundary, boundary + count_for_grade)
        boundary += count_for_grade

    df_sorted = df.sort_values(by='total scaled/100', ascending=False).reset_index(drop=True)
    grade_labels = []
    for i, row in df_sorted.iterrows():
        for grade, (lower, upper) in grade_boundaries.items():
            if lower <= i < upper:
                grade_labels.append(grade)
                break
    df_sorted['Grade'] = grade_labels
    return df_sorted

def generate_summary(df, schema, all_grades):
    total_students = len(df)
    summary_data = []
    for grade in all_grades:
        percentage = schema.get(grade, 0)
        counts = (percentage / 100) * total_students
        rounded_counts = round(counts)
        verified_counts = df['Grade'].value_counts().get(grade, 0)
        summary_data.append([grade, percentage, counts, rounded_counts, verified_counts])
    summary_df = pd.DataFrame(summary_data, columns=['Grade', 'Old IAPC Reco', 'Counts', 'Round', 'Count Verified'])
    summary_df.loc[-1] = ['Total Students', total_students, '', '', '']
    summary_df.index = summary_df.index + 1
    summary_df = summary_df.sort_index()
    return summary_df

# Set up Streamlit app
st.title("Grade Processing App")
st.write("Upload an Excel file to process grades and generate a summary.")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    column_names = df.iloc[0].values
    df.columns = column_names
    max_marks = df.iloc[1].values
    weightage = df.iloc[2].values
    marks_columns = df.columns[2:]

    # Calculate total marks
    df.loc[3:, 'total scaled/100'] = calculate_total_marks(df.loc[3:], marks_columns, max_marks, weightage)

    # Assign grades
    default_schema = {'AA': 5, 'AB': 15, 'BB': 25, 'BC': 30, 'CC': 15, 'CD': 5, 'DD': 5}
    all_grades = ['AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'F', 'I', 'PP', 'NP']
    df_with_grades = assign_grades(df.loc[3:], len(df.loc[3:]), default_schema)

    # Generate summary table
    summary_df = generate_summary(df_with_grades, default_schema, all_grades)

    # Display the processed data and summary
    st.subheader("Processed Data with Grades")
    st.write(df_with_grades)

    st.subheader("Grade Summary Table")
    st.write(summary_df)

    # Download processed file
    df_with_summary = pd.concat([df_with_grades, summary_df], axis=1)
    sorted_df = df_with_summary.sort_values(by='Roll')

    # Function to convert DataFrame to Excel in memory
    def convert_df_to_excel(df):
        # Create a BytesIO buffer to hold the file content
        output = io.BytesIO()
        # Create an ExcelWriter object and write the DataFrame to the buffer
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        # Get the binary content of the file
        processed_file = output.getvalue()
        return processed_file

    processed_file = convert_df_to_excel(df_with_summary)
    sorted_file = convert_df_to_excel(sorted_df)

    # Provide download buttons for processed files
    st.download_button("Download Processed Data", processed_file, "processed_data.xlsx")
    st.download_button("Download Sorted Data", sorted_file, "sorted_data.xlsx")