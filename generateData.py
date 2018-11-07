import MySQLdb
from random import randint

lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum aliquam nisl ac augue aliquet euismod at vel nulla."
max_module_fk =
max_user_fk =
max_exercise_fk =
next_user_id_number =
next_course_id_number =
next_exercise_id_number =
next_submission_id_number =

def generateUsers(db):
    c = db.cursor()

    for i in (0, 80):
        input_user_id = i + next_user_id_number
        input_first_name = 'Student' + str(i)
        input_last_name = 'Last' + str(i)
        input_email = first_name + last_name + '@ucmerced.edu'
        input_password = str(i) + 'abc123'
        input_type = '2' # or whatever student is, I don't remember

        insert_tuple = (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type)

        c.execute('''INSERT INTO `User`
        (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`)
        VALUES (?, ?, ?, ?, ?, ?''', insert_tuple);

    for i in (80, 100):
        input_user_id = i + next_exercise_id_number
        input_first_name = 'Professor' + str(i)
        input_last_name = 'Last' + str(i)
        input_email = first_name + last_name + '@ucmerced.edu'
        input_password = str(i) + 'abc123'
        input_type = '2' # or whatever student is, I don't remember

        insert_tuple = (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type)

        c.execute('''INSERT INTO `User`
        (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`)
        VALUES (?, ?, ?, ?, ?, ?''', insert_tuple);

    db.commit()

def generateCourses(db):
    c = db.cursor()

    for i in (0, 100):
        input_course_id = i + next_course_id_number
        input_title = 'Course ' + str(i)
        input_semester = 'Fall' if (i < 50) else 'Spring'
        input_code = 'CSE' + str(i)
        input_year = 2018 if (i < 50) else 2019

        insert_tuple = (input_course_id, input_title, input_semester, input_code, input_year)

        c.execute(''' INSERT INTO `Course`
            (`id`, `title`, `semester`, `code`, `year`)
            VALUES(?,?,?,?,?)''', insert_tuple)

    db.commit()

def generateExercises(db):
    c = db.cursor()

    for i in (0:200):
        input_exercise_id = i + next_exercise_id_number
        input_title = "title " + str(i)
        input_instructions = lorem_ipsum
        input_module_fk = i % max_module_fk

        insert_tuple = (input_exercise_id, input_title, input_instructions, input_module_fk)

        c.execute(''' INSERT INTO `Exercise`
            (`id`, `title`, `instructions`, `module-fk`)
            VALUES (?,?,?,?)''', insert_tuple)

    db.commit()

# FIXME: I don't have the updated schema for submsisions
def generateSubmissions(db):
    c = db.cursor()

    for i in (0:600):
        input_submission_id = i + next_submission_id_number
        input_user_fk = i % max_user_fk
        input_exercise_fk = i % max_user_fk
        input_grade = randint(0, 20)
        input_points = 20
        ...




if __name__ == "__main__":
    db = MySQLdb.connect(...)

    generateUsers(db)
