from flask import Flask, render_template, request, redirect, url_for, abort
import os
import csv
import json
import sys
import datetime as dt
from calendar import Calendar
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash

sys.path.insert(0, './main/algorithm')
try:
    from update_plan import *
    from generate_plan import *
    from process_garmin import *
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
# app.secret_key = 'some_secret'


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
                return redirect(url_for('.gohome', username=row[0]))

    myfile.close()
    return redirect(url_for('login'))


@app.route("/fi/<username>", methods=["GET", "POST"])
def gohome(username):

    generate_plan(username)
    turn_plan_to_json(users_folder_file_path, username)
    
    return redirect(url_for('.foo', username=username))


@app.route("/add/<username>", methods=['POST'])
def add(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        if data['runner_type'] == 1:
            data['training_level_increase'] = int(request.form['training_level_increase'])
            data['max_days_per_week'] = 99

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()
    return redirect(url_for('.gohome', username=username))

@app.route("/foo/<username>", methods=["POST"])
def home(username):
    """
    Renders the home page
    """
    inputdate = request.form['inputdate']
    inputmiles = request.form['inputmiles']
    inputtime = request.form['inputtime']
    inputtitle = request.form['inputtitle']

    if request.form['submit'] == 'add more':
        with open(users_folder_file_path + username + '/logged_training.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([inputdate, inputmiles, inputtime, inputtitle])

    elif request.form['submit'] == 'finish update':
        with open(users_folder_file_path + username + '/logged_training.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([inputdate, inputmiles, inputtime, inputtitle])
        update_plan(username)

    return redirect(url_for('.foo', username=username))


# @app.route("/<username>/home", methods=["GET", "POST"])
# def foo(username):
#     """
#     Renders the home page
#     """
#     return render_template('json.html', name=username)


# @app.route('/<username>/data')
# def return_data(username):
#     with open(users_folder_file_path + username + "/events.json", "r") as input_data:
#         return input_data.read()


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

        f = open(new_path + '/future_training.csv', 'w')
        f.close()

        g = open(new_path + '/logged_training.csv', 'w')
        writer = csv.writer(g)
        writer.writerow(['run_date', 'miles', 'time', 'title'])
        g.close()

        return render_template('race_distance.html', username=username)
    else:
        return redirect(url_for('showSignup'))


@app.route('/race_distance/<username>')
def race_distance(username):
    """
    Renders the race distance page
    """
    return render_template('race_distance.html', username=username)


@app.route('/runner_type/<username>', methods=['POST'])
def runner_type(username):
    """
    Renders the race date page and creates the preferences.txt file
    """
    new_path = users_folder_file_path + username

    data = {}
    data['username'] = username
    data['start_date'] = dt.datetime.today().strftime("%Y-%m-%d")
    data['difficulty'] = 1
    data['race_distance'] = int(request.form['race_distance'])
    data['race_date'] = request.form['race_date']
    data['runner_type'] = ''
    data['max_days_per_week'] = ''
    data['prior_training'] = ''
    data['prior_days_per_week'] = 0
    data['prior_miles_per_week'] = 0
    data['training_level_increase'] = 0

    with open(new_path + '/preferences.txt', 'w') as outfile:
        json.dump(data, outfile)

    return render_template('runner_type.html', username=username)


# @app.route("/runner_type/<username>", methods=['POST'])
# def runner_type(username):
#     """
#     Renders the runner type page
#     """
#     path = users_folder_file_path + username
#     with open(path + '/preferences.txt', 'r+') as json_file:
#         data = json.load(json_file)

#         data["race_date"] = request.form['race_date']

#         json_file.seek(0)  # rewind
#         json.dump(data, json_file)
#         json_file.truncate()

#     return render_template('runner_type.html', username=username)


# @app.route("/split/<username>", methods=['POST'])
# def split(username):
#     """
#     If user is a Novice, render the max days page
#     If user is an Intermediate, render the how page
#     """
#     path = users_folder_file_path + username
#     with open(path + '/preferences.txt', 'r+') as json_file:
#         data = json.load(json_file)

#         data["runner_type"] = int(request.form['runner_type'])

#         json_file.seek(0)  # rewind
#         json.dump(data, json_file)
#         json_file.truncate()

#     if request.form['runner_type'] == "0":
#         return render_template('max_days.html', username=username)
#     else:
#         return render_template('how.html', username=username)


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


@app.route("/rdirect/<username>", methods=["GET", "POST"])
def rdirect(username):
    """
    """

    path = users_folder_file_path + username

    with open(path + '/preferences.txt', 'r+') as json_file:
        # print("here!")
        data = json.load(json_file)

        if data['runner_type'] == "":
            data["prior_training"] = 1
            data['runner_type'] = 1

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()
            # print("im here!")

        elif data['runner_type'] == 0:
            # print(int(request.form["prior_training"]))
            data["prior_training"] = int(request.form["prior_training"])
            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()
            print("actually im here!")

    if data['prior_training'] == 1 and data['runner_type'] == 0:
        print("jere!")
        return render_template('approx.html', username=username)

    elif data['prior_training'] == 1 and data['runner_type'] == 1:
        return render_template('approx_int.html', username=username)
    
    elif data['prior_training'] == 0:
        generate_plan(username)
        turn_plan_to_json(users_folder_file_path, username)

        # return render_template('thankyou.html', username=username)
        return redirect(url_for('.gohome', username=username))
    # return render_template('upload.html', username=username)


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

        # return render_template('thankyou.html', username=username)
        return redirect(url_for('.gohome', username=username))
        # return redirect(url_for('.home', username=username))
    elif data['runner_type'] == 1:
        return render_template('daysperweek.html', username=username)


@app.route("/upload/<username>", methods=['GET', 'POST'])
def upload(username):
    return render_template('upload.html', username=username)


@app.route("/increase/<username>", methods=['POST'])
def increase(username):
    # file = request.files['newfile']
    # file.save('main/users/{}/activities.csv'.format(username))
    path = users_folder_file_path + username
    dow_list = request.form.getlist('available_days')
    dow_list_int = [int(x) for x in dow_list]
    
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data["max_days_per_week"] = int(request.form['max_days_per_week'])
        data["available_days"] = dow_list_int

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate() 
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

    if data['runner_type'] == 0:
        return render_template('max_days.html', username=username)
    elif data['runner_type'] == 1:
        return render_template('max_days_int.html', username=username)


@app.route("/thankyou/<username>", methods=['POST'])
def thankyou(username):
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['max_days_per_week'] = int(request.form['max_days_per_week'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    return redirect(url_for('.gohome', username=username))

@app.route("/daysperweek/<username>", methods=['POST'])
def daysperweek(username):
    
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)
        print(1)
        try:
            file = request.files['newfile']
            if file.filename == '':
                return render_template('upload.html', username=username)
            elif 'newfile' in request.files:
            # print("here!")
                data["runner_type"] = 1
                data["prior_training"] = 1
                json_file.seek(0)  # rewind
                json.dump(data, json_file)
                json_file.truncate()

                file = request.files['newfile']
                file.save('main/users/{}/activities.csv'.format(username))
                filepath = 'main/users/{}/activities.csv'.format(username)
                process_garmin(filepath, username)

                return render_template('daysperweek.html', username=username)
        except:
            data["runner_type"] = 0
            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()

            return render_template('max_days.html', username=username)
        # elif 'newfile' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
            
            # return render_template('max_days.html', username=username)


@app.route('/home/<username>', methods=['GET', 'POST'])
@app.route('/<int:year>/')
def foo(username):
    year = 2018
    cal = Calendar(0)
    training_list = []
    path = users_folder_file_path + username
    with open(path + '/planned_training.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        for row in readCSV:

            if datetime.strptime(row[3], '%Y-%m-%d')>= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) :
                training_list.append([row[1], int(row[3].split('-')[0]), int(row[3].split('-')[1]), int(row[3].split('-')[2])])


    logged_training = []
    with open(path + '/logged_training.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        for row in readCSV:
            if row[0] != '' and row[1] != '':
                logged_training.append([row[1], int(row[0].split('-')[0]), int(row[0].split('-')[1]), int(row[0].split('-')[2])])


    try:
        if not year:
            year = date.today().year
        cal_list = [
            cal.monthdatescalendar(year, i+1)
            for i in range(12)
        ]
    except:
        abort(404)
    else:
        return render_template('new_.html', username=username, year=year, cal=cal_list, training_list=training_list[:-1], logged_training=logged_training, race_date=training_list[-1])
    abort(404)


if __name__ == "__main__":
    app.debug = True
#    app.run(host = '0.0.0.0', port = 80)
    app.run()
