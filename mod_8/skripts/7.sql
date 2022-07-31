--оценки студентов в группе по предмету
SELECT grps.group_name, students.student_name, subjects.subject_name, grades.grade, grades.date_of
FROM students
JOIN grps ON students.group_id = grps.id
JOIN grades ON grades.student_id = students.id
JOIN subjects ON subjects.id = grades.subject_id
WHERE grps.group_name = '203_D' AND subjects.subject_name = 'IT'
ORDER BY students.student_name, grades.grade DESC;
	