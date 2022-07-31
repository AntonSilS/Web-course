--средний балл в группе по одному предмету
SELECT grps.group_name, subjects.subject_name, ROUND(AVG(grades.grade), 2) as avarage_grade
FROM students
JOIN grps ON students.group_id = grps.id
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE grps.group_name = '201_B' AND subjects.subject_name = 'Law';
