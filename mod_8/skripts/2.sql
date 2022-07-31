--1 студент с наивысшим средним баллом по одному предмету
SELECT students.student_name, ROUND(AVG(grades.grade), 0) as avr_grade, subjects.subject_name
FROM students
JOIN grades on students.id = grades.student_id 
JOIN subjects on subjects.id = grades.subject_id
WHERE subjects.subject_name = 'IT'
GROUP BY students.student_name
ORDER BY avr_grade DESC
LIMIT 1;
