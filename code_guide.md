# library
* pip install mysql-connector-python==9.4.0
* pip install python-dotenv==1.1.1
* pip install rich==14.1.0
* pip install typer==0.17.4
* pip install questionary==2.1.1
* pip install inquirerpy==0.3.4 # lib quá cũ ko dùng 
* pip install simple-term-menu==1.6.6 # lib quá cũ

# remove package
* pip uninstall inquirerpy simple-term-menu

# used
python registrar.py --help # view list command exist
python registrar.py add-student
python registrar.py add-student hai thai 1236
registrar.py add-course cs101 "intro to compsci" compsci
python registrar.py add-course cs102 "intro to intermediate compsci" compsci
python registrar.py add-course cs102 "intro to intermediate compsci" compsci
python registrar.py add-prereq cs102 cs101 --min-grade 70
python registrar.py reset-database # default with-data=True reset with data insert
python registrar.py reset-database --no-with-data # with-data=False reset with no data
python registrar.py show-prereqs MATH209
python registrar.py show-students Doe
python registrar.py show-courses Economics
python registrar.py enroll ab1 cs304
python registrar.py grade ab1 cs304 97 # grade là điểm
# Table link:

# - students should store
     * first_name
     * last_name
     * unix_id (a short-hand unique identifier that the school assigns to each student)

# - courses should store
     * moniker (a short-form id, like ECON101),
     * name (the full name of the course),
     * department

# prerequisites link course
```sql
INSERT INTO prerequisites (course, prereq, min_grade) VALUES
('CS201', 'CS101', 50);
```

* `course = CS201` → môn mà sinh viên muốn đăng ký (Data Structures)
* `prereq = CS101` → môn tiên quyết (Intro to Programming)
* `min_grade = 50` → điều kiện điểm tối thiểu

👉 Nghĩa là: **sinh viên chỉ được học CS201 nếu trước đó đã học CS101 và đạt ít nhất 50 điểm**.


