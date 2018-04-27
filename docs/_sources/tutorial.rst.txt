Tutorial
========

| To set up the environment on AWS, perform the following steps:
|
| Launch Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type t2.large (size may need to be bigger eventually)
|
| Connect to AWS instance
|
| In the terminal, run the following commands:
| sudo yum install python-setuptools python-setuptools-devel
| sudo easy_install pip
| sudo yum install git
|
| Navigate to the appropriate directory, then clone the git repo:
| git clone https://github.com/MSDS698/group-assignment-2-xcelerate
|
| Install the requirements:
| sudo pip install -r requirements.txt
|
| Activate the environment:
| source venv/bin/activate
|
| Run the deploy script:
| python app.py
|
| The server is now up and running!  You can collect user data!
|
| When you're done, don't forget to deactivate the environment:
| deactivate
