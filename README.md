# BludsFast
source venv/bin/activate

python3.9 -m pip install -r requirements.txt

python3.9 -m uvicorn app.main:app --reload

pip install fastapi uvicorn[standard] cryptography
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
