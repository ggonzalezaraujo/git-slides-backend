-- 1. Select all users
SELECT *
FROM User

-- 2. Select a specific user
SELECT *
FROM User
WHERE email = 'mchen73@ucmerced.edu'

-- 3. Insert a new user
INSERT INTO User
(id, first_name, last_name, email, password, type-fk)
VALUES (next_id, fname, lname, em, pw, type)

-- 4. Update user details
UPDATE User
SET first_name=fname, last_name=lname, email=em, password=pw
WHERE id=input_id

-- 5. Delete a user
DELETE FROM User
WHERE id=input_id

-- 6. List all courses
SELECT *
FROM Course

-- 7. List courses for a given user
SELECT title
FROM Registration r, Course c
WHERE r.user-fk=input_user_id
AND c.id=r.course-fk

-- 8. Get all users in a given course
SELECT first_name, last_name
FROM Registration r, User u
WHERE r.course-fk=input_course_id
AND u.id=r.user-fk

--9. Register user for a course
INSERT INTO Registration
(id, user-fk, course-fk)
VALUES (next_id, input_user-fk, input_course-fk)

-- 10. Remove user from a course
-- DELETE FROM Registration
-- WHERE user-fk=input_user-fk
-- AND course-fk=input_course-fk
DELETE FROM Registration
WHERE id=input_id

-- 11. Create a new course
INSERT INTO Course
(id, title, semester, code, year)
VALUES (next_id, input_title, input_semester, input_code, input_year)

-- 12. Delete an existing course
DELETE FROM Course
WHERE id=input_id

-- 13. Update a course
UPDATE Course
SET title=input_title, semester=input_semester, code=input_code, year=input_year
WHERE id=input_id

-- 14. 
