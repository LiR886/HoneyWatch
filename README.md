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

Purpose

HoneyWatch demonstrates a simple cybersecurity monitoring workflow:

Collect "Think about it..." Detect Alert Investigate

License and intended use
=======
HoneyWatch is a defensive Python web honeypot designed for cybersecurity learning, portfolio demonstrations, detection engineering practice, and controlled laboratory testing.

It presents a fake corporate login page, records authentication attempts, stores security events in SQLite, evaluates each event against configurable detection rules, creates alerts, and exposes a password-protected monitoring dashboard.

The project intentionally does not provide real authentication and does not store submitted passwords. It stores only whether a password was provided and the password length.

## Important safety and privacy note

Run HoneyWatch only on systems and networks that you own or are explicitly authorized to use.

The included simulator is intended only for controlled testing against your own HoneyWatch instance. Do not point it at third-party websites or systems without explicit authorization.

If you expose the honeypot to the public internet, remember that IP addresses and User-Agent strings can be personal or operational data. Follow applicable privacy, retention, and notification requirements. Change the default dashboard password before exposing the service outside your own machine.

## What the project includes

HoneyWatch includes:

- A FastAPI web application
- A fake corporate login portal
- SQLite event storage through SQLAlchemy
- Password-safe telemetry collection
- Source IP collection
- Username collection
- User-Agent collection
- Login timestamp collection
- Password length collection without storing password content
- Configurable detection rules
- Brute-force detection
- Username spraying detection
- Rapid-request detection
- High-value account targeting detection
- Alert cooldown logic to reduce duplicate alerts
- Rotating event logs
- Rotating alert logs
- HTTP Basic protected security dashboard
- Dashboard summary statistics
- Recent login attempt view
- Recent alert view
- Top targeted usernames
- Top source IPs
- Health endpoint
- Docker support
- Docker Compose support
- A controlled login attempt simulator
- A basic test suite

## Architecture

The application flow is:

```text
Browser or controlled simulator
        |
        v
FastAPI honeypot login endpoint
        |
        v
Login event creation
        |
        +----> SQLite database
        |
        +----> rotating event log
        |
        v
Detection engine
        |
        +----> brute-force rule
        +----> username-spray rule
        +----> rapid-request rule
        +----> high-value-account rule
        |
        v
Alert creation
        |
        +----> SQLite alerts table
        +----> rotating alert log
        |
        v
Protected dashboard
```

## Project structure

```text
honeywatch/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── honeypot.py
│   │   └── dashboard.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── client_ip.py
│   │   ├── dashboard_auth.py
│   │   ├── detection.py
│   │   └── logging_service.py
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── simulation/
│   └── login_simulator.py
├── tests/
│   └── test_detection.py
├── data/
├── logs/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requirements

For the Docker setup you need:

- Docker Desktop, Docker Engine, or another compatible Docker installation
- Docker Compose v2

Check your installation:

```bash
docker --version
docker compose version
```

You do not need to install Python locally if you run the project with Docker.

## Quick start with Docker

Open a terminal and enter the project directory:

```bash
cd honeywatch
```

Create your local environment file:

```bash
cp .env.example .env
```

Open `.env` and change this value before running the application:

```text
DASHBOARD_PASSWORD=replace-this-with-a-strong-password
```

For example, use a long random password that is only for this lab.

Build and start HoneyWatch:

```bash
docker compose up --build
```

When startup succeeds, the application is available at:

```text
http://127.0.0.1:8000/login
```

The monitoring dashboard is available at:

```text
http://127.0.0.1:8000/dashboard
```

Your browser will request HTTP Basic credentials.

The default username from `.env.example` is:

```text
admin
```

The password is the value you set in:

```text
DASHBOARD_PASSWORD
```

The health endpoint is:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "HoneyWatch"
}
```

## First manual test

Open:

```text
http://127.0.0.1:8000/login
```

Enter any test username and password.

Example:

```text
Username: admin
Password: password123
```

