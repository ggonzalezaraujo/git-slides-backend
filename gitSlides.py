from flask import Flask
from flask_cors import CORS
from flask import flash, redirect, render_template, request, session, abort, make_response
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from flask import request
import subprocess
import os
import MySQLdb



app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
CORS(app)

def ids():
    output = subprocess.check_output(['git', 'rev-list', 'HEAD'])
    items = output.split('\n')[0:-1]
    items.reverse()
    return items


def commandLines(id):
    baseCommand = 'git checkout '
    commandLine = []
    for i in id:
        commandLine.append(baseCommand + i)
    return commandLine


def extraction(commands, idList, module):
    slides = []
    for i in range(len(commands)):
        os.system("git checkout master")
        os.system(commands[i])

        try:
            file = open(module, 'r')
        except IOError:
            return "Could NOT Open File"

        file = open(module, 'r')
        slides.append({"commit:": idList[i], "code": file.read()})
        file.close()

    return slides


@app.route("/gitpresentation/<int:id>/<string:module>")
def gitpresentation(id, module):
    os.system("git checkout master")

    idList = ids()
    commands = commandLines(idList)
    slides = extraction(commands, idList, module)

    if slides == 'Could NOT Open File':
        return "File NOT FOUND"

    lecture = {"id": id, "slides": slides}

    return jsonify(lecture)


@app.route("/execute")
def execute():
    commit = request.args.get("id")

    os.system("git checkout master")
    os.system("git checkout " + commit)

    os.system("g++ -std=c++11 Demo.cpp -o main")
    os.system("./main < nums.txt > output.txt")

    #Reading text file and displaying output
    file = open("output.txt", 'r')
    output = file.read()
    file.close()

    return jsonify(output)


#Takes in a query and returns the result
def database(sql):
    db = MySQLdb.connect(host = "localhost", user = "root", passwd = "", db = "GitSlides")
    cur = db.cursor()
    result = []

    cur.execute(sql)

    result = cur.fetchall()

    db.close()

    return result


@app.route('/auth', methods = ['POST'])
def auth():

    POST_USERNAME = request.get_json()["user"]
    POST_PASSWORD = request.get_json()["password"]

    query = "SELECT `id`, `first_name`, `last_name`, `email`, `type-fk` FROM `User` WHERE `email` = '%s' AND `password` = '%s'" % (POST_USERNAME, POST_PASSWORD)
    result = database(query)

    if len(result) == 0:
        # return "Incorrect login details"
        return jsonify(-1)
    else :
        user_id = result[0][0]
        first_name = result[0][1]
        last_name = result[0][2]
        email = result[0][3]
        type_fk = result[0][4]

        query2 = "SELECT C.id, C.title FROM `User` U, `Course` C, `Registration` R WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND U.`id` = '%d'" % (user_id)
        result2 = database(query2)
        courses = []
        modules = []

        for i in result2:
            courses.append({"id": i[0], "name": i[1]})

        print (result2[0][0])

        query3 = "SELECT M.id, M.`title` FROM `User` U, `Course` C, `Registration` R, `Module` M WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(user_id), int(result2[0][0]))
        result3 = database(query3)

        for i in result3:
            modules.append({"module_id": i[0], "name": i[1]})

        print (result3)

        session['user-id'] = user_id
        return jsonify(user_id, first_name, last_name, email, type_fk, courses, modules)



@app.route('/courses')
def courses():
    if request.method == 'GET':

        userID = request.args.get('id')

        if session.get('user-id') is not None:
            user_id = session['user-id']

            if int(userID) == user_id:
                query = "SELECT C.title FROM `User` U, `Course` C, `Registration` R WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND U.`id` = '%d'" % (user_id)
                result = database(query)

                return jsonify(result)

            else:
                return "Incorrect User"

        else:
            return "Not Logged In"


@app.route('/modules', methods = ['GET'])
def modules():
    userID = request.args.get('user_id')
    courseID = request.args.get('course_id')

    if (userID and courseID) is not None:
        modules = []
        query = "SELECT M.`id`, M.`title` FROM `User` U, `Course` C, `Registration` R, `Module` M WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(userID), int(courseID))
        result = database(query)

        for i in result:
            modules.append({"module_id": i[0], "name": i[1]})

        return jsonify(modules)
    else :
        return jsonify(-1)


