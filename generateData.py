import MySQLdb

def generateUsers(db):
    c = db.cursor()
    character = 'A'

    for i in (0, 80):
        input_user_id = i + ____#next id number
        input_first_name = 'Student' + character
        input_last_name = 'Last' + character
        input_email = first_name + last_name + '@ucmerced.edu'
        input_password = character + 'abc123'
        input_type = '2' # or whatever student is, I don't remember

        c.execute('''INSERT INTO `User`
        (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`)
        VALUES (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type);

    for i in (0, 20):
        input_user_id = i + ____#next id number
        input_first_name = 'Professor' + character
        input_last_name = 'Last' + character
        input_email = first_name + last_name + '@ucmerced.edu'
        input_password = character + 'abc123'
        input_type = '1' # or whatever prof is, I don't remember

        c.execute('''INSERT INTO `User`
        (`id`, `first_name`, `last_name`, `email`, `password`, `type-fk`)
        VALUES (input_user_id, input_first_name, input_last_name, input_email, input_password, input_type);

    db.commit()




if __name__ == "__main__":
    db = MySQLdb.connect(...)

    generateUsers(db)
