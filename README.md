# Company Listing Webapp

## High-Level Architecture
<img width="900" height="662" alt="Architecture" src="https://github.com/user-attachments/assets/845633db-ae8b-484a-8160-f65b61811c5d" />

## Overview

This is a full-fledged web application built with Flask that serves as a comprehensive directory for companies and a platform for blog posts. It showcases a complete data pipeline, from web scraping and data processing to a robust backend and a dynamic frontend. This project highlights skills in web scraping, data processing, and full-stack web development with Python and Flask.

## Features

* **Extensive Company Directory:** Browse and search through a curated list of over **36,000 companies**.
    * Each company entry includes: Name, Location, Logo, Website, and Social Media links (Facebook, X/Twitter, LinkedIn).
* **Dynamic Blog Section:** A dedicated area for blog posts, managed by administrators.
* **User Authentication & Authorization:** Secure user login and registration.
* **Admin Dashboard:**
    * A dedicated interface for administrators to add and manage new company listings.
    * Tools for creating and managing blog posts.
* **Responsive Design:** Ensures a seamless user experience across various devices (desktop, tablet, mobile).
* **Search Functionality:** Efficiently search for companies based on various criteria.
* **Category-based Browsing:** Explore companies categorized by their services or industry.
* **Pagination:** Navigate large datasets of companies and blog posts with ease.
* **Flash Messaging:** Provides user feedback for various actions (e.g., successful login, form submission errors).

## Technologies Used

This project leverages a diverse set of technologies across its data pipeline and web application layers:

### 1. Data Acquisition & Processing

* **Python:** The core programming language for scripting.
* **Beautiful Soup:** For parsing HTML and extracting data from web pages.
* **Requests:** For making HTTP requests to fetch web content.
* **Proxy Integration:** Utilized for efficient and robust large-scale web scraping.
* **Pandas:** For cleaning, transforming, and structuring the scraped company data.

### 2. Database

* **SQLite3:** A lightweight, file-based relational database used for storing all company and blog data.
* **SQLAlchemy:** Python SQL toolkit and Object-Relational Mapper (ORM) for interacting with the database.

### 3. Backend (Flask Application)

* **Flask:** A lightweight Python web framework providing the core application structure.
* **Flask-SQLAlchemy:** Integrates SQLAlchemy with Flask for database operations.
* **Flask-Bcrypt:** For secure password hashing and verification.
* **Flask-Login:** Manages user sessions and provides user authentication features.
* **Flask-Mail:** Facilitates sending emails (e.g., for contact forms, and account recovery).
* **Serializer:** Used for secure data serialization, particularly for generating secure tokens (e.g., for password reset).

### 4. Frontend

* **Jinja2:** Flask's templating engine for rendering dynamic HTML content.
* **HTML5:** Standard markup language for creating web pages.
* **CSS3:** For styling the application's user interface.
* **Bootstrap 5:** A popular CSS framework for responsive and modern UI components.

## Project Structure (Key Components)

The Flask application follows a modular structure using Blueprints:

* `app.py`: The main application entry point, responsible for creating the Flask app instance and initializing extensions.
* `config.py`: Manages application-wide settings, including sensitive keys and database configurations, loaded from `config.json`.
* `main/`: Blueprint for public-facing pages (e.g., home, contact).
* `companies/`: Blueprint for company listings, search, and category-based views.
* `posts/`: Blueprint for blog posts and related functionalities.
* `users/`: Blueprint handling user authentication (registration, login, logout).
* `admin/`: Blueprint for the administrative dashboard, managing companies and posts.
* `errors/`: Blueprint for custom error handling pages.
* `static/`: Stores static assets like CSS, JavaScript, and images.
* `templates/`: Contains Jinja2 HTML templates.


## Server setup
* Create a project from google cloud
* create an instances with prefer os
* login through ssh from google cloud

#### Update and upgrade system
```bash
sudo apt update
sudo apt upgrade
```

#### Create a user and assign in sudo group to run admin commands
```bash
sudo adduser username       # create a new user
sudo adduser username sudo  # assign in sudo group

cat /etc/group          # check user added on sudo group
```

#### set ssh key based authentication for new user

