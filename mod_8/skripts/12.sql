--средний балл, который ставит преподаватель
SELECT subjects.teacher_name, ROUND(AVG(grades.grade), 0) as avg_grade
FROM students
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE subjects.teacher_name = 'Johnson Nill';