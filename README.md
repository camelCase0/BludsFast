# BludsFast💉🩸
## Description
>This is one of my first backend projects.

> The main aim was to develop blood donor registration service with notifications when you can become a donor again.

>The ability to subscribe to a person who needs a donor on a regular basis and help him.
## Used stack
- [x] Python
- [x] FastAPI
- [x] PostgreSql
- [x] Docker
- [x] Docker-compose
- [x] Heroku

**DB structure**

<img width="585" alt="image" src="https://github.com/camelCase0/BludsFast/assets/98086463/30be5dd5-ac84-4779-b6df-90004c4e728f">

## Installation (`no docker`)
```bash
source venv/bin/activate
```
```bash
python3.9 -m pip install -r requirements.txt
```
```bash

python3.9 -m uvicorn app.main:app --reload
```
```bash
pip install fastapi uvicorn[standard] cryptography
```
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