##### from local linux system bash
```bash
ssh-keygen -t ed25519 -C 'ubuntu-server'        # create cryptographic hash key
# save this key /home/username/.ssh/id_flask_server # id_flask_server, id_flask_server.pub

cat ~/.ssh/id_flask_server.pub              # get the ssh public key
# copy the key and paste in cloud ubuntu machine 
# .ssh/authorized_keys directory

# this is not necessary
nano ~/.ssh/config                  # add ssh configuration for easy access
-----------------------------------------|
Host flask-server            |
    Hostname ip              |      # copy external ip from google cloud
    User username            |
    IdentityFile ~/.ssh/id_flask_server  |      # ssh keys path which we have created
-----------------------------------------|

# after puting the public key on cloud server
ssh flask-server                    # login to remote server through ssh
```

##### from cloud server bash
```bash
su username             # switch to new user
    
mkdir ~/.ssh                # create a new .ssh directory
chmod 0700 .ssh             # update permission for .ssh directory

nano ~/.ssh/authorized_keys     # put the copied public key from local
chmod 0600 ~/.ssh/*         # update permission inside .ssh directory
exit                    # exit from cloud machine
```

#### from local linux system bash
```bash
ssh flask-server            # login to our remote server

# if ssh working than we don't want root login and password login for security
sudo nano /etc/ssh/sshd_config
PermitRootLogin no          # disable root login
PasswordAuthentication no       # disable pass login

sudo systemctl restart sshd.service # restart the service
```

#### clone flask application from github and configure to run
```bash
# clone the application
git clone https://github.com/mahfuz-prog/Flask.git

# create or move config.json `/etc/your_application_name/`

# install virtual environment on system
sudo apt install python3-venv

# create virtual env on Flask package
cd Flask
python3 -m venv .env

source .env/bin/activate                # activate virtual env
pip install -r requirements.txt         # install dependencies for app
rm ~/Flask/requirements.txt             # not to keep sensitive info on server
```

#### Test application on server
##### [update google cloud firewall](https://console.cloud.google.com/net-security/firewall-manager/firewall-policies/)
##### add new firewall rule to allow 5000 port for test
###### name
* allow-5000
###### Targets 
* all instancex in the network
* Source IPv4 ranges = 0.0.0.0/0
###### Protocols
* select Specified protocols and ports
* select TCP = 5000

```bash
export FLASK_APP=run.py     # temp variable
flask run --host=0.0.0.0    # access development server from outside

go to ipaddress:5000 to see the application is running
```
##### delete allow-5000 from google cloud. we don't need 5000 port further. the same way allow 80 port `TCP=80` from google cloud for run app in production

#### set up firewall on our server
##### the firewall rule we set on google cloud is applicable for all instances of a project and this configuration is applicable for only our remote machine
```bash
sudo apt install ufw            # install ufw
sudo ufw status             # see the status

sudo ufw default allow outgoing     # allow outgoing traffic from server
sudo ufw default deny incoming      # deny all incoming traffic
sudo ufw allow ssh          # allow ssh port for ssh login
sudo ufw allow http/tcp         # allow port 80 for production
sudo ufw enable             # enable firewall
sudo ufw disable            # disable ufw
```

#### set up nginx reverse proxy
```bash
sudo apt install nginx

# remove default nginx file
sudo rm /etc/nginx/sites-enabled/default

# create new nginx file
sudo nano /etc/nginx/sites-enabled/flaskapp

server {
    listen 80;
    server_name ip;
    
    location /static {
        alias /home/username/Flask/flaskapp/static;
    }
    
    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}

sudo systemctl restart nginx            # restart nginx
```
##### visit the ip address it should gives nginx error because it still doesn't know how to process python code. Now we need gunicorn

#### gunicorn setup 
```bash
pip install gunicorn            # install gunicorn in virtual env

nproc --all             # number of cores
worker = (2 * number of cores) + 1

# run has our flask application variable which is app
# run gunicorn
gunicorn -w 5 run:app           # check the app running
```

