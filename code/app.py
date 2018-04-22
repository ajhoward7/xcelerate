from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import json
import sys
import datetime as dt

sys.path.insert(0, './main/algorithm')
try:
    from algorithms import *
except ImportError:
    raise

# sys.path.insert(0, './main/algorithm')
# from algorithms import *

master_file_path = './main/users/master_users.csv'
users_folder_file_path = './main/users/'

app = Flask(__name__)


@app.route("/")
def login():
    """
    Renders the login.html
    """
    return render_template('login.html')


@app.route("/authenicate", methods=["POST"])
def authenticate():
    """
    Requests the username and password and authenticates them
    """
    username = request.form['inputName']
    password = request.form['inputPassword']
    myfile = open(master_file_path, 'r+')
    reader = csv.reader(myfile, delimiter=',')

    # check database whether the user's name or email already exists
    for row in reader:
        if (username == row[0] or username == row[1]) and password == row[2]:
            return redirect(url_for('.home', username=row[0]))

    myfile.close()
    return redirect(url_for('login'))


@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
    """
    Renders the home page
    """
    return render_template('home.html', name=username)


@app.route("/showSignup")
def showSignup():
    """
    Renders the signup page
    """
    return render_template('signup.html')


@app.route("/createUsers", methods=["POST"])
def createUsers():
    """
    Requests the new usre's username, email and password
    """
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

        # return redirect(url_for('.race_distance', username=username))
        return render_template('race_distance.html', username=username)
    else:
        return redirect(url_for('showSignup'))


@app.route('/race_distance/<username>')
def race_distance(username):
    """
    Renders the race distance page
    """
    return render_template('race_distance.html', username=username)


@app.route('/race_date/<username>', methods=['POST'])
def race_date(username):
    """
    Renders the race date page and creates the preferences.txt file
    """
    new_path = users_folder_file_path + username

    data = {}
    data['username'] = username
    data['start_date'] = dt.datetime.today().strftime("%Y-%m-%d")
    data['difficulty'] = 1
    data['race_distance'] = int(request.form['race_distance'])
    data['race_date'] = ''
    data['runner_type'] = ''
    data['max_days_per_week'] = ''
    data['prior_training'] = ''

    with open(new_path + '/preferences.txt', 'w') as outfile:
        json.dump(data, outfile)

    return render_template('race_date.html', username=username)


@app.route("/runner_type/<username>", methods=['POST'])
def runner_type(username):
    """
    Renders the runner type page
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["race_date"] = request.form['race_date']

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return render_template('runner_type.html', username=username)


@app.route("/split/<username>", methods=['POST'])
def split(username):
    """
    If user is a Novice, render the max days page
    If user is an Intermediate, render the how page
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["runner_type"] = int(request.form['runner_type'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    if request.form['runner_type'] == "0":
        return render_template('max_days.html', username=username)
    else:
        return render_template('how.html', username=username)


@app.route("/daysperweek/<username>", methods=['POST'])
def daysperweek(username):
    """
    Renders the dayperweek page
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["max_days_per_week"] = int(request.form['max_days_per_week'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()    

    return render_template('daysperweek.html', username=username)


@app.route("/prior_training/<username>", methods=['POST'])
def prior_training(username):
    """

    """
    path = users_folder_file_path + username
    dow_list = request.form.getlist('available_days')
    dow_list_int = [int(x) for x in dow_list]
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["available_days"] = dow_list_int

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate() 
    if data['runner_type'] == 0:
        return render_template('prior_training.html', username=username)
    elif data['runner_type'] == 1:
        return render_template('increase.html', username=username)


@app.route("/redirect/<username>", methods=['POST'])
def redirect(username):
    """
    """
    path = users_folder_file_path + username

    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["prior_training"] = int(request.form['prior_training'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()     

    if request.form['prior_training'] == "1":
        return render_template('approx.html', username=username)
    
    elif request.form['prior_training'] == "0":
        return render_template('thankyou.html', username=username)


@app.route("/fill/<username>", methods=['POST'])
def fill(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['prior_days_per_week'] = int(request.form['prior_days_per_week'])
        data['prior_miles_per_week'] = float(request.form['prior_miles_per_week'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()     

    if data['runner_type'] == 0:
        return render_template('thankyou.html', username=username)
    elif data['runner_type'] == 1:
        return render_template('daysperweek.html', username=username)


@app.route("/upload/<username>", methods=['GET'])
def upload(username):
    return render_template('upload.html', username=username)


@app.route("/increase/<username>", methods=['POST'])
def increase(username):
    return render_template('increase.html', username=username)


@app.route("/thankyou/<username>", methods=['POST'])
def thankyou(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['training_level_increase'] = int(request.form['training_level_increase'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate() 

    return render_template('thankyou.html', username=username)


@app.route("/backhome/<username>", methods=["POST"])
def backhome(username):
    """
    Renders the home page after a user signups
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["startdate"] = request.form['startdate']
        data["enddate"] = request.form['enddate']

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return redirect(url_for('.home', username=username))


@app.route('/inputs/<username>')
def render(username):
    """
    Renders the inputs page
    """
    return render_template('inputs.html', username=username)


@app.route('/home/<username>/results', methods=["POST"])
def inputs(username):
    """
    Renders the results page
    """
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

    return render_template('results.html', name=username, output=output)


if __name__ == "__main__":
    app.run()
