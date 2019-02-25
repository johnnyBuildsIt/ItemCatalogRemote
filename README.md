# Linux Server Configuration
#### For Full Stack Web Dev Nano Degree
#### By Johnny Rutkowski  
---
# Online
The app can be visited at www.johnnyrutkowski.com (18.204.218.32)

# Requirements and setup:
This project was created using Amazon Lightsail and is dependent on the following packages.
- [Python 2](https://www.python.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) - pip install SQLAlchemy
- [Flask](http://flask.pocoo.org/) - sudo apt install python-virtualenv
- Python [Requests](http://docs.python-requests.org/en/v1.0.0/community/out-there/) - sudo apt install python-requests
- Python [Httplib2](https://pypi.org/project/httplib2/) - sudo apt install python-httplib2
- [WSGI](https://www.fullstackpython.com/wsgi-servers.html)
 

# Configurations:
- Enabled ports(ufw):
-- SSH - 2200
-- HTTP - 80
-- NTP - 123
- Created grader user
- grader added to sudoers list
- ssh allowed only with public/private keys

# An online version of this project can be found at:
- www.johnnyrutkowski.com (18.204.218.32)
