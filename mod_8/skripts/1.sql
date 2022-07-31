--5 студентов с наибольшим средним баллом по всем предметам
SELECT students.student_name, ROUND(AVG(grades.grade), 0) as avr_grade
FROM grades
JOIN students on grades.student_id = students.id
GROUP BY grades.student_id
ORDER BY avr_grade DESC
LIMIT 5;