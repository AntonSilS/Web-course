--средний балл, который преподаватель ставит студенту
SELECT students.student_name, ROUND(AVG(grades.grade), 0) as avg_grade, subjects.teacher_name
FROM students
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE students.id = 1 AND subjects.teacher_name = 'Cons Freddy';