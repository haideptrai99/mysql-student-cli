# library
* pip install mysql-connector-python==9.4.0
* pip install python-dotenv==1.1.1
* pip install rich==14.1.0
* pip install typer==0.17.4

# used
python registrar.py --help # view list command exist
python registrar.py add-student
python registrar.py add-student hai thai 1236
registrar.py add-course cs101 "intro to compsci" compsci
python registrar.py add-course cs102 "intro to intermediate compsci" compsci
python registrar.py add-course cs102 "intro to intermediate compsci" compsci
python registrar.py add-prereq cs102 cs101 --min-grade 70
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


