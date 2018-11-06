-- 1. Select all users
SELECT *
FROM `User`;

-- 2. Select a specific user
SELECT *
FROM `User`
WHERE `email` = input_email;

-- 3. Insert a new user
INSERT INTO `User`
(`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`)
VALUES (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type);

-- 4. Update user details
UPDATE `User`
SET `first_name` = input_first_name, `last_name` = input_last_name, `email` = input_email, `password` = input_password
WHERE `id` = input_user_id;

-- 5. Delete a user
DELETE FROM `User`
WHERE `id` = input_user_id;

-- 6. List all courses
SELECT *
FROM `Course`;

-- 7. List courses for a given user
SELECT `title`
FROM `Registration` r, `Course` c
WHERE r.`user-fk` = input_user_id
AND c.`id` = r.`course-fk`;

-- 8. Get all users in a given course
SELECT `first_name`, `last_name`
FROM `Registration` r, `User` u
WHERE r.`course-fk` = input_course_id
AND u.`id` = r.`user-fk`;

-- 9. Register user for a course
INSERT INTO `Registration`
(`id`, `user-fk`, `course-fk`)
VALUES (input_registration_id, input_user_id, input_course_id);

-- 10. Remove user from a course
DELETE FROM `Registration`
WHERE `id` = input_user_id;

-- 11. Create a new course
INSERT INTO `Course`
(`id`, `title`, `semester`, `code`, `year`)
VALUES (input_course_id, input_title, input_semester, input_code, input_year);

-- 12. Delete an existing course
DELETE FROM `Course`
WHERE `id` = input_course_id;

-- 13. Update a course
UPDATE `Course`
SET `title` = input_title, `semester` = input_semester, `code` = input_code, `year` = input_year
WHERE `id` = input_course_id;

-- 14. List all modules
SELECT *
FROM `Module`;

-- 15. List of modules for a given course
SELECT m.`title`
FROM `Course` c, `Module` m
WHERE m.`course-fk` = c.`id` AND c.`id` = input_course_id;

-- 16. List of modules per class for a given user
SELECT c.`title`, m.`title`
FROM `User` u, `Registration` r, `Course` c, `Module` m
WHERE m.`course-fk` = c.`id` AND u.`id` = r.`user-fk` AND r.`course-fk` = c.`id` AND u.`id` = input_user_id;

-- 17. Add a module for a course
INSERT INTO `Module`
(`id`, `title`, `course-fk`)
VALUES (input_module_id, input_title, input_course_fk);

-- 18. Delete a module for a given course
DELETE FROM `Module`
WHERE `id` = input_module_id;

-- 19. Update a module for a given course
UPDATE `Module`
SET `title` = input_title
WHERE `id` = input_module_id;

-- 20. Get all the courses a student is registered for,
SELECT *
FROM `Course` c, `Registration` r, `User` u
WHERE c.`id` = r.`course-fk`
AND r.`user-fk`	 = u.`id`;

-- 21. Student makes a submission
INSERT INTO `Submission`
(`id`, `user-fk`, `exercise-fk`, `grade`)
VALUES (input_submission_id, input_user_id, input_exercise, input_grade);

-- 22. Get all submissions of a given student
SELECT *
FROM `Submission`
WHERE `user-fk` = input_user_id;

-- 23. Specific student grade for a given module.. UPDATE THE SCHEMA TO INCLUDE A TOTAL VALUE OF POSSIBLE POINTS IN EXERCISE
SELECT SUM(`points`)/SUM(e.`total`)
FROM `Exercise` e, `Module` m, (SELECT s.`exercise-fk`, MAX(`grade`) as points
								FROM `Submission` s, `Exercise` e, `Module` m
								WHERE s.`exercise-fk` = e.`id` AND e.`module-fk` = m.`id` AND s.`user-fk` = input_user_id AND m.`id` = input_module_id
								GROUP BY `exercise-fk`) AS SQ1
WHERE e.`id` = SQ1.`exercise-fk` AND e.`module-fk` = m.`id`;

-- 24. All students' grade for a given module.
SELECT SQ1.`user-fk`, SUM(`points`)/SUM(e.`total`)
FROM `Module` m, `Exercise` e, (SELECT `user-fk`, `exercise-fk`, MAX(`grade`) as points
  								FROM `Submission` s, `Exercise` e, `Module` m
  								WHERE s.`exercise-fk` = e.`id` AND e.`module-fk` = m.`id` AND m.`id` = input_module_id
  								GROUP BY `user-fk`, `exercise-fk`) AS SQ1
WHERE e.`id` = SQ1.`exercise-fk` AND e.`module-fk` = m.`id`
GROUP BY SQ1.`user-fk`;

-- 25. Student grade for a given course
SELECT SUM(`points`)/SUM(e.`total`)
FROM `Exercise` e, `Module` m, (SELECT s.`exercise-fk`, MAX(`grade`) as points
								FROM `Submission` s, `Exercise` e, `Module` m, `Course` c
								WHERE s.`exercise-fk` = e.`id` AND e.`module-fk` = m.`id` AND m.`course-fk` = c.`id` 
								AND s.`user-fk` = input_user_id AND c.`id` = input_course_id
								GROUP BY `exercise-fk`) AS SQ1
WHERE e.`id` = SQ1.`exercise-fk` AND e.`module-fk` = m.`id`;

-- 26. Student grade for all students for a given course
SELECT SQ1.`user-fk`, SUM(`points`)/SUM(e.`total`)
FROM `Exercise` e, `Module` m, (SELECT s.`user-fk`, s.`exercise-fk`, MAX(`grade`) as points
								FROM `Submission` s, `Exercise` e, `Module` m, `Course` c
								WHERE s.`exercise-fk` = e.`id` AND e.`module-fk` = m.`id` AND m.`course-fk` = c.`id` 
								AND c.`id` = input_course_id
								GROUP BY s.`user-fk`, s.`exercise-fk`) AS SQ1
WHERE e.`id` = SQ1.`exercise-fk` AND e.`module-fk` = m.`id`
GROUP BY SQ1.`user-fk`;
