from flask import Flask, render_template, request, redirect, url_for
import csv

mater_file_path = '../users/master_users.csv'

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/authenicate",methods=["POST"])
def authenticate():
    username = request.form['inputName']
    password = request.form['inputPassword']
    myFile = open(mater_file_path, 'r+')
    reader = csv.reader(myFile, delimiter=',')

    # check database whether the user's name or email already exists
    for row in reader:
        if (username == row[0] or username == row[1]) and password == row[2]:
            return redirect(url_for('.home', username=row[0]))

    myFile.close()
    return redirect(url_for('login'))

@app.route("/home/<username>")
def home(username):
    return render_template('home.html', name=username)

@app.route("/showSignup")
def showSignup():
    return render_template('signup.html')

@app.route('/racetype', methods=['POST'])
def racetype():
    # read the posted values from the UI
    username = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']

    # validate the received values
    if username and email and password:
        # write in the users file
        myData = []
        myData.append([username, email, password])

        myFile = open(mater_file_path, 'r+')

        reader = csv.reader(myFile, delimiter=',')
        # check database whether the user's name or email already exists
        for row in reader:
            if username == row[0] or email == row[1]:

                return render_template('signup.html')

        # write only if the user's email or name does not exist
        writer = csv.writer(myFile)
        writer.writerows(myData)

        myFile.close()

        # return render_template('home.html', username=_name)
        return render_template('racetype.html')
    else:
        return render_template('signup.html')

@app.route("/daysperweek", methods=['POST'])
def daysperweek():
    ###
    print(request.form['typerace'])
    ###
    return render_template('daysperweek.html')

@app.route("/runlevel", methods=['POST'])
def runlevel():
    ###
    print(request.form.getlist('dayofweek'))
    ###
    return render_template('runerlevel.html')

@app.route("/dates", methods=['POST'])
def dates():
    ###
    print(request.form['runlevel'])
    ###
    return render_template('dates.html')

@app.route("/home2",methods=["POST"])
def backhome():
    ###
    print(request.form['startdate'])
    print(request.form['enddate'])
    ###
    return render_template('home.html')

if __name__ == "__main__":
    app.run()
