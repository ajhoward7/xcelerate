from flask import Flask, render_template, request, redirect, url_for, abort
import os
import csv
import json
import sys
import datetime as dt
from calendar import Calendar
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash
from dateutil.relativedelta import relativedelta

sys.path.insert(0, './main/algorithm')
try:
    from update_plan import *
    from generate_plan import *
    from process_garmin import *
    from plotting_funcs import *
except ImportError:
    raise


master_file_path = './main/users/master_users.csv'
users_folder_file_path = './main/users/'
races_path = './main/races'


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
                return redirect(url_for('.foo', username=row[0]))

    myfile.close()
    return redirect(url_for('login'))


@app.route("/fi/<username>", methods=["GET", "POST"])
def gohome(username):
    """
    Generates user's training plan and redirects to home page
    """
    generate_plan(username)
    generate_mileage_line(username)
    if username == 'alex':
        last_date = '2018-04-18'
        generate_map(username, last_date)

    return redirect(url_for('.foo', username=username))


@app.route("/add/<username>", methods=['POST'])
def add(username):
    """
    Add training level increase and redirects to home page
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        if data['runner_type'] == 1:
            data['training_level_increase'] = \
                int(request.form['training_level_increase'])
            data['max_days_per_week'] = 99

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()
    return redirect(url_for('.gohome', username=username))


@app.route("/foo/<username>", methods=["POST"])
def home(username):
    """
    Renders the home page and save preferences
    """
    path = users_folder_file_path + username
    inputdate = request.form['inputdate']
    inputmiles = request.form['inputmiles']
    inputdifficulty = int(request.form['inputdifficulty'])

    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['difficulty'] = inputdifficulty
        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    if request.form['submit'] == 'Add More':
        with open(path + '/logged_training.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([inputdate, inputmiles])

    elif request.form['submit'] == 'Finished':
        with open(path + '/logged_training.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([inputdate, inputmiles])
        update_plan(username, inputdate)
        generate_mileage_line(username)
        if username == 'alex':
            last_date = '2018-04-18'
            generate_map(username, last_date)

    return redirect(url_for('.foo', username=username))


@app.route("/showSignup")
def showSignup():
    """
    Renders the signup page
    """
    return render_template('signup.html')


@app.route("/createUsers", methods=["POST"])
def createUsers():
    """
    Requests the new user's username, email and password
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

        g = open(new_path + '/logged_training.csv', 'w')
        writer = csv.writer(g)
        writer.writerow(['run_date', 'miles', 'time', 'title'])
        g.close()

        title = []
        distance = []
        location = []
        race_date = []
        url_link = []
        id_ = []

        with open(races_path + '/races.csv') as f:
            readCSV = csv.reader(f, delimiter=',')
            next(readCSV, None)

            for line in readCSV:
                title.append(line[1])
                distance.append(line[4])
                location.append(line[2])
                race_date.append(line[3])
                url_link.append(line[5])
                id_.append(line[0])

        printed_distance = []
        for i in distance:
            if i == "0":
                printed_distance.append('5k')
            elif i == "1":
                printed_distance.append('10k')
            elif i == "2":
                printed_distance.append('Half Marathon')
            elif i == "3":
                printed_distance.append('Marathon')

        return render_template('pick_race.html',
                               username=username,
                               title=title,
                               location=location,
                               race_date=race_date,
                               url_link=url_link,
                               id_=id_,
                               len1=len(id_),
                               printed_distance=printed_distance)
    else:
        return redirect(url_for('showSignup'))


@app.route('/race_distance/<username>')
def race_distance(username):
    """
    Renders the race distance page
    """
    return render_template('race_distance.html', username=username)


