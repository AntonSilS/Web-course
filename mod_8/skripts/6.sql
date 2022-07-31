--список студентов в группе
SELECT grps.group_name, students.student_name 
FROM students
JOIN grps ON students.group_id = grps.id
WHERE grps.group_name = '203_D';