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


@app.route("/presentation/<int:id>/<string:module>")
def presentation(id, module):
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

    print POST_USERNAME
    print POST_PASSWORD


    query = "SELECT `id`, `password` FROM `User` WHERE `email` = '%s'" % (POST_USERNAME)
    result = database(query)
    
    if len(result) == 0:
        return "Incorrect login details"
    else:
        row = result[0]

        user_id = row[0]
        user_password = row[1]

        if POST_PASSWORD == user_password:
            session['user-id'] = user_id
            return render_template('courses.html', id = user_id)
        else:
            return "Incorrect login detials"



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


@app.route('/modules')
def modules():
    userID = request.args.get('id')
    courseID = request.args.get('course')

    if session.get('user-id') is not None:
        user_id = session['user-id']

        if int(userID) == user_id:
            query = "SELECT C.`id` FROM `User` U, `Course` C, `Registration` R WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(userID), int(courseID))
            result = database(query)

            if len(result) == 0:
                return "Invalid Course"

            else:
                query = "SELECT M.`title` FROM `User` U, `Course` C, `Registration` R, `Module` M WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND U.`id` = '%d' AND C.`id` = '%d'" % (int(userID), int(courseID))
                result = database(query)
                session['course-id'] = courseID

                return jsonify(result)

        else:
            return "Incorrect User"

    else:
        return "Not Logged In"

@app.route('/module', methods = ['GET', 'POST'])
def module():
    if request.method == 'GET':

        userID = request.args.get('id')
        moduleID = request.args.get('module')

        if session.get('user-id') is not None:
            user_id = session['user-id']

            if int(userID) == user_id:
                course_id = session['course-id']

                query = "SELECT S.`code` FROM `User` U, `Course` C, `Registration` R, `Module` M, `Presentation` P, `Slide` S WHERE U.`id` = R.`user-fk` AND R.`course-fk` = C.`id` AND C.`id` = M.`course-fk` AND M.`id` = P.`module-fk` AND P.`id` = S.`presentation_fk` AND U.`id` = '%d' AND C.`id` = '%d' AND M.`id` = '%d'" % (int(userID), int(course_id), int(moduleID))
                result = database(query)
                
                if len(result) == 0:
                    return "Invalid Module"

                else:
                    return jsonify(result)

            else:
                return "Incorrect User"
        
        else:
            return "Not Logged In"

    elif request.method == 'POST':
        userID = request.get_json()['id']
        moduleID = request.get_json()['module']

        


        return data["test"]




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)


    

    
