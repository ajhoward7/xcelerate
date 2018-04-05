from flask import Flask, render_template, request, json, Response, redirect, url_for, request, session, abort
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user
import csv

file_path = '../users/master_users.csv'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/showlogin")
def showlogin():
    return render_template('login.html')

####################
@app.route("/login", methods=["POST"])
def login():
    print(1)
    username = request.form['inputName']
    password = request.form['inputPassword']

    myFile = open(file_path, 'r+')

    reader = csv.reader(myFile, delimiter=',')
    flag = 'Not in file'
    # check database whether the user's name or email already exists
    for row in reader:
        if (username == row[0] or username == row[1]) and password == row[2]:
            flag = 'In file'

            break

    print(flag)
    myFile.close()

    if flag == 'In file':
        # return render_template('home.html', username=_name)
        return json.dumps({'html': '<span>Good job</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})




        # if password == username + "_secret":
        #     id = username.split('user')[1]
        #     user = User(id)
        #     login_user(user)
        #     return redirect(request.args.get("next"))
        # else:
        #     return abort(401)
####################

@app.route("/showSignup")
def showSignup():
    return render_template('signup.html')

@app.route('/home', methods=['POST'])
def home():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        # print(_name)
        # write in the users file
        myData = []
        myData.append([_name, _email, _password])

        myFile = open(file_path, 'r+')

        reader = csv.reader(myFile, delimiter=',')
        flag = 'Not in file'
        # check database whether the user's name or email already exists
        for row in reader:
            if _name == row[0] or _email == row[1]:
                flag = 'In file'
                return render_template('signup.html')

        # write only if the user's email or name does not exist
        if flag == 'Not in file':
            writer = csv.writer(myFile)
            writer.writerows(myData)
        # else:
        #     return json.dumps({'html': '<span>Enter the required fields</span>'})

        myFile.close()

        # return render_template('home.html', username=_name)
        return render_template('home.html', name=_name)
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    app.run()
