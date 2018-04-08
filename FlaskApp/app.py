from flask import Flask, render_template, request
import csv

file_path = '../users/master_users.csv'

app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template('index.html')

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/home",methods=["POST"])
def home():
    username = request.form['inputName']
    password = request.form['inputPassword']
    myFile = open(file_path, 'r+')
    reader = csv.reader(myFile, delimiter=',')

    # check database whether the user's name or email already exists
    for row in reader:
        if (username == row[0] or username == row[1]) and password == row[2]:
            return render_template('home.html', name=row[0])

    myFile.close()
    return render_template('login.html')

@app.route("/showSignup")
def showSignup():
    return render_template('signup.html')

@app.route('/racetype', methods=['POST'])
def racetype():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:
        # write in the users file
        myData = []
        myData.append([_name, _email, _password])

        myFile = open(file_path, 'r+')

        reader = csv.reader(myFile, delimiter=',')
        # check database whether the user's name or email already exists
        for row in reader:
            if _name == row[0] or _email == row[1]:
                # flag = 'In file'
                return render_template('signup.html')

        # write only if the user's email or name does not exist
        writer = csv.writer(myFile)
        writer.writerows(myData)

        myFile.close()

        # return render_template('home.html', username=_name)
        return render_template('test.html')
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    app.run()