@app.route('/li/<username>/<race_id>', methods=['POST'])
def redirecting_pick_race(username, race_id):
    """
    Save the information from the race picked
    """
    with open(races_path + '/races.csv', 'r+') as f:
        readCSV = csv.reader(f, delimiter=',')
        for line in readCSV:
            if line[0] == race_id:
                miles = int(line[4])
                race_date = line[3]
    data = {}
    data['username'] = username
    data['start_date'] = dt.datetime.today().strftime("%Y-%m-%d")
    data['difficulty'] = 1
    data['race_distance'] = miles
    data['race_date'] = race_date
    data['runner_type'] = ''
    data['max_days_per_week'] = ''
    data['prior_training'] = ''
    data['prior_days_per_week'] = 0
    data['prior_miles_per_week'] = 0
    data['training_level_increase'] = 0

    new_path = users_folder_file_path + username
    with open(new_path + '/preferences.txt', 'w') as outfile:
        json.dump(data, outfile)

    return redirect(url_for('.runner_type', username=username))


@app.route('/la/<username>', methods=["POST"])
def redirecting_pick_miles(username):
    """
    Saves the information if the user manually added the miles and the date
    """
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

    new_path = users_folder_file_path + username
    with open(new_path + '/preferences.txt', 'w') as outfile:
        json.dump(data, outfile)
    return redirect(url_for('.runner_type', username=username))


@app.route('/runner_type/<username>', methods=["GET"])
def runner_type(username):
    """
    Renders the race date page and creates the preferences.txt file
    """
    return render_template('runner_type.html', username=username)


