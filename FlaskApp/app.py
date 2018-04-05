from flask import Flask, render_template, request, json
import csv

file_path = '../users/master_users.csv'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/showSignup")
def showSignup():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        print(_name)
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
                break

        # write only if the user's email or name does not exist
        if flag == 'Not in file':
            writer = csv.writer(myFile)
            writer.writerows(myData)
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

        myFile.close()

        # return render_template('home.html', username=_name)
        return json.dumps({'html': '<span>Good job</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

@app.route('/home/<string:username>')
def home(username):
    return render_template('home.html', username=username)


if __name__ == "__main__":
    app.run()
