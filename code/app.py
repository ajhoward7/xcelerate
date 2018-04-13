from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import json
import sys

sys.path.insert(0, './main/algorithm')
from algorithms import *


master_file_path = './main/users/master_users.csv'
users_folder_file_path = './main/users/'

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/authenicate",methods=["POST"])
def authenticate():
    username = request.form['inputName']
    password = request.form['inputPassword']
    myFile = open(master_file_path, 'r+')
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

@app.route("/createUsers", methods=["POST"])
def createUsers():
    username = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']

    # validate the received values
    if username and email and password:
        # write in the users file
        myData = []
        myData.append([username, email, password])

        myFile = open(master_file_path, 'r+')

        reader = csv.reader(myFile, delimiter=',')
        # check database whether the user's name or email already exists
        for row in reader:
            if username == row[0] or email == row[1]:
                return redirect(url_for('showSignup'))

        # write only if the user's email or name does not exist
        writer = csv.writer(myFile)
        writer.writerows(myData)

        myFile.close()

        new_path = users_folder_file_path + username
        os.makedirs(new_path)

        p = open(new_path + '/past_training.csv', 'w')
        p.close()

        f = open(new_path + '/future_training.csv', 'w')
        f.close()

        return redirect(url_for('.racetype', username=username))
    else:
        return redirect(url_for('showSignup'))


@app.route('/racetype/<username>')
def racetype(username):
    return render_template('racetype.html', username=username)

@app.route("/daysperweek/<username>", methods=['POST'])
def daysperweek(username):

    new_path = users_folder_file_path + username

    data = {}
    data['username'] = username
    data['typerace'] = request.form['typerace']
    data['dayofweek'] = ''
    data['runlevel'] = ''
    data['startdate'] = ''
    data['enddate'] = ''

    with open(new_path + '/preferences.txt', 'w') as outfile:
        json.dump(data, outfile)

    return render_template('daysperweek.html', username=username)

@app.route("/runlevel/<username>", methods=['POST'])
def runlevel(username):

    with open(users_folder_file_path + username +'/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["dayofweek"] = request.form.getlist('dayofweek')

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return render_template('runerlevel.html', username=username)

@app.route("/dates/<username>", methods=['POST'])
def dates(username):

    with open(users_folder_file_path + username +'/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["runlevel"] = request.form['runlevel']

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return render_template('dates.html', username=username)

@app.route("/backhome/<username>",methods=["POST"])
def backhome(username):

    with open(users_folder_file_path + username +'/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["startdate"] = request.form['startdate']
        data["enddate"] = request.form['enddate']

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return redirect(url_for('.home', username=username))

@app.route('/inputs/<username>')
def render(username):
    return render_template('inputs.html', username=username)

@app.route('/home/<username>/results', methods=["POST"])
def inputs(username):
    new_path = users_folder_file_path + username

    racelevel = request.form['racelevel']
    numdays = request.form['numdays']

    myFile = open(new_path + '/past_training.csv', 'r+')

    myData = []
    myData.append([racelevel, numdays])

    writer = csv.writer(myFile)
    writer.writerows(myData)
    myFile.close()

    output = algorithm(racelevel, numdays)

    myFile = open(new_path + '/future_training.csv', 'r+')

    myData = []
    myData.append([output])

    writer = csv.writer(myFile)
    writer.writerows(myData)
    myFile.close()

    # return redirect(url_for('.results', username = username, output = output))
    return render_template('results.html', name=username, output=output)

# @app.route('/results/<username>')
# def results(username, output):
#     return render_template('results.html', name = username, output = output)

if __name__ == "__main__":
    app.run()