@app.route("/prior_training/<username>", methods=['GET', 'POST'])
def prior_training(username):
    """
    Renders prior training page if Novice,
    Renders increase page if Intermediate
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
            data['prior_days_per_week'] = \
                int(request.form['prior_days_per_week'])
            data['prior_miles_per_week'] = \
                float(request.form['prior_miles_per_week'])

            json_file.seek(0)
            json.dump(data, json_file)
            json_file.truncate()

        return render_template('increase.html', username=username)


@app.route("/rdirect/<username>", methods=["GET", "POST"])
def rdirect(username):
    """
    Redirects to home page if Novice,
    Renders approximation page if Intermediate
    """
    path = users_folder_file_path + username

    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        if data['runner_type'] == "":
            data["prior_training"] = 1
            data['runner_type'] = 1

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()

        elif data['runner_type'] == 0:
            dow_list = request.form.getlist('available_days')
            dow_list_int = [int(x) for x in dow_list]

            data["max_days_per_week"] = int(request.form['max_days_per_week'])
            data["available_days"] = dow_list_int

            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()

    if data['prior_training'] == 1 and data['runner_type'] == 0:
        return render_template('approx.html', username=username)

    elif data['prior_training'] == 1 and data['runner_type'] == 1:
        return render_template('approx_int.html', username=username)
    elif data['runner_type'] == 0:
        generate_plan(username)
        generate_mileage_line(username)
        if username == 'alex':
            last_date = '2018-04-18'
            generate_map(username, last_date)

        return redirect(url_for('.gohome', username=username))


@app.route("/fill/<username>", methods=['POST'])
def fill(username):
    """
    Redirects to home page if Novice,
    Renders days per week page if Intermediate
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['prior_days_per_week'] = int(request.form['prior_days_per_week'])
        data['prior_miles_per_week'] = \
            float(request.form['prior_miles_per_week'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    if data['runner_type'] == 0:
        generate_plan(username)
        generate_mileage_line(username)
        if username == 'alex':
            last_date = "2018-04-18"
            generate_map(username, last_date)

        return redirect(url_for('.gohome', username=username))
    elif data['runner_type'] == 1:
        return render_template('daysperweek.html', username=username)


@app.route("/upload/<username>", methods=['GET', 'POST'])
def upload(username):
    """
    Renders upload page
    """
    return render_template('upload.html', username=username)


@app.route("/increase/<username>", methods=['POST'])
def increase(username):
    """
    Renders increase page
    """
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
    """
    Renders max days per week page
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)

        data['training_level_increase'] = \
            int(request.form['training_level_increase'])

        json_file.seek(0)  # rewind
        json.dump(data, json_file)
        json_file.truncate()

    if data['runner_type'] == 0:
        return render_template('max_days.html', username=username)
    elif data['runner_type'] == 1:
        return render_template('max_days_int.html', username=username)


@app.route("/thankyou/<username>", methods=['POST'])
def thankyou(username):
    """
    Redirects to home page
    """
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
    """
    Renders max days per week page if Novice,
    Renders days per week page if Intermediate
    """
    path = users_folder_file_path + username
    with open(path + '/preferences.txt', 'r+') as json_file:
        data = json.load(json_file)
        try:
            file = request.files['newfile']
            if file.filename == '':
                return render_template('upload.html', username=username)
            elif 'newfile' in request.files:
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
        except BaseException:
            data["runner_type"] = 0
            json_file.seek(0)  # rewind
            json.dump(data, json_file)
            json_file.truncate()

            return render_template('max_days.html', username=username)


@app.route('/home/<username>', methods=['GET', 'POST'])
@app.route('/<int:year>/')
def foo(username):
    """
    Renders calendar and home page
    """
    year = 2018
    cal = Calendar(-1)
    training_list = []
    path = users_folder_file_path + username

    weekdays = ['Sunday', 'Monday', 'Tuesday',
                'Wednesday', 'Thursday', 'Friday', 'Saturday']
    mydate = date.today()
    list_month = []
    for i in range(12):
        list_month.append(mydate.strftime("%B"))
        mydate = mydate + relativedelta(months=+1)

    logged_training = []

    with open(path + '/logged_training.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        for row in readCSV:
            if row[0] != '' and row[1] != '':

                logged_training.append(
                    [row[1], int(row[0].split('-')[0]),
                     int(row[0].split('-')[1]), int(row[0].split('-')[2])])

    if len(logged_training) > 0:
        dates = [training[1:] for training in logged_training]
        dates = [datetime.strptime('-'.join(str(x) for x in date1),
                                   '%Y-%m-%d') for date1 in dates]
        last_day = max(dates)
    else:
        last_day = datetime.now().replace(hour=0,
                                          minute=0,
                                          second=0,
                                          microsecond=0)

    with open(path + '/planned_training.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        for row in readCSV:
            if datetime.strptime(row[2], '%Y-%m-%d') > last_day:
                training_list.append([row[0],
                                      int(row[2].split('-')[0]),
                                      int(row[2].split('-')[1]),
                                      int(row[2].split('-')[2])])
    try:
        if not year:
            year = date.today().year
        cal_list = [
            cal.monthdatescalendar(year, i+1)
            for i in range(12)
            if i >= date.today().month - 1]
        cal_list2 = [
            cal.monthdatescalendar(year, i + 1)
            for i in range(12)
            if i < date.today().month - 1]

        cal_list3 = cal_list + cal_list2

    except IOError:
        abort(404)
    else:
        race_miles = training_list[-1][0]
        if username == 'alex':
            return render_template('new_alex.html',
                                   weekdays=weekdays,
                                   list_month=list_month,
                                   username=username,
                                   year=year,
                                   cal=cal_list3,
                                   training_list=training_list[:-1],
                                   logged_training=logged_training,
                                   race_date=training_list[-1],
                                   race_miles=race_miles)
        else:
            return render_template('new_.html',
                                   weekdays=weekdays,
                                   list_month=list_month,
                                   username=username,
                                   year=year,
                                   cal=cal_list3,
                                   training_list=training_list[:-1],
                                   logged_training=logged_training,
                                   race_date=training_list[-1],
                                   race_miles=race_miles)
    abort(404)


@app.route("/map/<username>/<last_date>", methods=["GET", "POST"])
def redirectmap(username, last_date):
    """
    Renders the home page
    """
    if username == 'alex':
        generate_map(username, str(last_date))
        return redirect(url_for('.foo', username=username))

    else:
        return redirect(url_for('.foo', username=username))


if __name__ == "__main__":
    app.debug = True
    # app.run(host='0.0.0.0', port=80)
    app.run()
