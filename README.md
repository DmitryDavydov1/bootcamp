cd app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

cd rec-admin
npm install
npm run dev 