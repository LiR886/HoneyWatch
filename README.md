# HoneyWatch

<<<<<<< HEAD
HoneyWatch is a lightweight Python web honeypot designed to capture and analyze suspicious login activity.

It looks like a normal admin login page, but there are no real accounts behind it. Every authentication attempt fails while HoneyWatch records and analyzes the activity.

Features

HoneyWatch detects:

* Brute-force login attempts
* Username spraying
* High-value account attempts such as `admin`, `root`, and `administrator`
* Rapid automated requests

Collected events and generated alerts are stored in SQLite and displayed through a protected monitoring dashboard.

The project also includes a controlled attack simulator for testing detection rules locally.

Tech Stack

* Python
* FastAPI
* Jinja2
* SQLAlchemy
* SQLite
* Docker
* Docker Compose

Run with Docker

Clone the repository and enter the project directory:

cd honeywatch

Configure dashboard credentials in `.env`, then build and start the application:

docker compose up --build

Open the honeypot:

http://127.0.0.1:8000/login


Open the monitoring dashboard:

http://127.0.0.1:8000/dashboard


Check application health:

http://127.0.0.1:8000/health


Test the Detection Engine

Run the controlled login simulator:

docker compose --profile tools run --rm simulator

Then refresh the dashboard to review generated events and alerts.

Testing Detection Rules

Once HoneyWatch is running, you can generate controlled suspicious activity directly from your terminal and check whether the detection engine responds correctly.

Note: These examples are intended for your local HoneyWatch environment or other systems you are explicitly authorized to test.

Username Spraying

A username spraying attack tries multiple usernames from the same source.

Run:

for user in admin root administrator support sysadmin finance; do
  curl -s -o /dev/null \
    -X POST \
    -d "username=$user&password=TestPassword123" \
    http://127.0.0.1:8000/login
done

Then refresh the dashboard.

HoneyWatch should detect the multiple usernames and generate a USERNAME_SPRAY alert. Attempts against usernames such as admin, root, or sysadmin may also trigger HIGH_VALUE_ACCOUNT_ATTEMPT.

Rapid Requests

This test sends multiple login requests almost simultaneously:

for i in {1..15}; do
  curl -s -o /dev/null \
    -X POST \
    -d "username=test&password=test123" \
    http://127.0.0.1:8000/login &
done
wait

HoneyWatch should generate a RAPID_REQUESTS alert.

A BRUTE_FORCE alert may also appear because the same activity can match more than one detection rule.

High-Value Account Attempt

HoneyWatch gives additional attention to commonly targeted administrative usernames.

Test it with:

curl -X POST \
  -d "username=root&password=whatever" \
  http://127.0.0.1:8000/login

Then check the dashboard for a HIGH_VALUE_ACCOUNT_ATTEMPT alert.

Review the Results

Open the monitoring dashboard:

http://127.0.0.1:8000/dashboard

You can also inspect the raw logs:

cat logs/honeypot.log
cat logs/alerts.log

License and intended use

HoneyWatch is a defensive Python web honeypot designed for detection engineering practice, and controlled laboratory testing.

It presents a fake corporate login page, records authentication attempts, stores security events in SQLite, evaluates each event against configurable detection rules, creates alerts, and exposes a password-protected monitoring dashboard.

The project intentionally does not provide real authentication and does not store submitted passwords. It stores only whether a password was provided and the password length.

This project is intended for education, defensive cybersecurity research, portfolio demonstration, and authorized laboratory testing.

You are responsible for how and where you deploy it. Dont do anything illegal, it is stupido.
