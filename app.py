from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create the database and table if not exists
def create_table():
    conn = sqlite3.connect('job_applications.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT, middle TEXT, last TEXT, email TEXT, mobile TEXT,
            gender TEXT, qualification TEXT, dob TEXT,
            father TEXT, mother TEXT,
            current_address TEXT, permanent_address TEXT,
            landline TEXT, birthplace TEXT, passing_year TEXT,
            languages TEXT, hobbies TEXT, about TEXT, nationality TEXT,
            aadhar TEXT, pan TEXT,
            edu_qual1 TEXT, edu_univ1 TEXT, edu_year1 TEXT, edu_marks1 TEXT,
            edu_qual2 TEXT, edu_univ2 TEXT, edu_year2 TEXT, edu_marks2 TEXT,
            edu_qual3 TEXT, edu_univ3 TEXT, edu_year3 TEXT, edu_marks3 TEXT,
            company1 TEXT, role1 TEXT, from1 TEXT, to1 TEXT,
            company2 TEXT, role2 TEXT, from2 TEXT, to2 TEXT,
            company3 TEXT, role3 TEXT, from3 TEXT, to3 TEXT,
            jobtype TEXT, joining_date TEXT, joining_time TEXT,
            location TEXT, relocate TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home route - displays the form
@app.route('/')
def form():
    return render_template('form.html')

# Submit route - stores form data
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()

    # Handle multi-select fields
    data['languages'] = ", ".join(request.form.getlist('languages'))
    data['hobbies'] = ", ".join(request.form.getlist('hobbies'))

    # Insert into database
    conn = sqlite3.connect('job_applications.db')
    c = conn.cursor()

    fields = [
        'first', 'middle', 'last', 'email', 'mobile',
        'gender', 'qualification', 'dob',
        'father', 'mother',
        'current_address', 'permanent_address',
        'landline', 'birthplace', 'passing_year',
        'languages', 'hobbies', 'about', 'nationality',
        'aadhar', 'pan',
        'edu_qual1', 'edu_univ1', 'edu_year1', 'edu_marks1',
        'edu_qual2', 'edu_univ2', 'edu_year2', 'edu_marks2',
        'edu_qual3', 'edu_univ3', 'edu_year3', 'edu_marks3',
        'company1', 'role1', 'from1', 'to1',
        'company2', 'role2', 'from2', 'to2',
        'company3', 'role3', 'from3', 'to3',
        'jobtype', 'joining_date', 'joining_time',
        'location', 'relocate'
    ]

    placeholders = ', '.join(['?'] * len(fields))
    query = f"INSERT INTO applications ({', '.join(fields)}) VALUES ({placeholders})"
    values = tuple(data.get(field, "") for field in fields)

    c.execute(query, values)
    conn.commit()
    conn.close()

    return '''
        <h2 style="text-align:center; color: green;">Form submitted successfully!</h2>
        <p style="text-align:center;"><a href="/">Back to Form</a></p>
        <p style="text-align:center;"><a href="/submissions">View Submissions</a></p>
    '''

# Submissions route - displays all submitted applications
@app.route('/submissions')
def submissions():
    conn = sqlite3.connect('job_applications.db')
    c = conn.cursor()
    c.execute('SELECT * FROM applications')
    rows = c.fetchall()
    conn.close()
    return render_template('submissions.html', applications=rows)

# Initialize table on start
if __name__ == '__main__':
    create_table()
    app.run(debug=True)
