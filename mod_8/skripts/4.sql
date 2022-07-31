--cредний балл в потоке
SELECT ROUND(AVG(grades.grade), 0) as avarage_grade
FROM students
JOIN grades ON grades.student_id = students.id;
