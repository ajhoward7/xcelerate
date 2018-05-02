from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import json
import sys
import datetime as dt
from werkzeug.security import check_password_hash, generate_password_hash

sys.path.insert(0, './main/algorithm')
try:
    from generate_plan import *
except ImportError:
    raise


def turn_plan_to_json(path, username):
    myfile = open(path + username + "/planned_training.csv", "r+")
    reader = csv.reader(myfile, delimiter=',')

    list_of_events = []
    for row in reader:
        if row[1] != "miles":
            list_of_events.append({"title": row[1] + " mile run", "start": str(row[3])})

    with open(path + username + "/events.json", 'w') as outfile:
        json.dump(list_of_events, outfile)
    return


master_file_path = './main/users/master_users.csv'
users_folder_file_path = './main/users/'

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


app = Flask(__name__)


@app.route("/")
def login():
    """
    Renders the login.html
    """
    return render_template('login.html')


@app.route("/authenticate", methods=["POST"])
def authenticate():
    """
    Requests the username and password and authenticates them
    """
    inputname = request.form['inputName']
    inputpassword = request.form['inputPassword']

    myfile = open(master_file_path, 'r+')
    reader = csv.reader(myfile, delimiter=',')

    for row in reader:
        if inputname == row[0] or inputname == row[1]:
            password = row[2]
            if check_password_hash(password, inputpassword):
                return render_template('welcomeback.html', username=row[0])

    myfile.close()
    return redirect(url_for('login'))


@app.route("/<username>/home", methods=["GET", "POST"])
def home(username):
    """
    Renders the home page
    """
    return render_template('json.html', name=username)


@app.route('/<username>/data')
def return_data(username):
    print('##')
    with open(users_folder_file_path + username + "/events.json", "r") as input_data:
        return input_data.read()


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
    real_p = request.form['inputPassword']

    user = User(username, real_p)
    password = user.password_hash

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
    data['prior_days_per_week'] = 0
    data['prior_miles_per_week'] = 0

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


# @app.route("/daysperweek/<username>", methods=['POST'])
# def daysperweek(username):
#     """
#     Renders the dayperweek page
#     """
#     path = users_folder_file_path + username
#     with open(path + '/preferences.txt', 'r+') as json_file:
#         data = json.load(json_file)

#         data["max_days_per_week"] = int(request.form['max_days_per_week'])

#         json_file.seek(0)  # rewind
#         json.dump(data, json_file)
#         json_file.truncate()    

#     if data['runner_type'] == 0:
#         return render_template('daysperweek.html', username=username)
#     elif data['runner_type'] == 1:
#         return render_template('thankyou.html', username=username)


@app.route("/prior_training/<username>", methods=['POST'])
def prior_training(username):
    """

    """
    path = users_folder_file_path + username
    dow_list = request.form.getlist('available_days')
    dow_list_int = [int(x) for x in dow_list]
    
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        if data['runner_type'] == 0:
            data["max_days_per_week"] = int(request.form['max_days_per_week'])
            data["available_days"] = dow_list_int

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate() 

            return render_template('prior_training.html', username=username)
        elif data['runner_type'] == 1:

            data["available_days"] = dow_list_int
            data['prior_days_per_week'] = int(request.form['prior_days_per_week'])
            data['prior_miles_per_week'] = float(request.form['prior_miles_per_week'])

            json_file.seek(0) 
            json.dump(data, json_file)
            json_file.truncate() 


        return render_template('increase.html', username=username)


@app.route("/rdirect/<username>", methods=['POST'])
def rdirect(username):
    """
    """
    path = users_folder_file_path + username

    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["prior_training"] = int(request.form['prior_training'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    if request.form['prior_training'] == "1" and data['runner_type'] == 0:
        return render_template('approx.html', username=username)

    elif request.form['prior_training'] == "1" and data['runner_type'] == 1:
        return render_template('approx_int.html', username=username)
    
    elif request.form['prior_training'] == "0":
        generate_plan(username)
        turn_plan_to_json(users_folder_file_path, username)

        return render_template('thankyou.html', username=username)


@app.route("/fill/<username>", methods=['POST'])
def fill(username):
    print(username)
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['prior_days_per_week'] = int(request.form['prior_days_per_week'])
        data['prior_miles_per_week'] = float(request.form['prior_miles_per_week'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()     

    if data['runner_type'] == 0:
        generate_plan(username)
        turn_plan_to_json(users_folder_file_path, username)

        return render_template('thankyou.html', username=username)
        # return redirect(url_for('.home', username=username))
    elif data['runner_type'] == 1:
        return render_template('daysperweek.html', username=username)


@app.route("/upload/<username>", methods=['GET', 'POST'])
def upload(username):
    return render_template('upload.html', username=username)


@app.route("/increase/<username>", methods=['POST'])
def increase(username):
    file = request.files['newfile']
    file.save('main/users/{}/activities.csv'.format(username))

    return render_template('increase.html', username=username)


@app.route("/max_days/<username>", methods=['POST'])
def max_days(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['training_level_increase'] = int(request.form['training_level_increase'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate() 

    return render_template('max_days.html', username=username)


@app.route("/thankyou/<username>", methods=['POST'])
def thankyou(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['training_level_increase'] = int(request.form['training_level_increase'])
        data['max_days_per_week'] = 99

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    generate_plan(username)
    turn_plan_to_json(users_folder_file_path, username)

    return render_template('thankyou.html', username=username)


if __name__ == "__main__":
    app.debug = True
#    app.run(host = '0.0.0.0', port = 80)
    app.run()
