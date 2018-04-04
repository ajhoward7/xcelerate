from flask import Flask, render_template, request, json
import csv

file_path = '/Users/danaiavg/Desktop/App_Developemnt/xcelerate/users/master_users.csv'

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
        # write in the users file
        myData = []
        myData.append([_name, _email, _password])

        myFile = open(file_path, 'a')
        writer = csv.writer(myFile)
        writer.writerows(myData)
        myFile.close()

        #### We need to check is the username and the email already exist

        return render_template('home.html', username=_name)
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

@app.route('/home/<string:username>')
def home(username):
    return render_template('home.html', username=username)

# @app.route('/logIn')
# def logIn():

if __name__ == "__main__":
    app.run()