HoneyWatch will always reject the login because the page is a honeypot and does not implement real authentication.

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard
```

You should now see one recorded login attempt.

The password itself is not stored. The dashboard will show only the password length.

## Generate controlled attack-like activity

HoneyWatch includes a simulator that generates repeated login attempts against the honeypot.

The safest and easiest Docker command is:

```bash
docker compose --profile tools run --rm simulator
```

The simulator service communicates directly with the HoneyWatch container over the Docker Compose network.

By default it generates 15 requests with a short delay between requests. This should trigger several detection rules.

After it finishes, refresh:

```text
http://127.0.0.1:8000/dashboard
```

You should see new attempts and alerts.

Typical alert types are:

```text
HIGH_VALUE_ACCOUNT_ATTEMPT
BRUTE_FORCE
USERNAME_SPRAY
RAPID_REQUESTS
```

## Run the simulator manually from your host

If Python is installed locally, install the requests package or use the full project environment and run:

```bash
python simulation/login_simulator.py --target http://127.0.0.1:8000/login --count 15 --delay 0.25
```

You can change the number of requests:

```bash
python simulation/login_simulator.py --target http://127.0.0.1:8000/login --count 30 --delay 0.5
```

The simulator limits the maximum count to 500 requests as a basic guardrail.

Use the simulator only against systems you own or are explicitly authorized to test.

## Detection rules

### Brute-force detection

Default configuration:

```text
BRUTE_FORCE_THRESHOLD=5
BRUTE_FORCE_WINDOW_SECONDS=60
```

If one source IP creates at least five login attempts within 60 seconds, HoneyWatch creates a `BRUTE_FORCE` alert.

### Username spraying detection

Default configuration:

```text
USERNAME_SPRAY_THRESHOLD=5
USERNAME_SPRAY_WINDOW_SECONDS=120
```

If one source IP attempts at least five distinct usernames within 120 seconds, HoneyWatch creates a `USERNAME_SPRAY` alert.

### Rapid request detection

Default configuration:

```text
RAPID_REQUEST_THRESHOLD=10
RAPID_REQUEST_WINDOW_SECONDS=10
```

If one source IP creates at least ten login attempts within ten seconds, HoneyWatch creates a `RAPID_REQUESTS` alert.

### High-value account detection

Default configuration:

```text
HIGH_VALUE_USERNAMES=admin,administrator,root,sysadmin,support
```

Any login attempt targeting one of these usernames can create a `HIGH_VALUE_ACCOUNT_ATTEMPT` alert.

The comparison is case-insensitive.

## Alert cooldown

Repeated events can create a large number of duplicate alerts. HoneyWatch therefore implements an alert cooldown.

Default value:

```text
ALERT_COOLDOWN_SECONDS=60
```

For the same source IP and alert type, another identical alert will not be created until the cooldown has expired.

This keeps the dashboard useful while preserving all individual login attempts in the event database.

## Stored data

The `login_attempts` table stores:

- Event ID
- UTC timestamp
- Source IP
- Username attempt
- Whether a password was provided
- Password length
- User-Agent
- Requested endpoint
- HTTP method

HoneyWatch deliberately does not store plaintext passwords.

The `alerts` table stores:

- Alert ID
- UTC timestamp
- Alert type
- Severity
- Source IP
- Alert title
- Alert description

## Database location

When running with Docker Compose, SQLite is persisted on the host in:

```text
data/honeywatch.db
```

The container sees the same database at:

```text
/app/data/honeywatch.db
```

Because `data/` is mounted as a Docker volume, restarting the container does not normally remove your database.

## Log files

Event logs are written to:

```text
logs/honeypot.log
```

Alert logs are written to:

```text
logs/alerts.log
```

The logger uses file rotation. A log file is rotated when it reaches approximately 2 MB and up to five backup files are kept.

To follow the container output:

```bash
docker compose logs -f honeywatch
```

To inspect the event log directly:

```bash
cat logs/honeypot.log
```

To inspect alerts:

```bash
cat logs/alerts.log
```

On Windows PowerShell you can use:

```powershell
Get-Content .\logs\honeypot.log
Get-Content .\logs\alerts.log
```

## Dashboard security

The dashboard uses HTTP Basic authentication.

Configure it in `.env`:

```text
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your-strong-password
```

Do not keep the example password if you expose the application outside localhost.

HTTP Basic credentials are not encrypted by themselves. If this project is exposed over a network, place it behind HTTPS before using the dashboard remotely.

For a local lab at `127.0.0.1`, this setup is sufficient for demonstration and development.

## Source IP behavior

By default:

```text
TRUST_PROXY_HEADERS=false
```

HoneyWatch uses the network peer address reported by FastAPI.

This is intentional because blindly trusting `X-Forwarded-For` can allow clients to spoof their source address.

If you later place HoneyWatch behind a reverse proxy that you fully control, you may set:

```text
TRUST_PROXY_HEADERS=true
```

Only do this when untrusted clients cannot directly reach the application and your trusted proxy correctly overwrites forwarding headers.

## Stop the project

If Docker Compose is running in the foreground, press:

```text
Ctrl+C
```

Then remove the containers:

```bash
docker compose down
```

Your SQLite database and log files remain in the `data/` and `logs/` directories.

## Start the project again

Run:

```bash
docker compose up
```

A rebuild is not necessary unless code, dependencies, or the Dockerfile changed.

If code changed, run:

```bash
docker compose up --build
```

## Reset all collected test data

Stop the application:

```bash
docker compose down
```

Remove the database and log files:

```bash
rm -f data/honeywatch.db
rm -f logs/*.log
```

Then start the application again:

```bash
docker compose up --build
```

On Windows PowerShell:

```powershell
Remove-Item .\data\honeywatch.db -ErrorAction SilentlyContinue
Remove-Item .\logs\*.log -ErrorAction SilentlyContinue
```

## Run tests with Docker

Build the image first:

```bash
docker compose build
```

Run pytest inside a temporary container:

```bash
docker compose run --rm honeywatch pytest -q
```

Expected output should show the test suite passing.

## Run without Docker

Docker is the recommended way to run this project, but local Python is also possible.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the configuration:

```bash
cp .env.example .env
```

When running outside Docker, change these two values in `.env`:

```text
DATABASE_URL=sqlite:///./data/honeywatch.db
LOG_DIR=./logs
```

Create local directories if they do not already exist:

```bash
mkdir -p data logs
```

Run the application:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/login
```

## Configuration reference

`APP_NAME`

Application display name.

`APP_HOST`

Host configured for deployment tooling. Docker starts Uvicorn on `0.0.0.0` directly.

`APP_PORT`

Application port metadata. Docker exposes port 8000 by default.

`DATABASE_URL`

SQLAlchemy database URL.

`LOG_DIR`

Directory where rotating event and alert logs are written.

`DASHBOARD_USERNAME`

HTTP Basic dashboard username.

`DASHBOARD_PASSWORD`

HTTP Basic dashboard password.

`TRUST_PROXY_HEADERS`

Controls whether the application trusts `X-Forwarded-For` or `X-Real-IP` headers.

`BRUTE_FORCE_THRESHOLD`

Minimum attempts required for the brute-force rule.

`BRUTE_FORCE_WINDOW_SECONDS`

Time window for the brute-force rule.

`USERNAME_SPRAY_THRESHOLD`

Minimum distinct usernames required for username-spray detection.

`USERNAME_SPRAY_WINDOW_SECONDS`

Time window for username-spray detection.

`RAPID_REQUEST_THRESHOLD`

Minimum attempts required for rapid-request detection.

`RAPID_REQUEST_WINDOW_SECONDS`

Time window for rapid-request detection.

`ALERT_COOLDOWN_SECONDS`

Minimum time before an identical alert type from the same IP can be generated again.

`HIGH_VALUE_USERNAMES`

Comma-separated account names that should generate an alert when targeted.

## Useful Docker commands

Show running containers:

```bash
docker compose ps
```

Show application logs:

```bash
docker compose logs honeywatch
```

Follow application logs continuously:

```bash
docker compose logs -f honeywatch
```

Restart the application:

```bash
docker compose restart honeywatch
```

Rebuild after source changes:

```bash
docker compose up --build
```

Stop and remove containers:

```bash
docker compose down
```

Open a shell inside the running container:

```bash
docker compose exec honeywatch sh
```

## Suggested demo workflow

For a portfolio demonstration, use this sequence:

1. Start HoneyWatch with Docker Compose.
2. Open the login portal in a browser.
3. Submit one manual login attempt.
4. Open the protected dashboard and show the new event.
5. Run the controlled simulator.
6. Refresh the dashboard.
7. Show the generated brute-force, username-spray, rapid-request, and high-value-account alerts.
8. Open `logs/honeypot.log` and `logs/alerts.log`.
9. Explain that plaintext passwords are intentionally not retained.
10. Explain how the thresholds can be tuned through environment variables.

## Security design decisions

### Passwords are not stored

A real honeypot can capture credentials, but doing so creates unnecessary security and privacy risk for a portfolio project. HoneyWatch records only whether a password was provided and its length.

### Proxy headers are not trusted by default

Client-controlled forwarding headers can be spoofed. HoneyWatch uses the direct network peer unless the operator explicitly enables trusted proxy headers.

### Dashboard access is protected

Operational data should not be publicly visible. The dashboard therefore requires credentials.

### Detection thresholds are configuration, not source code constants

Detection engineering frequently requires tuning. Environment variables make thresholds easy to change without modifying code.

### Alerts use cooldown logic

A single noisy source should not create an unusable number of identical alerts. Raw attempts remain available while alerts are deduplicated for a configurable period.

## Current limitations

HoneyWatch is intentionally a small learning project rather than a production SIEM or enterprise honeypot.

Current limitations include:

- SQLite is designed for a small deployment, not large event volumes
- The dashboard does not provide advanced search or filtering
- There is no IP geolocation or ASN enrichment
- There is no automatic firewall blocking
- There is no external alert delivery to Slack, email, or a SIEM
- HTTP Basic authentication should be placed behind HTTPS for remote use
- Detection logic is threshold-based rather than behavioral or statistical

These limitations are useful directions for future development.

## Possible future improvements

Good next features include:

- PostgreSQL support
- Redis-backed counters for higher event volumes
- IP geolocation using an offline GeoIP database
- ASN enrichment
- Prometheus metrics
- Grafana dashboards
- JSON event export
- CSV export
- Webhook alerts
- Slack alerts
- Email alerts
- Sigma-style detection rules
- Allowlist support
- Additional fake endpoints
- Fake API token portal
- Canary tokens
- Reverse proxy deployment with HTTPS
- Retention policies
- Role-based dashboard access
- Automated integration tests

## Portfolio description

A short CV description could be:

> Developed HoneyWatch, a Dockerized Python/FastAPI web honeypot that captures suspicious authentication activity, stores security telemetry in SQLite, detects brute-force and username-spraying behavior, generates security alerts, and provides a protected monitoring dashboard. Implemented privacy-aware credential handling, configurable detection thresholds, structured event storage, rotating logs, and controlled attack simulation for laboratory testing.

## License and intended use
>>>>>>> 7852134 (Initial HoneyWatch project)

This project is intended for education, defensive cybersecurity research, portfolio demonstration, and authorized laboratory testing.

You are responsible for how and where you deploy it.
