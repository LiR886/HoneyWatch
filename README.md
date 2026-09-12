# HoneyWatch

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

Purpose

HoneyWatch demonstrates a simple cybersecurity monitoring workflow:

Collect "Think about it..." Detect Alert Investigate

License and intended use

This project is intended for education, defensive cybersecurity research, portfolio demonstration, and authorized laboratory testing.

You are responsible for how and where you deploy it.