@app.route('/presentation')
def presentation():
    userID = request.args.get('user_id')
    courseID = request.args.get('course_id')
    moduleID = request.args.get('module_id')

    if (courseID and moduleID) is not None:
        #presentation = []
        query = "SELECT P.`file` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Presentation` P WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = P.`module-fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d'" % (int(userID), int(courseID), int(moduleID))
        result = database(query)
        print (result)
        return jsonify(result)


@app.route('/exercise')
def exercise():
    userID = request.args.get('user_id')
    courseID = request.args.get('course_id')
    moduleID = request.args.get('module_id')


    if (courseID and moduleID) is not None:
        #exercise = []
        query = "SELECT E.`title` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Exercise` E WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = E.`module-fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d'" % (int(userID), int(courseID), int(moduleID))

        result = database(query)
        print (result)
        return jsonify(result)

@app.route('/gradebook')
def gradebook():
    userID = request.args.get('user_id')
    #courseID = request.args.get('course_id')

    query = "SELECT SQ1.course_title, SUM(`points`)/SUM(e.`total`) FROM `Exercise` e, `Module` m, (SELECT c.`title` as course_title, s.`exercise-fk`, MAX(`grade`) as points FROM `Submission` s, `Exercise` e, `Module` m, `Course` c WHERE s.`exercise-fk` = e.`id` AND e.`module-fk` = m.`id` AND m.`course-fk` = c.`id` AND s.`user-fk` = '%d' GROUP BY `exercise-fk`) AS SQ1 WHERE e.`id` = SQ1.`exercise-fk` AND e.`module-fk` = m.`id` GROUP BY SQ1.course_title" % (int(userID))
    result = database(query)

    grades = []
    for i in result:
        grades.append({"course_name": i[0], "grade": float(i[1])})

    print(grades)

    return jsonify(grades)


@app.route('/slides')
def slides():
    userID = request.args.get('user_id')
    courseID = request.args.get('course_id')
    moduleID = request.args.get('module_id')
    presentationID = request.args.get('presentation_id')

    query = "SELECT S.`code` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Presentation` P, `Slide` S WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = P.`module-fk` AND P.`id` = S.`presentation_fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d' AND P.`id` = '%d'" % (int(userID), int(courseID), int(moduleID), int(presentationID))

    result = database(query)
    print (result)
    return jsonify(result)

@app.route('/exercise/instructions')
def exercise_instructions():
    userID = request.args.get('user_id')
    courseID = request.args.get('course_id')
    moduleID = request.args.get('module_id')
    exerciseID = request.args.get('exercise_id')

    if (courseID and moduleID) is not None:
        #exercise = []
        query = "SELECT E.`instructions` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Exercise` E WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = E.`module-fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d' AND E.`id` = '%d'" % (int(userID), int(courseID), int(moduleID), int(exerciseID))

        result = database(query)

        return jsonify(result)


# @app.route('/modules')
# def modules():
#     userID = request.args.get('id')
#     courseID = request.args.get('course')

#     if session.get('user-id') is not None:
#         user_id = session['user-id']

#         if int(userID) == user_id:
#             query = "SELECT C.`id` FROM `User` U, `Course` C, `Registration` R WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(userID), int(courseID))
#             result = database(query)

#             if len(result) == 0:
#                 return "Invalid Course"

#             else:
#                 query = "SELECT M.`title` FROM `User` U, `Course` C, `Registration` R, `Module` M WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(userID), int(courseID))
#                 result = database(query)
#                 session['course-id'] = courseID

#                 return jsonify(result)

#         else:
#             return "Incorrect User"

#     else:
#         return "Not Logged In"


# @app.route('/module', methods = ['GET', 'POST'])
# def module():
#     if request.method == 'GET':

#         userID = request.args.get('id')
#         moduleID = request.args.get('module')

#         if session.get('user-id') is not None:
#             user_id = session['user-id']

#             if int(userID) == user_id:
#                 course_id = session['course-id']

#                 query = "SELECT S.`code` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Presentation` P, `Slide` S WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = P.`module-fk` AND P.`id` = S.`presentation_fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d'" % (int(userID), int(course_id), int(moduleID))
#                 result = database(query)

#                 if len(result) == 0:
#                     return "Invalid Module"

#                 else:
#                     return jsonify(result)

#             else:
#                 return "Incorrect User"

#         else:
#             return "Not Logged In"

#     elif request.method == 'POST':
#         userID = request.get_json()['id']
#         moduleID = request.get_json()['module']




#         return data["test"]




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # app.run(debug=True,host='172.20.10.2', port=4000)
    app.run(debug=True,host='0.0.0.0', port=4000)
