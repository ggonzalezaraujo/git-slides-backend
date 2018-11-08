import MySQLdb
import random
import math
from random import randint

lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum aliquam nisl ac augue aliquet euismod at vel nulla."
# max_module_fk =
# max_user_fk =
# max_exercise_fk =
next_user_id_number = 11
next_course_id_number = 9
next_exercise_id_number = 33
next_submission_id_number = 73

def generateUsers(db):
    c = db.cursor()

    for i in range(1, 81):
        input_user_id = i
        input_first_name = 'Student' + str(i)
        input_last_name = 'Last' + str(i)
        input_email = input_first_name + input_last_name + '@ucmerced.edu'
        input_password = str(i) + 'abc123'
        input_type = '4' # or whatever student is, I don't remember

        query = """INSERT INTO `User` (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`) VALUES (%s, %s, %s, %s, %s, %s)"""

        c.execute(query, (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type))


    for i in range(81, 101):
        input_user_id = i
        input_first_name = 'Professor' + str(i)
        input_last_name = 'Last' + str(i)
        input_email = input_first_name + input_last_name + '@ucmerced.edu'
        input_password = str(i) + 'abc123'
        input_type = '2' # or whatever student is, I don't remember

        query2 = """INSERT INTO `User` (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`) VALUES (%s, %s, %s, %s, %s, %s)"""
        c.execute(query2, (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type))

    db.commit()

def generateCourses(db):
    c = db.cursor()

    for i in range(1, 101):
        input_course_id = i
        input_title = 'Course ' + str(i)
        input_semester = 'Fall' if (i < 50) else 'Spring'
        input_code = 'CSE' + str(i)
        input_year = 2018 if (i < 50) else 2019

        query = """INSERT INTO `Course` (`id`, `title`, `semester`, `code`, `year`) VALUES (%s, %s, %s, %s, %s)"""

        c.execute(query, (input_course_id, input_title, input_semester, input_code, input_year))


    db.commit()

def generateModule(db):
    c = db.cursor()

    for i in range(1,201):
        input_module_id = i
        input_module_title = 'Module' + str(i)
        if (i % 2 == 0):
            input_course_fk = (i / 2)
        else:
            temp = i + 1
            input_course_fk = (temp / 2)

        query = """INSERT INTO `Module` (`id`, `title`, `course-fk`) VALUES (%s, %s, %s)"""
        c.execute(query, (input_module_id, input_module_title, input_course_fk))

    db.commit()

def generateExercise():
    c = db.cursor()

    for i in range(1, 401):
        input_ex_id = i
        input_ex_title = 'Exercise' + str(i)
        input_ex_instructions = 'Instruction #' + str(i) + 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        if (i % 2 == 0):
            input_ex_module = (i / 2)
        else:
            temp = i + 1
            input_ex_module = (temp / 2)
        input_ex_total = '100.00'

        query = """INSERT INTO `Exercise` (`id`, `title`, `instructions`, `module-fk`, `total`) VALUES (%s, %s, %s, %s, %s)"""

        c.execute(query, (input_ex_id, input_ex_title, input_ex_instructions, input_ex_module, input_ex_total))

    db.commit()



def generateRegistrion(temp):
    c =db.cursor()
    # for i in range(1, 321):
    #     input_id = i
    #
    #     temp2 = i - 1
    #
    #     if(temp2 == 0):
    #         input_user_fk = 1
    #     else:
    #         if(temp2 % 4 == 0):
    #             temp = temp + 1
    #
    #         input_user_fk = temp
    #
    #     input_course_fk = random.randint(1, 80)
    #
    #     query = """INSERT INTO `Registration` (`id`, `user-fk`, `course-fk`) VALUES (%s, %s, %s)"""
    #
    #     c.execute(query, (input_id, input_user_fk, input_course_fk))

    for i in range(1, 101):
        input_id = i + 320

        temp2 = i - 1

        if(temp2 == 0):
            input_user_fk = 81
        else:
            if(temp2 % 5 == 0):
                temp = temp + 1

            input_user_fk = temp + 80

        input_course_fk = i

        query = """INSERT INTO `Registration` (`id`, `user-fk`, `course-fk`) VALUES (%s, %s, %s)"""

        c.execute(query, (input_id, input_user_fk, input_course_fk))



    db.commit()

def generateSubmission(temp):
    c = db.cursor()

    query = """SELECT r.`course-fk`, r.`user-fk`
              FROM `Registration` r, `User` u
              WHERE r.`user-fk` = u.`id` AND u.`type-fk` = 4
              GROUP BY r.`course-fk`, r.`user-fk`;"""

    c.execute(query)

    rows = c.fetchall()

    user = []
    course = []

    for i in rows:
        course.append(i[0])
        user.append(i[1])


    for i in range(1, 318):

        course_end = course[i - 1] * 4
        user_id = user[i - 1]

        for j in range(0, 4):

            randNum = random.random()
            perc = randNum * 100
            grade = round(perc, 2)

            query = """INSERT INTO `Submission` (`id`, `user-fk`, `exercise-fk`, `grade`) VALUES (%s, %s, %s, %s)"""

            c.execute(query, (temp, user_id, course_end, grade))

            course_end = course_end - 1
            temp = temp + 1


    db.commit()


def generatePresentation():
    c = db.cursor()

    for i in range(1, 201):
        id = i
        repo_path = 'User/Documents/file/' + str(i)
        file = 'File#' + str(i)
        pdf_path = 'User/Documents/PDF/' + str(i)
        module_fk = i


        query = """INSERT INTO `Presentation` (`id`, `repo-path`, `file`, `pdf-path`, `module-fk`) VALUES (%s, %s, %s, %s, %s)"""

        c.execute(query, (id, repo_path, file, pdf_path, module_fk))

    db.commit()


def generateSlide():
    c = db.cursor()

    for i in range(1, 201):
        id = i
        presentation_mod_fk = i
        code = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vitae aliquet nec ullamcorper sit amet risus nullam eget. Scelerisque mauris pellentesque pulvinar pellentesque habitant.'
        commit = 'Commit#' + str(i)

        query = """INSERT INTO `Slide` (`id`, `presentation_fk`, `code`, `commit`) VALUES (%s, %s, %s, %s)"""

        c.execute(query, (id, presentation_mod_fk, code, commit))

    db.commit()




if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="GitSlides")

    temp = 1
    #generateUsers(db)
    #generateCourses(db)
    #generateModule(db)
    #generateExercise()
    #generateRegistrion(temp)
    #generateSubmission(temp)
    #generatePresentation()
    #generateSlide()