#### Supervisor process manager
```bash
sudo apt install supervisor     # install supervisor

# create a config file
sudo nano /etc/supervisor/conf.d/flaskapp.conf

[program:flaskapp]
directory=/home/username/Flask/
command=/home/username/Flask/.env/bin/gunicorn -w 5 flaskapp:app
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flaskapp/flaskapp.err.log
stdout_logfile=/var/log/flaskapp/flaskapp.out.log
```

##### create those file and directory defined on supervisor config
```bash
sudo mkdir -p /var/log/flaskapp/
sudo touch /var/log/flaskapp/flaskapp.err.log
sudo touch /var/log/flaskapp/flaskapp.out.log
```

##### before start supervisor we need one more setting to go
##### [hostname resolution](https://www.debian.org/doc/manuals/debian-reference/ch05.en.html#_the_hostname_resolution)
```bash
hostname            # check the hostname
hostnamectl set-hostname name   # set a hostname

# edit hosts file and put ip address with hostname below localhost
sudo nano /etc/hosts

127.0.0.1 localhost
yourip     hostname
```

#### Run the flask app on production
```bash
sudo supervisorctl reload       # start running the application
sudo supervisorctl status       # check the status of supervisor
```

## Quick recap
* `cat /etc/group` check user in sudo group.
* `ls -la ~` .ssh permission should `700(drwx------)` for .ssh directory of our remote server.
* `ls -la ~/.ssh` authorized_keys which contain ssh public key should have `600(-rw-------)` permission.
* `cat /etc/ssh/sshd_config` PermitRootLogin and PasswordAuthentication should no
* `ls /etc/nginx/sites-enabled/` there should be only one file which contain nginx configuration
* `cat /etc/nginx/sites-enabled/flaskapp` check nginx config
* `cat /etc/supervisor/conf.d/flaskapp.conf` supervisor configuration
* `ls /var/log/flaskapp/` supervisor logfile
* `cat /var/log/flaskapp/flaskapp.err.log` check the log file of supervisor
* `cat /etc/hosts` there should be external ip address with hostname
* `ssh, http/tcp` should allow on [google cloud firewall](https://console.cloud.google.com/net-security/firewall-manager/firewall-policies/)
* `sudo ufw status`
```bash
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
```

## Add custom domain
#### Go to google cloud [Dns zone](https://console.cloud.google.com/net-services/dns/) and create a zone.

##### Add standard
* `DNS name = blank`. it will help to load the domain without www. 
* Resource recoed type =  A
* `IPv4 address = ip`. ip address of our server.
##### Add standard
* `DNS name = www`
* Resource recoed type =  CNAME
* `Canonical name = demo.com`. put your domain name here.
##### Copy all NS record and put them on Domain service provider namespace

## Enable ssl certificate
#### Firewalls update from google cloud dashboard
* Click on server name from google cloude VM instances
* edit and active HTTP traffic and HTTPS traffic from Firewalls section

#### change nginx configuration
```bash
sudo nano /etc/nginx/sites-enabled/flaskapp
# from server block change ip address to domain name.
server {
    server_name ip; # replace to
    server_name webwaymark.com www.webwaymark.com; # this
}

sudo systemctl restart nginx
```

#### update ubuntu server firewalls(ufw)
```bash
sudo ufw allow https
sudo ufw status
```

## Ubuntu 20.04.6 LTS server configuration for ssl
#### [Free ssl - certbot](https://certbot.eff.org/)
```bash
sudo apt update
sudo apt install certbot
sudo apt install software-properties-common
sudo apt install python3-certbot-nginx
sudo apt update

sudo certbot --nginx
- email
- accept tos
- newslatter email subscription Yes/No
- enter domain name
- select name for activate HTTPS or blank for apply all
- Redirect

# It should change some of nginx configuration
sudo cat nano /etc/nginx/sites-enabled/flaskapp
nginx -t        # test nginx permission issues are okay.
sudo nginx -t   # test should pass

sudo systemctl restart nginx
```

#### renew ssl certificates automatic
```bash
# jumi mimic tge process
sudo certbot renew --dry-run

# edit crontab for renew certificate automatically after a certain amount of time
sudo crontab -e
# minutes hour day *(every month) *(day of the week) 
30 4 1 * * sudo certbot renew --quiet
```
