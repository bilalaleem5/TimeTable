from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

lab_keywords = ['C-Margalla 1', 'C-Margalla 3', 'C-Margalla 4', 'C-Rawal 1', 'Rawal 3 (B-232)', 'C-Rawal 4', 
                'C-GPU Lab', 'A-Karakoram 1', 'A-Karakoram 2', 'A-Karakoram 3', 'A-Mehran 1', 'A-Mehran 2', 
                'B-Digital', 'A-CALL-1', 'A-CALL-2', 'A-CALL-3']

def load_timetable(file_path):
    file = pd.ExcelFile(file_path)
    all_DFs = []

    for sheet in file.sheet_names[1:]:
        df = pd.read_excel(file, sheet, header=4)
        df = df.dropna(axis=1, how='all')

        data = []
        prev_time = None

        for i, row in enumerate(df.index):
            for j, col in enumerate(df.columns):
                cell = df.at[row, col]
                time = prev_time if 'Unnamed' in col else df.columns[j]
                prev_time = time if 'Unnamed' not in col else prev_time

                start_index = str(cell).find('(')
                end_index = str(cell).find(')')
                extracted_string = str(cell)[start_index + 1:end_index]

                new_row = {
                    'Class': df.at[i, df.columns[0]],
                    'Day': sheet,
                    'Course': str(cell).split('(')[0],
                    'Section': extracted_string if start_index != -1 and end_index != -1 else str(cell).split('(')[0]
                }

                if new_row['Class'] in lab_keywords:
                    new_row['Type'] = 'Lab'
                    lab_time = df.iat[36, j] if j < len(df.columns) else ''
                    new_row['Time'] = lab_time
                else:
                    new_row['Type'] = 'Theory'
                    new_row['Time'] = time 

                data.append(new_row)

        new_data = pd.DataFrame(data)
        new_data.dropna(inplace=True)
        new_data = new_data[~new_data.eq('').any(axis=1)]
        new_data = new_data[~new_data.eq('nan').any(axis=1)]
        new_data = new_data[~new_data['Time'].isin(['Room', 'Lab'])]
        new_data = new_data[~new_data['Class'].eq('Lab')]
        new_data.reset_index(drop=True, inplace=True)
        all_DFs.append(new_data)
    return all_DFs

@app.route('/')
def index():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    selected_day = request.args.get('day', 'Monday')
    timetables = load_timetable('TimeTable.xlsx')
  
    day_timetable = pd.concat(timetables).query('Day == @selected_day')
    return render_template('index.html', days=days, selected_day=selected_day, day_timetable=day_timetable.iterrows())

@app.route('/search', methods=['POST'])
def search():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetables = load_timetable('TimeTable.xlsx')
    course = request.form.get('course', '')
    day = request.form.get('day', '')
    degree = request.form.get('degree', '')
    class_section = request.form.get('class_section', '')

    timetable = pd.concat(timetables)

    # Apply filters
    if day:
        timetable = timetable[timetable['Day'] == day]
    if course:
        timetable = timetable[timetable['Course'].str.contains(course, case=False)]
    if degree:
        timetable = timetable[timetable['Section'].str.contains(f'{degree}-', case=False)]
    if class_section:
        timetable = timetable[timetable['Section'].str.match(f'{degree}-{class_section}', case=False)]

    return render_template('index.html', days=days, selected_day=day, day_timetable=timetable.iterrows())

if __name__ == '__main__':
    app.run(debug=True)
