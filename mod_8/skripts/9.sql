--список курсов, которые посещает студент
SELECT students.student_name, subjects.subject_name
FROM students
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE students.id = 1
GROUP BY subjects.subject_name;