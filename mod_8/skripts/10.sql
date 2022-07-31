--список курсов, которые студенту читает преподаватель
SELECT students.student_name, subjects.subject_name, subjects.teacher_name
FROM students
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE students.id = 1 AND subjects.teacher_name = 'Johnson Nill'
GROUP BY subjects.subject_name;