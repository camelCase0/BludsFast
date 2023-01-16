# BludsFast
source venv/bin/activate

python3.9 -m pip install -r requirements.txt

python3.9 -m uvicorn app.main:app --reload
